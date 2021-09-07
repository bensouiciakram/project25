import scrapy
from scrapy import Request 
from scrapy.loader import ItemLoader
from torrents_elastic.items import TorrentsElasticItem


class PiratbaySpider(scrapy.Spider):
    name = 'piratbay'
    allowed_domains = [
        'apibay.org',
        'thepiratebay.org'
        ]
    start_urls = ['https://apibay.org/precompiled/data_top100_recent.json']


    def __init__(self):


        self.torrent_template = 'https://apibay.org/t.php?id={}'



    def start_requests(self):
        yield Request(
            self.start_urls[0],
            callback=self.parse_initial_id
        )

    def parse_initial_id(self,response):
        max_id = max([int(torrent['id']) for torrent in response.json()])
        for torrent in range(max_id,1,-1):
            yield Request(
                self.torrent_template.format(torrent),
                meta ={
                    'id':torrent
                }
            )

    def parse(self, response):
        if self.not_exist(response) :
            self.logger.info('\n\n no torrent found with id {} \n\n'.format(response.meta['id']))
            return 

        torrent = response.json()
        loader = ItemLoader(TorrentsElasticItem(),response)
        loader.add_value('id_value',torrent['id'])
        loader.add_value('website','piratbay')
        #loader.add_value('category',torrent['category'])
        loader.add_value('name',torrent['name'])
        loader.add_value('num_files',torrent['num_files'])
        loader.add_value('seeders',torrent['seeders'])
        loader.add_value('leechers',torrent['leechers'])
        loader.add_value('hash_info',torrent['info_hash'])
        loader.add_value('size',str(torrent['size']))
        loader.add_value('description',torrent['descr'])
        loader.add_value('status',torrent['status'])
        yield loader.load_item()

    def not_exist(self,response):
        return 'not exsist' in response.json()['name']

