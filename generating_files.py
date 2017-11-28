import sys,re

#three dictionaries storing three different file information 
terms_dict = dict()
year_dict = dict()
rec_dict = dict()

def main():
    
    
    read_file()
    write_file()
    
#read the information from the xml files
def read_file(): 
    global terms_dict,year_dict,rec_dict
   
    file_name = sys.argv[1] 
    
    with open(file_name,'r') as input_file:
        
        data_string = input_file.read()

    #get the string from the xml file
    data_list = data_string.strip().split("\n")
    del data_list[0] # delete the header
    
    for line in data_list: # process each line
        value_list =[]
        # find the key
        # using regular expression matching the strings
        key_pattern = re.compile(r'\"(.+?)\"')
        key_find = re.findall(key_pattern,line)
        
        if (len(key_find)) == 0:
            continue
        key = key_find[0]
          
        #store the whole line into records dictionary        
        rec_dict[key] = line  

    data_list = data_string.strip().split("\n")

    del data_list[0] #delete the header
    del data_list[-1] #delete the tail
    
    for line in data_list:
        p = False
        value_list =[]
        
        # find the key
        # using regular expression matching the strings
        key_pattern = re.compile(r'\"(.+?)\"')
        key_find = re.findall(key_pattern,line)
        
        if (len(key_find)) == 0: #if we do not find the key
            continue
        
        key = key_find[0]
       
        terms_dict[key] = []
            
   
        #find the title\
        title_list = []
        # using regular expression matching the strings
        title_pattern = re.compile(r'\<title>(.*?)\</title>')
        for title in re.findall(title_pattern,line):
            
            title_list.append(title.lower())
            
        terms_dict[key].append(title_list)

        #find the author
        # using regular expression matching the strings
        author_pattern = re.compile(r'\<author>(.*?)\</author>')
        author_list  = []
        for author in re.findall(author_pattern,line):
           
            author_list.append(author.lower())
        terms_dict[key].append(author_list)
            
        #find others
        other_list = []
        # using regular expression matching the strings
        journal_pattern = re.compile(r'\<journal>(.*?)\</journal>')
        booktitle_pattern = re.compile(r'\<booktitle>(.*?)\</booktitle>')
        publisher_pattern = re.compile(r'\<publisher>(.*?)\</publisher>')
        find_journal = re.findall(journal_pattern,line)
        find_booktitle = re.findall(booktitle_pattern,line)
        find_publisher = re.findall(publisher_pattern,line)
        if len(find_journal) != 0:
            for journal in find_journal:
                other_list.append(journal.lower())
      
        if len(find_booktitle) != 0:
            for booktitle in find_booktitle:
                other_list.append(booktitle.lower())        
                
        if len(find_publisher) != 0:
            for publisher in find_publisher:
                other_list.append(publisher.lower())  
           
        terms_dict[key].append(other_list) # append other to the terms dictionary
        
        #find year
        # using regular expression matching the strings
        year_pattern = re.compile(r'\<year>(.*?)\</year>')
        find_year = re.findall(year_pattern,line)
        for year in find_year:
            year_dict[key] = year #apped the year to the year dictionary
        
        
        
        
 

def write_file(): # write the output
    
    global terms_dict,year_dict,rec_dict
    
    #below are the three output file names
    term_file_name = "./phase1_out/terms.txt"
    year_file_name = "./phase1_out/years.txt"
    rec_file_name = "./phase1_out/recs.txt"
    
    # write the corresponding data to each file
    with open(rec_file_name,'w') as output_file:
        for key in rec_dict.keys():
            line = rec_dict[key]
            con_line = "%s:%s\n"%(key,line)
            output_file.write(con_line)
            
    with open(year_file_name,'w') as output_file:
        for key in year_dict.keys():
            year = year_dict[key]
            con_line = "%s:%s\n"%(year,key)
            output_file.write(con_line)

    with open(term_file_name,'w') as output_file:
        
    
        match_pattern = re.compile(r"[A-Za-z0-9_]*")
        #split the data
        
        for key in terms_dict.keys():
            data_list = terms_dict[key]

            
            title_list = data_list[0]
            author_list = data_list[1]
            other_list = data_list[2]
     
            for title in title_list: #write the title terms
                if title[-1] == ".": #eliminate period
                    title = title[:-1]
                title_find = re.findall(match_pattern,title)
               
                for word in title_find:
                    if len(word) > 2: #omit the term having less than 3 letters
                        con_line = "t-%s:%s\n"%(word,key)
                        output_file.write(con_line)
           
            
            for other in other_list: #write the other terms
                if other[-1] == ".": #eliminate period
                    other = other[:-1]
                other_find = re.findall(match_pattern,other)
               
               
                for word in other_find:
                    if len(word) > 2: #omit the term having less than 3 letters
                        con_line = "o-%s:%s\n"%(word,key)
                        output_file.write(con_line)
                        
                        
            for author in author_list: #write the author terms
                if author[-1] == ".": #eliminate period
                    author = author[:-1]
                author_find = re.findall(match_pattern,author)
    
                for word in author_find:
                    if len(word) > 2: #omit the term having less than 3 letters
                        con_line = "a-%s:%s\n"%(word,key)
                        output_file.write(con_line)
	    
     
                    

main()
