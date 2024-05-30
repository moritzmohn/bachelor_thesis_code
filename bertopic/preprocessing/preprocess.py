from lxml import etree
import json

def get_sorted_data_list():
    with open("data/sorted_data/sorted_data_list_84-23_v6", "r") as fp:
        data_list = json.load(fp)
    return data_list

   
def extract_content(data_list):

    content_list = []
    for article_list in data_list:
        content = article_list[5] +" // "+ article_list[-1]
        content_list.append(content)
    return content_list

    
def remove_html_tags(data_list):
    plain_texts = []
    for article in data_list:
        parser = etree.HTMLParser()
        tree = etree.fromstring(article, parser)
        text = etree.tostring(tree, encoding='unicode', method='text')
        plain_texts.append(text)
        
    return plain_texts
    
def save_sorted_plain_text(plain_texts):
    with open("data/sorted_title_content_84-23_v6", "w") as fp:
        json.dump(plain_texts, fp)
    
    

def main():
    data_list = get_sorted_data_list()
    data_list = extract_content(data_list) 
    plain_texts= remove_html_tags(data_list)
        
    save_sorted_plain_text(plain_texts)
    
    

   
if __name__ == '__main__':
    main() 