# SemioGraph

<img src="https://github.com/texttechnologylab/SemioGraph/blob/master/Semiograph.png" width="30%">
We introduce SemioGraph, that is, graphs whose vertices and edges are simultaneously mapped onto different systems of types or labels. To this end, we present a technique for visualizing SemioGraphs in an interactive manner. SemioGraph aims at coding as much information as possible within the same graph representation. This is interesting in cases such as word networks in which one has to visualize information units such as POS, node weight, node salience, node centrality etc. To showcase SemioGraph, we use word embedding networks. Word embeddings have become indispensable in the field of NLP, as they allow for significantly improving many tasks in machine learning. Therefore we built a website to facilitate the analysis of pre-trained word embedding models based on SemioGraph.


# Embeddings

## Use of existing embeddings
Embeddings can be visualized with Semiograph. We already created many embeddings, which are available for download under http://embeddings.texttechnologylab.org.

## Generation of new embeddings
<img src="https://github.com/texttechnologylab/SemioGraph/blob/master/SemiographPipeline.png" width="100%">

### Preprocessing


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

### Graphicalization
