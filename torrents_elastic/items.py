# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst
from time import time

size_units = {
    'KB': 2**10,
    'MB': 2**20,
    'GB': 2**30, 
}

time_units = {
    'second':1,
    'minute':60,
    'hour':3600,
    'day':86400,
    'week':604800,
    'year':31536000,
    "decade":94608000
}

def delete_poctuation(number_list):
    if type(number_list[0]) == float :
        return number_list
    
    ponctuation = [',']
    return [
        number.replace(ponc,'') for ponc in ponctuation 
        for number in number_list
    ]

class TorrentsElasticItem(scrapy.Item):
    name = scrapy.Field(
        output_processor = TakeFirst()
    )
    description = scrapy.Field(
        output_processor = TakeFirst()
    )
    hash_info = scrapy.Field(
        output_processor = TakeFirst()
    )
    size = scrapy.Field(
        output_processor = TakeFirst()
    )
    id_value = scrapy.Field(
        output_processor = TakeFirst()
    )
    uploader = scrapy.Field(
        output_processor = TakeFirst()
    )
    category = scrapy.Field(
        output_processor = TakeFirst()
    )
    num_files = scrapy.Field(
        output_processor = TakeFirst()
    )
    seeders = scrapy.Field(
        output_processor = TakeFirst()
    )
    leechers = scrapy.Field(
        output_processor = TakeFirst()
    )
    status = scrapy.Field(
        output_processor = TakeFirst()
    )
    website = scrapy.Field(
        output_processor = TakeFirst()
    )


def convert_to_byte(size_list):
    return [
        float(size.split()[0]) * size_units[size.split()[1]] for size in size_list
    ]

def normalize_date(date_list):
    date = date_list[0]
    count = date.split()[0]
    unit = date.split()[1]
    for key in time_units.keys():
        if unit.lower().startswith(key.lower()):
            unit = key 
            break
    return [
        time() - int(count) * time_units[key]
    ]

    
class S1337xItem(scrapy.Item):
    name = scrapy.Field(
        output_processor = TakeFirst()
    )
    description = scrapy.Field(
        output_processor = TakeFirst()
    )
    hash_info = scrapy.Field(
        output_processor = TakeFirst()
    )
    size = scrapy.Field(
        input_processor = convert_to_byte,
        output_processor = TakeFirst()
    )
    id_value = scrapy.Field(
        output_processor = TakeFirst()
    )
    uploader = scrapy.Field(
        output_processor = TakeFirst()
    )
    url = scrapy.Field(
        output_processor = TakeFirst()
    )
    website = scrapy.Field(
        output_processor = TakeFirst()
    )
    seeders = scrapy.Field(
        input_processor = lambda seeders_list:[int(seeder) for seeder in seeders_list],
        output_processor = TakeFirst()
    )
    leechers = scrapy.Field(
        input_processor = lambda leechers_list:[int(leecher) for leecher in leechers_list],
        output_processor = TakeFirst()
    )
    added = scrapy.Field(
        input_processor = normalize_date,
        output_processor = TakeFirst()
    )
    category = scrapy.Field(
        output_processor = TakeFirst()
    )