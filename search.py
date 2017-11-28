import re

full_out = False

# change the flag indicating whether to do the full output or the key output
def change_full_out(full): 
    global full_out
    full_out = full

#do the equaliy search 
def equality_search(curs_ye, curs_te, curs_re, match, key): 
    key = key.lower()

    curs1 = curs_te
    curs2 = curs_re
    
    # set the tag
    if match == "title":
        tag = "t-"

    elif match == "author":
        tag = "a-"

    elif match == "other":
        tag = "o-"
    elif match == "year":
        tag = ""
        curs1 = curs_ye

    result = set() #output set
    key = tag + str(key) # combine the tag with the term
    iter1 = curs1.set(key.encode("utf-8"))
    while iter1: #handling duplicates
        terms = iter1[0]
        recs = iter1[1]
        if full_out:

            iter2 = curs2.set(recs)
            while iter2:
                rec1 = iter2[0]
                data = iter2[1]
                result.add(data)
                iter2 = curs2.next_dup()
        else:
            result.add(recs)

        iter1 = curs1.next_dup()
    return result

# do the range search, only for the year
def range_search(curs_ye, curs_te, curs_re, match, start, end): 
    if match == "year":

        start = str(int(start) + 1) #make sure not euqal
        end = str(int(end) - 1) #make sure not equal

        search_result = set()
        result = curs_ye.set_range(start.encode("utf-8"))
        
        #traverse the output in that range in sequence
        while result: 
            key = result[1]
            if int(result[0].decode("utf-8")) > int(end):
                break

            if full_out:
                data = curs_re.set(key)[1]
                search_result.add(data)

            else:
                search_result.add(key)

            result = curs_ye.next()

        return search_result


def phrase_search(curs_ye, curs_te, curs_re, match, phrase): #search for phrase
    
    #set the tag
    if match == "title":
        tag = "t-"
        pattern = re.compile(r'\<title>(.*?)\</title>')
    elif match == "author":
        tag = "a-"
        pattern = re.compile(r'\<author>(.*?)\</author>')
        
    #other contains journal, publisher,bookiltle, so we need three patterns to match the strings
    elif match == "other": 
        tag = "o-"
        pattern_list = [re.compile(r'\<journal>(.*?)\</journal>'), re.compile(r'\<publisher>(.*?)\</publisher>'),
                        re.compile(r'\<booktitle>(.*?)\</booktitle>')]

    result = set()
    not_updated = True
    
    # eliminate the euotation marks in the phrase
    phrase = phrase.replace("\"", "")

    phrase_list = phrase.split("-") #split the phrase by "-"
    phrase = phrase.replace("-", "")# eliminate all the "-" in the phrase
    
    # traverse throught the single term in a phrase    
    for word in phrase_list: 
        word = tag + str(word) #combine the word with the tag

        iter1 = curs_te.set(word.encode("utf-8"))

        temp = set() #temporary set that store all the possible output

        while iter1:

            key = iter1[1]
            temp.add(key)
            iter1 = curs_te.next_dup()
            
        if not_updated:
            result.update(temp)
            not_updated = False
        else:
            result = result.intersection(temp)

            
    final_result = set() #store the final output to be returned
    for ele in result: #make a copy of the result set
        final_result.add(ele)

    for key in result:
        data = curs_re.set(key)[1]
        
        #check if the phrase satisfies the order of the original data in records
        if match == "other": 
            #each set in the list represents the possible key for booktitle,publisher and journal of "other"
            final_result = [set(), set(), set()] 
            
            for final in final_result: #copy the contents
                for ele in result:
                    final.add(ele)
            
            #traverse through all the other tags (booktitle,publisher and journal)
            for index in range(len(final_result)):  
                final = final_result[index] # the set for the paricular other tag
                
                # if the record does not contain the particular tag
                if len(re.findall(pattern_list[index], data.decode("utf-8"))) == 0: 
                    if key in final:
                        final.remove(key) #remove the key from that tag set
                        
                correct_order = False #indicate whether the phrase follows the correct order
                
                for title in re.findall(pattern_list[index], data.decode("utf-8")):
                    
                    #find the paricluar term that the phrase possibly match
                    title = re.sub('[^0-9a-zA-Z]+', '', title).lower() 
                    flag = phrase in title
                    if flag:
                        correct_order = True
                
                # if it does not follow the correct order, remove the key
                if not correct_order: 
                    if key in final:
                        final.remove(key)
            
            # Union the outputs of all possible other tags
            union_set = set()
            union_set.update(final_result[0])
            union_set = union_set.union(final_result[1])
            union_set = union_set.union(final_result[2])
            final_result = union_set
        else: #check the phrase other than "other"
            correct_order = False
            
            # check if the phrase follows the correct order
            for title in re.findall(pattern, data.decode("utf-8")): 

                title = re.sub('[^0-9a-zA-Z]+', '', title).lower() #extract the term from the records
                flag = phrase in title
                if flag:
                    correct_order = True
            #remove the key if it does not follow the correct order
            if not correct_order: 
                if key in final_result:
                    final_result.remove(key)
                    
    # for full output, return the data
    if full_out: 
        data_result = set()
        for key in final_result:
            data_result.add(curs_re.set(key)[1])
        return data_result

    return final_result
