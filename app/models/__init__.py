import datetime
from sqlalchemy.types import BLOB, TEXT

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
    processes = db.Column(db.String)
    status = db.relationship('Status', backref='file')
    result = db.relationship('Result', backref='file', uselist=False)

    def __init__(self, title, processes, user_id):
        self.title = title
        self.processes = processes
        self.user_id = user_id

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def add(self):
        db.session.add(self)
        db.session.commit()

    def read(self):
        file_to_read = open(self.file_name, "r")
        while True:
            line = file_to_read.readline(200)
            if line:
                return line
            break


class Result(db.Model):
    __tablename__ = "results"
    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.Integer, db.ForeignKey('files.id'))
    words = db.Column(db.Integer)
    uniq_words = db.Column(db.Integer)
    sentences = db.Column(db.Integer)

    def __init__(self, file_id, words, uniq_words, sentences):
        self.file_id = file_id
        self.words = words
        self.uniq_words = uniq_words
        self.sentences = sentences

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def add(self):
        db.session.add(self)
        db.session.commit()


class Status(db.Model):
    __tablename__ = "status"
    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.Integer, db.ForeignKey('files.id'))
    lemat = db.Column(db.Boolean)
    token = db.Column(db.Boolean)
    pos_tag = db.Column(db.Boolean)
    stop_word = db.Column(db.Boolean)
    freq_dist = db.Column(db.Boolean)
    finished = db.Column(db.Boolean)

    # link to celelry task with celery_taskmeta.id
    # process_status

    def __init__(self, file_id, lemat=False, token=False, pos_tag=False,
                 stop_word=False, freq_dist=False, finished=False):
        self.file_id = file_id
        self.lemat = lemat
        self.token = token
        self.pos_tag = pos_tag
        self.stop_word = stop_word
        self.freq_dist = freq_dist
        self.finished = finished


class CeleryTask(db.Model):
    __tablename__ = "celery_taskmeta"
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.String(155))
    status = db.Column(db.String(50))
    result = db.Column(BLOB)
    date_done = db.Column(db.DateTime)
    traceback = db.Column(TEXT)
    name = db.Column(db.String(155))
    args = db.Column(BLOB)
    kwargs = db.Column(BLOB)
    worker = db.Column(db.String(155))
    retries = db.Column(db.Integer)
    queue = db.Column(db.String(155))
