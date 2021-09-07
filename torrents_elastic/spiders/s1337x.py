import scrapy
from scrapy import Request
from scrapy.loader import ItemLoader
from torrents_elastic.items import S1337xItem


class S1337xSpider(scrapy.Spider):
    name = 's1337x'
    allowed_domains = ['1337x.to']
    start_urls = ['http://1337x.to/']

    def __init__(self):
        self.torrent_template = 'https://1337x.to/torrent/{}/--/'
        
    def start_requests(self):
        yield Request(
            'https://1337x.to/popular-movies',
            callback=self.parse_initial_id 
        )

    def parse_initial_id(self,response):
        urls = response.xpath('//td/a[2]/@href').getall()
        max_id = max([int(url.split('/')[2]) for url in urls])
        for torrent in range(max_id,max_id-500,-1):#1,-1):
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

        loader = ItemLoader(S1337xItem(),response)
        loader.add_value('website','1337x')
        loader.add_value('url',response.url)
        loader.add_value('id_value',response.meta['id'])
        loader.add_xpath('hash_info','//strong[contains(text(),"Infohash :")]/following-sibling::span/text()')
        #loader.add_xpath('category','//strong[contains(text(),"Category")]/following-sibling::span/text()')
        loader.add_css('name','h1::text')
        loader.add_xpath('size','//strong[contains(text(),"Total size")]/following-sibling::span/text()')
        loader.add_xpath('seeders','//strong[contains(text(),"Seeders")]/following-sibling::span/text()')
        loader.add_xpath('leechers','//strong[contains(text(),"Leechers")]/following-sibling::span/text()')
        loader.add_xpath('uploader','string(//strong[contains(text(),"Uploaded By")]/following-sibling::span)')
        loader.add_xpath('added','//strong[contains(text(),"Date uploaded")]/following-sibling::span/text()')
        loader.add_xpath('description','string(//div[@class="tab-content"])')
        yield loader.load_item()



    def not_exist(self,response):
        return 'Error' in response.xpath('//title/text()').get()

