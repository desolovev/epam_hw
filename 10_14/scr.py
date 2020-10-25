import psycopg2
from tabulate import tabulate
import sys
from scr_connect import DB_NAME, DB_PORT, DB_USR, DB_PWD, DB_HOST

try:
    connection = psycopg2.connect(user=DB_USR,
                                  password=DB_PWD,
                                  host=DB_HOST,
                                  port=DB_PORT,
                                  database=DB_NAME)

    cursor = connection.cursor()


    def find_film(cursor, film_name, genre):
        # film_name = 'big | hero'
        # genre = 'comedy & drama'
        query = """
            select movie_title
                , actor_1_name
                , imdb_score
                , genres
            from (
                select ts_rank(to_tsvector(movie_title), to_tsquery('english', %s)) as rank
                , movie_title
                , actor_1_name
                , imdb_score
                , genres
                , ts_rank(to_tsvector(genres), to_tsquery('english', %s)) as genres_rank
                from imdb
                ) s
            where rank > 0.0001 and genres_rank > 0.0001
            order by imdb_score desc;
        """
        cursor.execute(query, (film_name, genre))
        final_rec = []
        for rec in cursor:
            rec = list(rec)
            final_rec.append(rec)

        rec = (tabulate(final_rec, headers=["movie_title",
                                            "actor_1_name",
                                            "imdb_score",
                                            "genres"],
                        tablefmt="github"))
        return rec

except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)

if __name__ == '__main__':
    # film_name = 'big | hero'
    # genre = 'comedy & drama'

    film_name = sys.argv[1]
    genre = sys.argv[2]

    print(find_film(cursor, film_name, genre))

    if (connection):
        cursor.close()
        connection.close()
