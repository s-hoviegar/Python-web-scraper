import scrapy
from ..items import LinksFollowItem
from urllib.parse import urlparse

class LinksFollowSpider(scrapy.Spider):
    name = "links"
    start_urls = [
        "http://quotes.toscrape.com/"
    ]

    def parse(self, response):

        items = LinksFollowItem()

        all_a_links = response.css("a")
        current_page = response.url
        parsed_uri = urlparse(response.url)
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        print (domain)

        for l in all_a_links:
            text = l.css("a::text").extract()
            link = l.css("a::attr(href)").extract()
            #link = str(current_page) + str(link[0])

            items["link_text"] = text[0]
            items["link_href"] = domain[:-1] + link[0]
            items["current_page"] = current_page
            
            yield items

            if ( items["current_page"] != items["link_href"] ):
                yield response.follow(items["link_href"], callback=self.parse)
