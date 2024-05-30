import csv
import pandas as pd
import json
import random
from openai import OpenAI
import os
from gensim.models import LdaModel
from gensim import corpora


def get_sorted_data_list():
    with open("data/sorted_data/sorted_title_content_84-23_v6", "r") as fp:
        plain_texts = json.load(fp)
    return plain_texts

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

    
def get_10_documents_of_topic(topic_id, docs_per_topic, plain_texts):

    doc_list = docs_per_topic[topic_id]
    possible_docs = [id_and_score for id_and_score in doc_list if id_and_score[1] > 0.5]
    if len(possible_docs) < 10:
        possible_docs = [id_and_score for id_and_score in doc_list if id_and_score[1] > 0.4]
    if len(possible_docs) < 10:
        possible_docs = [id_and_score for id_and_score in doc_list if id_and_score[1] > 0.3]
    
    selection = random.sample(possible_docs, 10)
    docs = []
    for id_and_score in selection:
        docs.append(plain_texts[id_and_score[0]])
    
    return docs
    
def get_50_first_words_doc(doc):

    result_list = doc.split()[:50]
    result_str = " ".join(result_list)
    return result_str
    
def get_label_gpt(doc, labels):

    os.environ["OPENAI_API_KEY"] = ""
    client = OpenAI()

    completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": "You are a helpful research assistant with lots of knowledge about topic models. You are given a document and three possible categories. Which of the following labels describes the document best: " + labels +
        " Reply only with one of the given labels"},
        {"role": "user", "content": doc}
      ],
      seed=0
    )

    return completion.choices[0].message.content
    
def get_df_experiment(plain_texts, docs_per_topic):

    goldlabels = {0: "Gerichtsprozess", 1: "Politik International", 2: "Auto", 3: "Wirtschaft", 4: "Verkehrsunfall", 6: "Politik Zürich", 7: "Lastwagenunfall", 8: "Bahnverkehr", 9: "Politik Europa", 10: "Gotthardtunnel", 11: "Wirtschaft", 13: "Veranstaltungen", 15: "Fahrzeugtechnik", 16: "Luftverkehr", 17: "Ortsplanung", 18: "Stadtverkehr", 19: "Politik Schweiz"}
    topic_ids = list(range(20))
    topic_ids.remove(5)
    topic_ids.remove(12)
    topic_ids.remove(14)
    
    data = {}
    data["goldlabel"] = []
    data["intruder 1"] = []
    data["intruder 2"] = []
    data["gpt guess"] = []
    data["doc"] = []
    
    for topic_id in topic_ids:
        docs = get_10_documents_of_topic(topic_id, docs_per_topic, plain_texts)
    
        for doc in docs:
        
            doc_short = get_50_first_words_doc(doc)
            data["doc"].append(doc_short)
            
            if topic_id == 3 or topic_id == 11:
                possible_choices = [v for v in topic_ids if v != 3 and v != 11]
            else:
                possible_choices = [v for v in topic_ids if v != topic_id]
                
            intruder_topics = random.sample(possible_choices, 2)
            
            goldlabel = goldlabels[topic_id]
            intruder1 = goldlabels[intruder_topics[0]]
            intruder2 = goldlabels[intruder_topics[1]]
            
            data["goldlabel"].append(goldlabel)
            data["intruder 1"].append(intruder1)
            data["intruder 2"].append(intruder2)
            
            labels = [goldlabel, intruder1, intruder2]
            random.shuffle(labels)
            labels = ", ".join(str(x) for x in labels)
            
            #gpt request
            gpt_label = get_label_gpt(doc_short, labels)
            
            data["gpt guess"].append(gpt_label)
        
    df = pd.DataFrame(data)
    print(df)
    df.to_csv('tables/validation_evaluation/topic_intrusion_v6.csv')
    
    
    
def main():
    
    plain_texts = get_sorted_data_list()
    corpus = corpora.MmCorpus('data/corpus/corpus_84-23_v6')
    model = LdaModel.load('model/models_v6/model_static_84-23_20t_v6.model')
    docs_per_topic = get_documents_per_topic(model, corpus)
    
    get_df_experiment(plain_texts, docs_per_topic)    
    
    
if __name__ == '__main__':
    main()