from app import celery
from app.file_processing.nlp import *
from app.settings import Config
from app.models.file import Pages, Sentences, Words
from app.database import db
from itertools import islice

from ftfy import fix_encoding
import json
import os
import time


@celery.task()
def process_file(id, filename, processes):

    file_path = os.path.join(Config.UPLOAD_FOLDER, filename)

    if "lemat" in processes:

        with open(file_path, "r", encoding='utf-8') as file:

            page_start = 0
            while True:
                text = ''.join(islice(file, 25))
                if not text:
                    break

                print(text)
                page_end = page_start + len(text)
                page_db = Pages(id, page_start, page_end)
                #print(f"Pages:  {page_start}, {page_end}")
                page_db.flush()

                #print(type(text))
                list_of_sentences = split_sentences(text)

                sentence_start = 0
                for sentences in list_of_sentences:
                    sentence_end = sentence_start + len(sentences)
                    sentence_db = Sentences(page_db.id, sentence_start, sentence_end)
                    sentence_db.flush()
                    #print(f"Sentence: {page_db.id}, {sentence_start}, {sentence_end}")

                    lemmatized_words = lemmatize(tokenize(remove_punctuation(sentences)))
                    for word in lemmatized_words:
                        words_db = Words(sentence_db.id, word[3], word[4], word[0], word[1], word[2])
                        words_db.flush()
                        #print(f"Words: {sentence_db.id}, {word[3]}, {word[4]}, {word[0]}, {word[1]}, {word[2]}")

                    sentence_start = sentence_end + 1

                page_start = page_end + 1
            #db.session.commit()


# @celery.task()
# def process_file(file, processes):
#
#     path = os.path.join(Config.UPLOAD_FOLDER, file)
#
#     with open(path, "r", encoding='utf-8') as fp:
#         text = fix_encoding(fp.read())
#         lenght_of_file = len(text)
#
#     if "freq_dist" in processes:
#         result_json = frequency_distribution(text)
#         data = json.dumps(result_json, ensure_ascii=False, indent=1)
#         with open(f"app/uploads/freq_dist.json", "w", encoding='utf-8') as fp:
#             fp.write(data)
#
#     if "lemat" in processes:
#         list_of_sentences = split_sentences(text)
#         i = 0
#
#         while i < len(list_of_sentences):
#             text_chunk = list_of_sentences[i:i+25]
#             print(text_chunk)
#             page_db = Pages(i, i+25)
#             db.session.add(page_db)
#             db.session.flush()
#
#             start_index = 0
#             end_index = 0
#
#             start_time = time.time()
#             for words in text_chunk:
#                 end_index = start_index + len(words)
#                 sentence_db = Sentences(page_db.id, start_index, end_index)
#                 db.session.add(sentence_db)
#                 db.session.flush()
#                 start_index = end_index + 1
#
#                 lemmatized_words = lemmatize(tokenize(remove_punctuation(words)))
#
#                 for word in lemmatized_words:
#                     words_db = Words(sentence_db.id, word[3], word[4], word[0], word[1], word[2])
#                     db.session.add(words_db)
#
#             db.session.commit()
#             i += 25
#
#             print("Total time elapsed: ", time.time() - start_time)