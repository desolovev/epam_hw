# homework 14.10

file **db_10_14.backup** contains db dump (postgres:postgres)

Write a program in which takes some string as an input and performs search by title over movie database.
Search should work for partial match, be case insensitive and should cover different words forms, like "big heroes"
input, "Bih Hero 6" movie should be found. For each found movie, display its title, main actor, genres and imdb_score.
Sort results by imdb_score.

how to run:  
``python3 scr.py film_name genres``  

example:  
``python3 scr.py do1 'big | hero' 'comedy & drama'``  

