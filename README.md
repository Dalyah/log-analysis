# log-analysis
This project uses news database to analyze user experience and figure out the popular articles and authors.
It also shows the days with the most request errors.

# Requirements
The following are required to run the project.
1. Python 3
2. PostgreSQL
3. NEWS database from https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip. After downloading the database, unzip the folder and put newsdata.sql in your PostgreSQL working directory and run the following command in the shell to load the data: psql -d news -f newsdata.sql


# Running the project
To run the project, create the following SQL views using the queries below:

## article_log View
 CREATE VIEW article_log AS select * from log where path like '%article/%';

## article_count View
CREATE VIEW article_count AS select path , count(*) as views from article_log group by path order by views DESC;

## author_count View
CREATE VIEW author_count AS  select article_count.path, article_count.views, authors.name as author from article_count,
articles, authors WHERE substring(article_count.path from 10) = articles.slug and authors.id = articles.author;

After you create the views, you can run the project by running: python report.py
