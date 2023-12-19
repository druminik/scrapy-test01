from typing import Any
from scrapy.http import Response
import scrapy
import csv


class QuotesSpider(scrapy.Spider):
    name = "raiffeisen_casa"
    # allowed_domains = ["immo.raiffeisen.ch"]
    start_urls = ["https://immo.raiffeisen.ch/immobilien-kaufen/haus/"]

    def parse_detail(self, response: Response, **kwargs: Any) -> Any:
        div_selection = response.css("div.flex.flex-col.pl-d40")
        type = "".join(div_selection[0].css("h2::text").re(r"[a-zA-Z]"))
        price = div_selection[1].css("p::text")[1].re(r"\D*([\d’]+)")[0]
        property_area = div_selection[2].css(
            "p::text")[1].re(r"\D*([\d’]+)")[0]
        living_space = div_selection[3].css("p::text")[1].re(r"\D*([\d’]+)")[0]
        rooms = div_selection[4].css("p::text")[1].re(r"\D*([\d’]+)")[0]
        description = " ".join(response.css(
            "div.w-full.col-span-4.mt-d60 div")[14].css("p::text").getall()).replace('\n', '')

        location = response.css(
            "span.p-2.cursor-default.font-small-bold.shrink-0").re(r"in\s(.*)")

        yield {
            "title": response.css("p.font-t100.mb-d40::text").get(),
            # "price": response.css("p.mb-0.hyphens-manual.font-t300::text").re(r"\D*([\d’]+)")[0],
            "price": price,
            "type": type,
            "property_area": property_area,
            "living_space": living_space,
            "description": description,
            "location": location,
            "rooms": rooms,
            "link": response.url,
        }

    def parse(self, response: Response, **kwargs: Any) -> Any:
        for building in response.css("div.relative.teaser.group"):
            detail_page = building.css(
                "div.w-full.overflow-hidden.mb-d40 a::attr(href)").get()
            if detail_page is not None:
                next_page = response.urljoin(detail_page)
                yield scrapy.Request(next_page, callback=self.parse_detail)

        next_page = response.css("li a.next::attr(href)").get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
