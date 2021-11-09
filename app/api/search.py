from flask_restful import Resource, reqparse

from app.models.ner_tagging import NerTagType, NerTags
from app.models.file import File, Words, Sentences
from app.database import db


def is_list(value):
    if type(value) == list:
        return value
    else:
        raise ValueError


class SearchApi(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'query',
        type=is_list,
        required=True,
        nullable=False,
        location='json',
        help='"query" argument is missing or is not a list'
    )

    def get(self, file_id):
        query = SearchApi.parser.parse_args()['query']
        print(query)
        print(file_id)
        if type(query[0]) != list:
            all_words = Words.query.all()

            found_words = []
            for word in all_words:
                print(word.sentences)

                tags = word.pos_tags.split(',')
                for tag in query:
                    if tag not in tags:
                        break
                else:
                    found_words.append(word)

            obj = Words.query.get(4)
            var = obj.pos_tags.split(',')
            # print(var)
            # print(type(var))
            print(found_words)

            found_sentence_ids = [w.sentence_id for w in found_words]
            print(found_sentence_ids)
            print(type(found_sentence_ids[0]))
            found_sentences = Sentences.query.filter(Sentences.id.in_(found_sentence_ids)).all()
            print('found sentences', found_sentences)
            found_words = [word.raw for word in found_words]

            return {'resp': found_words}
