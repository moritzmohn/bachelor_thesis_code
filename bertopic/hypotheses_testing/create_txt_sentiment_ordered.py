import pandas as pd
from bertopic import BERTopic
import json
from germansentiment import SentimentModel
import spacy
from transformers import pipeline

def get_plane_docs(model, plain_texts):
    
    df = model.get_document_info(plain_texts)
    count = 0
    document_list = []
    
    for index, row in df.iterrows():
        if row["Topic"] == 3:
            document_list.append(row["Document"])
            count+=1
            
    print(count)    
    return document_list
   

   
def get_pos_neg_sentences(document_list, nlp, sentiment_model):
    
    positive_sentences = []
    negative_sentences = []
    
    #get the probabilities of sentence pairs
    for doc in document_list:
    
        doc = nlp(doc)
        index = 0
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
                    if classes == "positive":
                        positive_sentences.append((sentences, probabilities))
                    if classes == "negative":
                        negative_sentences.append((sentences, probabilities))
                        
    return negative_sentences, positive_sentences
            
def get_sentiment(doc, sentiment_model):

    classes, probabilities = sentiment_model.predict_sentiment([doc], output_probabilities = True)
    if classes[0] == "positive":
        return "positive", probabilities[0][0][1]
    if classes[0] == "negative":
        return "negative", probabilities[0][1][1]
    else:
        return "neutral", 0
        
def sort_sentences_list(list_of_tuples, ascending):
    
    if ascending:
        sorted_list = sorted(list_of_tuples, key=lambda x: x[1])
        
    else:
        sorted_list = reversed(sorted(list_of_tuples, key=lambda x: x[1]))
    return sorted_list
    
def attach_senti_word(sentence_list, word):

    new_list = []
    
    for pair in sentence_list:
    
        new_sent = pair[0] + " " + word
        new_list.append(new_sent)
        
    return new_list
    
def write_txt_file(positive_sentences, negative_sentences):

    with open('hypotheses_testing/planes_docs_v1.txt', 'w') as f:
        for sentence in negative_sentences:
            f.write(sentence + '\n')
        for sentence in positive_sentences:
            f.write(sentence + '\n')
    
    
def main():
    
    model = BERTopic.load("models/static_model_84-23_v6")
    with open("data/sorted_title_content_84-23_v6", "r") as fp:
        plain_texts = json.load(fp)
        
    plain_texts.pop()
        
    document_list = get_plane_docs(model, plain_texts)
    sentiment_model = SentimentModel()
    
    nlp = spacy.load("de_core_news_sm")
    nlp.add_pipe("sentencizer")
    
    negative_sentences, positive_sentences = get_pos_neg_sentences(document_list, nlp, sentiment_model)
    
    sorted_negative = sort_sentences_list(negative_sentences, False)
    sorted_positive = sort_sentences_list(positive_sentences, True)
    
    positive_complete = attach_senti_word(sorted_positive, "sentipositive")
    negative_complete = attach_senti_word(sorted_negative, "sentinegative")
    
    print(len(positive_complete))
    print(len(negative_complete))
    
    write_txt_file(positive_complete, negative_complete)
    
    
    
if __name__ == '__main__':
    main()