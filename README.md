Not too fancy code for the Reddit bot

Cloned from XSlicer's MTG version of this bot, found here: https://github.com/XSlicer/RedditMTGBot

Things needed to run this:
- Python 2.7+ (but < 3.0). https://www.python.org/downloads/
- praw (pip install praw). https://praw.readthedocs.org/en/latest/
- Beautiful Soup 4 (pip install beautifulsoup4). https://www.crummy.com/software/BeautifulSoup/
- OAauth2Util (pip install praw-oauth2util). https://github.com/SmBe19/praw-OAuth2Util
- titlecase (pip install titlecase). https://github.com/ppannuto/python-titlecase

##How to use##

If an Item is mentioned in a post with `[[Itemname]]` (uniques only) the bot replies in a comment with the stats about that item

You can also message the bot directly and it will reply with the formatted item information so you can use it in your post
