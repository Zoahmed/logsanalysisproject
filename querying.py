#!/usr/bin/env python3
import psycopg2

query1 = """SELECT articles.title,view2.num
FROM articles
INNER JOIN view2
ON view2.path
LIKE CONCAT ('%',articles.slug,'%')
ORDER BY view2.num desc;"""

query2 = """SELECT authors.name,SUM(view3.num) as num
FROM authors
INNER JOIN view3 ON view3.author=authors.id
GROUP BY authors.name
ORDER BY num desc;"""

query3 = """SELECT thedate,error_status/all_status::float*100 AS error_percentage
FROM view6
WHERE error_status/all_status::float>0.01;"""

DBNAME = "news"


db = psycopg2.connect(database=DBNAME)
c = db.cursor()

# First Answer
c.execute(query1)
answer1 = c.fetchall()
print("\n Most popular three articles of all time:")
for answer in answer1:
    print(" ", answer[0], "-", answer[1], "views")

# Second Answer
c.execute(query2)
answer2 = c.fetchall()
print("\n Most popular article authors of all time:")
for answer in answer2:
    print(" ", answer[0], "-", answer[1], "views")

# Third Answer
c.execute(query3)
answer3 = c.fetchall()
print("\n Days on which more than 1% of requests lead to errors:")
for answer in answer3:
    print(" ", answer[0], "-", answer[1], "% errors")

db.close()
