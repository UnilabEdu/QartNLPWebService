from flask_restful import Resource, reqparse


class NerTagApi(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'words',
        type=list,
        required=True,
        help='missing "words" argument'
    )
    parser.add_argument(
        'ner_tag',
        type=int,
        required=True,
        help='missing "ner_tag_" argument'
    )

    def get(self):
        received = NerTagApi.parser.parse_args()
        return {'response': f"This is the item with ID {received['id']}: 17589327851273852130"}, 200

    def post(self):
        received = NerTagApi.parser.parse_args()
        words = ["w1", "w2"]
        
        return {'response': 'done'}

    def put(self):
        return {'response': 'done'}

    def delete(self):
        return {'response': 'done'}

    def get_list(self):
        return {'response': 'done'}
