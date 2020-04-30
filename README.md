# SemioGraph

<img src="https://github.com/texttechnologylab/SemioGraph/blob/master/Semiograph.png" width="30%">
We introduce SemioGraph, that is, graphs whose vertices and edges are simultaneously mapped onto different systems of types or labels. To this end, we present a technique for visualizing SemioGraphs in an interactive manner. SemioGraph aims at coding as much information as possible within the same graph representation. This is interesting in cases such as word networks in which one has to visualize information units such as POS, node weight, node salience, node centrality etc. To showcase SemioGraph, we use word embedding networks. Word embeddings have become indispensable in the field of NLP, as they allow for significantly improving many tasks in machine learning. Therefore we built a website to facilitate the analysis of pre-trained word embedding models based on SemioGraph.


# Embeddings

## Use of existing embeddings
Embeddings can be visualized with Semiograph. We already created many embeddings, which are available for download under http://embeddings.texttechnologylab.org.

## Generation of new embeddings
<img src="https://github.com/texttechnologylab/SemioGraph/blob/master/SemiographPipeline.png" width="100%">

### Preprocessing
The preprocessing was done by the **TextImager** (https://textimager.hucompute.org/). The resulting file (data/example.tei)  was prepared for vectorization according to the model of Mikolov, but others are also possible (data/trainingfile.txt). The example is a small extract from the corpus of the New York Times (2018 / 01).


### Vectorisation
After successfully creating a training file, the embeddings have to be calculated. There are several possibilities for this, we use **word2vec** and **fastText**. By adjusting parameters, different embeddings can be created. The parameters of embedding generation used in SemioGraph are documented by the individual entries.

**word2vec**
```
word2vec -train $trainingsfile -output $trainingresult
```
#### Exemplary training
```
word2vec -train $trainingsfile -output $trainingresult -size 500 -window 5 -iter 5
```

- *size* Set size of word vectors
- *window* Max skip length between words
- *iter* Count of training interations
- *cbow* Use the continuous bag of words model (1); (0) skip-gram model is used



**fastText**
```
fasttext skipgram -input $trainingsfile -output $trainingresult
```
#### Exemplary training
```
fasttext skipgram -input $trainingsfile -output $trainingresult -dim 300 -minn 3 -maxn 6 -epoch 5
```

- *skipgram* Replace with cbow to use continuous bag of words model instead
- *dim* Set size of word vectors
- *epoch* Count of training interations
- *minn*, *maxn* Min/max length of char ngram

For a list of all available arguments see https://github.com/facebookresearch/fastText/

### Graphicalization
The SemioGraph web interface uses SemioGraph shelve files for visualization. The shelves contain precalculated nearest neighbors data, for quick access instead of having to use the full embeddings files. Optionally, we also add DDC topic labels using text2ddc (available at https://textimager.hucompute.org/DDC/). To generate these shelves we use **Gensim**.

```
python3 semiograph_shelve_create.py [-n TOP_N] [--is_binary_file] [-l LANG] [--ignore_pos] [-i EMBEDDING_ID] [-c MIN_COUNT] [--min_count_corpus MIN_COUNT_CORPUS] embeddings_input_file shelve_output_file
```

#### Example

```
python3 semiograph_shelve_create.py $trainingresult "${trainingresult}.shelve" -n 50 --ignore_pos
```

We provide a simple **shelve-viewer** script to easily check the contents of a shelve. This opens a command prompt that allows to query the shelve for words.

#### Example

```
python3 semiograph_shelve_viewer.py "${trainingresult}.shelve"
```


# Cite

When using SemioGraph cite the following according to AGPL licence (http://www.gnu.org/licenses/agpl-3.0.en.html).

```
@article{Mehler:et:al:2020b,
    author={Mehler, Alexander and Geelhaar, Tim and Henlein, Alexander and Abrami, Giuseppe and Baumartz, Daniel and Uslu, Tolga and Hemati, Wahed and Jussen, Bernhard},
    title={The Frankfurt Latin Lexicon. From Morphological Expansion and Word Embeddings to SemioGraphs},
    journal={Studi e Saggi Linguistici},
    year={2020},
    note={accepted}
}
```
