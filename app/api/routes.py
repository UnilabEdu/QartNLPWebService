from flask_restful import Resource, reqparse

from app.models.ner_tagging import NerTagType, NerTags
from app.models.file import File
from app.database import db


class NerTagApi(Resource):
    post_parser = reqparse.RequestParser()
    post_parser.add_argument(
        'words',
        action='append',
        type=dict,
        required=True,
        help='missing "words" argument'
    )
    post_parser.add_argument(
        'ner_tag',
        type=str,
        required=True,
        help='missing "ner_tag" argument'
    )
    post_parser.add_argument(
        'file_id',
        type=int,
        required=True,
        help='missing "file_id" argument'
    )
    post_parser.add_argument(
        'page_id',
        type=int,
        required=True,
        help='missing "page_id" argument'
    )

    delete_parser = reqparse.RequestParser()
    delete_parser.add_argument(
        'word_ids',
        type=list,
        required=True,
        location='json',
        help='missing "word_ids" argument'
    )
    delete_parser.add_argument(
        'file_id',
        type=int,
        required=True,
        help='missing "file_id" argument'
    )
    delete_parser.add_argument(
        'page_id',
        type=int,
        required=True,
        help='missing "page_id" argument'
    )
    
    def post(self):
        """
        - Load File object from db with file_id
        - Load Page object by ID from File object
        - Load words via indexes of words in request from Page object
        - create new ner_tag object with arguments
        - save object to DB
        """
        # Parse request
        received_arguments = NerTagApi.post_parser.parse_args()
        print(received_arguments)

        # Prepare db objects for work
        current_file = File.query.get(received_arguments["file_id"])
        current_page = current_file.pages[received_arguments["page_id"]-1]

        # Get words list from JSON object
        words = received_arguments["words"]

        # Find ner_tag from db via ner_tag provided in request
        ner_tag_type = NerTagType.find_tag_by_name(received_arguments["ner_tag"])
        print(received_arguments['ner_tag'])
        print(ner_tag_type)
        print(current_page)
        print(ner_tag_type.id)
        print(current_page.id)
        # Add NerTag object with selected page and ner_tag_type
        new_ner_tag = NerTags(ner_tag_type.id, current_page.id)

        db.session.add(new_ner_tag)
        db.session.flush()
        # Add NerTag object ID to selected words' ner_tags_id (relationship) column
        for word in words:
            word_from_db = current_page.word_by_id(int(word["id"]))
            word_from_db.ner_tags_id = new_ner_tag.id
            db.session.add(word_from_db)

        db.session.commit()
        return {'words': [word['id'] for word in words],
                'tag_type': ner_tag_type.title}
    
    def delete(self):
        received_arguments = NerTagApi.delete_parser.parse_args()

        current_file = File.query.get(received_arguments["file_id"])
        current_page = current_file.pages[received_arguments["page_id"]-1]
        word_ids = received_arguments["word_ids"]
        target_words = []
        target_ner_tag_id = None

        for id_ in word_ids:
            found_word = current_page.word_by_id(id_)
            target_words.append(found_word)
            target_ner_tag_id = found_word.ner_tags_id
            print('target_ner_tag_id:', target_ner_tag_id)
            found_word.ner_tags_id = None

        target_ner_tag = NerTags.query.get(target_ner_tag_id)
        db.session.delete(target_ner_tag)
        db.session.commit()
        return {'words': word_ids,
                'delete_ner_tag_id': target_ner_tag_id}
