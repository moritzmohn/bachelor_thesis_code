import gensim
from gensim import corpora
from gensim.models import LdaModel
from gensim.corpora import Dictionary

import logging

def train_model(dictionary, corpus):

    # Set training parameters.
    num_topics = 23
    chunksize = 1000
    passes = 25
    iterations = 600
    eval_every = None

    # Make an index to word dictionary.
    temp = dictionary[0]  # This is only to "load" the dictionary.
    id2word = dictionary.id2token

    model = LdaModel(
        corpus=corpus,
        id2word=id2word,
        chunksize=chunksize,
        alpha='auto',
        eta='auto',
        iterations=iterations,
        num_topics=num_topics,
        passes=passes,
        eval_every=eval_every
    )

    model.save('model/models_v6/model_static_84-23_23t_v6.model')
    return model



def main():
    
    logging.basicConfig(format ='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level = logging.INFO)
    dictionary = corpora.Dictionary.load('data/dictionary/dictionary_84-23_v6')
    corpus = corpora.MmCorpus('data/corpus/corpus_84-23_v6')
    
    model = train_model(dictionary, corpus)
    
    top_topics = model.print_topics()
    print(top_topics)
    
if __name__ == '__main__':
    main()