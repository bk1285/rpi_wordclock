import os
import feedparser


class plugin:
    """
    A class to display the latest headline from rss-feed
    """

    def __init__(self, config):
        """
        Initializations for the startup of the rss-feed
        """
        # Get plugin name (according to the folder, it is contained in)
        self.name = os.path.dirname(__file__).split('/')[-1]
        self.rss_url = config.get('plugin_' + self.name, 'rss_url')
        self.pretty_name = "RSS-feed parser"
        self.description = "Displays latest news from " + self.rss_url + "."

    def run(self, wcd, wci):
        """
        Displaying latest news
        """
        feed = feedparser.parse(self.rss_url)
        wcd.showText(feed["items"][0]["title"], fps=15)
