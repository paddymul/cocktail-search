from urlparse import urljoin

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

from lxml.cssselect import css_to_xpath

from cocktails.items import CocktailItem
from cocktails.utils import html_to_text

xp_ingredients = css_to_xpath('.ingredient')

class DrinkBoySpider(CrawlSpider):
	name = 'drinkboy'
	allowed_domains = ['www.drinkboy.com']
	start_urls = ['http://www.drinkboy.com/Cocktails/']

	rules = (
		Rule(SgmlLinkExtractor(allow=r'/Cocktails/Recipe.aspx'), callback='parse_recipe'),
	)

	def parse_recipe(self, response):
		hxs = HtmlXPathSelector(response)

		for title in hxs.select("//*[@itemprop='name']").extract():
			break
		else:
			return []

		for picture in hxs.select("//img[@itemprop='image']/@src").extract():
			picture = urljoin(response.url, picture)
			break
		else:
			picture = None

		ingredients = hxs.select(xp_ingredients).extract()

		return [CocktailItem(
			title=html_to_text(title),
			picture=picture,
			url=response.url,
			source='DrinkBoy',
			ingredients=map(html_to_text, ingredients),
		)]
