import csv
import os

from app.database import db
from app.models.ner_tagging import NerTagType
from app.models.grammatical_cases import GrammaticalCase


def populate_db_nertags():
    with open(f"{os.path.dirname(__file__)}/data/ner_names.csv") as nertags_file:
        csv_reader = csv.reader(nertags_file, delimiter=',')

        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
                continue

            if not NerTagType.query.filter_by(title=row[1]).first():
                new_obj = NerTagType(name=row[0],
                                     title=row[1],
                                     description=row[2],
                                     short_name=row[3])
                db.session.add(new_obj)
        db.session.commit()


def populate_grammatical_cases():
    with open(f"{os.path.dirname(__file__)}/data/grammatical_cases.csv", encoding='utf-8') \
            as grammar_tags_file:
        csv_reader = csv.reader(grammar_tags_file, delimiter=',')
        next(csv_reader)  # skip the first row

        current_part_of_speech = None
        for row in csv_reader:
            if row[0] == row[1] and row[1] == row[2]:
                current_part_of_speech = row[0]
                continue

            new_obj = GrammaticalCase(
                part_of_speech=current_part_of_speech if current_part_of_speech != row[1] else None,
                full_name_en=row[0],
                full_name_ge=row[1],
                short_name=row[2]
            )
            db.session.add(new_obj)

        db.session.commit()
