from sentence_transformers import SentenceTransformer, util
import pandas as pd

def read_data_frame():
    
    df = pd.read_csv("tables/topic_labels/all_labels_csv.csv", sep = ';')
    return df


def compute_cosine_similarity(text1, text2, model):
    embeddigs1 = model.encode(text1, convert_to_tensor=True)
    embeddigs2 = model.encode(text2, convert_to_tensor=True)
    return util.cos_sim(embeddigs1, embeddigs2)
    
    
def get_gpt_similarity(df, model):

    similarity_sum = 0
    count = 0
    gpt_similarities = {}
    
    for ind in df.index:
    
        text1 = df['Goldlabel'][ind]
        text2 = df['GPT label'][ind]
        
        
        if ind != 5 and ind != 12 and ind != 14:
            print(ind)
            print(text1, text2)
            sim = compute_cosine_similarity(text1, text2, model)
            print(sim.item())
            similarity_sum+=sim.item()
            count+=1
            
            gpt_similarities[ind] = sim.item()
            
    average = similarity_sum / 17
    print(average)
    return average, gpt_similarities
    

def get_annotator_similarity(df, model):

    similarity_sum = 0
    count = 0
    annotator_similarities = {}
    
    for ind in df.index:
    
        goldlabel = df['Goldlabel'][ind]
        annotator_1 = df['Annotator 1'][ind]
        annotator_2 = df['Annotator 2'][ind]
        
        
        if ind != 5 and ind != 12 and ind != 14:
            print(ind)
            print(goldlabel, annotator_1, annotator_2)
            sim1 = compute_cosine_similarity(goldlabel, annotator_1, model)
            sim2 = compute_cosine_similarity(goldlabel, annotator_2, model)
            sim_sum = sim1.item()+sim2.item()
            
            print(sim_sum)
            
            similarity_sum+=sim_sum
            count+=1
            
            annotator_similarities[ind] = sim_sum
            
    average = similarity_sum / 34
    print(average)
    return average, annotator_similarities
    

def print_ordered_similarities(similarity_dictionay):

    sorted_dict = {k: v for k, v in sorted(similarity_dictionay.items(), key=lambda item: item[1])}
    print(sorted_dict)
        
    


def main():

    df = read_data_frame()
    model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    
    gpt_average, gpt_similarities = get_gpt_similarity(df, model)
    
    annotator_average, annotator_similarities = get_annotator_similarity(df, model)
    
    print_ordered_similarities(gpt_similarities)
      
if __name__ == '__main__':
    main()