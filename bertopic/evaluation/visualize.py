from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
import json

def get_sorted_plain_texts():
    with open("data/sorted_title_content_84-23", "r") as fp:
        data_list = json.load(fp)
    return data_list

def visualize_topics(model):

    plot = model.visualize_topics()
    plot.write_html('visualizations/v2_topics.html')
    
def visualize_documents(model, docs):

    sentence_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    embeddings = sentence_model.encode(docs, show_progress_bar=False)
    plot = model.visualize_documents(docs, embeddings=embeddings)
    plot.write_html('visualizations/test_model4_docs.html')
    
def visualize_hierarchy(model):

    fig = model.visualize_hierarchy()
    fig.write_html('visualizations/v6_hierarchy.html')
    
    



def main():
    
    model = BERTopic.load('models/static_model_84-23_v6')
    
    #data_list = get_sorted_plain_texts()
    #data_list.pop()
    #visualize_documents(model, data_list)
    
    #visualize_topics(model)
    visualize_hierarchy(model)
    
if __name__ == '__main__':
    main()