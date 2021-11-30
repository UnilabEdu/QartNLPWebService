from app.database import db


class GrammaticalCase(db.Model):
    __tablename__ = "grammatical_cases"

    id = db.Column(db.Integer, primary_key=True)
    part_of_speech = db.Column(db.String)
    short_name = db.Column(db.String)
    full_name_ge = db.Column(db.String)
    full_name_en = db.Column(db.String)

    def __init__(self, part_of_speech, short_name, full_name_ge, full_name_en):
        self.part_of_speech = part_of_speech
        self.short_name = short_name
        self.full_name_ge = full_name_ge
        self.full_name_en = full_name_en

    def to_json(self, part_of_speech=False):
        if not part_of_speech:
            return {
                'full_name_ge': self.full_name_ge,
                'full_name_en': self.full_name_en,
                'short_name': self.short_name,
                'part_of_speech': self.part_of_speech
            }
        else:
            return {
                    "full_name_en": self.full_name_en,
                    "short_name": self.short_name,
                    "tags": []
                }
