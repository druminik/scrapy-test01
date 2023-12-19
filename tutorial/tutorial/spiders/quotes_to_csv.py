from typing import Any
from scrapy.http import Response
import scrapy
import csv


class QuotesSpider(scrapy.Spider):
    name = "quotes_to_csv"
    # allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/page/1/"]

    def write_to_csv(self, quotes):
        with open('quotes.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['text', 'author', 'tags'])
            for quote in quotes:
                text = quote.css("span.text::text").get(),
                author = quote.css("small.author::text").get(),
                tags = quote.css("div.tags a.tag::text").getall(),
                writer.writerow([text, author, tags])

    def parse(self, response: Response, **kwargs: Any) -> Any:
        self.write_to_csv(response.css("div.quote"))
        return None
        # for quote in response.css("div.quote"):
        #     yield {
        #         "text": quote.css("span.text::text").get(),
        #         "author": quote.css("small.author::text").get(),
        #         "tags": quote.css("div.tag a.tag::text").getAll()
        #     }
