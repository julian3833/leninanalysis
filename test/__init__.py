import logging
import sys

import config
import unittest
import ming
from pymongo import MongoClient

ming_config = {'ming.document_store.uri': config.TEST_DATABASE_URL}
ming.configure(**ming_config)

def init_logging():
    logger = logging.getLogger('lenin')
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler('test.log')
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)


init_logging()
client = MongoClient()

class LeninTestCase(unittest.TestCase):
    def setUp(self):
        init_logging()
    
        print "Dropping database %s in setup" % config.DATABASE_NAME
        client.drop_database(config.DATABASE_NAME)
    
    def tearDown(self):
        print "Dropping database %s in teardown" % config.DATABASE_NAME
        client.drop_database(config.DATABASE_NAME)
        