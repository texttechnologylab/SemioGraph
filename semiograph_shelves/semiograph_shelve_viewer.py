# -*- coding: utf-8 -*-

import argparse
import shelve


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='View SemioGraph shelve file')
    parser.add_argument('shelve_input_file',
                        type=str,
                        help='shelve input file')

    args = parser.parse_args()
    shelve_input_file = args.shelve_input_file

    print("opening shelve", shelve_input_file)
    with shelve.open(shelve_input_file) as embeddings_shelve:
        print("enter word to see nearest neighbors in shelve, CTRL+C to cancel")
        example_word = ""
        for word in embeddings_shelve:
            example_word = word
            break
        print("e.g. try '" + example_word + "'")
        try:
            while True:
                word = input("word: ")
                if word not in embeddings_shelve:
                    print(word, "not in shelve file...")
                    continue
                print(embeddings_shelve[word])
        except KeyboardInterrupt:
            print("exiting...")
