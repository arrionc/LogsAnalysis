# Logs Analysis 

A program that retrieves information from a database using the following tools: 
    
- A linux-based virtual machine
- PostgreSQL
- The [news database](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
- Python

I've used vagrant as my virtual machine. To load the database to vagrant use the command:

`psql -d news -f newsdata.sql` 

## The Reporting Tool

The program creates a reporting tool using Python that prints out reports (in plain text) based on the data in the database. It uses the following modules: 

`import psycopg2`

`from datetime import datetime`

## Requirements

The reporting tool should answer the following questions:
- What are the most popular three articles of all time?
- What are the most popular article authours of all time?
- On which days did more than 1% of requests lead to errors?

**Each of these questions should be answered with a single database query.**

In order to fulfill  the requirements, I've created three views in the database:

``` 
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
```
