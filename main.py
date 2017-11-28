from bsddb3 import db
import search
import re, sys


def main():
    global curs_ye, curs_te, curs_re
     #open database and cursors
    database_ye = db.DB()
    database_te = db.DB()
    database_re = db.DB()

    file_ye = "./phase2_out/ye.idx"
    file_te = "./phase2_out/te.idx"
    file_re = "./phase2_out/re.idx"

    database_ye.set_flags(db.DB_DUP)
    database_ye.open(file_ye)
    curs_ye = database_ye.cursor()

    database_te.set_flags(db.DB_DUP)
    database_te.open(file_te)
    curs_te = database_te.cursor()

    database_re.set_flags(db.DB_DUP)
    database_re.open(file_re)
    curs_re = database_re.cursor()

    
    #main block, asking for the input
    while 1:
        try:
            user_input = input(">>")
            if user_input.strip() == "":
                break
        except:
            break

        determine_query(user_input)

    

    curs_ye.close()
    database_ye.close()

    curs_te.close()
    database_te.close()

    curs_re.close()
    database_re.close()

# determine the kind of the inputted query
def determine_query(user_input): 
    global curs_ye, curs_te, curs_re
    
    # "change output to full or key "outpu=full""
    if "output=" in user_input: 
        input_list = user_input.lower().split("=")

        if input_list[1] == "full": #Full output
            search.change_full_out(True)# set the flag
        elif input_list[1] == "key": #key output
            search.change_full_out(False) #set the flag
        else:
            print("Invalid input")
        return

    # seeking for the phrase (inluding quataion marks)
    if "\"" in user_input: 
        
        # extract the phrase inside the quotes"
        phrase_pattern = re.compile(r'\"(.+?)\"')
        phrase_find = re.findall(phrase_pattern, user_input)
        temp = []
        for phrase in phrase_find:
            #replace the white space in the prase by "-"
            #so that it would not be spliited by white space            
            temp.append((phrase, phrase.replace(" ", "-"))) 
        for phrase, new_phrase in temp:
            user_input = user_input.replace(phrase, new_phrase)
            
    #split the multiple conditions by the white space
    input_list = user_input.split(" ") 

    # multiple conditions
    result = set() # the set containing the output
    not_updated = True #indicate if the set has been updated

    # 2 means get both start and end of the range search , then start range search
    range_search_start_and_end_get = 0  
    
    try:
        #loop through each condition
        for i in range(len(input_list)): 
            one_condition = input_list[i]
            
            # split by : determine whether to do the equality search
            splitted_input_list = one_condition.split(":")  
            if len(splitted_input_list) > 1:  
                if "\"" in splitted_input_list[1]:# phrase search
                    match = splitted_input_list[0]
                    phrase = splitted_input_list[1]
                    search_result = search.phrase_search(curs_ye, curs_te, curs_re, match, phrase) # get the search result
                    
                    #if the set has not been updated, update it
                    if not_updated:
                        result.update(search_result) 
                        not_updated = False
                    else:
                        # intersect the ouputs, finally will get the output that satisfiies all the conditions
                        result = result.intersection(search_result) 
                        
                else: #euquality search
                    search_result = search.equality_search(curs_ye, curs_te, curs_re, splitted_input_list[0],
                                                           splitted_input_list[1])
                    if not_updated:
                        result.update(search_result)
                        not_updated = False
    
                    else:
                        result = result.intersection(search_result)
    
            # range search with two operators < and >            
            elif ">" in user_input and "<" in user_input and (
                            ">" in one_condition or "<" in one_condition):  
    
    
                if "<" in one_condition: # samller that
                    splitted_input_list = one_condition.split("<")
                    end = splitted_input_list[1] #end point of the range search
                    range_search_start_and_end_get += 1
    
    
                else: # greater than
                    splitted_input_list = one_condition.split(">")
                    start = splitted_input_list[1] #starting point of the range search
                    range_search_start_and_end_get += 1
    
            # range search with only one operator >        
            elif ">" in one_condition:  
    
                splitted_input_list = one_condition.split(">")
                start = splitted_input_list[1] #starting point
                search_result = search.range_search(curs_ye, curs_te, curs_re, "year", start, "5000")
    
                if not_updated:
                    result.update(search_result)
                    not_updated = False
                else:
                    result = result.intersection(search_result)
                    
            # range search with only one operator <
            elif "<" in one_condition:  
                splitted_input_list = one_condition.split("<")
                end = splitted_input_list[1] #end point
                search_result = search.range_search(curs_ye, curs_te, curs_re, "year", "0", end)
    
                if not_updated:
                    result.update(search_result)
    
                    not_updated = False
                else:
                    result = result.intersection(search_result)
    
    
            else:  # only one term, such as database
                # go through all the tags
                search_result1 = search.equality_search(curs_ye, curs_te, curs_re, "title", splitted_input_list[0])
                search_result2 = search.equality_search(curs_ye, curs_te, curs_re, "author", splitted_input_list[0])
                search_result3 = search.equality_search(curs_ye, curs_te, curs_re, "other", splitted_input_list[0])
                search_result4 = search.equality_search(curs_ye, curs_te, curs_re, "year", splitted_input_list[0])
                search_result = search_result1.union(search_result2)
                search_result = search_result.union(search_result3)
                search_result = search_result.union(search_result4)
    
                if not_updated:
                    result.update(search_result)
                    not_updated = False
                else:
                    result = result.intersection(search_result)
                    
            #Only  we get both start and end, then we start range search
            if range_search_start_and_end_get == 2: 
    
                search_result = search.range_search(curs_ye, curs_te, curs_re, "year", start, end)
                if not_updated:
                    result.update(search_result)
                    not_updated = False
    
                else:
                    result = result.intersection(search_result)
    
                range_search_start_and_end_get = 0 #reset to 0
                
        print_output(result) # print the output
        
    except:
        #error message
        print("Invalid Query!!!")
    


def print_output(result_set):
    print("\n")
    if len(result_set) > 0:
        for ele in result_set:
            print(ele.decode("utf-8"))
            print("\n")


main()
