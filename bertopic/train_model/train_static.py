from bertopic import BERTopic
from hdbscan import HDBSCAN
from sklearn.feature_extraction.text import CountVectorizer
from bertopic.representation import PartOfSpeech
from bertopic.vectorizers import ClassTfidfTransformer
from bertopic.representation import MaximalMarginalRelevance
from sentence_transformers import SentenceTransformer
from umap import UMAP
import json
import spacy


def get_sorted_plain_texts():
    with open("data/sorted_title_content_84-23", "r") as fp:
        data_list = json.load(fp)
    return data_list
    
def train_model(plain_texts):

    sentence_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    embeddings = sentence_model.encode(plain_texts, show_progress_bar=False)
    umap_embeddings = UMAP(n_neighbors=15, n_components=5, min_dist=0.0, metric='euclidean').fit_transform(embeddings)

    hdbscan_model = HDBSCAN(min_cluster_size=200, metric='euclidean', cluster_selection_method='eom', prediction_data=True)
    
    vectorizer_model = CountVectorizer(max_df = 0.5, min_df=10)
    
    ctfidf_model = ClassTfidfTransformer(reduce_frequent_words=True)
    
    pos_patterns = [
            [{'POS': 'ADJ'}],
            [{'POS': 'NOUN'}],
            [{'POS': 'PROPN'}]
    ]
    
    mmr = MaximalMarginalRelevance(diversity=0.9)
    pos = PartOfSpeech("de_core_news_sm", pos_patterns=pos_patterns)
    representation_models = [pos, mmr]

    topic_model = BERTopic(low_memory=True,
                            hdbscan_model=hdbscan_model,
                            ctfidf_model=ctfidf_model,
                            representation_model=representation_models,
                            vectorizer_model=vectorizer_model)
                            
    topics, probs = topic_model.fit_transform(plain_texts, umap_embeddings)
    
    table = topic_model.get_topic_info()
    table.to_csv('tables/model_84-23_topics.csv')
    print(topic_model.get_topic_info())
    print(topic_model.get_topic(0))
    
    return topic_model
    
def save_model(topic_model):

    # Method 1 - safetensors
    embedding_model = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    topic_model.save("models/static_model_84-23", serialization="safetensors", save_ctfidf=True, save_embedding_model=embedding_model)

    
    
    
def main():
    plain_texts = get_sorted_plain_texts()
    plain_texts.pop()
    
    topic_model = train_model(plain_texts)
    save_model(topic_model)
    
    
    

   
if __name__ == '__main__':
    main() 