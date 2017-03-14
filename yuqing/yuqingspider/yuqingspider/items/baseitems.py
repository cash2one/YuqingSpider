from scrapy.item import Item, Field

class SpiderItem(Item):
    title = Field()
    link = Field()
    source = Field()
    abstract = Field()
    publishtime = Field()
