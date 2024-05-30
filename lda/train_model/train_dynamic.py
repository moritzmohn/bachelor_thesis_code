from gensim.models import LdaSeqModel
import gensim
from gensim import corpora
from gensim.models import LdaModel
from gensim.corpora import Dictionary

import logging


def train_model(corpus, time_slice, dictionary, static_model):

    # Make an index to word dictionary.
    temp = dictionary[0]  # This is only to "load" the dictionary.
    id2word = dictionary.id2token
    
    ldaseq = LdaSeqModel(corpus=corpus,
                        id2word=id2word,
                        time_slice=time_slice,
                        num_topics=20,
                        initialize='ldamodel',
                        lda_model=static_model,
                        em_min_iter=1,
                        em_max_iter=1,
                        chunksize=1000)
    
    ldaseq.save('model/model_dynamic_84-23_20t.model')
    return ldaseq


def main():
    
    logging.basicConfig(format ='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level = logging.INFO)
    
    dictionary = corpora.Dictionary.load('data/dictionary_84-23')
    corpus = corpora.MmCorpus('data/corpus_84-23')
    model = LdaModel.load('model/model_static_84-23_20t.model')
    
    ldaseq = train_model(corpus, [851, 2421, 50400, 121187, 132092, 113725, 91526, 68723], dictionary, model)
    print(ldaseq.print_topics(time=0))
    print(ldaseq.print_topic_times(topic=0))
    
if __name__ == '__main__':
    main()