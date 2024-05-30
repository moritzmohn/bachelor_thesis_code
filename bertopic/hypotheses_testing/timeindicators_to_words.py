


def write_new_txt():

    file = open("hypotheses_testing/txt_files/planes_docs_time_english_100_v2.txt", "w")
    old_file = open("hypotheses_testing/txt_files/planes_docs_time_english_100.txt", "r")
    count = 0
    
    for line in old_file:
    
        if line == "1994\n":
            file.write("ninetyfour\n")
            count+=1
            
        elif line == "1999\n":
            file.write("ninetynine\n")
            count+=1
            
        elif line == "2004\n":
            file.write("four\n")
            count+=1
            
        elif line == "2009\n":
            file.write("nine\n")
            count+=1
            
        elif line == "2014\n":
            file.write("fourteen\n")
            count+=1
            
        elif line == "2019\n":
            file.write("nineteen\n")
            count+=1
            
        else:
            file.write(line)
            
    print(count)
    

def write_new_txt_decades():

    file = open("hypotheses_testing/txt_files/planes_docs_time_english_100_v3.txt", "w")
    old_file = open("hypotheses_testing/txt_files/planes_docs_time_english_100.txt", "r")
    count = 0
    
    for line in old_file:
    
        if line == "1994\n" or line == "1999\n":
            file.write("firstdecade\n")
            count+=1
            
        elif line == "2004\n" or line == "2009\n":
            file.write("seconddecade\n")
            count+=1
            
        elif line == "2014\n" or line == "2019\n":
            file.write("thirddecade\n")
            count+=1
            
        else:
            file.write(line)
            
    print(count)
    
    
def write_new_txt_decades_v2():

    file = open("hypotheses_testing/txt_files/bicycles_docs_time_english_v2.txt", "w")
    old_file = open("hypotheses_testing/txt_files/bicycles_docs_time_english.txt", "r")
    count = 0
    
    for line in old_file:
    
        if line == "1994\n" or line == "1999\n" or line == "2004\n" or line == "2009\n":
            file.write("firstandseconddecade\n")
            count+=1
            
        elif line == "2014\n" or line == "2019\n":
            file.write("thirddecade\n")
            count+=1
            
        else:
            file.write(line)
            
    print(count)
           
           


def main():
    
    write_new_txt_decades_v2()
    
    
    
if __name__ == '__main__':
    main()       