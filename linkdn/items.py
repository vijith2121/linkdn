import scrapy


class LinkdnItem(scrapy.Item):
    # define the fields for your item here like:
    profile_url = scrapy.Field()
    profile_url_slug = scrapy.Field()
    first_name = scrapy.Field()
    last_name = scrapy.Field()
    headline = scrapy.Field()
    publicIdentifier = scrapy.Field()
    show_more_profile_urls = scrapy.Field()
    about = scrapy.Field()
    Causes = scrapy.Field()
    show_more_profile = scrapy.Field()