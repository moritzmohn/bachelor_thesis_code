from gensim.models import LdaModel
import gensim
from gensim import corpora
import matplotlib.pyplot as plt
import numpy as np

def get_distribution_timeslice(corpus, start, end, model):
    '''get the distribution over topics for one timeslice / calculated as the average attention for a topic in a document (only use documents in the timeslice)'''
    num_docs = end - start
    
    scores =[0] * 20
    
    for doc_bow in corpus[start:end]:
    
        for topic_id, score in model.get_document_topics(doc_bow):
            scores[topic_id] += score
        
    average_score = [score / num_docs for score in scores]
    return average_score
    
    
def get_all_distributions(timeslices, corpus, model):
    '''get all distributions for all timeslices'''
    
    all_dist = []
    current_start = 0
    current_end = 0
    
    for num_docs in timeslices:
        current_end+=num_docs
        all_dist.append(get_distribution_timeslice(corpus, current_start, current_end, model))
        current_start = current_end
        
    return all_dist
    
def create_line_chart_planes(distributions):

    '''create a line chart showing the evolution of attention for some topics'''

    y_4 = [array[16] for array in distributions]
    x = ["1984-88", "1989-93", "1994-98", "1999-2003", "2004-08", "2009-13", "2014-18", "2019-23"]
    
    plt.figure(figsize=(9,6), dpi=300)
    plt.plot(x, y_4, label='topic 16')
    
    plt.xlabel("year")  # add X-axis label
    plt.ylabel("attention")
    
    plt.legend()
    plt.savefig('time_series/planes_lda.png')
    

def create_line_chart_gotthard(distributions):

    '''create a line chart showing the evolution of attention for some topics'''

    y_4 = [array[10] for array in distributions]
    x = ["1984-88", "1989-93", "1994-98", "1999-2003", "2004-08", "2009-13", "2014-18", "2019-23"]
    
    plt.figure(figsize=(9,6), dpi=300)
    plt.plot(x, y_4, label='topic 10')
    
    plt.xlabel("year")  # add X-axis label
    plt.ylabel("attention")
    
    plt.legend()
    plt.savefig('time_series/gotthard_lda.png')


def main():

    corpus = corpora.MmCorpus('data/corpus/corpus_84-23_v6')
    model = LdaModel.load('model/models_v6/model_static_84-23_20t_v6.model')
    
    distributions = get_all_distributions([144,384,12008,31680,32204,26269,22273,16413], corpus, model)
    
    create_line_chart_planes(distributions)
    create_line_chart_gotthard(distributions)
    
if __name__ == '__main__':
    main()