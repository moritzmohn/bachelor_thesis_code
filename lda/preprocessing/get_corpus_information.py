import lzma
import spacy
from gensim.corpora import Dictionary
from gensim import corpora
import json
import pandas as pd

def get_sorted_data_list():
    with open("data/sorted_data_list_84-23_v6", "r") as fp:
        data_list = json.load(fp)
    return data_list
    
def generate_timeslices(data_list):
    #get how many documents are in each time slice
    timeslices = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0}
    for article_list in data_list:
        if article_list[1].startswith(('1984', '1985', '1986', '1987', '1988')):
            timeslices[1]+=1
        if article_list[1].startswith(('1989', '1990', '1991', '1992', '1993')):
            timeslices[2]+=1
        if article_list[1].startswith(('1994', '1995', '1996', '1997', '1998')):
            timeslices[3]+=1
        if article_list[1].startswith(('1999', '2000', '2001', '2002', '2003')):
            timeslices[4]+=1
        if article_list[1].startswith(('2004', '2005', '2006', '2007', '2008')):
            timeslices[5]+=1
        if article_list[1].startswith(('2009', '2010', '2011', '2012', '2013')):
            timeslices[6]+=1
        if article_list[1].startswith(('2014', '2015', '2016', '2017', '2018')):
            timeslices[7]+=1
        if article_list[1].startswith(('2019', '2020', '2021', '2022', '2023')):
            timeslices[8]+=1
    return timeslices
    
def get_newspapers(data_list):
    newspapers = {'WEW': 0, 'TA': 0, 'NZZ': 0, 'NMZ': 0, 'BZ': 0, 'BLI': 0, 'BAZ': 0}
    for article_list in data_list:
        if article_list[2] == 'TA':
            newspapers['TA'] += 1
        if article_list[2] == 'WEW':
            newspapers['WEW'] += 1
        if article_list[2] == 'NZZ':
            newspapers['NZZ'] += 1
        if article_list[2] == 'NMZ':
            newspapers['NMZ'] += 1
        if article_list[2] == 'BZ':
            newspapers['BZ'] += 1
        if article_list[2] == 'BLI':
            newspapers['BLI'] += 1
        if article_list[2] == 'BAZ':
            newspapers['BAZ'] += 1
    return newspapers
    
def get_newspapers_per_timeslice(data_list):

    WEW = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0}
    TA = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0}
    NZZ = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0}
    NMZ = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0}
    BZ = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0}
    BLI = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0}
    BAZ = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0}
    news_in_slice = {"WEW": WEW, "TA": TA, "NZZ": NZZ, "NMZ": NMZ, "BZ": BZ, "BLI": BLI, "BAZ": BAZ}
    for article_list in data_list:
    
        if article_list[1].startswith(('1984', '1985', '1986', '1987', '1988')):
            news_in_slice[article_list[2]][1] += 1
        if article_list[1].startswith(('1989', '1990', '1991', '1992', '1993')):
            news_in_slice[article_list[2]][2] += 1
        if article_list[1].startswith(('1994', '1995', '1996', '1997', '1998')):
            news_in_slice[article_list[2]][3] += 1
        if article_list[1].startswith(('1999', '2000', '2001', '2002', '2003')):
            news_in_slice[article_list[2]][4] += 1
        if article_list[1].startswith(('2004', '2005', '2006', '2007', '2008')):
            news_in_slice[article_list[2]][5] += 1
        if article_list[1].startswith(('2009', '2010', '2011', '2012', '2013')):
            news_in_slice[article_list[2]][6] += 1
        if article_list[1].startswith(('2014', '2015', '2016', '2017', '2018')):
            news_in_slice[article_list[2]][7] += 1
        if article_list[1].startswith(('2019', '2020', '2021', '2022', '2023')):
            news_in_slice[article_list[2]][8] += 1
            
    return news_in_slice
    
    
def get_doc_types(data_list):
    doc_types = {'PRD': 0, 'PND': 0, 'PJO': 0, 'PMA': 0}
    for article_list in data_list:
        if article_list[4] == 'PND':
            doc_types['PND'] += 1
        elif article_list[4] == 'PRD':
            doc_types['PRD'] += 1
        elif article_list[4] == 'PJO':
            doc_types['PJO'] += 1
        elif article_list[4] == 'PMA':
            doc_types['PMA'] += 1
    return doc_types
    
def get_data_frames(data_list):

    timeslices = generate_timeslices(data_list)
    dct = {k:[v] for k,v in timeslices.items()}
    df = pd.DataFrame(dct)
    df.to_csv('tables/corpus_info/corpus_info_timeslices_v6.csv')
    print(df)
    
    newspapers = get_newspapers(data_list)
    dct = {k:[v] for k,v in newspapers.items()}
    df = pd.DataFrame(dct)
    df.to_csv('tables/corpus_info/corpus_info_newspapers_v6.csv')
    print(df)
    '''
    doc_types = get_doc_types(data_list)
    dct = {k:[v] for k,v in doc_types.items()}
    df = pd.DataFrame(dct)
    print(df)
    '''
    
def get_data_frame_news_per_slice(news_per_slice):

    df = pd.DataFrame(news_per_slice)
    df.to_csv('tables/corpus_info/corpus_info_newspapers_per_slice_v6.csv')
    print(df)
    
def get_number_of_unique_tokens():
    
    dictionary = corpora.Dictionary.load('data/dictionary_84-23_v6')
    print('Number of unique tokens: %d' % len(dictionary))
    
def get_number_of_documents():

    corpus = corpora.MmCorpus('data/corpus_84-23_v6')
    print('Number of documents: %d' % len(corpus))
    
    
def main():
    data_list = get_sorted_data_list()
    get_data_frames(data_list)
    get_number_of_unique_tokens()
    get_number_of_documents()
    news_per_slice = get_newspapers_per_timeslice(data_list)
    print(news_per_slice)
    get_data_frame_news_per_slice(news_per_slice)
    
    
if __name__ == '__main__':
    main() 