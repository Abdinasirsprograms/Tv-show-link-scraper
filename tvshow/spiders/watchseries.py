import scrapy
import base64
import logging
from scrapy.exceptions import CloseSpider
import re

class watchSpider(scrapy.Spider):
    def __init__(self):
        self.search_title = str(re.findall(r'\w',input('Enter the title of a TV show: '))).lower()
        self.tv_show_link = ''
        self.tv_show = ''
        self.selected_episode = ''
        self.selected_season = ''
        self.direct_links = []
        self.stop_following = False
    name = "watchSpider"
    start_urls = [str(base64.b64decode('aHR0cHM6Ly93d3cxLnN3YXRjaHNlcmllcy50by9zZXJpZXMvMQ==').decode('UTF-8'))]
    def parse(self, response):
        for links in response.css('.category-item'):
            self.tv_show = links.css('a::attr(title)').extract_first()
            if self.stop_following:
                break
            if str(re.findall(r'\w',self.tv_show)).lower() == self.search_title:
                self.tv_show_link = links.css('a::attr(href)').extract_first()
                yield scrapy.Request(self.tv_show_link, callback=self.season_episodes)
                self.stop_following = True
                break
            else:
                next_page = response.css('ul.pagination li a::attr(href)').extract()
                for page in next_page:
                    if page is not None:
                       yield response.follow(page,callback=self.parse)
    def season_episodes(self,response):
        input_season = 'Season ' + (input('Enter a season number: '))
        seasons = response.css('h2.lists a span::text').extract()
        if input_season in seasons:
            self.selected_season = input_season[7:]
            self.selected_episode = int(input('Enter episode number: '))
            episode_search = 's{}_e{}.html'.format(self.selected_season,self.selected_episode)
            episode_link = response.xpath('//li/meta[contains(@content,"'+episode_search+'")]/@content').extract()
            if episode_link is not None:
                yield scrapy.Request(episode_link[0], callback=self.episode_linked)
    def episode_linked(self,response):
        number_of_links = response.css('h1.channel-title a::text').extract()[2:3]
        get_links = response.xpath('//a[@class="watchlink"]/@href').extract()
        current_episode = response.css('div [itemprop=episodeNumber]::attr(content)').extract()
        current_season = response.css('div [itemprop=seasonNumber]::attr(content)').extract()
        clean_links = []
        start_of_data = get_links[0].index('=')
        cleaner_links = []
        for links in range(len(get_links)-1):
            clean_links += [get_links[links][start_of_data:-1]]
        self.direct_links = serialize_in.decode(clean_links)
        for links in self.direct_links:
            finished_links = yield scrapy.Request(links, callback=self.is_404, meta = {'links':
            links, 'cleaner_links':cleaner_links})
        clean_search_title = ''.join(self.search_title)
    def is_404(self, response):
        locate_url = response.url
        links = response.meta['links']
        cleaner_links = response.meta['cleaner_links']
        if ('404.html' not in locate_url) or (response.status != 404):
            cleaner_links.append(links)
            return {'finished links:': cleaner_links}
        else:
            return None

class serialize_in():
    def decode(serialize_in):
        finished_result = []
        for position in range(len(serialize_in)-1):
            serialized = ''
            located_position = serialize_in[position]
            if (len(located_position)%4) != 1:
                located_position = str(located_position) + '='
                serialized = (str(base64.b64decode(located_position).decode('UTF-8')).
                replace('.htm',''))
                finished_result.append(serialized)
        return finished_result
