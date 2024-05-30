from gensim.models import LdaSeqModel
import gensim
from gensim import corpora
from gensim.models import LdaModel
import pandas as pd


def get_top_keywords_static(model, topic_id):

    keywords = [item[0] for item in model.show_topic(topic_id, 20)]
    return keywords
    
def get_top_keywords_dynamic(model, topic_id, time):

    return model.print_topic(topic_id, time, 10)
    
def get_top_keywords_evolving(model, topic_id):

    return model.print_topic_times(topic_id, 10)
    
    
def get_topic_distribution(model, corpus):

    scores =[0] * 20
    
    for doc_bow in corpus:
    
        for topic_id, score in model.get_document_topics(doc_bow):
            scores[topic_id] += score
            
    average_score = [score / 141375 for score in scores]
    return average_score

    
    
def get_table_keywords_static(model, nr_topics, corpus):

    data = {}
    data["topic"] = []
    data["keywords"] = []
    data["attention"] = []
    
    topic_distribution = get_topic_distribution(model, corpus)
    
    for topic in range(nr_topics):
        data["topic"].append(topic)
        data["keywords"].append(get_top_keywords_static(model, topic))
        data["attention"].append(topic_distribution[topic])
        
    df = pd.DataFrame(data)

    df.to_csv('tables/topics_20t_v6.csv')


def main():

    #dynamic_model = LdaSeqModel.load('model/model_dynamic.model')
    static_model = LdaModel.load('model/model_static_84-23_20t_v6.model')
    
    corpus = corpora.MmCorpus('data/corpus_84-23_v6')
    
    get_table_keywords_static(static_model, 20, corpus)
    
    
if __name__ == '__main__':
    main()

