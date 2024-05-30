from gensim.models import LdaModel
from gensim import corpora
import random
import pandas as pd


def get_term_top_3_topics(term, model, dictionary):

    index =  dictionary.doc2idx([term])
    topics = model.get_term_topics(index, minimum_probability=0.0001)
    topics.sort(key = lambda row: row[1][0], reverse = True)
    topics = [item[0] for item in topics][:3]
    
    return topics
    
def select_5_random_keywords(model, topic_id):

    keywords = [item[0] for item in model.show_topic(topic_id, 10)]
    selection = random.sample(keywords, 5)
    
    return selection
    
    
def select_intruder(model, topic_id, dictionary):

    keywords = []
    
    for index in range(20):
    
        if index == topic_id:
            continue
            
        else:
            keywords += [item[0] for item in model.show_topic(index, 10)]
    
    while True:
        
        intruder = random.choice(keywords)
        
        if topic_id in get_term_top_3_topics(intruder, model, dictionary):
            continue
            
        else:
            break
            
    return intruder
    

def create_df(model, dictionary):

    data = {}
    
    data["topic_id"] = []
    data["keywords"] = []
    data["intruder"] = []
    
    for topic_id in range(20):
    
        data["topic_id"].append(topic_id)
        data["keywords"].append(select_5_random_keywords(model, topic_id))
        data["intruder"].append(select_intruder(model, topic_id, dictionary))
        
    df = pd.DataFrame(data)

    df.to_csv('tables/validation_evaluation/word_intrusion_v6.csv')





def main():

    model = LdaModel.load('model/models_v6/model_static_84-23_20t_v6.model')
    dictionary = corpora.Dictionary.load('data/dictionary/dictionary_84-23_v6')
    
    #print(get_term_top_3_topics("Fahrzeug", model, dictionary))
    
    #select_5_random_keywords(model, 5)
    
    #select_intruder(model, 0, dictionary)
    
    create_df(model, dictionary)
    
    
    
       
if __name__ == '__main__':
    main()