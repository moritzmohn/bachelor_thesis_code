import pyLDAvis
import pyLDAvis.gensim
from gensim import corpora
from gensim.models import LdaModel
from gensim.corpora import Dictionary

def visualize(model, corpus, dictionary):

    vis_data = pyLDAvis.gensim.prepare(model, corpus, dictionary, sort_topics=False)
    pyLDAvis.save_html(vis_data, 'visualizations/20topics_84-23_pyldavis_v6.html')
    



def main():
    dictionary = corpora.Dictionary.load('data/dictionary_84-23_v6')
    corpus = corpora.MmCorpus('data/corpus_84-23_v6')
    
    model = LdaModel.load('model/model_static_84-23_20t_v6.model')
    
    visualize(model, corpus, dictionary)
    
if __name__ == '__main__':
    main()