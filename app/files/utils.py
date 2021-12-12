import json

from flask import session

from app.database import db
from app.models.grammatical_cases import GrammaticalCase


def image_crop_and_resize(filepath, size_pixels=256):
    from PIL import Image
    img = Image.open(filepath)

    width, height = img.size

    if width != height:
        offset = int(abs(height - width) / 2)
        if width > height:
            img = img.crop([offset, 0, width - offset, height])
        else:
            img = img.crop([0, offset, width, height - offset])

    img = img.resize((size_pixels, size_pixels), Image.ANTIALIAS)
    img.save(filepath)


def escape_for_xml(string_to_format):
    table = string_to_format.maketrans({
        "<": "&lt;",
        ">": "&gt;",
        "&": "&amp;",
        '"': "&quot;",
        "'": "&apos;"
    })
    return string_to_format.translate(table)


def get_search_form():
    parts_of_speech = GrammaticalCase.query.filter_by(part_of_speech=None).all()
    grammatical_cases = GrammaticalCase.query.filter(GrammaticalCase.part_of_speech != None).all()

    search_form = {
        part_of_speech.full_name_ge: part_of_speech.to_json(part_of_speech=True)
        for part_of_speech in parts_of_speech}

    for tag in grammatical_cases:
        search_form[tag.part_of_speech]['tags'].append(tag.to_json())

    return json.dumps(search_form, ensure_ascii=False)


def get_search_query_results(all_queries, file_id, results_page_id, file_object):
    from app.models.file import Sentences, Words, Pages

    file_id = str(file_id)

    original_query = all_queries

    if 'search_results' not in session.keys() or 'search_stats' not in session.keys():
        session['search_results'] = {}
        session['search_stats'] = {}

    if file_id not in session['search_results'].keys() or all_queries not in session['search_results'][file_id].keys():
        all_words = (db.session.query(Words)
                     .join(Pages.sentences)
                     .join(Sentences.words)
                     .filter(Pages.file_id == file_id))

        all_queries = all_queries.split('_')
        all_queries = [q.split(',') for q in all_queries]
        query = all_queries[0]

        found_words = []
        if query[0][0] == '"' and query[-1][0] == '"':
            all_words = all_words.filter(Words.raw.ilike("%" + query[0][1:-1] + "%")).all()
            found_words.extend(all_words)
        else:
            for word in all_words.all():
                if check_word_tags(word, query):
                    found_words.append(word)

        result = []
        current_result_page_data = []
        count = 0
        sentence_amount = 0
        found_words_amount = len(found_words)

        for word in found_words:
            secondary_words = []

            sentence_word_objects = word.sentences.get_word_objects()

            for secondary_query in all_queries[1:]:

                search_range = int(secondary_query[0])
                current_word_index = sentence_word_objects.index(word)

                min_index = current_word_index - search_range if current_word_index - search_range >= 0 else 0
                max_index = current_word_index + search_range + 1 if current_word_index + search_range + 1 <= len(sentence_word_objects) else len(sentence_word_objects)

                words_in_range = sentence_word_objects[min_index:max_index]
                words_in_range.pop(words_in_range.index(word))

                match = False
                for secondary_word in words_in_range:
                    if check_word_tags(secondary_word, secondary_query[1:]):
                        secondary_words.append(secondary_word)
                        match = True
                        break
                if not match:
                    found_words_amount -= 1
                    break

            else:
                if len(current_result_page_data) \
                        and current_result_page_data[-1]['sentence_id'] == word.sentence_id:
                    current_result_page_data[-1]['words'].append(word)
                    current_result_page_data[-1]['secondary_words'].extend(secondary_words)
                    # current_result_page_data[-1]['word_index_tuples'].append((word.start_index, word.end_index))
                else:
                    count += 1
                    current_page_number = file_object.pages.index(word.sentences.pages) + 1
                    current_result_page_data.append({
                        "sentence_text": word.sentences,
                        # "sentence_text": remove_punctuation(word.sentences.get_text().strip()),
                        "words": [word],
                        "secondary_words": secondary_words,
                        # "word_index_tuples": [(word.start_index, word.end_index)],
                        "file_page_id": (word.sentences.pages.file_id, current_page_number),
                        "sentence_id": word.sentence_id
                    })

            if count == 10:
                result.append(current_result_page_data)
                current_result_page_data = []
                sentence_amount += count
                count = 0
        sentence_amount += count

        if len(current_result_page_data):
            result.append(current_result_page_data)

        # Mark found words as bold and secondary words as italics
        for page in result:
            for sentence in page:
                sentence['sentence_text'] = sentence['sentence_text'].get_words_raw_formatted(bold_words=sentence['words'],
                                                                                              italics_words=sentence['secondary_words'])
                del sentence['words']
                del sentence['secondary_words']

                # index_shift_amount = 0
                # for word_range_indices in sentence['word_index_tuples']:
                # word_length = word_range_indices[1] - word_range_indices[0]
                #
                # word_start_index = word_range_indices[0] + index_shift_amount
                # word_end_index = word_start_index + word_length
                #
                # sentence['sentence_text'] = sentence['sentence_text'][:word_start_index] + \
                #                             bold_start + \
                #                             sentence['sentence_text'][word_start_index:word_end_index] + \
                #                             bold_end + \
                #                             sentence['sentence_text'][word_end_index:]
                # index_shift_amount += len(bold_start) + len(bold_end)

        search_stats = {
            "words": found_words_amount,
            "sentences": sentence_amount,
            "pages": len(result),
        }

        session['search_results'][file_id] = {}
        session['search_stats'][file_id] = {}

        session['search_results'][file_id][original_query] = result
        session['search_stats'][file_id][original_query] = search_stats

    if results_page_id > len(session['search_results'][file_id][original_query]):
        return [], {"words": 0, "sentences": 0, "pages": 0}

    return session['search_results'][file_id][original_query][results_page_id-1], \
           session['search_stats'][file_id][original_query]


def check_word_tags(word, query):
    tags = word.pos_tags.split(',')
    for tag in query:
        if tag not in tags:
            break
    else:
        return True
