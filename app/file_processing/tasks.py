from app import celery
from app.file_processing.nlp import *
from app.settings import Config
from app.models import Sentences, Words
from app.database import db

from ftfy import fix_encoding
import json
import os
import time


@celery.task()
def process_file(file, processes):

    path = os.path.join(Config.UPLOAD_FOLDER, file)

    with open(path, "r", encoding='utf-8') as fp:
        text = fix_encoding(fp.read())

    if "freq_dist" in processes:
        result_json = frequency_distribution(text)
        data = json.dumps(result_json, ensure_ascii=False, indent=1)
        with open(f"app/uploads/freq_dist.json", "w", encoding='utf-8') as fp:
            fp.write(data)

    if "token" in processes:
        pass

    if "lemat" in processes:

        list_of_sentences = split_sentences(text)
        start_index = 0
        end_index = 0

        start_time = time.time()
        for words in list_of_sentences:

            #print("######################")
            #sentences_time = time.time()

            end_index = start_index + len(words)
            sentence_db = Sentences(start_index, end_index)
            db.session.add(sentence_db)
            db.session.flush()

            #print("Adding sentence to db took: ", time.time() - sentences_time)

            start_index = end_index + 1

            #lemma_time = time.time()
            lemmatized_words = lemmatize(tokenize(remove_punctuation(words)))
            #print("Lemmatizing took: ", time.time() - lemma_time)


            for word in lemmatized_words:
                #word_db_time = time.time()

                words_db = Words(sentence_db.id, word[3], word[4], word[0], word[1], word[2])
                db.session.add(words_db)

                #print("Adding word to db took: ", time.time() - word_db_time)

        db.session.commit()

        # result_json = {"data": lemmatized_text}
        # data = json.dumps(result_json, ensure_ascii=False, indent=1)
        # with open(f"{Config.UPLOAD_FOLDER}lemmatized.json", "w", encoding='utf-8') as fp:
        #     fp.write(data)

        print("Total time elapsed: ", time.time() - start_time)