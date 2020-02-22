import scrapy
from ..items import LinksFollowItem

class LinksFollowSpider(scrapy.Spider):
    name = "links"
    start_urls = [
        "http://quotes.toscrape.com/"
    ]

    def parse(self, response):

        items = LinksFollowItem()

        all_a_links = response.css("a")

        for l in all_a_links:
            text = l.css("a::text").extract()
            link = l.css("a::attr(href)").extract()
            #tag = l.css(".tag::text").extract()

            items["link_text"] = text
            items["link_href"] = link
            #items["tag"] = tag
            
            yield items