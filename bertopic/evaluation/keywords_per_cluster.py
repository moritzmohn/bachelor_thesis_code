from bertopic import BERTopic
import json


def get_doc_info_df(model):
    with open("data/sorted_title_content_84-23", "r") as fp:
        data_list = json.load(fp)
        
    data_list.pop()
        
    df = model.get_document_info(data_list)
    return df
    
def count_keywords_per_cluster(df):

    keyword_dict = {}
    
    keywords = ['Verkehr', 'Mobilität', 'Strasse', 'Schiene', 'Fahrzeug', 'Auto', 'Flugzeug', 'Fahrrad', 'Velo', 'Bus', 'Tram', 'Eisenbahn', 'Postauto', 'Fussgänger', 'SBB']

    for i in range(65):
    
        keyword_dict[i] = {'Verkehr': 0, 'Mobilität': 0, 'Strasse': 0, 'Schiene': 0, 'Fahrzeug': 0, 'Auto': 0, 'Flugzeug': 0, 'Fahrrad': 0, 'Velo': 0, 'Bus': 0, 'Tram': 0, 'Eisenbahn': 0, 'Postauto': 0, 'Fussgänger': 0, 'SBB':0}
    
    keyword_dict[-1] = {'Verkehr': 0, 'Mobilität': 0, 'Strasse': 0, 'Schiene': 0, 'Fahrzeug': 0, 'Auto': 0, 'Flugzeug': 0, 'Fahrrad': 0, 'Velo': 0, 'Bus': 0, 'Tram': 0, 'Eisenbahn': 0, 'Postauto': 0, 'Fussgänger': 0, 'SBB':0}
    print(keyword_dict)    

    for ind in df.index:
        topic = df["Topic"][ind]
        for keyword in keywords:
            count = df['Document'][ind].count(keyword)
            keyword_dict[topic][keyword] += count
            
    return keyword_dict

def get_docs_only_car_street(df):

    dictionary = {}
    
    for i in range(65):
    
        dictionary[i] = 0
        
    dictionary[-1] = 0
        
    keywords = ['Verkehr', 'Mobilität', 'Schiene', 'Fahrzeug', 'Flugzeug', 'Fahrrad', 'Velo', 'Bus', 'Tram', 'Eisenbahn', 'Postauto', 'Fussgänger', 'SBB']
    
    for ind in df.index:
        count = 0
        topic = df["Topic"][ind]
        for keyword in keywords:
            count += df['Document'][ind].count(keyword)
        if count == 0:
            dictionary[topic] += 1
            
    return dictionary
    
def get_docs_automobil(df):

    dictionary = {}
    
    for i in range(65):
    
        dictionary[i] = 0
        
    dictionary[-1] = 0
    
    for ind in df.index:
        topic = df["Topic"][ind]
        count = df['Document'][ind].count("Automobil ")
        if count > 0:
            dictionary[topic]+=1
            
        
    return dictionary
    
def get_remaining_docs(df):

    keywords = ['Verkehr', 'Mobilität', 'Automobil', 'Fahrzeug', 'Flugzeug', 'Fahrrad', 'Velo', 'Bus', 'Tram', 'Eisenbahn', 'Postauto', 'Fussgänger', 'SBB']
    
    dictionary = {}
    
    for i in range(65):
    
        dictionary[i] = 0
        
    dictionary[-1] = 0
    
    for ind in df.index:
        topic = df["Topic"][ind]
        
        for keyword in keywords:
        
            count = df['Document'][ind].count(keyword)
            
            if count > 0:
                dictionary[topic]+=1
                break
                
    return dictionary
    
    
            


def main():
    
    model = BERTopic.load("models/static_model_84-23_v2")
    
    df = get_doc_info_df(model)
    
    print(get_remaining_docs(df))
    
    
    
    
if __name__ == '__main__':
    main()