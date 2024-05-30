from sentence_transformers import SentenceTransformer, util
import pandas as pd

def read_data_frame():
    
    df = pd.read_csv("tables/topic_labels/all_labels_csv.csv", sep = ';')
    return df


def compute_cosine_similarity(text1, text2, model):
    embeddigs1 = model.encode(text1, convert_to_tensor=True)
    embeddigs2 = model.encode(text2, convert_to_tensor=True)
    return util.cos_sim(embeddigs1, embeddigs2)
    
    
def get_similarity_relevant(df, model):

    similarity_sum = 0
    relevant_similarities = {}
    
    for ind in df.index:
    
        goldlabel = df['Goldlabel'][ind]
        gpt_label = df['GPT label'][ind]
        annotator_1 = df['Annotator 1'][ind]
        annotator_2 = df['Annotator 2'][ind]
        
        
        if ind in [0, 1, 2, 3, 11, 12, 13, 15, 18, 19, 22, 23, 24, 28, 29, 31, 33, 35, 36]:
            print(ind)
            print(goldlabel, gpt_label, annotator_1, annotator_2)
            
            sim1 = compute_cosine_similarity(goldlabel, annotator_1, model)
            sim2 = compute_cosine_similarity(goldlabel, annotator_2, model)
            sim3 = compute_cosine_similarity(goldlabel, gpt_label, model)
            
            sim_sum = sim1.item()+sim2.item()+sim3.item()
            #sim_sum = sim3.item()
            
            print(sim_sum)
            
            similarity_sum+=sim_sum
            
            relevant_similarities[ind] = sim_sum
            
    average = similarity_sum / 57
    #average = similarity_sum / 19
    print(average)
    return average, relevant_similarities
    

def get_similarity_nonrelevant(df, model):

    similarity_sum = 0
    nonrelevant_similarities = {}
    
    for ind in df.index:
    
        goldlabel = df['Goldlabel'][ind]
        gpt_label = df['GPT label'][ind]
        annotator_1 = df['Annotator 1'][ind]
        annotator_2 = df['Annotator 2'][ind]
        
        
        if ind in [4, 5, 6, 7, 8, 10, 14, 16, 17, 21, 25, 26, 27, 30, 32, 34]:
            print(ind)
            print(goldlabel, gpt_label, annotator_1, annotator_2)
            
            sim1 = compute_cosine_similarity(goldlabel, annotator_1, model)
            sim2 = compute_cosine_similarity(goldlabel, annotator_2, model)
            sim3 = compute_cosine_similarity(goldlabel, gpt_label, model)
            
            sim_sum = sim1.item()+sim2.item()+sim3.item()
            #sim_sum = sim3.item()
            
            print(sim_sum)
            
            similarity_sum+=sim_sum
            
            nonrelevant_similarities[ind] = sim_sum
            
    average = similarity_sum / 48
    #average = similarity_sum / 16
    print(average)
    return average, nonrelevant_similarities
    

def print_ordered_similarities(similarity_dictionay):

    sorted_dict = {k: v for k, v in sorted(similarity_dictionay.items(), key=lambda item: item[1])}
    print(sorted_dict)
        
    


def main():

    df = read_data_frame()
    model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    
    relevant_average, relevant_similarities = get_similarity_relevant(df, model)
    
    print_ordered_similarities(relevant_similarities)
    
    nonrelevant_average, nonrelevant_similarities = get_similarity_nonrelevant(df, model)
    
    print_ordered_similarities(nonrelevant_similarities)
      
if __name__ == '__main__':
    main()