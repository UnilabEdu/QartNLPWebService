from flask import request
import json
from flask_restful import Resource, reqparse

from app.models import File, NerTags, NerTagType


class NerTagApi(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'words',
        required=True,
        help='missing "words" argument'
    )
    parser.add_argument(
        'ner_tag',
        type=str,
        required=True,
        help='missing "ner_tag" argument'
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
        """TODO
        - Load File object from db with file_id
        - Load Page object by ID from File object
        - Load words via indexes of words in request from Page object
        - create new ner_tag object with arguments
        - save object to DB
        """
        # request_arguments = NerTagApi.parser.parse_args()
        # Get request body
        request_arguments = request.get_json()
        # print(request_arguments)
        # Prepare db objects for work
        current_file = File.query.get(request_arguments["file_id"])
        current_page = current_file.pages[request_arguments["page_id"]]

        # get words list from JSON object
        words = request_arguments["words"][0]
        # print(words)
        # Find ner_tag from db via ner_tag provided in request
        ner_tag_type = NerTagType.find_tag_by_name(request_arguments["ner_tag"])
        # print(ner_tag_type)
        new_ner_tag = NerTags(ner_tag_type.id, current_page.id)
        new_ner_tag.save()
        # print(new_ner_tag)
        for word in words:
            word_from_db = current_page.word_by_id(int(word["id"]))
            word_from_db.ner_tags_id = new_ner_tag.id
            word_from_db.save()
        return {'response': 'done'}
