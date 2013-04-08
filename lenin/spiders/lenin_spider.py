# coding: utf-8
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from lenin.items import LeninWork
from work_assembler import WorkAssembler
from work_builder import SimpleWorkBuilder
import nltk

class LeninSpider(CrawlSpider):
    name = "lenin"
    allowed_domains = ["marxists.org"]
    start_urls = [
    "http://www.marxists.org/archive/lenin/by-date.htm"
    ]

    INDEX_REGEX = '.+/archive/lenin/.*index\.htm'
    CHAPTER_REGEX = '.+/archive/lenin/works/.+/(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec).+\.htm'
    #Estas son las reglas que aplica a cada link que encuentra
    rules = (
      Rule(SgmlLinkExtractor(allow=".+devel.+"), callback='nada'),
      # Idem si es un indice (de una obra)
      Rule(SgmlLinkExtractor(allow=(INDEX_REGEX)), callback='parse_indexed_work'),
      # Si no es ninguna de las anteriores, es una obra y hay que parsearla!
      Rule(SgmlLinkExtractor(allow=(CHAPTER_REGEX)), callback='parse_unindexed_work')
    )
    
    def nada(self, response):
      print "llame nada" + response.url
      pass

    def parse_indexed_work(self, response):
      """ This function parses a sample response. Some contracts are mingled
      with this docstring.

      @url http://www.marxists.org/archive/lenin/works/1917/staterev/index.htm
      @returns items 0 0
      @returns requests 8 8
      """
      print "\n*************************************************"
      print "Entrando a indice....:"+response.url
      assembler = WorkAssembler(response)
      return assembler.get_requests()

    def parse_unindexed_work(self, response):
      print "\nParseando obra : %s" % response.url
      work = SimpleWorkBuilder(response).get_work()
      print("Titulo : %s" % work['name'].encode('ascii', 'ignore'))
      return work
     