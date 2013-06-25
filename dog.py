## Imports
import yaml
import twitter
import re
import urllib
import datetime
import hashlib
from mandrill import Mandrill
from mandrill import Error
from SimpleLogger import SimpleLogger
from SimpleTimer import SimpleTimer

## Globals

## Main
def main():
    global logger, timer

    logger = SimpleLogger("dog.log")
    logger.initialize()
    logger.log("\n\n\nRunning dog on " + str(datetime.datetime.now()))

    timer = SimpleTimer()

    sources = loadSources()
    emailsWithLinks = getEmailsWithLinks(sources)
    filteredEmailsWithLinks = filterEmailsWithLinks(emailsWithLinks)
    sendEmails(filteredEmailsWithLinks)
    logger.log("Done!")
    logger.finalize()
    return

## Helpers
def filterEmailsWithLinks(emailsWithLinks):
    logger.log("Filtering emails")
    logger.log(timer.start())
    acceptableDomains = getConfig("acceptableDomains")
    results = []
    for emailWithLink in emailsWithLinks:
        for acceptableDomain in acceptableDomains:
            if acceptableDomain in emailWithLink[0]:
                results.append(emailWithLink)
    logger.log(timer.stop())
    return results

def loadSources():
    logger.log("Loading Sources")
    logger.log(timer.start())
    file = open("sources.yaml")
    data = yaml.safe_load(file)
    sourcesList = data["sources"]
    sourcesHandles = []
    for source in sourcesList:
        sourcesHandles.append(source["handle"])
    logger.log(timer.stop())
    return sourcesHandles

def getEmailsWithLinks(sources):
    logger.log("Getting emailsWithLinks")
    logger.log(timer.start())
    tweets = getTweets(sources)
    links = getLinks(tweets)
    emailsWithLinks = []
    for link in links:
        emails = getEmails(link)
        for email in emails:
            emailsWithLinks.append((email, link))

    logger.log(timer.stop())
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
    twitterConfig = getConfig("twitterAuth")
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

def getConfig(identifier):
    logger.log("Loading twitter config")
    file = open("config.yaml")
    data = yaml.safe_load(file)
    file.close()
    return data[identifier]

def send(email, link):
    try:
        M = Mandrill('-DUetSCLhDtp3EU4C3Ymsg')
        template_content = []
    	message = {
    		'from_email': 'dog@deltaFunction.co',
    		'from_name': 'Dog',
    		'headers': {'Reply-To': 'inbox@deltaFunction.co'},
    		'subject': 'Your e-mail has been found in a compromised account list',
    		'tags': ['dog'],
            'global_merge_vars': [
                {"name": "LISTURL", "content": link },
                {"name": "EMAIL", "content": email },
                ],
            'merge_tags':[],
    		'to': [{'email': email}],
            'inline_css': True }

        result = M.messages.send_template(
            template_name = 'a-type',
            template_content = template_content,
            message = message,
            async = True,
            ip_pool = 'Main Pool')

    except Error, e:
    	# Mandrill errors are thrown as exceptions
    	logger.log('A mandrill error occurred: %s - %s' % (e.__class__, e))

def sendEmails(emailsWithLinks):
    logger.log("Sending emails!")
    logger.log(timer.start())
    for emailWithLink in emailsWithLinks:
        send(emailWithLink[0], str(emailWithLink[1]))
        logger.log("Emailed: " + str(emailWithLink))
    logger.log(timer.stop())
    return

main()
