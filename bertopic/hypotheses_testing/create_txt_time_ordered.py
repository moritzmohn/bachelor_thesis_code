import pandas as pd
from bertopic import BERTopic
import json
import spacy


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
    

def make_document_lists(timeslices, model, plain_texts):

    current_start = 528
    current_end = 528
    documents_lists = []
    
    for num_docs in timeslices:
        current_end+=num_docs
        document_list = get_docs_per_timeslice(current_start, current_end, model, plain_texts)
        current_start = current_end
        print(len(document_list))
        documents_lists.append(document_list)
        
    return documents_lists
    
def write_txt(documents_lists, nlp):

    file = open("hypotheses_testing/txt_files/bicycles_docs_time_de.txt", "w")
    
    for index, doc_list in enumerate(documents_lists):

        for doc in doc_list:
        
            split_doc(doc, nlp, file)
            
            if index == 0:
                file.write("1994\n")
            if index == 1:
                file.write("1999\n")
            if index == 2:
                file.write("2004\n")
            if index == 3:
                file.write("2009\n")
            if index == 4:
                file.write("2014\n")
            if index == 5:
                file.write("2019\n")
        

def split_doc(doc, nlp, file):

    doc = nlp(doc)
    index = 1
    sentences = ""
    
    #get the probabilities of sentence pairs
    for sent in doc.sents:
    
        sentence = " ".join([token.text for token in sent])
        
        if index%3 != 0:
            sentences = sentences + " " + sentence
            index += 1
        
        #put 3 sentences in file
        else:
            sentences = sentences + " " +  sentence
            index += 1
            file.write(sentences + "\n")
            sentences = ""
            
        

def main():
    
    model = BERTopic.load("models/static_model_84-23_v6")
    with open("data/sorted_title_content_84-23_v6", "r") as fp:
        plain_texts = json.load(fp)
        
    plain_texts.pop()
    
    nlp = spacy.load("de_core_news_sm")
    nlp.add_pipe("sentencizer")
        
    documents_lists = make_document_lists([12008,31680,32204,26269,22273,16413], model, plain_texts)
    write_txt(documents_lists, nlp)
    
    
    
    
    
if __name__ == '__main__':
    main()