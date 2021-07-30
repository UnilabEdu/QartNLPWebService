from app import celery
from app.database import db
from app.file_processing.nlp import *
from app.models.file import File, Pages, Sentences, Words, Statistics

from itertools import islice
from ftfy import fix_encoding
import os


@celery.task()
def process_file(id, user, filename, processes):
    from app.commands import manager

    with manager.app.app_context():
        file_path = os.path.join(Config.UPLOAD_FOLDER, str(user), filename)
        if "lemat" in processes:

            with open(file_path, "r", encoding='utf-8') as file:

                page_start = 0
                while True:
                    text = fix_encoding(''.join(islice(file, 75)))
                    if not text:
                        break

                    page_end = page_start + len(text)
                    page_db = Pages(id, page_start, page_end)
                    # print(f"Pages:  {page_start}, {page_end}")
                    page_db.flush()

                    # print(type(text))
                    list_of_sentences = split_sentences(text)

                    sentence_start = 0
                    for sentences in list_of_sentences:
                        sentence_end = sentence_start + len(sentences)
                        sentence_db = Sentences(page_db.id, sentence_start, sentence_end)
                        sentence_db.flush()
                        # print(f"Sentence: {page_db.id}, {sentence_start}, {sentence_end}")

                        lemmatized_words = lemmatize(tokenize(remove_punctuation(sentences)))
                        for word in lemmatized_words:
                            words_db = Words(sentence_db.id, word[3], word[4], word[0], word[1], word[2])
                            words_db.flush()
                            # print(f"Words: {sentence_db.id}, {word[3]}, {word[4]}, {word[0]}, {word[1]}, {word[2]}")

                        sentence_start = sentence_end + 1

                    page_start = page_end
                db.session.commit()

            file = File.file_by_id(id)
            statistics = Statistics(id, file.get_word_count(), file.get_unique_word_count(), file.get_sentence_count(),
                                    None, None)
            statistics.save()

            file.status[0].completed = True
            db.session.commit()
