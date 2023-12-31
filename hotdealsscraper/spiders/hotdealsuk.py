import scrapy


class HotdealsukSpider(scrapy.Spider):
    name = "hotdealsuk"
    allowed_domains = ["hotdukeals.com"]
    start_urls = ["https://www.hotukdeals.com/new"]

    def parse(self, response):
        items = response.css('div.threadGrid');
        for item in items:
            desc = item.css('div.threadGrid > div.threadGrid-body > div > div::text').get()
            title = item.css('div.threadGrid-title > strong > a::text').get()
            
            if (desc == None or desc == "null" or desc == "" or title == None or title == ""):
                continue

            desc = desc.replace("\n", "").replace("\t","").replace("\r","")
            title = title.replace("'", "")
            
            product = {
                'title' : title,
                'price' : item.css('div.threadGrid-title > span > span.overflow--wrap-off > span::text').get(),
                'link' : item.css('div.threadGrid-title > strong > a::attr(href)').get(),
                'image' : item.css('div.threadGrid > div.threadGrid-image > span > img::attr(src)').get(),
                'desc' : desc
            }
            yield product;
        pass