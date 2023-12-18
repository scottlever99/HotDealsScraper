# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class HotdealsscraperPipeline:
    def process_item(self, item, spider):
        return item


import mysql.connector

class SaveToMySQLPipeline:

    def __init__(self):
        self.conn = mysql.connector.connect(
            host = 'ecomclubdata.mysql.database.azure.com',
            user = 'ecomadmin',
            password = '$cupcatdog1',
            database = 'discord'
        )

        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        self.cur.execute("SELECT * FROM hotdeals WHERE hot_title = '" + item["title"] + "' LIMIT 1")
        existingitem = self.cur.fetchall()
        print("EXISTING: ", existingitem)
        if (existingitem == None or len(existingitem) < 1):   
            self.cur.execute(""" INSERT INTO hotdeals 
                            (hot_title,
                            hot_desc,
                            hot_link,
                            hot_price,
                            hot_image) 
                            VALUES
                            (%s,
                            %s,
                            %s,
                            %s,
                            %s)""", (
                                item["title"],
                                item["desc"],
                                item["link"],
                                item["price"],
                                item["image"]
                            ))
            
            self.conn.commit()
        return item
    
    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()
        