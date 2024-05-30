import json
from bertopic import BERTopic
import pandas as pd
import matplotlib.pyplot as plt


def get_docs_per_timeslice(start, end, model, plain_texts):
    
    df = model.get_document_info(plain_texts)
    df_part = df.iloc[start:end]
    count = 0
    document_list = []
    
    for index, row in df_part.iterrows():
        if row["Topic"] == 29:
            document_list.append(row["Document"])
            count+=1
            
    print(count)    
    return document_list
    

def get_docs_with_word(document_list, word):

    count_with_word = 0
    total_count = 0
    
    for doc in document_list:
    
        total_count+=1
    
        if word in doc:
            count_with_word+=1
            #print(doc)
            
    return count_with_word, total_count
    
    
def get_all_counts(timeslices, plain_texts, model, word):
    '''get all distributions for all timeslices'''
    
    all_counts = []
    with_word_counts = []
    current_start = 0
    current_end = 0
    
    for num_docs in timeslices:
        current_end+=num_docs
        document_list = get_docs_per_timeslice(current_start, current_end, model, plain_texts)
        
        count, total_count = get_docs_with_word(document_list, word)
        
        all_counts.append(total_count)
        with_word_counts.append(count)
        current_start = current_end
        
    print("the total number of plane documents in slice: ")
    print(all_counts)
    print("the number of documents containing " + word)
    print(with_word_counts)
    
    ratio = [i / j for i, j in zip(with_word_counts, all_counts)]
    print("The ratios:")
    print(ratio)
    return ratio

    
def create_time_series(ratio1, ratio2, ratio3):

    x = ["1984-88", "1989-93", "1994-98", "1999-2003", "2004-08", "2009-13", "2014-18", "2019-23"]
    plt.figure(figsize=(9,6), dpi=300)
    plt.plot(x, ratio1, label='share of documents containing "Klima"')
    plt.plot(x, ratio2, label='share of documents containing "Klimawandel"')
    plt.plot(x, ratio3, label='share of documents containing "Emissionen"')
        
    plt.xlabel("time span")  # add X-axis label
    plt.ylabel("proportion")
    
    plt.legend()
    plt.savefig('time_series/plane_proportions_v2.png')
            

def main():
    
    model = BERTopic.load("models/static_model_84-23_v6")
    with open("data/sorted_title_content_84-23_v6", "r") as fp:
        plain_texts = json.load(fp)
        
    plain_texts.pop()
        
    #document_list = get_docs_per_timeslice(0,12536, model, plain_texts)
    #document_list = get_docs_per_timeslice(124962,141375, model, plain_texts)
    
    #get_docs_with_word(document_list, "Klima")
    
    '''
    ratio1 = get_all_counts([144,384,12008,31680,32204,26269,22273,16413], plain_texts, model, "Klima")
    ratio2 = get_all_counts([144,384,12008,31680,32204,26269,22273,16413], plain_texts, model, "Klimawandel")
    ratio3 = get_all_counts([144,384,12008,31680,32204,26269,22273,16413], plain_texts, model, "Emissionen")
    create_time_series(ratio1, ratio2, ratio3)
    '''
    ratio1 = get_all_counts([102689,38686], plain_texts, model, "Veloweg")
    ratio1 = get_all_counts([102689,38686], plain_texts, model, "Veloroute")
    ratio1 = get_all_counts([102689,38686], plain_texts, model, "Route")
    
    
    
    
if __name__ == '__main__':
    main()