import feedparser

def print_top_headlines(rss_url, top_limit):
    feed = feedparser.parse(rss_url)
    return feed.entries[:top_limit]
