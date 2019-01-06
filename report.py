import psycopg2, bleach

DBNAME = "news"

def get_popular_articles():
    """ Returns the most three popular articles from news db"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    # #Create article_log view
    # c.execute("CREATE VIEW article_log AS select * from log where path like "+
    # "'%article/%';");
    # #Create article_count view
    # c.execute("CREATE VIEW article_count AS select path , count(*) as views"+
    # "from article_log group by path order by views DESC;");
    # c.commit()
    #popular articles
    c.execute("select substring(path from 10), views from article_count limit 3;")
    articles = c.fetchall()
    db.close()
    return articles

def get_popular_authors():
    """ Returns the most three popular authors from news db"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    # #Create author_count view
    # c.execute("CREATE VIEW author_count AS  select article_count.path,"+
    # "article_count.views, authors.name as author from article_count, articles,"+
    # "authors WHERE substring(article_count.path from 10) = articles.slug and "+
    # "authors.id = articles.author;");
    # c.commit()
    #popular authors
    c.execute("select sum(views) author_views, author from author_count group "+
    "by author order by author_views DESC limit 3;")
    authors = c.fetchall()
    db.close()
    return authors

def get_error_days():
    """ Returns the day with more than 1% errors"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("select time::date from "+
    "(select time::date, sum(num)/(1189674)*100 as err_per from "+
    "(select time::date , count(*) as num from"+
    "(select * from log where status like '4%' or status like '5%') as subq"+
    " group by time::date order by num DESC) as sub group by time::date "+
    "order by err_per DESC) as subq3 where err_per > 1;")
    days = c.fetchall()
    db.close()
    return days

if __name__ == '__main__':
    print get_popular_articles()
    print get_popular_authors()
    print get_error_days()
