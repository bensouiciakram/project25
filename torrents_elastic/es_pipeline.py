import json
import traceback

import treq

from urllib.parse import quote
from twisted.internet import defer
from scrapy.exceptions import NotConfigured
from twisted.internet.error import ConnectError
from twisted.internet.error import ConnectingCancelledError
from elasticsearch import Elasticsearch
import pickle
import os 
from scrapy.signals import engine_stopped

class EsWriter(object):
    """A pipeline that writes to Elastic Search"""
    
    es = Elasticsearch(['localhost:9200'])


    @classmethod
    def from_crawler(cls, crawler):

        # Get Elastic Search URL
        es_url = crawler.settings.get('ES_PIPELINE_URL', None)

        # If doesn't exist, disable
        if not es_url:
            raise NotConfigured

        return cls(es_url)

    def __init__(self, es_url):
        

        # Store the url for future reference
        self.es_url = es_url
        if os.path.exists('hashes.pkl') :
            self.hashes = pickle.load(open('hashes.pkl','rb'))
        else :
            self.hashes = set()

    #@defer.inlineCallbacks
    def process_item(self, item, spider):
        print('inside pipeline')
        if item['hash_info'] in self.hashes : 
            document = self.es.get(index='torrents',id=item['hash_info']) 
            for dictionary in document['_source']['data']:
                if item['id_value'] == dictionary['id_value']:
                    return 
            document['_source']['data'].append(dict(item))
            self.es.index(
                index = 'torrents',
                id = item['hash_info'],
                body = document['_source'] 
            )
        else :
            self.add_item(item)
        self.hashes.add(item['hash_info'])


            
    def create_es_document(self,item):
        return {
            'hash':item['hash_info'],
            'data':[
                dict(item),
            ]
        }



    def add_item(self,item):
        self.es.index(
                index='torrents',
                id=item['hash_info'],
                body=self.create_es_document(item)
                )

    
    def close_spider(self,spider):
        print('\n\n\n\n\n\n\ inside \n\n\n\n\n\n')
        pickle.dump(self.hashes,open('hashes.pkl','wb'))