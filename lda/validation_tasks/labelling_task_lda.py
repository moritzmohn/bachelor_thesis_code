from openai import OpenAI
import os
from gensim.models import LdaModel
import pandas as pd

def get_label_gpt(keywords):

    os.environ["OPENAI_API_KEY"] = ""
    client = OpenAI()

    completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": "You are a helpful assistant evaluating the most representative words of a topic model output for a given topic. Please provide a category in German describing the following keywords. Try to give very specific labels. The topic model is trained on Swiss newspaper articles from 1984 to 2023 and many of them are about traffic. The response can be one or two words long."},
        {"role": "user", "content": keywords}
      ],
      seed=0
    )

    return completion.choices[0].message.content
    
    
def create_dataframe_gpt_labels(model):

    data = {}
    data["topic_id"] = []
    data["label"] = []

    for topic_id in range(20):
        keywords = [item[0] for item in model.show_topic(topic_id, 10)]
        keywords = ", ".join(str(x) for x in keywords)
        
        label = get_label_gpt(keywords)
        
        data["topic_id"].append(topic_id)
        data["label"].append(label)
    
    df = pd.DataFrame(data)
    print(df)
    df.to_csv('tables/topic_labels/gpt_labels_v6.csv')

    


def main():

    model = LdaModel.load('model/models_v6/model_static_84-23_20t_v6.model')
    
    create_dataframe_gpt_labels(model)
    
    
    
    
    
if __name__ == '__main__':
    main()