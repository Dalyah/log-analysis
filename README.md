# log-analysis
This project uses news database to analyze user experience and figure out the popular articles and authors.
It also shows the days with the most request errors.

# The views
For ease, these views were created.

## article_log View
 CREATE VIEW article_log AS select * from log where path like '%article/%';

## article_count View
CREATE VIEW article_count AS select path , count(*) as views from article_log group by path order by views DESC;

## author_count View
CREATE VIEW author_count AS  select article_count.path, article_count.views, authors.name as author from article_count,
articles, authors WHERE substring(article_count.path from 10) = articles.slug and authors.id = articles.author;

