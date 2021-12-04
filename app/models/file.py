import datetime
import json
import os

from flask_login import current_user

from app.database import db
from app.models.ner_tagging import NerTagType, NerTags
from app.settings import Config
from app.files.utils import escape_for_xml


class File(db.Model):
    __tablename__ = "files"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String)
    file_name = db.Column(db.String)
    upload_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    date_modified = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    pages = db.relationship('Pages', backref='file')
    status = db.relationship('Status', backref='file')
    statistics = db.relationship('Statistics', backref='file', uselist=False)

    def __init__(self, title, user_id, file_name):
        self.title = title
        self.user_id = user_id
        self.file_name = file_name

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def disable(self):
        self.status[0].active = False
        db.session.commit()

    def read(self, amount):
        file_path = os.path.join(Config.UPLOAD_FOLDER, str(current_user.id), self.file_name)
        file_to_read = open(file_path, "r", encoding='utf-8')
        while True:
            line = file_to_read.read(amount)
            if line:
                return line
            break

    @classmethod
    def file_by_id(cls, id):
        return cls.query.get(id)

    @classmethod
    def get_active_files(cls, user_id):
        active_files = cls.query.join(cls.status).filter(cls.user_id==user_id).filter(Status.active==True)

        return active_files

    def get_word_count(self):
        word_count = (db.session.query(Words)
                      .join(Pages.sentences)
                      .join(Sentences.words)
                      .filter(Pages.file_id == self.id)).count()
        return word_count

    def relative_page_by_id(self, page_id):
        for i in range(len(self.pages)):
            if self.pages[i].id == page_id:
                return i+1

    def get_unique_word_count(self):
        unique_word_count = (db.session.query(Words)
                             .join(Pages.sentences)
                             .join(Sentences.words)
                             .filter(Pages.file_id == self.id)
                             ).group_by(Words.raw).count()
        return unique_word_count

    def get_sentence_count(self):
        sentence_count = (db.session.query(Sentences)
                          .join(Pages.sentences)
                          .filter(Pages.file_id == self.id)).count()
        return sentence_count

    def create_json(self):
        file_path_json = os.path.join(Config.UPLOAD_FOLDER, str(current_user.id), f"{self.title}-lemmatized.json")
        file_path_xml = os.path.join(Config.UPLOAD_FOLDER, str(current_user.id), f"{self.title}-lemmatized.xml")

        all_words = (db.session.query(Pages, Sentences, Words)
                       .join(Pages.sentences)
                       .join(Sentences.words)
                       .filter(Pages.file_id == self.id))

        ner_tag_short_names = NerTagType.get_nertag_short_names()
        all_pages = Pages.query.filter_by(file_id=self.id).all()
        all_pages = [page.id for page in all_pages]
        all_ner_tag_connections = NerTags.query.filter(NerTags.page_id.in_(all_pages)).all()
        all_ner_tag_connections_dict = {}
        print(len(all_ner_tag_connections))
        for connection in all_ner_tag_connections:
            print(type(connection.id))
            all_ner_tag_connections_dict.update({str(connection.id): connection.ner_tag_type_id})

        result_json = []
        result_xml = []
        result_xml.append('<?xml version="1.0" encoding="UTF-8"?>\n<words>\n')
        word_index = 0
        # Write JSON
        with open(file_path_json, 'w', encoding="utf-8") as f:
            start = 0
            while True:
                stop = start + 10000
                db_chunk = all_words.slice(start, stop).all()

                if len(db_chunk) == 0:
                    break

                for result in db_chunk:
                    word_index += 1

                    ner_tag_type_name = ''
                    if result[2].ner_tags_id:
                        ner_tag_connection_id = result[2].ner_tags_id
                        ner_tag_type_id = all_ner_tag_connections_dict[str(ner_tag_connection_id)]
                        ner_tag_type_name = ner_tag_short_names[str(ner_tag_type_id)]

                    dict = {
                        "word": result[2].raw,
                        "lemma": result[2].lemma,
                        "tags": result[2].pos_tags,
                        "ner_tag": ner_tag_type_name,
                        "page": {
                            "start": result[0].start_index,
                            "end": result[0].end_index
                        },
                        "sentence": {
                            "start": result[1].start_index,
                            "end": result[1].end_index
                        },
                    }

                    xml = f'    <word number="{word_index}">\n' \
                          f'        <raw>{escape_for_xml(result[2].raw)}</raw>\n' \
                          f'        <lemma>{escape_for_xml(result[2].lemma)}</lemma>\n' \
                          f'        <tags>{escape_for_xml(result[2].pos_tags)}</tags>\n' \
                          f'        <ner_tags>{escape_for_xml(ner_tag_type_name)}</ner_tags>\n\n' \
                          f'        <page>\n' \
                          f'            <start>{result[0].start_index}</start>\n' \
                          f'            <end>{result[0].end_index}</end>\n' \
                          f'        </page>\n\n' \
                          f'        <sentence>\n' \
                          f'            <start>{result[1].start_index}</start>\n' \
                          f'            <end>{result[1].end_index}</end>\n' \
                          f'        </sentence>\n' \
                          f'    </word>\n\n'

                    result_json.append(dict)
                    result_xml.append(xml)

                start += 10000

            f.write(json.dumps(result_json, ensure_ascii=False, indent=4))

        # Write XML
        with open(file_path_xml, 'w', encoding="utf-8") as f:
            result_xml.append('</words>')
            f.write(''.join(result_xml))


class Pages(db.Model):
    __tablename__ = "pages"

    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.Integer, db.ForeignKey("files.id"))
    start_index = db.Column(db.Integer)
    end_index = db.Column(db.Integer)
    sentences = db.relationship("Sentences", backref="pages")

    def __init__(self, file_id, start_index, end_index):
        self.file_id = file_id
        self.start_index = start_index
        self.end_index = end_index

    def __repr__(self):
        return f"Page starting at index {self.start_index}, with ID {self.id}"

    def flush(self):
        db.session.add(self)
        db.session.flush()

    def word_by_id(self, word_id):
        if word_id < 1:
            raise IndexError("ID can not be lower than 1")

        word_id -= 1
        for sentence in self.sentences:
            if word_id < len(sentence.words):
                return sentence.words[word_id]
            else:
                word_id -= len(sentence.words)

    def get_text(self):
        file_path = os.path.join(Config.UPLOAD_FOLDER, str(current_user.id), self.file.file_name)
        raw_text = ""

        with open(file_path, "r", encoding="utf-8") as file:
            file.read(self.start_index)
            raw_text = file.read(self.end_index-self.start_index)

        return raw_text

    def get_all_words(self):
        all_words = (db.session.query(Words)
                       .join(Pages.sentences)
                       .join(Sentences.words)
                       .filter(Pages.id == self.id))

        return all_words


class Sentences(db.Model):
    __tablename__ = "sentences"
    id = db.Column(db.Integer, primary_key=True)
    page_id = db.Column(db.Integer, db.ForeignKey("pages.id"))
    start_index = db.Column(db.Integer)
    end_index = db.Column(db.Integer)
    words = db.relationship('Words', backref="sentences")

    def __init__(self, page_id, start_index, end_index):
        self.page_id = page_id
        self.start_index = start_index
        self.end_index = end_index

    def flush(self):
        db.session.add(self)
        db.session.flush()

    def get_text(self):
        file_path = os.path.join(Config.UPLOAD_FOLDER, str(current_user.id), self.pages.file.file_name)
        raw_text = ""

        with open(file_path, "r", encoding="utf-8") as file:
            file.read(self.start_index + self.pages.start_index)
            raw_text = file.read(self.end_index - self.start_index)
            while raw_text[:1] == '\n':
                raw_text = raw_text[1:]
        return raw_text.replace('\n', ' ')


class Words(db.Model):
    __tablename__ = "words"
    id = db.Column(db.Integer, primary_key=True)
    sentence_id = db.Column(db.Integer, db.ForeignKey("sentences.id"))
    start_index = db.Column(db.Integer)
    end_index = db.Column(db.Integer)
    raw = db.Column(db.String)
    lemma = db.Column(db.String)
    pos_tags = db.Column(db.String)
    ner_tags_id = db.Column(db.Integer, db.ForeignKey("ner_tags.id"))

    def __init__(self, sentence_id, start_index, end_index, raw, lemma, pos_tags):
        self.sentence_id = sentence_id
        self.start_index = start_index
        self.end_index = end_index
        self.raw = raw
        self.lemma = lemma
        self.pos_tags = pos_tags

    def __repr__(self):
        return self.raw

    def save(self):
        db.session.add(self)
        db.session.commit()

    def flush(self):
        db.session.add(self)
        db.session.flush()

    @classmethod
    def search_by_raw(cls, file_id, raw):
        search_results = (db.session.query(Pages, Sentences, Words)
                          .join(Sentences, Pages.sentences)
                          .join(Words, Sentences.words)
                          .filter(Pages.file_id == file_id)
                          .filter(Words.raw == raw)
                          )

        return search_results

    @classmethod
    def search_by_lemma(cls, file_id, lemma):
        search_results = (db.session.query(Pages, Sentences, Words)
                          .join(Sentences, Pages.sentences)
                          .join(Words, Sentences.words)
                          .filter(Pages.file_id == file_id)
                          .filter(Words.lemma == lemma)
                          )

        return search_results

    @classmethod  # TODO: fix search_by_tag
    def search_by_tag(cls, file_id, tags):
        search_results = (db.session.query(Pages, Sentences, Words)
                          .join(Sentences, Pages.sentences)
                          .join(Words, Sentences.words)
                          .filter(Pages.file_id == file_id)
                          .filter(Words.pos_tags.contains(tags))
                          )

        return search_results

    def get_ner_tag(self):
        ner_tag_type = None
        if self.ner_tags_id:
            nertag = NerTags.query.filter_by(id=self.ner_tags_id).first()
            ner_tag_type = NerTagType.query.filter_by(id=nertag.ner_tag_type_id).first().title
        return ner_tag_type.replace(' ', '_')


class Statistics(db.Model):
    __tablename__ = "statistics"
    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.Integer, db.ForeignKey('files.id'))
    words = db.Column(db.Integer)
    uniq_words = db.Column(db.Integer)
    sentences = db.Column(db.Integer)
    avg_words_in_sentence = db.Column(db.Integer)
    avg_chars_in_sentence = db.Column(db.Integer)

    def __init__(self, file_id, words, uniq_words, sentences, avg_words_in_sentence, avg_chars_in_sentence):
        self.file_id = file_id
        self.words = words
        self.uniq_words = uniq_words
        self.sentences = sentences
        self.avg_words_in_sentence = avg_words_in_sentence
        self.avg_chars_in_sentence = avg_chars_in_sentence

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def statistics_for_file(cls, id):
        return Statistics.query.filter_by(file_id=id).first()


class Status(db.Model):
    __tablename__ = "status"
    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.Integer, db.ForeignKey('files.id'))
    lemmatized = db.Column(db.Boolean)
    tokenized = db.Column(db.Boolean)
    pos_tagged = db.Column(db.Boolean)
    stop_words_removed = db.Column(db.Boolean)
    frequency_distribution_calculated = db.Column(db.Boolean)
    completed = db.Column(db.Boolean)
    punctuation_removed = db.Column(db.Boolean)
    cleared_html_tags = db.Column(db.Boolean)
    special_chars_removed = db.Column(db.Boolean)
    cleared_whitespaces = db.Column(db.Boolean)
    html_tags_removed = db.Column(db.Boolean)
    expanded_acronyms = db.Column(db.Boolean)
    words_enumerated = db.Column(db.Boolean)
    active = db.Column(db.Boolean)

    def __init__(self, file_id, lemmatized=False, tokenized=False, pos_tagged=False,
                 stop_words_removed=False, frequency_distribution_calculated=False, completed=False,
                 punctuation_removed=False, cleared_html_tags=False, html_tags_removed=False,
                 expand_acronyms=False, words_enumerated=False, active=True):
        self.file_id = file_id
        self.lemmatized = lemmatized
        self.tokenized = tokenized
        self.pos_tagged = pos_tagged
        self.stop_words_removed = stop_words_removed
        self.frequency_distribution_calculated = frequency_distribution_calculated
        self.completed = completed
        self.punctuation_removed = punctuation_removed
        self.cleared_html_tags = cleared_html_tags
        self.html_tags_removed = html_tags_removed
        self.expanded_acronyms = expand_acronyms
        self.words_enumerated = words_enumerated
        self.active = active

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
