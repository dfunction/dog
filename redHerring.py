## Imports
import yaml
import twitter
import re
import urllib
from SimpleLogger import SimpleLogger

## Globals

## Main
def main():
    global logger

    logger = SimpleLogger("redHerring.log")
    logger.initialize()
    logger.log("\n\n\nRunning redHerring")

    sources = loadSources()
    emailsWithLinks = getEmailsWithLinks(sources)

    logger.log("Done!")
    logger.finalize()
    return

## Helpers
def loadSources():
    logger.log("Loading Sources")
    file = open("sources.yaml")
    data = yaml.safe_load(file)
    sourcesList = data["sources"]
    sourcesHandles = []
    for source in sourcesList:
        sourcesHandles.append(source["handle"])
    return sourcesHandles

def getEmailsWithLinks(sources):
    tweets = getTweets(sources)
    links = getLinks(tweets)
    emailsWithLinks = []
    for link in links:
        emails = getEmails(link)
        emailsWithLinks.append((link, emails))

    return emailsWithLinks

def getEmails(link):
    urlPointer = urllib.urlopen(link)
    emails = set()
    mailsrch = re.compile(r'[\w\-][\w\-\.]+@[\w\-][\w\-\.]+[a-zA-Z]{1,4}')
    if urlPointer.getcode() == 200:
        raw = urlPointer.read()
        emails.update(mailsrch.findall(raw))
    logger.log("Fetched " + str(len(emails)) + " emails")
    return emails

def getLinks(tweets):
    links = []
    for tweet in tweets:
        if "emails" in tweet.lower():
            links.append(re.search("(?P<url>https?://[^\s]+)", tweet).group("url"))
    logger.log("Fetched " + str(len(links)) + " links")
    return links

def getTweets(sources):
    logger.log("Getting tweets")
    twitterConfig = getTwitterConfig()
    twitterApi = twitter.Api(consumer_key=twitterConfig["consumerKey"],
                          consumer_secret=twitterConfig["consumerSecret"],
                          access_token_key=twitterConfig["accessTokenKey"],
                          access_token_secret=twitterConfig["accessTokenSecret"])
    tweets = []
    for source in sources:
        results = twitterApi.GetUserTimeline(screen_name = source)
        for tweet in results:
            tweets.append(tweet.text)
    logger.log("Fetched " + str(len(tweets)) + " tweets")
    return tweets

def getTwitterConfig():
    logger.log("Loading twitter config")
    file = open("config.yaml")
    data = yaml.safe_load(file)
    file.close()
    return data["twitterAuth"]


main()
