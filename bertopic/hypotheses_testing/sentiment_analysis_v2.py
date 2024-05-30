import pandas as pd
from bertopic import BERTopic
import json
from germansentiment import SentimentModel
import spacy
from transformers import pipeline

def get_docs_per_timeslice(start, end, model, plain_texts):
    
    df = model.get_document_info(plain_texts)
    df_part = df.iloc[start:end]
    count = 0
    document_list = []
    
    for index, row in df_part.iterrows():
        if row["Topic"] == 3:
            document_list.append(row["Document"])
            count+=1
            
    print(count)    
    return document_list

   
def split_doc(doc, nlp, sentiment_model):

    doc = nlp(doc)
    index = 0
    probabilities_list = []
    
    
    #get the probabilities of sentence pairs
    for sent in doc.sents:
    
        sentence = " ".join([token.text for token in sent])
        if len(sentence) > 15:
        
            if index%2 == 0:
                sentences = sentence
                index += 1
            
            #get the probabilities after 2 sentences have been added together
            else:
                sentences = sentences + " " +  sentence
                index += 1
            
                classes, probabilities = get_sentiment(sentences, sentiment_model)
                probabilities_list.append(probabilities)
    
    #get the sentiment of a whole document
    sentiment_total = {'positive': 0, 'negative': 0, 'neutral': 0}
    for probabilities in probabilities_list:
        for probability in probabilities[0]:
            sentiment_total[probability[0]] += probability[1]
            
    sentiment_doc = max(sentiment_total, key=sentiment_total.get)
    
    #return the probabilities of the sentence pairs and the sentiment of the document
    return probabilities_list, sentiment_doc
        
        
def get_sentiment(doc, sentiment_model):

    classes, probabilities = sentiment_model.predict_sentiment([doc], output_probabilities = True)
    return classes, probabilities

    
    

def get_sentiment_slice(document_list, sentiment_model, nlp):
    
    #total scores for sentiments
    sentiment_total = {'positive': 0, 'negative': 0, 'neutral': 0}
    #number of documents per class
    sentiment_doc_list = {'positive': 0, 'negative': 0, 'neutral': 0}
    
    classes_list = []
    all_probabilities_list = []
    
    
    for doc in document_list:
        probabilities_list, sentiment_doc = split_doc(doc, nlp, sentiment_model)
        all_probabilities_list += probabilities_list
        sentiment_doc_list[sentiment_doc] += 1
    
    #count together all probabilities
    for probabilities in all_probabilities_list:
        for probability in probabilities[0]:
            sentiment_total[probability[0]] += probability[1]
    
    total = len(all_probabilities_list)
    
    sentiment_weights = {k: v / total for k, v in sentiment_total.items()}
    print(sentiment_weights)
    print(sentiment_doc_list)
    

def get_negative_documents(document_list, sentiment_model):

    for i in range(len(document_list)):
    
        sentiment = sentiment_model.predict_sentiment(document_list[i])
        
        if sentiment[0] == "negative":
        
            print(document_list[i])


def main():
    
    model = BERTopic.load("models/static_model_84-23_v6")
    with open("data/sorted_title_content_84-23_v6", "r") as fp:
        plain_texts = json.load(fp)
        
    plain_texts.pop()
        
    #document_list = get_docs_per_timeslice(0,12536, model, plain_texts)
    document_list = get_docs_per_timeslice(124962,141375, model, plain_texts)
    sentiment_model = SentimentModel()
    
    nlp = spacy.load("de_core_news_sm")
    nlp.add_pipe("sentencizer")
    
    
    get_sentiment_slice(document_list, sentiment_model, nlp)
    
    #get_negative_documents(document_list, sentiment_model)
    
    
if __name__ == '__main__':
    main()