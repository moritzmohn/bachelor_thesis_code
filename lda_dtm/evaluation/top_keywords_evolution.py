from gensim.models.wrappers import DtmModel
import pandas as pd

def one_topic_evolving_keywords(topic_id, model):

    for i in range(8):
        print("-" *40)
        print(model.show_topic(topic_id, i, 20))
        
        
def create_df_keywords(model):

    data_list = []

    for i in range(20):
    
        for time in range(8):
    
            keyword_list = [i, time, model.show_topic(i, time, 20)]
            data_list.append(keyword_list)
            
    df = pd.DataFrame(data_list, columns=['Topic ID', 'time span', 'keywords'])
    df.to_csv('tables/dtm_output.csv')
    print(df)

    



def main():
    
    model = DtmModel.load("model/model_dtm_84-23_20t.model")
    #one_topic_evolving_keywords(19, model)
    
    create_df_keywords(model)
    
    
if __name__ == '__main__':
    main()