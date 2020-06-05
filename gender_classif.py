# import praw
import pandas as pd
import datetime
import numpy as np
import twint
import pickle
import nltk
# import nest_asyncio
# nest_asyncio.apply()
import datetime


def gen_time_window(start, end, step, length):
    
    start_datetime_object = datetime.datetime.strptime(start, '%Y-%m-%d')
    
    end_datetime_object = datetime.datetime.strptime(end, '%Y-%m-%d')

    iterator = start_datetime_object
    output = []
    while iterator < end_datetime_object:
        since = str(iterator)[:10]
#         until = str(iterator + datetime.timedelta(days=step))[:10]
        until = str(min(end_datetime_object, iterator + datetime.timedelta(days=length)))[:10]
        output.append((since,until))
        iterator += datetime.timedelta(days=step)
    
    return output



def get_tweets(search, since, until, limit=100, db=True):
    dbname = search.replace(" ","_") + ".db"
    c = twint.Config()
    c.Search = search
    c.Limit = limit # If not specified, scrapes all...
    c.Pandas = True
    c.Pandas_clean = True
    c.Since = since
    c.Until = until
    c.Database = dbname
    c.Hide_output = True
    
    twint.run.Search(c)
    if db==False:
        return twint.output.panda.Tweets_df
    else: print("Done: "+ since + " to " + until, twint.output.panda.Tweets_df.shape[0], "entries")


def scrape_to_db(keyword, start_date, end_date, step, length, limit):
    dates = gen_time_window(start_date, end_date, step, length)
    for i in dates:
        get_tweets(keyword, i[0], i[1], limit=limit)


def main():
    scrape_to_db(keyword = "digital health", 
                start_date = '2018-01-01', 
                end_date = '2020-06-01', 
                step = 14, 
                length = 1, 
                limit = 1000)

if __name__ == '__main__':
    # test1.py executed as script
    # do something
    main()