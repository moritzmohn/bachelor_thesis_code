import json
from bertopic import BERTopic
import pandas as pd

def get_sorted_data_list():
    with open("data/sorted_data_list_84-23_v6", "r") as fp:
        data_list = json.load(fp)
    return data_list
    
def get_sorted_plain_texts():
    with open("data/sorted_title_content_84-23_v6", "r") as fp:
        data_list = json.load(fp)
    return data_list
    
def read_data_frame():
    
    df = pd.read_csv("tables/dtm_84-23_v2.csv")
    return df
    
def get_timestamps(data_list):

    timestamps = []
    
    for article in data_list:
        timestamps.append(article[1][:10])
        
    return timestamps
    
def train_dynamic(model, plain_texts, timestamps):

    topics_over_time = model.topics_over_time(plain_texts, timestamps, nr_bins=8, evolution_tuning = False, global_tuning = False)
    
    topics_over_time.to_csv('tables/dtm_84-23_v6.csv')
    
    return topics_over_time
    
def visualize_topics_over_time(model, topics_over_time):

    plot = model.visualize_topics_over_time(topics_over_time, topics=[0, 2, 3, 17], normalize_frequency=True)
    plot.write_html('visualizations/dtm_maintransport_normalized_84-23.html')
    

    
    
def main():

    plain_texts = get_sorted_plain_texts()
    data_list = get_sorted_data_list()
    
    model = BERTopic.load("models/static_model_84-23_v6")
    
    timestamps = get_timestamps(data_list)
    
    timestamps.pop()
    plain_texts.pop()
    
    print(len(plain_texts))
    print(len(timestamps))
    
    
    topics_over_time = train_dynamic(model, plain_texts, timestamps)
    
    
    #topics_over_time = read_data_frame()
    #visualize_topics_over_time(model, topics_over_time)
    
   
if __name__ == '__main__':
    main() 