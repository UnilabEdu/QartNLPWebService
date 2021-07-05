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
    parser.add_argument(
        'file_id',
        type=int,
        required=True,
        help='missing "file_id" argument'
    )
    parser.add_argument(
        'page_id',
        type=int,
        required=True,
        help='missing "page_id" argument'
    )

    def get(self):
        received = NerTagApi.parser.parse_args()
        return {'response': f"This is the item with ID {received['id']}: 17589327851273852130"}, 200

    def post(self):
        received = NerTagApi.parser.parse_args()
        words_index_on_page = ["1", "2"]  # relative to the page
        """TODO
        - Load File object from db with file_id
        - Load Page object by ID from File object
        - Load words via indexes of words in request from Page object
        - create new ner_tag object with arguments
        - save object to DB
        """
        return {'response': 'done'}
