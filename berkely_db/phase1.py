import re
import sys
## The regular libery is learned from Google, and conmunicate with other groups about use of re.findall and re.splite 
def create_terms(file):

    file2 = open("terms.txt", 'w')
    
    
    for line in file:
        
        key = re.findall('key="(.*?)"', line)

        if len(key) != 0:

            for title in re.findall("<title>(.*?)</title>", line):
                for term in re.split("[^0-9a-zA-Z_]", title):
                    if len(term) >=3:
                        
                        file2.write('t-')
                        file2.write(term.lower())
                        file2.write(':')
                        file2.write(key[0])
                        file2.write('\n')
                        

                        


            for journal in re.findall("<journal>(.*?)</journal>", line):
                for term in re.split("[^0-9a-zA-Z_]", journal):
                    if len(term) >= 3:
                   
                        file2.write('o-')
                        file2.write(term.lower())
                        file2.write(':')
                        file2.write(key[0])
                        file2.write('\n')
                       

            for publisher in re.findall("<publisher>(.*?)</publisher>", line):
                for term in re.split("[^0-9a-zA-Z_]", publisher):
                    if len(term) >= 3:
                       
                        file2.write('o-')
                        file2.write(term.lower())
                        file2.write(':')
                        file2.write(key[0])
                        file2.write('\n')

                       

            for bookTitle in re.findall("<booktitle>(.*?)</booktitle>", line):
                for term in re.split("[^0-9a-zA-Z_]", bookTitle):
                    if len(term) >= 3:
                     
                        file2.write('o-')
                        file2.write(term.lower())
                        file2.write(':')
                        file2.write(key[0])
                        file2.write('\n')
                        

            for author in re.findall("<author>(.*?)</author>", line):
                for term in re.split("[^0-9a-zA-Z_]", author):
                    if len(term) >= 3:
                      
                        file2.write('a-')
                        file2.write(term.lower())
                        file2.write(':')
                        file2.write(key[0])
                        file2.write('\n')
        

    file2.close()
    return


def create_years(file):
    file.seek(0)
    file2 = open("years.txt", 'w')
   

    for line in file:
        key = re.findall('key="(.*?)"', line) 

        if len(key) != 0:
            for years in re.findall("<year>(.*?)</year>", line): 
                for year in re.split("[^0-9a-zA-Z_]", years):
                    file2.write(year)
                    file2.write(':')
                    file2.write(key[0])
                    file2.write('\n')
    file2.close()
    return


def create_recs(file):
    file.seek(0)
    file2 = open("recs.txt", 'w')
  
    for line in file:
        key = re.findall('key="(.*?)"', line)

        if len(key) != 0:
            file2.write(key[0])
            file2.write(':')
            file2.write(line)
        

    file2.close()
    return
    
   
def main():
    path = sys.argv[1]
    file = open(path, 'r')

    create_terms(file)
    create_years(file)
    create_recs(file)

    file.close()
    return


if __name__ == '__main__':
    main()



