#!/usr/bin/env python2

import psycopg2
import bleach

DBNAME = "news"


def get_popular_articles():
    """ Returns the most three popular articles from news db"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    # popular articles
    c.execute(
        "select substring(path from 10), views from article_count limit 3;")
    articles = c.fetchall()
    db.close()
    return articles


def get_popular_authors():
    """ Returns the most three popular authors from news db"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    # popular authors
    c.execute(
        "select author, sum(views) author_views from author_count" +
        " group by author order by author_views DESC limit 3;")
    authors = c.fetchall()
    db.close()
    return authors


def get_error_days():
    """ Returns the days with more than 1% errors"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(
        "select time::date, err_perc from (select time::date, " +
        "sum(CAST(num AS float)/ CAST(num_requests AS float))*100 as" +
        " err_perc from (select time_err.time::date, num, num_requests from " +
        "time_err, time_req where time_err.time::date = time_req.time::date)" +
        " as subq group by time::date order by err_perc DESC) as subq2" +
        " where err_perc >1.1;")
    days = c.fetchall()
    db.close()
    return days


if __name__ == '__main__':
    print "Popular Articles:"
    for i in get_popular_articles():
        article = i[0] + "--" + str(i[1]) + " Views."
        print article

    print "\nPopular Authors:"
    for au in get_popular_authors():
        author = au[0] + "--" + str(au[1]) + " Views."
        print author

    print "\nDays with more than 1% request errors:"
    if not get_error_days():
        print "No Days with more than 1% request errors"
    for day in get_error_days():
        day_err = str(day[0]) + "--" + str(day[1]) + " % errors."
        print day_err
