import scrapy
from ..items import LinksFollowItem
from urllib.parse import urlparse
from scrapy.linkextractors import LinkExtractor

class LinksFollowSpider(scrapy.Spider):
    name = "links"
    start_urls = [
        "http://google.com"
    ]

    def parse(self, response):

        items = LinksFollowItem()

        # all_a_links = response.css("a")
        current_page = response.url
        parsed_uri = urlparse(response.url)
        # domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        domain_less = '{uri.netloc}'.format(uri=parsed_uri)
        # print (domain)
        # print (domain_less)


        int_extractor = LinkExtractor(allow_domains=domain_less)
        ext_extractor = LinkExtractor(deny_domains=domain_less)
        internal_links = int_extractor.extract_links(response)
        external_links = ext_extractor.extract_links(response)

        title = response.css("title::text").extract()
        title = title[0]
        # print(title)

        for link in internal_links:
            # print ("internal: " + link.url)
            
            text = link.text
            link = link.url

            items["link_text"] = text
            items["link_href"] = link
            items["link_type"] = "Internal"
            items["current_page"] = current_page
            items["page_title"] = title

            yield items

            if ( items["current_page"] != items["link_href"] ):
                yield response.follow(items["link_href"], callback=self.parse)


        for link in external_links:
            # print ("external: " + link.url)
            
            text = link.text
            link = link.url

            items["link_text"] = text
            items["link_href"] = link
            items["link_type"] = "External"
            items["current_page"] = current_page
            items["page_title"] = title

            yield items

            if ( items["current_page"] != items["link_href"] ):
                yield response.follow(items["link_href"], callback=self.parse)

        # for link in all_a_links:
        #     text = link.css("a::text").extract()
        #     link = link.css("a::attr(href)").extract()
        #     #link = str(current_page) + str(link[0])

        #     items["link_text"] = text[0]
        #     items["link_href"] = domain[:-1] + link[0]
        #     items["current_page"] = current_page
            
            
