import datetime

from app import db
from app.models.ner_tagging import NerTagType


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

    def read(self):
        file_to_read = open(self.file_name, "r")
        while True:
            line = file_to_read.readline(200)
            if line:
                return line
            break

    @classmethod
    def file_by_id(cls, id):
        return cls.query.get(id)


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
                 expand_acronyms=False, words_enumerated=False):
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

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


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
        """TODO
        - შესაბამისი ფაილიდან მოცემული ოფსეტის ტექსტის ამოკითხვა
        """
        raw_text = "ამ გვერდის ობიექტების ინდექს შორის ფაილში არსებული მთელი ტექსტი"
        return raw_text


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
        """TODO
        - შესაბამისი ფაილიდან მოცემული ოფსეტის ტექსტის ამოკითხვა
        """
        raw_text = "ამ გვერდის ობიექტების ინდექს შორის ფაილში არსებული მთელი ტექსტი"
        return raw_text


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
                          ).all()

        return search_results

    @classmethod
    def search_by_lemma(cls, file_id, lemma):
        search_results = (db.session.query(Pages, Sentences, Words)
                          .join(Sentences, Pages.sentences)
                          .join(Words, Sentences.words)
                          .filter(Pages.file_id == file_id)
                          .filter(Words.lemma == lemma)
                          ).all()

        return search_results

    @classmethod
    def search_by_tag(cls, file_id, tags):
        search_results = (db.session.query(Pages, Sentences, Words)
                          .join(Sentences, Pages.sentences)
                          .join(Words, Sentences.words)
                          .filter(Pages.file_id == file_id)
                          .filter(Words.pos_tags.contains(tags))
                          ).all()

        return search_results

    def get_ner_tag(self):
        ner_tag_id = NerTagType.query.filter_by(id=self.ner_tags_id).first()
        ner_tag_type = None
        if ner_tag_id:
            ner_tag_type = ner_tag_id.name

        return ner_tag_type
