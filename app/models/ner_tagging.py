from app import db


class NerTagType(db.Model):
    __tablename__ = "ner_tag_type"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    title = db.Column(db.String)
    description = db.Column(db.String)
    short_name = db.Column(db.String)
    ner_tags = db.relationship('NerTags', backref='ner_tag_type', lazy=True)

    @classmethod
    def find_tag_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def __init__(self, name, title, description, short_name):
        self.name = name
        self.title = title
        self.short_name = short_name
        self.description = description

    def __repr__(self):
        return f"NerTagType ({self.id}): {self.name}"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class NerTags(db.Model):
    __tablename__ = "ner_tags"
    id = db.Column(db.Integer, primary_key=True)
    page_id = db.Column(db.Integer, db.ForeignKey("pages.id"))
    ner_tag_type_id = db.Column(db.Integer, db.ForeignKey("ner_tag_type.id"))
    words = db.relationship('Words', backref='ner_tags', lazy=True)

    def __init__(self, ner_tag_type_id, page_id):
        self.page_id = page_id
        self.ner_tag_type_id = ner_tag_type_id

    def __repr__(self):
        return f"{self.words=} tagged into ner_tag type-{self.ner_tag_type_id}"

    def connected_words(self):
        """
        :return: list of word objects in relationship
        """
        pass

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()