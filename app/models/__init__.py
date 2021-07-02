import datetime

from app.database import db


class Profile(db.Model):
    __tablename__ = "profiles"
    id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    date_of_birth = db.Column(db.DATE, nullable=False)
    img_url = db.Column(db.String)
    comp_name = db.Column(db.String(64))
    web_page = db.Column(db.String(64))
    info = db.Column(db.Text)

    def __init__(self, first_name, last_name, date_of_birth, img_url, comp_name, web_page, info):
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.img_url = img_url
        self.comp_name = comp_name
        self.web_page = web_page
        self.info = info


class File(db.Model):
    __tablename__ = "files"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String)
    file_name = db.Column(db.String)
    upload_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    date_modified = db.Column(db.DateTime, default=datetime.datetime.utcnow)
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
    start_index = db.Column(db.Integer)
    end_index = db.Column(db.Integer)
    sentences = db.relationship("Sentences")


class Sentences(db.Model):
    __tablename__ = "sentences"
    id = db.Column(db.Integer, primary_key=True)
    page_id = db.Column(db.Integer, db.ForeignKey("pages.id"))
    start_index = db.Column(db.Integer)
    end_index = db.Column(db.Integer)
    words = db.relationship('Words')

    def __init__(self, start_index, end_index):
        self.start_index = start_index
        self.end_index = end_index


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

    def __init__(self, sentence_id, start_index, end_index, raw, lemma, pos_tags, ner_tags_id):
        self.sentence_id = sentence_id
        self.start_index = start_index
        self.end_index = end_index
        self.raw = raw
        self.lemma = lemma
        self.pos_tags = pos_tags
        self.ner_tags_id = ner_tags_id


class NerTagType(db.Model):
    __tablename__ = "ner_tag_type"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    title = db.Column(db.String)
    description = db.Column(db.String)
    ner_tags = db.relationship('NerTags', backref='ner_tag_type', lazy=True)

    def __init__(self, name, title):
        self.name = name
        self.title = title

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class NerTags(db.Model):
    __tablename__ = "ner_tags"
    id = db.Column(db.Integer, primary_key=True)
    ner_tag_type_id = db.Column(db.Integer, db.ForeignKey("ner_tag_type.id"))
    words = db.relationship('Words', backref='ner_tags', lazy=True)

    def __init__(self, ner_tag_type_id):
        self.ner_tag_type_id = ner_tag_type_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

