import sys
import tweepy
import discord
import requests
import datetime
import urllib.request, urllib.error

# set tokens
Bearer_Token = '<bearer_token>'
webhook      = '<discord_webhook>'

# set api
auth         = tweepy.OAuth2BearerHandler(Bearer_Token)
api          = tweepy.API(auth)

dt_now       = datetime.datetime.now().date()

# set keywords
targets      = ['<keywords>']

# search on twitter
ret_url_list = []
tweets = []
try:
    for target in targets:
        res_search = api.search_tweets(q=target, result_type="recent", count=20)
        for result in res_search:
            if 'media' in result.entities:
                for media in result.entities['media']:
                    url = media['url']

                if url not in ret_url_list and str(result.created_at)[:10] == str(dt_now):
                    ret_url_list.append(url)
                    tweets.append(['\n' + '\n' + result.user.name + ' :\n' + result.text.replace(url, '') + '\n' + url])
    
    # post to discord channel
    if tweets != []:
        for tweet in tweets:
            content = {
                'content' : tweet[0]
            }
            requests.post(webhook, content)

except Exception as error:
    print(error)

except KeyboardInterrupt:
    # end with keyboard action: Ctrl-C
    sys.exit()
