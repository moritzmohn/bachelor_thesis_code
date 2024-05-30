import csv
import pandas as pd
from bertopic import BERTopic
import json
import random
from openai import OpenAI
import os


def get_10_docs_per_topic(topic_id, model, plain_texts):
    
    df = model.get_document_info(plain_texts)
    
    doc_list = df.loc[df['Topic'] == topic_id, 'Document'].tolist()
    
    selection = random.sample(doc_list, 10)
    return selection
    
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
    
def get_df_experiment(model, plain_texts):

    goldlabels = {0: "Auto", 1: "Verkehrsunfall", 2: "Öffentlicher Verkehr", 3: "Luftfahrt", 4: "Politik Schweiz", 5: "Politik International", 6: "Gerichtsverhandlungen", 7: "Kriminalität", 8: "Unwetter", 10: "Brand", 11: "Verkehrskontrolle / Raser", 12: "Verkehrsunfall", 13: "Parkplätze", 14: "Schule / Schulweg", 15: "Tunnel", 16: "Wirtschaft", 17: "Sport", 18: "Unfallstatistik", 19: "Verkehrspolitik", 21: "Tiere", 22: "Motorradunfall", 23: "Brücken", 24: "Formel 1", 25: "Finanzpolitik", 26: "EU-Abkommen", 27: "Kultur / Veranstaltungen", 28: "Tempolimit", 29: "Velo", 30: "Digitale Technologien", 31: "Streiks", 32: "China", 33: "Busunfall", 34: "Pandemie", 35: "Strassenbau", 36: "Mobilität für Menschen mit Behinderungen"}
    topic_ids = list(range(37))
    topic_ids.remove(9)
    topic_ids.remove(20)
    
    data = {}
    data["goldlabel"] = []
    data["intruder 1"] = []
    data["intruder 2"] = []
    data["gpt guess"] = []
    data["doc"] = []
    
    for topic_id in topic_ids:
        docs = get_10_docs_per_topic(topic_id, model, plain_texts)
    
        for doc in docs:
        
            doc_short = get_50_first_words_doc(doc)
            data["doc"].append(doc_short)
            
            if topic_id == 1 or topic_id == 12:
                possible_choices = [v for v in topic_ids if v != 1 and v != 12]
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
    
    model = BERTopic.load("models/static_model_84-23_v6")
    with open("data/sorted_title_content_84-23_v6", "r") as fp:
        plain_texts = json.load(fp)
        
    plain_texts.pop()
    get_df_experiment(model, plain_texts)
    
    
if __name__ == '__main__':
    main()