from googletrans import Translator
import time


def write_english_txt(german_txt):

    translator = Translator()
    german_file = open(german_txt, "r")
    english_file = open("hypotheses_testing/txt_files/bicycles_docs_time_english.txt", "w")
    
    for line in german_file:
        if line != "\n":
        
            while True:
                try:
                    print(line)
                    translation_object = translator.translate(line, src = "de")
                    translated_text = translation_object.__dict__()["text"]
                    print(translated_text)
                    english_file.write(translated_text + "\n")
                    break
                except:
                    time.sleep(60)
            
        
    german_file.close()
    english_file.close()
    
        
def main():
    
    write_english_txt("hypotheses_testing/txt_files/bicycles_docs_time_de.txt")
    
    
    
if __name__ == '__main__':
    main()