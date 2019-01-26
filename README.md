Fullstack Nanodegree Project: Logs Analysis
=================================================
Project Description: This project creates  a reporting tool that prints out reports (in plain text) based on the data in the database. This reporting tool is a Python program using the psycopg2 module to connect to the database. Using the module, I have connected to the news database and queried using PostgreSQL. There are three queries at the top of the source code, each of which answers one of the questions the reporting tool has to report on. The views used are at the bottom of this README file.

The news database has three tables: articles, authors and log.

Question1: What are the most popular three articles of all time? 
Method of tackling it: Created view1 to count the times each distinct path was successfully accessed in the log table and view2 to limit the results of view1 to only the top 3. Then I used query1 to match the 3 most popular article paths to their article names by performing an inner join on view2 and the articles table.


Question2: Who are the most popular article authors of all time?
Method of tackling it: I first created view3 to output each author's ID and views of each article they had written. Next, using query2 I joined the author's ID in view3 with that in the authors table to get the authors name. In query2 I also summed up the views of every article an author had written, and grouped the results by author. 


Question3: On which days did more than 1% of requests lead to errors?
Method of tackling it: For this I created view4 to count the  error for each day and view5 to count the total number of requests for each day. I next created view6 to join these two so that I could easily query the table. I next used query3 to get the percentage of errors per day, and used a WHERE statement to filter for days where more than 1% of requests lead to errors.


NOTE: I am aware that instead of creating views I could have used subqueries; however, despite spending a week over it I could not get subqueries to run on the Virtual Machine.



Views used:
1) Query for view1: "CREATE VIEW view1 AS SELECT DISTINCT path, count (status) as num FROM log WHERE path!='/' AND status='200 OK' GROUP BY path, author ORDER BY num desc; " 
2) Query for view2: "CREATE VIEW view2 AS SELECT * FROM view1 LIMIT 3; "
3) Query for view3: " CREATE VIEW view3 AS SELECT articles.author, view1.num FROM articles  INNER JOIN view1 ON view1.path LIKE CONCAT ('%', articles.slug, '%') ORDER BY view1.num desc" //creating view3
4) Query for view4: "CREATE VIEW view4 AS select count(status) as error_status, date(time) as thedate from log where status NOT LIKE '2%' GROUP BY thedate;
5) Query for view5: CREATE VIEW view5 AS select count(status) as all_status , date(time) as thedate from log GROUP BY thedate;
6: Query for view6: CREATE VIEW view6 AS select view4.thedate, view4.error_status, view5.all_status from view4 inner join view5 on view4.thedate=view5.thedate;
