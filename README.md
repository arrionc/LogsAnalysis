Logs Analysis: 

A program that retrieves information from a database using the following tools: 
-A linux-based virtual machine
-PostgreSQL
-The database (newsdata.sql) from https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip

I've used vagrant as my virtual machine:
-Load the database to vagrant using the following command: psql -d news -f newsdata.sql 


The program creates a reporting tool that prints out reports (in plain text) based on the data
in the database. This reporting tool is a python program (newsdb.py) using the psycopg2 module 
to connect to the database.
Also include the datetime module. 

The reporting tool should answer the following questions:
-What are the most popular three articles of all time?
-What are the most popular article authours of all time?
-On which days did more than 1% of requests lead to errors?

Each of these questions should be answered with a single database query.

Use the following create view commands in the database:
 
create view topArticles as
    select articles.title, count(*) as num from log, articles  
    where articles.slug = (select substring(log.path, 10))
    group by articles.title 
    order by num desc;


create view authorTop as
    select articles.author, sum(num) from topArticles, articles
    where topArticles.title = articles.title
    group by articles.author
    order by sum desc;

create view percenterror as 
    select time::date, (
    sum(case when status != '200 OK' then 1.0 else 0 end) /
    sum(case when status = '200 OK' then 1.0 else 0 end)) * 100 as error
    from log group by time::date;   