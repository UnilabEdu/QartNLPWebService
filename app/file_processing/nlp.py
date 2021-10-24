from string import punctuation as default_punctuation
from collections import Counter as count_words
import re


from app.settings import Config

try:
    from app.file_processing.foma import FST
except ImportError:
    pass


def frequency_distribution(text):
    """
    Counts how many times a word occurs in a given sentence
    """
    unpunctuated_text = remove_punctuation(text)
    word_frequency = count_words(unpunctuated_text.split())

    return word_frequency


def remove_punctuation(text, punctuation=None):
    """
    Removes all punctuation from the input
    """

    if punctuation is None:
        translation_table = str.maketrans('', '', default_punctuation)
    else:
        translation_table = str.maketrans('', '', punctuation)

    unpunctuated_text = text.translate(translation_table)

    return unpunctuated_text


def split_sentences(text):

    sentences_list = []
    for sentence in text.split("."):
        sentences_list.append(sentence)

    return sentences_list


def tokenize(text):
    """
    Takes string as an input and splits it into a list of words
    """

    word_list = []
    for words in text.split():
        word_list.append(words)

    return word_list


def remove_html_tags(text):
    html_regex_pattern = re.compile('<.*?>')
    cleaned_text = re.sub(html_regex_pattern, '', text)

    return cleaned_text


def remove_trailing_spaces(text):
    while '  ' in text:
        text = text.replace('  ', ' ')

    return text


def remove_special_characters(text):
    return re.sub('\W', '', text)


def lemmatize(text):

    fst = FST.load(Config.NLP_LIBS_FOLDER + "\\geo.fst")

    lemmatized_words = []
    word_start = 0

    for word in text:

        lemmatization_result = list(fst.apply_up(word))

        if len(lemmatization_result) == 0:
            lemm_word = ''
            tags = ''
        else:
            split_result = list(lemmatization_result)[-1].split('+')

            if split_result[0] == "Pfv" or split_result[0] == "Ipfv":
                split_result[1], split_result[0] = split_result[0], split_result[1]

            lemm_word = split_result[0]
            tags = split_result[1:]

        word_end = word_start + len(word)
        list_separator = ','

        lemm_list = (word, lemm_word, list_separator.join(tags), word_start, word_end)

        word_start = word_end + 1
        lemmatized_words.append(lemm_list)

    return lemmatized_words


# def lemmatize(text):
#
#     fst = FST.load(Config.NLP_LIBS_FOLDER + "\\geo.fst")
#
#     lemmatized_words = []
#     word_start = 0
#
#     for word in text:
#
#         lemmatization_result = list(fst.apply_up(word))
#
#         if len(lemmatization_result) is 0:
#             lemm_word = ''
#             tags = ''
#         else:
#             split_result = list(lemmatization_result)[-1].split('+')
#
#             if (split_result[0] == "Pfv" or split_result[0] == "Ipfv"):
#                 split_result[1], split_result[0] = split_result[0], split_result[1]
#
#             lemm_word = split_result[0]
#             tags = split_result[1:]
#
#         word_end = word_start + len(word)
#
#         lemm_dict = {
#             'word': word,
#             'lemm': lemm_word,
#             'tags': tags,
#             'index' : {
#                 'start' : word_start,
#                 'end' : word_end
#             }
#         }
#
#         word_start = word_end + 1
#         lemmatized_words.append(lemm_dict)
#
#     return lemmatized_words
