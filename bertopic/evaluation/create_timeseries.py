import json
from bertopic import BERTopic
import pandas as pd
import matplotlib.pyplot as plt

def read_data_frame():
    
    df = pd.read_csv("tables/dtm/dtm_84-23_v6.csv")
    return df
    
def visualize_topics_over_time(model, topics_over_time):

    plot = model.visualize_topics_over_time(topics_over_time, topics=[0, 2, 3, 17], normalize_frequency=True)
    plot.write_html('visualizations/dtm_maintransport_normalized_84-23.html')
    

def get_score_over_time(topic_id, timeslices, topics_over_time):

    rows = topics_over_time.loc[topics_over_time['Topic'] == topic_id]
    total_freq = rows["Frequency"].tolist()
    
    weighted_freq = [i / j for i, j in zip(total_freq, timeslices)]
    print(weighted_freq)
    return weighted_freq
    

def create_linechart_planes(topics_over_time):

    topic_3 = get_score_over_time(3, [144,384,12008,31680,32204,26269,22273,16413], topics_over_time)
    x = ["1984-88", "1989-93", "1994-98", "1999-2003", "2004-08", "2009-13", "2014-18", "2019-23"]
    plt.figure(figsize=(9,6), dpi = 300)
    plt.plot(x, topic_3, label='Topic 3')
    
    
    plt.xlabel("year")  # add X-axis label
    plt.ylabel("attention")
    
    plt.legend()
    plt.savefig('time_series/planes.png')
    
def create_linechart_bicycles(topics_over_time):

    topic_29 = get_score_over_time(29, [12008,31680,32204,26269,22273,16413], topics_over_time)
    x = ["1994-98", "1999-2003", "2004-08", "2009-13", "2014-18", "2019-23"]
    plt.figure(figsize=(9,6), dpi = 300)
    plt.plot(x, topic_29, label='Topic 29')
    
    
    plt.xlabel("year")  # add X-axis label
    plt.ylabel("attention")
    
    plt.legend()
    plt.savefig('time_series/bicycles.png')

    
    
def main():
    
    model = BERTopic.load("models/static_model_84-23_v2")
    
    topics_over_time = read_data_frame()
    #visualize_topics_over_time(model, topics_over_time)
    
    create_linechart_bicycles(topics_over_time)
    create_linechart_planes(topics_over_time)
    
   
if __name__ == '__main__':
    main() 