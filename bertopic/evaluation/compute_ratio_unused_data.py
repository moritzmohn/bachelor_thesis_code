from transformers import AutoTokenizer
import json

def get_sorted_plain_texts():
    with open("data/sorted_title_content_84-23_v6", "r") as fp:
        data_list = json.load(fp)
    return data_list

def compute_unused_data(data_list, tokenizer):

    truncated_articles = 0
    tokens_lost = 0
    total_tokens = 0

    for item in data_list:
        
        tokens = tokenizer(item)
        
        token_number = len(tokens['input_ids'])
        
        if token_number > 128:
            truncated_articles += 1
            
        tokens_lost = tokens_lost + (token_number - 128)
        total_tokens = total_tokens + token_number
            
    return truncated_articles, tokens_lost, total_tokens  






def main():

    tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
    
    data_list = get_sorted_plain_texts()
    
    truncated_articles, tokens_lost, total_tokens = compute_unused_data(data_list, tokenizer)
    
    print(truncated_articles)
    print(tokens_lost)
    print(total_tokens)
    
      
if __name__ == '__main__':
    main()