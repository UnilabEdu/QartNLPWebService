from flask_restful import Resource, reqparse
from app.file_processing.nlp import lemmatize, tokenize, remove_punctuation


class Lemmatization(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'text',
        type=str,
        required=True,
        help='missing "text" argument'
    )

    def post(self):
        received_text = Lemmatization.parser.parse_args()['text']
        print('lemma api reached')
        print(received_text)

        lemmatized_text = lemmatize(tokenize(remove_punctuation(received_text)))

        formatted_result = {
            word[0]: {
                "lemma": word[1],
                "pos_tags": word[2]
            } for word in lemmatized_text
        }

        return formatted_result
