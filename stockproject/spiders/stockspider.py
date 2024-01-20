
# from urllib.parse import urljoin
# import scrapy

# class StockSpider(scrapy.Spider):
#     name = "stockspider"
#     allowed_domains = ["www.moneycontrol.com"]
#     start_urls = ["https://www.moneycontrol.com/india/stockpricequote/A"]
                  
#     def parse(self, response):
#         # Extract links from the current page
#         links = response.css('table.pcq_tbl a.bl_12::attr(href)').extract()

#         # Process each link and follow to the next page
#         for link in links:
#             full_url = response.urljoin(link)  # Combine with the base URL
#             yield scrapy.Request(full_url, callback=self.parse_book_page)

#         # Follow the link to the next page
#         next_page = response.css('div.MT2.PA10 a.cur + a::attr(href)').get()
#         if next_page is not None:
#             full_next_page = urljoin(response.url, next_page)
#             yield response.follow(full_next_page, callback=self.parse)

#     def parse_book_page(self, response):
#         name = response.css('div.inid_name h1::text').get()

#         if name is not None:
#             yield {
#                 'NAME': name,
#                 'TYPE': response.css('div.frs_spn strong::text').get(),
#                 'COST':response.css('div#bsecp::text').get(),
#                 'STRENGTH': response.css('a.kbyistrengths em::text').get(),
#                 'WEAKNESS': response.css('a.kbyiweaknesses em::text').get(),
#                 'OPPORTUNITIES': response.css('a.kbyiopportunities em::text').get(),
#                 'THREATS': response.css('a.kbyithreats em::text').get(),
#                 'P_LOW': response.css('div#sp_low::text').get(),
#                 'P_HIGH': response.css('div#sp_high::text').get(),
#                 'YEARLY_LOW':response.css('div#sp_yearlylow::text').get(),
#                 'YEARLY_HIGH':response.css('div#sp_yearlyhigh::text').get()
#             }
import time
from urllib.parse import urljoin
import scrapy
import requests

class StockSpider(scrapy.Spider):
    name = "stockspider"
    allowed_domains = ["www.moneycontrol.com"]
    start_urls = ["https://www.moneycontrol.com/india/stockpricequote/A"]
                  
    def parse(self, response):
        # Extract links from the current page
        links = response.css('table.pcq_tbl a.bl_12::attr(href)').extract()

        # Process each link and follow to the next page
        for link in links:
            full_url = response.urljoin(link)  # Combine with the base URL
            yield scrapy.Request(full_url, callback=self.parse_book_page)

        # Follow the link to the next page
        next_page = response.css('div.MT2.PA10 a.cur + a::attr(href)').get()
        if next_page is not None:
            full_next_page = urljoin(response.url, next_page)
            yield response.follow(full_next_page, callback=self.parse)

    def parse_book_page(self, response):
        name = response.css('div.inid_name h1::text').get()

        if name is not None:
            yield {
                'NAME': name,
                'TYPE': response.css('div.frs_spn strong::text').get(),
                'COST':self.fetch_stock_cost(response.css('div#bsecp::text').get()),
                'STRENGTH': response.css('a.kbyistrengths em::text').get(),
                'WEAKNESS': response.css('a.kbyiweaknesses em::text').get(),
                'OPPORTUNITIES': response.css('a.kbyiopportunities em::text').get(),
                'THREATS': response.css('a.kbyithreats em::text').get(),
                'P_LOW': response.css('div#sp_low::text').get(),
                'P_HIGH': response.css('div#sp_high::text').get(),
                'YEARLY_LOW':response.css('div#sp_yearlylow::text').get(),
                'YEARLY_HIGH':response.css('div#sp_yearlyhigh::text').get()
            }

    def fetch_stock_cost(self, cost):
        # Fetch the stock cost from the given cost
        if cost is not None:
            try:
                return float(cost)
            except (ValueError, TypeError):
                # If the cost is not currently available or not a valid float, move on
                pass

    def fetch_stock_data_for_all_pages(self):
        # Fetch stock data for all pages
        stock_data = []
        for page_url in self.start_urls:
            stock_data.append(self.fetch_stock_data(page_url))
        return stock_data

    def fetch_stock_data(self, url):
        # Fetch the stock data from the given URL
        response = requests.get(url)
        response.raise_for_status()
        return self.parse_book_page(response)