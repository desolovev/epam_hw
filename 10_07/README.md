# homework 07.10

file **db_10_07.backup** contains db dump (postgres:postgres)

**task1:**

Write a program which takes date range as an input and displays for that range list of all product names,  
amount of issues (complaints) for each product name, how much issues were done with timely response and how much were disputed by customer.  
Display results sorted by amount of issues in descending order.    

how to run:  
``python3 scr.py do1 data_start data_end``  

example:  
``python3 scr.py do1 '2012-07-29' '2014-07-29'``  

**task2:**  

Write a program which takes company name as an input, finds state name with biggest amount of issues for that company  
(filter out empty state values) and displays list of all issues (with all related attributes) for that company and state name.  

how to run:  
``python3 scr.py do2 company_name``  

example:  
``python3 scr.py do2 'Wells Fargo & Company'``   
