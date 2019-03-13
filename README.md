# Logs Analysis - Udacity
## Full Stack Web Development ND

### About

This project creates  a reporting tool that prints out reports (in plain text) based on the data in the database. This reporting tool is a Python program using the psycopg2 module to connect to the database. Using the module, I have connected to the news database and queried using PostgreSQL. There are three queries at the top of the source code, each of which answers one of the questions the reporting tool has to report on. The views used are at the bottom of this README file.

This project makes use of a same Linux-based virtual machine (VM) to run an SQL database server and a web app that uses it. It uses tools called *Vagrant* and *VirtualBox* to install and manage the VM.

### Getting Started :rocket:

### Prerequisites

**Prerequisite** | **How to Install**
------------ | -------------
Python 3 | The project is based on the latest version of the Python language, which can be downloaded from [here] (https://www.python.org/downloads/)
Virtual Box | VirtualBox is the software that actually runs the virtual machine. It can be downloaded from [here] (https://www.virtualbox.org/wiki/Download_Old_Builds_5_1). Install the platform package for your operating system. You do not need the extension pack or the SDK. You do not need to launch VirtualBox after installing it; Vagrant will do that.
Vagrant | Vagrant is the software that configures the VM and lets you share files between your host computer and the VM's filesystem. Get it from [vagrantup.com] (https://www.vagrantup.com/downloads.html). Install the version for your operating system.
psycopg2  | Psycopg is a PostgreSQL adapter for the Python programming language. Instructions on installing it can be found [here] (http://initd.org/psycopg/docs/install.html)


### Getting and Setting up the News Database :hammer_and_wrench:

To get the database, you can can use Github to fork and clone the repository [here] (https://github.com/udacity/fullstack-nanodegree-vm). You will end up with a new directory containing the VM files. Change to this directory in your terminal with `<cd>`. Inside, you will find another directory called vagrant. Change directory to the vagrant directory:

Next, [download the data here] (https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip). You will need to unzip this file after downloading it. The file inside is called **newsdata.sql**. Put this file into the vagrant directory, which is shared with your virtual machine.

Next clone this current repository in the vagrant directory.

You'll then need to load the data into your local database.
To load the data, `<cd>` into the vagrant directory and use the command `<psql -d news -f newsdata.sql>`.
Here's what this command does:
* psql — the PostgreSQL command line program
* -d news — connect to the database named news which has been set up for you
* -f newsdata.sql — run the SQL statements in the file newsdata.sql

Running this command will connect to your installed database server and execute the SQL commands in the downloaded file, creating tables and populating them with data.


### Exploring the data :mag:
Once you have the data loaded into the database, connect to your database using `<psql -d news>` and explore the tables using the `<\dt>` and `<\d>` table commands and select statements.

* `<\dt>`— display tables — lists the tables that are available in the database.
* `<\d>`table — (replace table with the name of a table) — shows the database schema for that particular table.
* Get a sense for what sort of information is in each column of these tables.

The database includes three tables:

* The authors table includes information about the authors of articles.
* The articles table includes the articles themselves.
* The log table includes one entry for each time a user has accessed the site.


### Starting up the Virtual Machine	:arrow_up:

From your terminal, inside the __vagrant__ subdirectory, run the command `<vagrant up>`. This will cause Vagrant to download the Linux operating system and install it. This may take quite a while (many minutes) depending on how fast your Internet connection is.

When `<vagrant up>` is finished running, you will get your shell prompt back. At this point, you can run `<vagrant ssh>` to log in to your newly installed Linux VM!

The PostgreSQL database server will automatically be started inside the VM. You can use the psql command-line tool to access it and run SQL statements.


### Connecting from the code :link:
The database that you're working with in this project is running PostgreSQL. So in your code, you'll want to use the __psycopg2__ Python module to connect to it, for instance:

```python
db = psycopg2.connect("dbname=news")
```
###Running the script :running_man:

Once logged into the VM, __cd__ into the __logsanalysisproject__ directory and use the following code to run the script
`<python querying.py>`

### Examples of how to tackle questions :question:

##### Question1: What are the most popular three articles of all time?
Method of tackling it: Created view1 to count the times each distinct path was successfully accessed in the log table and view2 to limit the results of view1 to only the top 3. Then I used query1 to match the 3 most popular article paths to their article names by performing an inner join on view2 and the articles table.


##### Question2: Who are the most popular article authors of all time?
Method of tackling it: I first created view3 to output each author's ID and views of each article they had written. Next, using query2 I joined the author's ID in view3 with that in the authors table to get the authors name. In query2 I also summed up the views of every article an author had written, and grouped the results by author.


##### Question3: On which days did more than 1% of requests lead to errors?
Method of tackling it: For this I created view4 to count the  error for each day and view5 to count the total number of requests for each day. I next created view6 to join these two so that I could easily query the table. I next used query3 to get the percentage of errors per day, and used a WHERE statement to filter for days where more than 1% of requests lead to errors.


#### Views Used :eyes:


1) Query for view1: "CREATE VIEW view1 AS SELECT DISTINCT path, count (status) as num FROM log WHERE path!='/' AND status='200 OK' GROUP BY path, author ORDER BY num desc; "
2) Query for view2: "CREATE VIEW view2 AS SELECT * FROM view1 LIMIT 3; "
3) Query for view3: " CREATE VIEW view3 AS SELECT articles.author, view1.num FROM articles  INNER JOIN view1 ON view1.path LIKE CONCAT ('%', articles.slug, '%') ORDER BY view1.num desc" //creating view3
4) Query for view4: "CREATE VIEW view4 AS select count(status) as error_status, date(time) as thedate from log where status NOT LIKE '2%' GROUP BY thedate;
5) Query for view5: CREATE VIEW view5 AS select count(status) as all_status , date(time) as thedate from log GROUP BY thedate;
6: Query for view6: CREATE VIEW view6 AS select view4.thedate, view4.error_status, view5.all_status from view4 inner join view5 on view4.thedate=view5.thedate;
