import time
import praw
import re
import urllib2
import signal, sys
import itemparser as ip
import OAuth2Util
import redis

# Are comments, submissions and messages really unique among each other?
# Can a comment and a private message have the same ID?
def is_parsed(id):
    return redis.sismember("parsed_comments", id)

def add_parsed(id):
    return redis.sadd("parsed_comments", id)

def bot_comments():
    sub_comments = subreddit.get_comments()
    for comment in sub_comments:
        # Checks if the post is not actually the bot itself (since the details say [[NAME]])
        if not is_parsed(comment.id) and not str(comment.author) == username:
            reply = build_reply(comment.body)
            if reply:
                try:
                    comment.reply(reply)
                except Exception, e:
                    print str(e)
            # Add the post to the set of parsed comments
            add_parsed(comment.id)

def bot_submissions():
    sub_subs = subreddit.get_new(limit=5)
    for submission in sub_subs:
        if not is_parsed(submission.id):
            reply = build_reply(submission.selftext)
            if reply:
                try:
                    submission.add_comment(reply)
                except Exception, e:
                    print str(e)
            add_parsed(submission.id)

def bot_messages():
    msg_messages = r.get_messages(limit=20)
    for message in msg_messages:
        if not is_parsed(message.id):
            reply = build_reply(message.body)
            if reply:
                try:
                    message.reply(reply)
                except Exception, e:
                    print str(e)
            add_parsed(comment.id)

def build_reply(text):
    # Regex Magic that finds the text encaptured with [[ ]]
    links = re.findall("\[\[([^\[\]]*)\]\]", text)
    reply = ""
    if len(links) == 0: return reply

    # Remove duplicates
    unique_links = []
    for i in links:
        if i not in unique_links:
            unique_links.append(i)
    # Because a comment can only have a max length, limit to only the first 30 requests
    if len(unique_links) > 30: unique_links = unique_links[0:30]
    for i in unique_links:
        print i
        i = i.split('/')[0]
        # Converts obscure characters like AE to a URL-valid text
        # j = urllib2.quote(i.encode('utf-8'))
        link = name_to_link(i)
        page = get_page(link)
        if page is not None:
            reply += "[%s](%s)\n\n" % (i, link)
            reply += ip.parse_item(page)
    if reply is "": 
        return None        
    return reply + "^\(Questions? ^Message ^/u/ha107642 ^- ^Call ^wiki ^pages ^((e.g. items or gems)^) ^with ^[[NAME]])"

# Function that checks if the requested wiki page exists.
def get_page(link):
    try:
        request = urllib2.Request(link, headers={"User-Agent": "PoEWiki"})
        response = urllib2.urlopen(request)
        return response.read()
    except urllib2.HTTPError, e:
        return None
    except AttributeError, e:
        print "ERROR: %s" % str(e)
        return None

def name_to_link(name):
    # Replace & because it breaks URLs
    link = name.replace("&", "%26")
    # Replace " " because that's how URLs are formatted on the wiki.. (probably more rules to that).
    link = link.replace(" ", "_")
    return "https://pathofexile.gamepedia.com/%s" % link

# Function that is called when ctrl-c is pressed. It backups the current parsed comments into a backup file and then quits.
def signal_handler(signal, frame):
    write_done()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# This string is sent by praw to reddit in accordance to the API rules
user_agent = ("REDDIT Bot v1.4 by /u/ha107642")
r = praw.Reddit(user_agent=user_agent)

redis = redis.StrictRedis(host="localhost")

oauth = OAuth2Util.OAuth2Util(r)
username = r.get_me().name

# Fill in the subreddit(s) here. Multisubs are done with + (e.g. MagicTCG+EDH)
subreddit = r.get_subreddit('pathofexile')

# Infinite loop that calls the function. The function outputs the post-ID's of all parsed comments.
# The ID's of parsed comments is compared with the already parsed comments so the list stays clean
# and memory is not increased. It sleeps for 20 seconds to wait for new posts.
while True:
    bot_comments()
    time.sleep(5)
    bot_submissions()
    time.sleep(5)
    bot_messages()
    oauth.refresh()
    time.sleep(10)
