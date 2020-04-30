# -*- coding: utf-8 -*-

import pickle
import shelve


def try_get_pos(word):
    data = word.split('_')
    if len(data) == 2:
        return "".join(data[0:-1]), data[-1]
    return word, None


def generate_pickle(pickle_filename, embedding_filename):
    all_words = {}

    # prepare words in shelve for search functionality
    with shelve.open(embedding_filename) as embeddings_shelve:
        num = len(embeddings_shelve)
        counter = 0
        for word in embeddings_shelve:
            counter += 1
            if counter % 1000 == 0:
                print("search:", counter, "/", num)

            # skip empty/invalid words
            if word is not None and word != "":
                # get word without pos for search
                word_nopos, word_pos = try_get_pos(word)

                # search lowercase
                word_search = word_nopos.lower()

                # get first char to cluster search words
                first_char = ""
                if len(word_search) > 0:
                    first_char = word_search[0]

                if first_char not in all_words:
                    all_words[first_char] = {}

                words = all_words[first_char]
                if word_search in words:
                    # add to existing
                    if word not in words[word_search]["w"]:
                        words[word_search]["w"].append(word)
                else:
                    # add new
                    words[word_search] = {
                        "w": [word],
                        "s": word_search,
                    }

        print("search:", counter, "/", num)

    print("writing search file...")
    with open(pickle_filename, "wb") as pickle_file:
        pickle.dump(all_words, pickle_file, protocol=pickle.HIGHEST_PROTOCOL)
