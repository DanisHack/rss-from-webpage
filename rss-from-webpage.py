"""
    Turn a web page into an RSS feed.
    Assumes a CSS-selector identifiable that contains children
        and currently hard codes how each article is extracted
        (title between A tags, link in the A href,
        description = a single P within the child. or something.)
"""

# TODO: Output on the web somewhere
# TODO: Test against RSS validator
# TODO: don't hard code item extraction selectors - pass in somehow
# TODO: automatically get title etc from page
# TODO:   but allow overrides e.g. title
# TODO: optionally get content from each link target
# TODO: optionally take RSS with summaries, add full content (selector specified, finding content too hard)
# TODO: get dates on items from...HTTP?
# TODO: get dates on items from selector (parsing a date string)
# TODO: get dates on items from selector (on top page or article page)
# TODO: other attributes? of feed / items?
# TODO: be a good citizen
# TODO: - check if there's already a feed and say so
# TODO: - keep local cache (just the RSS? serialised as JSON? pickle?)
# TODO: - don't scrape top page if HTTP says cached / date unchanged
# TODO: - don't scrape article page if HTTP says date unchanged
# TODO: - don't scrape item if date (from selector / date string parsing) unchanged
# TODO: better docstrings
# TODO: allow to be run as a web service. fire only when output url is hit/run
# TODO: a repository / dictionary of feed_settings definitions
# TODO: a shared / master repository of feed_settings definitions
# TODO: define a pattern common to multiple pages on site, allow choosing by name
# TODO: - e.g. columnists listed on page, link to each of their names
# TODO: take feed definition name as URL parameter
# TODO: handle routes so /feed/feed_name/ works
# TODO: or take all feed settings as URL parameters?
# TODO: requirements.txt
# TODO: any kind of unit test :|

import collections

import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator


def get_articles_from_html(container_html):
    """
    Takes an HTML string and extracts children according to
    Returns a set of namedtuples with link, title and description
    """

    feed_article = collections.namedtuple('feed_article',
                                          {'link', 'title', 'description', })
    articles = set()
    for child in container_html:
        # TODO pass in criteria for choosing item, don't hard code

        link = child.find('a')['href']  # TODO hardcoded
        title = child.find('a').string  # TODO hardcoded
        description = child.find('p').string  # TODO hardcoded

        articles.add(
            feed_article(link=link, title=title, description=description))

    return articles


def generate_rss_from_articles(feed_settings, articles):
    """
    Creates a FeedGenerator feed from a set of feed_entries.
    
    :param feed_settings: a feed_settings object containing 
    :param articles: 
    :return: 
    """

    # create the feed
    output_feed = FeedGenerator()

    # add metadata to the feed
    # TODO this feels like it can be done without output_rss on every line but...Python newbie
    output_feed.title(feed_settings.title)
    output_feed.author(feed_settings.author)
    output_feed.link(href=feed_settings.source_page_url, rel='alternate')
    output_feed.link(href=feed_settings.output_url, rel='self')
    output_feed.logo(feed_settings.logo_img_url)
    output_feed.subtitle(feed_settings.subtitle)
    output_feed.language(feed_settings.language)
    # output_rss.id(UM_SOMETHING)

    # add each feed item
    for article in articles:
        feed_entry_added = output_feed.add_entry()
        feed_entry_added.id(article.link) # ATOM
        # guid for RSS?
        feed_entry_added.link(href=article.link, rel='alternate') # ATOM
        feed_entry_added.title(article.title)
        feed_entry_added.description(article.description)
        # feed_entry_added.link(article.link)

    return output_feed


def output_rss(rss, filename):
    """
    Sends RSS to a file, and stdout if debugging
    :param feed_xml: valid RSS XML
    :return: none
    """

    if debug:
        print(rss.rss_str(pretty=True))
    rss.rss_file(filename)


def rss_from_webpage(feed_settings):
    """
    TODO docstring
    :param feed_settings: 
    :return: 
    """

    source_page_html = requests.get(feed_settings.source_page_url).content
    soup = BeautifulSoup(source_page_html, 'html.parser')
    container_html = soup.select(feed_settings.container_CSS_selector)
    articles = get_articles_from_html(container_html)
    rss = generate_rss_from_articles(feed_settings, articles)
    return rss


def main():
    """
    TODO docstring
    :return: 
    """

    # TODO: feels like this doesn't go in main. what goes in main normally? do I need a function with the same name as the module?

    feed_settings = collections.namedtuple('feed_settings',
                                           {'source_page_url',
                                            'container_CSS_selector',
                                            'output_file', 'output_url',
                                            'title', 'subtitle', 'author',
                                            'logo_img_url',
                                            'language', })

    # TODO: feels like this should be only used as debug / when nothing passed in given it's default/test values
    this_feed_settings = feed_settings(
        source_page_url='http://www.smh.com.au/comment/by/Annabel-Crabb-hvecc',
        container_CSS_selector='main.main div.story__wof',
        output_file='annabel-crabb-smh.rss',
        output_url='http://lukemorey.com/rss/annabel-crabb-smh.rss',
        title='Annabel Crabb SMH',
        subtitle='Annabel Crabb is a regular columnist, TV host and leading political commentator.',
        author={'name': 'Annabel Crabb'},
        # there are other field options here like email...
        logo_img_url='http://www.smh.com.au/content/dam/images/h/v/e/c/d/image.imgtype.columnistThumbnail.90x90.png/1408400781813.png',
        language='en')

    rss = rss_from_webpage(this_feed_settings)
    output_rss(rss, this_feed_settings.output_file)


debug = True

if __name__ == "__main__":
    main()
