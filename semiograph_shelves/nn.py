# -*- coding: utf-8 -*-

import shelve

import gensim.models.keyedvectors as word2vec


def word_ok(word, lang):
    # filter words based on their pos
    data = word.split('_')
    if len(data) == 2:
        pos = data[-1]
        # TODO make user configurable
        if lang == "en":
            return pos == 'PROPN' or pos == 'NOUN' or pos == 'VERB' or pos == 'ADJ'
        else:
            return pos == 'NE' or pos == 'NN' or pos == 'V' or pos == 'ADJ'
    return False


def generate_shelve(embeddings_file, output_filename, top_n, is_binary_file, lang, ignore_pos, min_count, min_count_corpus):
    # load/tokenize corpus if needed
    corpus = {}
    if min_count > 0 and min_count_corpus:
        print("loading corpus file", min_count_corpus)
        corpus_total = 0
        with open(min_count_corpus, "r", encoding="UTF-8") as corpus_file:
            for line in corpus_file:
                words = line.strip().split(" ")
                for word in words:
                    corpus_total += 1
                    if corpus_total % 1000 == 0:
                        print("corpus:", len(corpus), "unique words,", corpus_total, "total")
                    if word not in corpus:
                        corpus[word] = 1
                    else:
                        corpus[word] += 1
        print("corpus:", len(corpus), "unique words,", corpus_total, "total")

    # load embedding file
    embeddings = word2vec.KeyedVectors.load_word2vec_format(embeddings_file, binary=is_binary_file,
                                                            encoding='utf8', unicode_errors='ignore')

    # write precalculated nn to shelve file
    with shelve.open(output_filename) as db:
        counter_exports = 0
        counter_all = 0
        num = len(embeddings.vocab)
        initial_top_n = top_n
        if top_n is None or min_count > 0:
            top_n = num

        for word in embeddings.vocab:
            counter_all += 1
            if counter_all % 1000 == 0:
                print("exported:", counter_exports, "/", counter_all, "from", num)

            # sync to shelve regularly
            if counter_all % 100000 == 0:
                db.sync()

            # filter words using pos
            if not ignore_pos and not word_ok(word, lang):
                continue

            counter_exports += 1

            # get nn from embedding
            ms = embeddings.most_similar(word, topn=top_n)

            if min_count > 0:
                # filter and limit to initial_top_n
                # always take if word not in corpus (e.g. </s>...)
                ms = [s for s in ms if s[0] not in corpus or corpus[s[0]] >= min_count][:initial_top_n]

            db[word] = ms

        # final sync
        db.sync()
        print("exported:", counter_exports, "/", counter_all, "from", num)
