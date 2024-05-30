import random
import pandas as pd
import ast
from openai import OpenAI
import os

def read_data_frame():
    
    df = pd.read_csv("tables/validation_evaluation/word_intrusion_v6.csv")
    return df
    
def make_keyword_lists(df):

    keyword_lists = []
    
    for ind in df.index:
        keywords = df["keywords"][ind]
        keywords = ast.literal_eval(keywords)
        keywords.append(df["intruder"][ind])
        random.shuffle(keywords)
        keywords = ", ".join(str(x) for x in keywords)
        keyword_lists.append(keywords)
        
    return keyword_lists
    
def get_label_gpt(keywords):

    os.environ["OPENAI_API_KEY"] = ""
    client = OpenAI()

    completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": "You are a helpful assistant evaluating the top words of a topic model output for a given topic. Select which word is the least related to all other words. If multiple words do not fit, choose the word that is most out of place. Reply with one or two words."},
        {"role": "user", "content": keywords}
      ],
      seed=0
    )

    return completion.choices[0].message.content
    
def gpt_word_intrusion(keyword_lists):

    data = {}
    data["selected intruder gpt"] = []

    for keyword_list in keyword_lists:
    
        data["selected intruder gpt"].append(get_label_gpt(keyword_list))
        
    df = pd.DataFrame(data)

    df.to_csv('tables/validation_evaluation/word_intrusion_gpt_v6.csv')   

def main():

    df = read_data_frame()
    keyword_lists = make_keyword_lists(df)
    
    data = {}
    data["keyword lists"] = keyword_lists
    df = pd.DataFrame(data)
    df.to_csv('tables/validation_evaluation/word_intrusion_humans_v6.csv') 
    
    gpt_word_intrusion(keyword_lists)

    
    
    
    
       
if __name__ == '__main__':
    main()