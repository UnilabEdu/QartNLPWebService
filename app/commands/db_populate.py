import csv
import os

from app.database import db
from app.models.ner_tagging import NerTagType


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
