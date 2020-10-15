import psycopg2
from tabulate import tabulate
import sys

try:
    connection = psycopg2.connect(user="user_pg",
                                  password="user_pg_pass",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="db1")

    cursor = connection.cursor()

    def do1(cursor, date_start, date_end):
        query = """
            select product_name,
            count(issue) issues,
            count(timely_response) filter (where timely_response is true) as timely_response,
            count(consumer_disputed) filter (where consumer_disputed is true) as consumer_disputed
            from epam.epam_10_07
            where date_received between %s and %s
            group by product_name
            order by issues desc
        ;"""
        cursor.execute(query, (date_start, date_end))
        final_rec = []
        for rec in cursor:
            rec = list(rec)
            final_rec.append(rec)

        rec = (tabulate(final_rec, headers=["product_name",
                                           "issues",
                                           "timely_response",
                                           "consumer_disputed"],
                                            tablefmt="github"))
        return rec

    def do2(cursor, comp):
        query = """
            with st as (
                select State_Name,
                    count(Issue) AS ct
            from epam.epam_10_07
            where Company = %s
            group by State_Name
            order by ct desc
            limit 1
            )
            
            select * from epam.epam_10_07
            where State_Name = (select st.State_Name from st)
            and Company = %s
            limit 10
        ;"""
        # and Company = %s
        cursor.execute(query, (comp, comp))
        final_rec = []
        for rec in cursor:
            rec = list(rec)
            final_rec.append(rec)

        rec = (tabulate(final_rec, headers=["Date_Received",
                                    "Product_Name",
                                    "Sub_Product",
                                    "Issue",
                                    "Sub_Issue",
                                    "Consumer_Complaint_Narr",
                                    "Company_Public_Response",
                                    "Company",
                                    "State_Name",
                                    "Zip_Code",
                                    "Tags",
                                    "Consumer_Consent_Provid",
                                    "Submitted_via",
                                    "Date_Sent_to_Company",
                                    "Company_Response_to_Co",
                                    "Timely_Response",
                                    "Consumer_Disputed",
                                    "Complaint_ID"],
                                    tablefmt="github"))

        return rec

except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)


if __name__ == '__main__':
    # par_1 = 'do1'
    # par_2 = '2012-07-29'
    # par_3 = '2014-07-29'
    # or
    # par_1 = 'do2'
    # par_2 = 'Wells Fargo & Company'
    par_1 = sys.argv[1]
    par_2 = sys.argv[2]
    par_3 = sys.argv[3]
    if par_1 == 'do1':
        print(do1(cursor, par_2, par_3))
    elif par_1 == 'do2':
        print(do2(cursor, par_2))

    if (connection):
        cursor.close()
        connection.close()
