#!/usr/bin/env python3

import psycopg2
from datetime import datetime

db = psycopg2.connect(database='news')
c = db.cursor()
# Determining the top 3 most views articles
c.execute('''select * from topArticles limit 3''')
rows = c.fetchall()
print('The top three articles are:')
for row in rows:
    print('"' + row[0] + '"' + ' -- ' + str(row[1]) + ' views')

print('\n')
# Determining the most popular articles
c.execute('''select authors.name, authorTop.sum from authors, authorTop
                where authors.id = authorTop.author
                order by sum desc''')
rows1 = c.fetchall()
print('The most popular authors of all time:')
for row in rows1:
    print(row[0] + ' -- ' + str(row[1]) + ' views')

print('\n')
# Determining the percentage error
c.execute('''select * from percenterror where error > 1.0''')
rows2 = c.fetchall()
print('Days in which requests led to more than 1% errors: ')
for row in rows2:
    date = row[0].strftime('%B %d, %Y')
    errors = round(row[1], 1)
    print(date + ' -- ' + str(errors) + '% errors')

db.close()
