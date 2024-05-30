import csv
import pandas as pd
from bertopic import BERTopic
import json


def get_content_top_3(id_topic):

    with open('tables/model_84-23_topics_v6.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
            if line_count == id_topic+2:
                for item in row[:-1]:
                    print(item)
                for item in row[-1].split("', "):
                    print(item)
                
            line_count += 1
            
def make_table_top_doc(nr_topics):

    data = {}
    data["topic_id"] = []
    
    for topic_index in range(nr_topics):
        data["topic_id"] += [topic_index]
        
    data["title"] = []
        
    with open('tables/model_84-23_topics_v2.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count >1:
                for item in row[-1].split("\n', "):
                    index = item.find(" //")
                    data["title"].append(item[2:index])
                
            line_count += 1
        
    df = pd.DataFrame(data)

    print(df)
    df.to_csv('tables/top_document_per_topic.csv')
    
def get_docs_per_topic(topic_id, model, plain_texts):
    
    df = model.get_document_info(plain_texts)
    
    for index, row in df.iterrows():
        if row["Topic"] == topic_id:
            print(row["Document"])

def main():
    
    model = BERTopic.load("models/static_model_84-23_v6")
    with open("data/sorted_title_content_84-23_v6", "r") as fp:
        plain_texts = json.load(fp)
        
    plain_texts.pop()
        
    get_docs_per_topic(1, model, plain_texts)


    #get_content_top_3(0)
    #make_table_top_doc(65)
    
    
if __name__ == '__main__':
    main()
