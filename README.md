# scrapStock  Initialization: We set up the web scraping Spider, defining its name, allowed domains, and starting URLs.
Parsing: The parse method initiates the scraping process by extracting links and navigating through pages.
Data Extraction: The parse_book_page method dives into each stock page, extracting detailed information like name, type, cost, strengths, weaknesses, opportunities, and threats.
Handling Cost: The fetch_stock_cost method ensures the accurate handling of stock cost data, converting it to a float for enhanced usability.
 
