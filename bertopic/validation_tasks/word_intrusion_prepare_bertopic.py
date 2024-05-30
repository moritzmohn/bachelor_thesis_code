import pandas as pd
from bertopic import BERTopic
import random


def get_term_top_3_topics(term, model):

    topics = model.find_topics(term, top_n = 5)
    topics = topics[0]
    
    return topics


def select_5_random_keywords(model, topic_id):

    keywords = [item[0] for item in model.get_topic(topic_id)]
    selection = random.sample(keywords, 5)

    return selection
    
    
def select_intruder(model, topic_id):

    keywords = []
    
    for index in range(37):
    
        if index == topic_id:
            continue
            
        else:
            keywords += [item[0] for item in model.get_topic(index)]
    
    while True:
        
        intruder = random.choice(keywords)
        
        if topic_id in get_term_top_3_topics(intruder, model) or intruder in [item[0] for item in model.get_topic(topic_id)]:
            continue
            
        else:
            break
            
    return intruder
    

    
def create_df(model):

    data = {}
    
    data["topic_id"] = []
    data["keywords"] = []
    data["intruder"] = []
    
    for topic_id in range(37):
    
        data["topic_id"].append(topic_id)
        data["keywords"].append(select_5_random_keywords(model, topic_id))
        data["intruder"].append(select_intruder(model, topic_id))
        
    df = pd.DataFrame(data)

    df.to_csv('tables/validation_evaluation/word_intrusion_v6.csv')


def main():

    model = BERTopic.load("models/static_model_84-23_v6")
    
    #print(select_5_random_keywords(model, 0))    
    
    #print(get_term_top_3_topics("BMW", model))
    #select_intruder(model, 0)
    
    create_df(model)
    
    
    
if __name__ == '__main__':
    main()