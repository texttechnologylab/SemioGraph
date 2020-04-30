# -*- coding: utf-8 -*-

import argparse
from sys import exit

import nn
import search

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create SemioGraph shelve files')
    parser.add_argument('embeddings_input_file',
                        type=str,
                        help='embeddings input file')
    parser.add_argument('shelve_output_file',
                        type=str,
                        help='shelve output file, _search added for search data')
    parser.add_argument('-n', '--top_n',
                        type=int,
                        help='top n nearest neighbors to calculate, set to -1 for all',
                        default=100)
    parser.add_argument('--is_binary_file',
                        action='store_true',
                        help='is embeddings filetype binary?')
    parser.add_argument('-l', '--lang',
                        type=str,
                        help='language',
                        default='de')
    parser.add_argument('--ignore_pos',
                        action='store_true',
                        help='ignore and remove pos')
    parser.add_argument('-i', '--embedding_id',
                        type=str,
                        help='id of the embedding, if empty automatically generated from filename',
                        default='')
    parser.add_argument('-c', '--min_count',
                        type=int,
                        help='minimal count of words in corpus to include',
                        default=0)
    parser.add_argument('--min_count_corpus',
                        type=str,
                        help='corpus to use for min-count calculation')

    args = parser.parse_args()
    input_file_embeddings = args.embeddings_input_file
    output_file_shelve = args.shelve_output_file
    top_n = args.top_n if args.top_n >= 0 else None
    is_binary_file = args.is_binary_file
    lang = args.lang
    ignore_pos = args.ignore_pos
    embedding_id = args.embedding_id
    min_count = args.min_count
    min_count_corpus = args.min_count_corpus

    # usage of min-count requires corpus filename
    if min_count > 0 and not min_count_corpus:
        print("min_count is >0 but no corpus specified")
        exit(1)

    print("creating SemioGraph shelve file")
    print("embeddings imput:", input_file_embeddings)
    print("output file:", output_file_shelve)

    # use filename for embedding id
    if embedding_id == '':
        embedding_id = output_file_shelve.split("/")[-1]
        print("auto generated embedding id:", embedding_id)

    # step 1: precalculate the top n nearest neighbors
    nn.generate_shelve(input_file_embeddings, output_file_shelve,
                       top_n, is_binary_file,
                       lang, ignore_pos,
                       min_count, min_count_corpus)

    # DDC steps ommitted
    # ...

    # step 5: generate search data
    search_data_filename = output_file_shelve + '_search'
    search.generate_pickle(search_data_filename, output_file_shelve)

    print("done")
