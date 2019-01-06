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


if __name__ == '__main__':
    print get_popular_articles()
    print get_popular_authors()
