## Cooperated with: Monica Bui, Minghan Li
## Image Overviews
![screenshot from 2018-01-10 16-50-16](https://user-images.githubusercontent.com/27936587/34802097-ff3fb378-f628-11e7-9cc7-2d24d95c21a4.png)
![screenshot from 2018-01-10 16-51-00](https://user-images.githubusercontent.com/27936587/34802102-00bddd10-f629-11e7-878d-0c612d0f847c.png)

				       
				       General Overview and User Guide
The database contains records from papers that have several features but not limited to such as a key, author(s), paper title, etc. The user is then able to query specific results they want to see and can filter output with a specific category in mind such as papers from a specific year and author. 

To run phase 1 - type in command line “python3 generating_files.py name_of_input_xml_file”
To run phase 2 - type in command line “bash run.sh”
To run phase 3 - type in command line “python3 main.py” where then the user can input which queries they want from there. 

                                    Assumption and Possible Limitations:
To run our program, users must create two folders -- “phase1_out” and ”phase2_out”  in advance to store particular files.
Users cannot input queries that contain other than alphanumeric letters, colons, quotation marks, greater-than signs and less-than signs. Colons can only be used to separate the term and the searching word. Quotation marks can only be used to surround the phrase. Range search is limited to the term “year”. White spaces can only be used to separate multiple conditions.
We have used Perl script from eclass to remove backslash characters.

                                          Detailed Description
Equality search: First find all the keys that match the input and retrieve their values in the ye.idx or te.idx file, and then use the values as the keys to retrieve all the records in re.idx file.  
Range search: Range search can be called either with one operator or two operators. (1) If there is only “>” in the query, we only get the starting point from the query and set the ending-point to be an extremely large value so that the cursor will reach the end of the database before reach this value. (2) If  only “<” is inside the query, we only get the ending-point from the query. Due to the property of set_range function in Berkeley DB, we can only get the least element that is greater than or equal to the desired point. It will raise some errors if we want to go from the end to the front. So we set an extremely small starting point so that the cursor will go from the beginning of the database and stop until it reach the ending-point. (3) If both “>” and “<” is inside the query, we can get both starting and ending points from the query. Then set the cursor to the starting point and then go through the database until it reached the ending point.
Wild cards: First we extract every word in the phrase and then find the records that contains all these words. Next we extract the corresponding data and eliminate all the non-alphanumeric letters of this data. Finally we check if the phrase follows the order of the data (we check if the phrase is the substring of the data). If so, keep the record. Else, delete the violating record. 
Multiple conditions: Since each condition will return some results, we go through the condition one at a time and hold these results in a set for each condition. Finally intersect all the sets to get the outputs that satisfy every condition.

                                           Efficiency analysis:
Equality search/Range search/Wild cards: When output=key, since we are using the B+-tree so the overall time complexity would be O(logn) to just retrieve the keys; when output=full, since we are using the Hash index to retrieve the data, the time complexity will be O(logn + 1) which is O(logn).
Multiple conditions: If there are k conditions, the overall time complexity will be O(klogn) which is just O(logn).

                                             Testing Strategy
Divide and conquer: Test the three phases independently.
Phase 1:
We test phase 1 using the 10 records, 1000 records and 20k records files respectively to see if the program generates the correct .txt files as well as compiles in reasonable time.
Phase 2:	
We test the command lines in run.sh file separately, including splitting, sorting as well as building indexes, and at the same time record the individual run time to find the bottlenecks.
We also use db_dump to build and test the correctness of our indexes.
Phase 3:
First,  we break down the testing process into several test blocks, including equality search test, range search test, general search test(e.g. database)  and phrase search test ( e.g. “main memory” ) .
Second is multiple condition test,  where we arbitrarily combine the test blocks above to test the program.
The last one  is format test to see if  inputs like “output=full” can change the output format properly. 
	
                                             Ensure Robustness: 
Use random inputs to see if the  “check valid inputs” statement fails.
Use redirected file that contains random inputs to see if it can be handled correctly.


                                               Group Break Down
Phase 1 was worked on by all members through pair programming. Time spent 5 hours.
Phase 2 was worked on by Cijie. Both Monica and Minghan tested and fixed bugs during this process. Time spent 3 hours.
Phase 3. Monica did the main structure of this phase and queries 1-5, time spent 6 hours. Minghan did queries 6-7, time spent 4 hours. Cijie did queries 9-10, time spent 4 hours. All members pair programmed on query 8 (phrase search) time spent 5 hours. 
Minghan was the main tester of the project but we all did testing and helped fix bugs when needed. Time spent 5 hours. 
We used GitHub as a collaboration tool to keep track of our commits to the project plus our changes and fixes to bugs. 



