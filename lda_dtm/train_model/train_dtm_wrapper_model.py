from gensim.models.wrappers import DtmModel

import gensim
from gensim import corpora
from gensim.corpora import Dictionary

import logging

def train_model(corpus, timeslices, dictionary):

    path_to_dtm_binary = "dtm/dtm/main"
    
    # Make an index to word dictionary.
    temp = dictionary[0]  # This is only to "load" the dictionary.
    id2word = dictionary.id2token
    
    model = DtmModel(
            path_to_dtm_binary,
            corpus=corpus,
            id2word=id2word,
            time_slices=timeslices,
            num_topics=20,
            lda_sequence_min_iter=6,
            lda_sequence_max_iter=12,
            lda_max_em_iter=10
            )

    model.save('model/model_dtm_84-23_20t.model')
    
    return model


def main():
    
    logging.basicConfig(format ='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level = logging.INFO)
    
    dictionary = corpora.Dictionary.load('data/dictionary_84-23_v6')
    corpus = corpora.MmCorpus('data/corpus_84-23_v6')
    
    ldadtm = train_model(corpus, [144, 384, 12008, 31680, 32204, 26269, 22273, 16414], dictionary)
    
    print(ldadtm.show_topics())
    
    
if __name__ == '__main__':
    main()

