# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BikeDbItem(scrapy.Item):
    brand = scrapy.Field()
    model = scrapy.Field()
    submodel = scrapy.Field()
    year = scrapy.Field()
    description = scrapy.Field()
    category = scrapy.Field()
    engine_size = scrapy.Field()
    engine_type = scrapy.Field()
    power = scrapy.Field()
    top_speed = scrapy.Field()
    torque = scrapy.Field()
    fuel_system = scrapy.Field()
    final_drive = scrapy.Field()
    fuel_consumption = scrapy.Field()
    greenhouse_gases = scrapy.Field()
    frame_type = scrapy.Field()
    rake = scrapy.Field()
    weight_full = scrapy.Field()
    seat_height = scrapy.Field()
    seat_alternate_height = scrapy.Field()
    height = scrapy.Field()
    lenght = scrapy.Field()
    width = scrapy.Field()
    fuel_capacity = scrapy.Field()
    fuel_reserve_capacity = scrapy.Field()
    colors = scrapy.Field()
    starter = scrapy.Field()
    electrical = scrapy.Field()
    url = scrapy.Field()
