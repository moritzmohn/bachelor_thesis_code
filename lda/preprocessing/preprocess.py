import lzma
import spacy
from gensim.corpora import Dictionary
from gensim import corpora
import json

def read_tsv():
    
    data_list = []
    with lzma.open('data/dataset_84-23_v6.tsv.xz', mode='rt') as file:
        for line in file:
           l=line.split('\t')
           data_list.append(l)
    return data_list
    
def sort_corpus(data_list):
    data_list.sort(key = lambda row: row[1])
    return data_list
    
def save_sorted_data(data_list):
    with open("data/sorted_data_list_84-23_v6", "w") as fp:
        json.dump(data_list, fp)
    
    
def extract_content(data_list):

    content_list = []
    for article_list in data_list:
        content_list.append(article_list[-1])
    return content_list
        

def tokenize_lemmatize(data):

    # Preparing the data
    
    nlp = spacy.load("de_core_news_sm")
    lemmas = []
    
    index = 0
    for doc in nlp.pipe(data, disable=["parser", "ner"]):
        lemmas.append([])
        for token in doc:
            #only take certain pos tagged tokens and only take tokens with only letters and longer than 2 characters
            if token.pos_ in ['ADJ', 'NOUN', 'PROPN', 'VERB', 'X'] and token.lemma_.isalpha() and len(token.lemma_) > 2:
                lemmas[index].append(token.lemma_)
        index+=1
    
    return lemmas
    
def save_corpus_and_dict(preprocessed_data):
    dictionary = Dictionary(preprocessed_data)

    # Filter out words that occur less than 200 documents, or more than 25% of the documents.
    dictionary.filter_extremes(no_below=200, no_above=0.25, keep_n=None)

    # Bag-of-words representation of the documents.
    corpus = [dictionary.doc2bow(d) for d in preprocessed_data]
    
    dictionary.save('data/dictionary_84-23_v6')
    corpora.MmCorpus.serialize('data/corpus_84-23_v6', corpus)
    
    return dictionary, corpus
    
def main():
    data_list = read_tsv()
    data_list = sort_corpus(data_list)
    save_sorted_data(data_list)
    content_list = extract_content(data_list)
    preprocessed_data = tokenize_lemmatize(content_list)
    dictionary, corpus = save_corpus_and_dict(preprocessed_data)
    print('Number of unique tokens: %d' % len(dictionary))
    print('Number of documents: %d' % len(corpus))
    

   
if __name__ == '__main__':
    main() 
