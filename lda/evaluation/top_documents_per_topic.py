import gensim
from gensim.models import LdaModel
from gensim import corpora
import json
import pandas as pd


def get_sorted_data_list():
    with open("data/sorted_data/sorted_data_list_84-23_v6", "r") as fp:
        data_list = json.load(fp)
    return data_list

def get_documents_per_topic(model, corpus):
    
    # setup: get the model's topics in their native ordering...
    all_topics = model.print_topics()
    print(all_topics)
    # ...then create a empty list per topic to collect the docs:
    docs_per_topic = [[] for _ in all_topics]
    
    # now, for every doc...
    for doc_id, doc_bow in enumerate(corpus):
        # ...get its topics...
        doc_topics = model.get_document_topics(doc_bow)
        # ...& for each of its topics...
        for topic_id, score in doc_topics:
            # ...add the doc_id & its score to the topic's doc list
            docs_per_topic[topic_id].append((doc_id, score))
            
    return docs_per_topic
    
def get_top_document_of_topic(topic_id, docs_per_topic, data_list, ranking):

    doc_list = docs_per_topic[topic_id]
    doc_list.sort(key=lambda id_and_score: id_and_score[1], reverse=True)
    top_id = doc_list[ranking][0]
    top_score = doc_list[ranking][1]
    return data_list[top_id], top_score, top_id
    
def get_data_frame_topdocuments(docs_per_topic, corpus, data_list, nr_topics):

    data = {}
    data["topic_id"] = []
    
    for topic_index in range(nr_topics):
        data["topic_id"] += [topic_index] * 10
    
    data["score"] = []
    data["newspaper"] = []
    data["title"] = []
    data["content"] = []
    
    for topic_id in range(nr_topics):
        for ranking in range(10):
            all_info, top_score, document_id = get_top_document_of_topic(topic_id, docs_per_topic, data_list, ranking)
            data["score"].append(top_score)
            data["title"].append(all_info[5])
            data["newspaper"].append(all_info[3])
            data["content"].append(all_info[-1])
    
    df = pd.DataFrame(data)

    print(df)
    df.to_csv('tables/validation_evaluation/documents_per_topic_v6.csv')



def main():
    corpus = corpora.MmCorpus('data/corpus/corpus_84-23_v6')
    model = LdaModel.load('model/models_v6/model_static_84-23_20t_v6.model')
    data_list = get_sorted_data_list()
    docs_per_topic = get_documents_per_topic(model, corpus)
    
    get_data_frame_topdocuments(docs_per_topic, corpus, data_list, 20)
    
if __name__ == '__main__':
    main()