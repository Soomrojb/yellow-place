import scrapy
from scrapy.item import Item, Field
from unidecode import unidecode

class YellowItems(Item):
	CityTitle = Field()
	CityURL = Field()
	IndustryTitle = Field()
	IndustryURL = Field()
	CategoryURL = Field()
	CategoryTitle = Field()
	ImageURL = Field()
	PostTitle = Field()
	PostURL = Field()
	PostAddress = Field()
	PostCategory = Field()
	RangePrice = Field()
	Categories = Field()
	Description = Field()
	Pricerange = Field()
	CompanyOView = Field()
	GeneralInfo = Field()
	FoodStyle = Field()
	ResSpecial = Field()
	Services = Field()
	GeneralMgr = Field()
	Parking = Field()
	CulinaryTeam = Field()
	Biography = Field()
	Founders = Field()
	ViewImage = Field()

class YellowPlace(scrapy.Spider):
	name = 'yellowplace'
	start_urls = ['https://yellow.place/en/r/pakistan']
	custom_settings = {
		'FEED_FORMAT' : 'csv',
		'FEED_URI' : 'imp_spider1.csv'
	}

	def parse(self, response):
		for City in response.css("div[class='wrap'] > div[id='content_data'] > a[class='js_title']"):
			Item = YellowItems()
			Item['CityTitle'] = City.css("::text").extract()
			Item['CityURL'] = response.urljoin(City.xpath("@href").extract()[0])
			yield scrapy.Request(Item['CityURL'], meta={'FirstItem':Item}, callback=self.parse_second)
	
	def parse_second(self, response):
		PrvItem = response.meta['FirstItem']
		for Industry in response.css("div[class='wrap'] > div[class='block-list'] > div > a[class='block-title']"):
			Item = YellowItems()
			Item['CityTitle'] = PrvItem['CityTitle']
			Item['CityURL'] = PrvItem['CityURL']
			Item['IndustryURL'] = response.urljoin(Industry.xpath("@href").extract()[0])
			Item['IndustryTitle'] = Industry.css("::text").extract()
			yield scrapy.Request(Item['IndustryURL'], meta={'SecondItem':Item}, callback=self.parse_third)
	
	def parse_third(self, response):
		PrvItem = response.meta['SecondItem']
		for Category in response.css("div[class='wrap'] > div[class='link-list'] > a[class='js_title']"):
			Item = YellowItems()
			Item['CityTitle'] = PrvItem['CityTitle']
			Item['CityURL'] = PrvItem['CityURL']
			Item['IndustryURL'] = PrvItem['IndustryURL']
			Item['IndustryTitle'] = PrvItem['IndustryTitle']
			Item['CategoryURL'] = response.urljoin(Category.xpath("@href").extract()[0])
			Item['CategoryTitle'] = Category.css("::text").extract()
			yield scrapy.Request(Item['CategoryURL'], meta={'ThirdItem':Item}, callback=self.parse_fourth)

	def parse_fourth(self, response):
		PrvItem = response.meta['ThirdItem']
		for Post in response.css("div[class='wrap'] > div[class='list-b full'] > div"):
			Item = YellowItems()
			Item['CityTitle'] = PrvItem['CityTitle']
			Item['CityURL'] = PrvItem['CityURL']
			Item['IndustryURL'] = PrvItem['IndustryURL']
			Item['IndustryTitle'] = PrvItem['IndustryTitle']
			Item['CategoryTitle'] = PrvItem['CategoryTitle']
			Item['CategoryURL'] = PrvItem['CategoryURL']
			Item['ImageURL'] = Post.xpath("//a[@class='pic-frame']/img/@src").extract()
			Item['PostURL'] = response.urljoin(Post.xpath("//a[@class='title']/@href").extract()[0])
			Item['PostTitle'] = Post.css("a[class='title'] ::text").extract()
			Item['PostAddress'] = Post.css("p ::text").extract()
			Item['PostCategory'] = Post.css("div[class='link-list'] ::text").extract()
			yield scrapy.Request(Item['PostURL'], meta={'ForthItem':Item}, callback=self.parse_fifth)

	def parse_fifth(self, response):
		PrvItem = response.meta['ForthItem']
		try:
			CatArray = []
			Categories = response.xpath("//th[. = 'Categories']/following::td[1]/div[@class='link']")
			for CatDiv in Categories:
				NewValue = CatDiv.xpath("text()[1]").extract()[0] + "" + CatDiv.xpath(".//a/text()").extract()[0]
				CatArray.append(NewValue)
			Categoriez = "|".join(CatArray)
		except:
			Categoriez = '-'
		try:
			Description = response.xpath("//th/h3[. = 'Description']/following::td[1]//text()").extract()
		except:
			Description = '-'
		try:
			Pricerange = response.xpath("//th/h3[text() = 'Price range']/following::td[1]//text()").extract()
		except:
			Pricerange = '-'
		try:
			About = response.xpath("//th/h3[. = 'About']/following::td[1]//text()").extract()
		except:
			About = '-'
		try:
			ContactNumb = response.xpath("//div[@class='view-header']/div[@class='contacts']//text()").extract()
		except:
			ContactNumb = '-'
		try:
			Website = response.xpath("//div[@class='view-header']/div[@class='link-list']/a//text()").extract()
		except:
			Website = '-'
		try:
			Mission = response.xpath("//th/h3[. = 'Mission']/following::td[1]//text()").extract()
		except:
			Mission = '-'
		try:
			Products = response.xpath("//th/h3[. = 'Products']/following::td[1]//text()").extract()
		except:
			Products = '-'
		try:
			Founded = response.xpath("//th/h3[. = 'Founded']/following::td[1]/text()").extract()
		except:
			Founded = '-'
		try:
			Awards = response.xpath("//th/h3[. = 'Awards']/following::td[1]/text()").extract()
		except:
			Awards = '-'
		try:
			MAPValues = response.xpath("//div[@class='nav-column']/script").re(r"uluru\s+=(.+)")[0]
		except:
			MAPValues = '-'
		try:
			CompanyOView = response.xpath("//th/h3[. = 'Company overview']/following::td[1]//text()").extract()
		except:
			CompanyOView = '-'
		try:
			GeneralInfo = response.xpath("//th/h3[. = 'General info']/following::td[1]//text()").extract()
		except:
			GeneralInfo = '-'
		try:
			FoodStyle = response.xpath("//th/h3[. = 'Food styles']/following::td[1]//text()").extract()
		except:
			FoodStyle = '-'
		try:
			ResSpecial = response.xpath("//th/h3[. = 'Restaurant specialties']/following::td[1]//text()").extract()
		except:
			ResSpecial = '-'
		try:
			Services = response.xpath("//th/h3[. = 'Services']/following::td[1]//text()").extract()
		except:
			Services = '-'
		try:
			GeneralMgr = response.xpath("//th/h3[. = 'General manager']/following::td[1]//text()").extract()
		except:
			GeneralMgr = '-'
		try:
			Parking = response.xpath("//div[@class='nav-column']/div[@class='box']//td[@rowspan='7']/text()").extract()
		except:
			Parking = '-'
		try:
			CulinaryTeam = response.xpath("//th/h3[. = 'Culinary team']/following::td[1]//text()").extract()
		except:
			CulinaryTeam = '-'
		try:
			Biography = response.xpath("//th/h3[. = 'Biography']/following::td[1]//text()").extract()
		except:
			Biography = '-'
		try:
			Founders = response.xpath("//th/h3[. = 'Founders']/following::td[1]//text()").extract()
		except:
			Founders = '-'
		try:
			ViewImage = response.xpath("//div[@class='view-image']/img/@src").extract()
		except:
			ViewImage = '-'
		try:
			WDayArray = []
			WorkingDayz = response.xpath("//div[@class='box']/table/tbody/tr")
			for WDDiv in WorkingDayz:
				NewValue = WDDiv.xpath("./td[1]//text()").extract()[0] + " > " + unidecode(WDDiv.xpath('./td[2]//text()').extract()[0]).strip()
				WDayArray.append(NewValue)
			WorkingDays = "|".join(WDayArray)
		except:
			WorkingDays = '-'
		yield {
			'CityTitle' : unidecode("".join(PrvItem['CityTitle'])),
			'CityURL' : PrvItem['CityURL'],
			'IndustryURL' : PrvItem['IndustryURL'],
			'IndustryTitle' : unidecode("".join(PrvItem['IndustryTitle'])),
			'CategoryTitle' : unidecode("".join(PrvItem['CategoryTitle'])),
			'CategoryURL' : PrvItem['CategoryURL'],
			'ImageURL' : PrvItem['ImageURL'],
			'PostURL' : PrvItem['PostURL'],
			'PostTitle' : unidecode("".join(PrvItem['PostTitle'])),
			'PostAddress' : PrvItem['PostAddress'],
			'PostCategory' : PrvItem['PostCategory'],
			'About' : unidecode("".join(About)),
			'Description' : unidecode("".join(Description)),
			'Pricerange' : unidecode("".join(Pricerange)),
			'Categoriez' : unidecode("".join(Categoriez)),
			'Website' : Website,
			'ContactNumb' : ContactNumb,
			'Mission' : unidecode("".join(Mission)),
			'Products' : unidecode("".join(Products)),
			'Founded' : unidecode("".join(Founded)),
			'Awards' : unidecode("".join(Awards)),
			'MAPValues' : MAPValues,
			'CompanyOView' : unidecode("".join(CompanyOView)),
			'GeneralInfo' : unidecode("".join(GeneralInfo)),
			'FoodStyle' : unidecode("".join(FoodStyle)),
			'ResSpecial' : unidecode("".join(ResSpecial)),
			'Services' : unidecode("".join(Services)),
			'GeneralMgr' : unidecode("".join(GeneralMgr)),
			'Parking' : unidecode("".join(Parking)),
			'CulinaryTeam' : unidecode("".join(CulinaryTeam)),
			'Biography' : unidecode("".join(Biography)),
			'Founders' : unidecode("".join(Founders)),
			'WorkingDays' : "".join(WorkingDays),
			'ViewImage' : ViewImage,
		}

