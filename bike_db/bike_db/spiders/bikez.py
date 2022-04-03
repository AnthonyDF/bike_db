import scrapy
from bike_db.items import BikeDbItem


class BikezSpider(scrapy.Spider):
    name = 'bikez'
    allowed_domains = ['www.bikez.com', 'bikez.com']

    def start_requests(self):
        yield scrapy.Request(
            url='https://bikez.com/brands/index.php',
            callback=self.parse,
            headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, '
                                   'like Gecko) Chrome/94.0.4606.81 Safari/537.36 '}
        )

    def parse(self, response):
        for brand_xpath in response.xpath("//table[@class='zebra']//a[contains(@href,'models')]"):
            brand_url = brand_xpath.xpath(".//@href").get()
            brand = brand_xpath.xpath(".//text()").get().replace('motorcycles', '').strip()

            yield response.follow(url=brand_url, callback=self.parse_brand, headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/94.0.4606.81 Safari/537.36 '}, meta={'brand': brand})

    def parse_brand(self, response):
        brand = response.request.meta['brand']
        for model_ in response.xpath(
                "//table[@class='zebra']//a[not(contains(@href,'google')) and not(contains(@href,'expser')) and not(contains(@name,'toplist'))and not(contains(@href,'_models.php'))]"):
            model = model_.xpath(".//text()").get().replace(brand, '').strip()
            model_url = model_.xpath(".//@href").get()
            yield response.follow(url=model_url, callback=self.parse_model, headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/94.0.4606.81 Safari/537.36 '}, meta={'brand': brand,
                                                                           'model': model
                                                                           })

    def parse_model(self, response):
        brand = response.request.meta['brand']
        model = response.request.meta['model']
        for sub_model_ in response.xpath(
                "//*[contains(@id,'ListBikes')]/following-sibling::table[1]//span[@style='font-size:18px']/parent::a"):
            submodel = sub_model_.xpath(".//span/b/text()").get()
            submodel_url = sub_model_.xpath(".//@href").get()
            yield response.follow(url=submodel_url, callback=self.parse_submodel, headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/94.0.4606.81 Safari/537.36 '}, meta={'brand': brand,
                                                                           'model': model,
                                                                           'submodel': submodel
                                                                           })

    def parse_submodel(self, response):
        brand = response.request.meta['brand']
        model = response.request.meta['model']
        submodel = response.request.meta['submodel']
        year = response.xpath("//b[contains(text(),'Year')]/parent::td/following-sibling::td/text()").get()
        description = response.xpath(
            "//b[contains(text(),'profilation of this')]/parent::td/parent::tr/following-sibling::tr/td/text()").get()
        category = response.xpath("//b[contains(text(),'Category')]/parent::td/following-sibling::td/text()").get()
        engine_size = response.xpath(
            "//a[contains(text(),'Displacement')]/parent::b/parent::td/following-sibling::td/text()").get()
        engine_type = response.xpath(
            "//b[contains(text(),'Engine type')]/parent::td/following-sibling::td/text()").get()
        power = response.xpath("//b[contains(text(),'Power')]/parent::td/following-sibling::td/text()").get()
        top_speed = response.xpath("//b[contains(text(),'Top speed')]/parent::td/following-sibling::td/text()").get()
        torque = response.xpath(
            "//a[contains(text(),'Torque')]/parent::b/parent::td/following-sibling::td/text()").get()
        fuel_system = response.xpath(
            "//b[contains(text(),'Fuel system')]/parent::td/following-sibling::td/text()").get()
        final_drive = response.xpath(
            "//b[contains(text(),'Transmission type')]/parent::td/following-sibling::td/text()").get()
        fuel_consumption = response.xpath(
            "//b[contains(text(),'Fuel consumption')]/parent::td/following-sibling::td/text()").get()
        greenhouse_gases = response.xpath(
            "//b[contains(text(),'Greenhouse gases')]/parent::td/following-sibling::td/text()").get()
        frame_type = response.xpath("//b[contains(text(),'Frame type')]/parent::td/following-sibling::td/text()").get()
        rake = response.xpath("//b[contains(text(),'Rake')]/parent::td/following-sibling::td/text()").get()
        weight_full = response.xpath(
            "//b[contains(text(),'Weight incl. oil, gas')]/parent::td/following-sibling::td/text()").get()
        seat_height = response.xpath(
            "//b[contains(text(),'Seat height:')]/parent::td/following-sibling::td/text()").get()
        seat_alternate_height = response.xpath(
            "//b[contains(text(),'Alternate seat height')]/parent::td/following-sibling::td/text()").get()
        height = response.xpath("//b[contains(text(),'Overall height:')]/parent::td/following-sibling::td/text()").get()
        lenght = response.xpath("//b[contains(text(),'Overall lenght:')]/parent::td/following-sibling::td/text()").get()
        width = response.xpath("//b[contains(text(),'Overall width:')]/parent::td/following-sibling::td/text()").get()
        fuel_capacity = response.xpath(
            "//b[contains(text(),'Fuel capacity')]/parent::td/following-sibling::td/text()").get()
        fuel_reserve_capacity = response.xpath(
            "//b[contains(text(),'Reserve fuel capacity')]/parent::td/following-sibling::td/text()").get()
        colors = response.xpath("//b[contains(text(),'Color options')]/parent::td/following-sibling::td/text()").get()
        starter = response.xpath("//b[contains(text(),'Starter')]/parent::td/following-sibling::td/text()").get()
        electrical = response.xpath("//b[contains(text(),'Electrical')]/parent::td/following-sibling::td/text()").get()

        if brand is not None:
            brand = brand.lower().strip()
        if model is not None:
            model = model.lower().strip()
        if submodel is not None:
            submodel = submodel.replace(year, '').lower().replace(brand, '').strip()
        if category is not None:
            category = category.lower().strip()
        if engine_size is not None:
            engine_size = float(engine_size.split(' ccm')[0].strip())
        if power is not None:
            power = float(power.strip())
        if top_speed is not None:
            top_speed = float(top_speed.split(' km/h')[0].strip())
        if torque is not None:
            torque = float(torque.split(' Nm')[0].strip())
        if fuel_consumption is not None:
            fuel_consumption = float(fuel_consumption.split(' litres/100 km')[0].strip())
        if greenhouse_gases is not None:
            greenhouse_gases = float(greenhouse_gases.split(' CO')[0].strip())
        if rake is not None:
            rake = float(rake.split('°')[0].strip())
        if weight_full is not None:
            weight_full = float(weight_full.split(' kg')[0].strip())
        if seat_height is not None:
            seat_height = int(seat_height.split(' mm')[0].strip())
        if seat_alternate_height is not None:
            seat_alternate_height = int(seat_alternate_height.split(' mm')[0].strip())
        if height is not None:
            height = int(height.split(' mm')[0].strip())
        if width is not None:
            width = int(width.split(' mm')[0].strip())
        if lenght is not None:
            lenght = int(lenght.split(' mm')[0].strip())
        if fuel_capacity is not None:
            fuel_capacity = float(fuel_capacity.split(' litres')[0].strip())
        if fuel_reserve_capacity is not None:
            fuel_reserve_capacity = float(fuel_reserve_capacity.split(' litres')[0].strip())

        item = BikeDbItem()
        item['brand'] = brand
        item['model'] = model
        item['submodel'] = submodel
        item['year'] = year
        item['description'] = description
        item['category'] = category
        item['engine_size'] = engine_size
        item['engine_type'] = engine_type
        item['power'] = power
        item['top_speed'] = top_speed
        item['torque'] = torque
        item['fuel_system'] = fuel_system
        item['final_drive'] = final_drive
        item['fuel_consumption'] = fuel_consumption
        item['greenhouse_gases'] = greenhouse_gases
        item['frame_type'] = frame_type
        item['rake'] = rake
        item['weight_full'] = weight_full
        item['seat_height'] = seat_height
        item['seat_alternate_height'] = seat_alternate_height
        item['height'] = height
        item['lenght'] = lenght
        item['width'] = width
        item['fuel_capacity'] = fuel_capacity
        item['fuel_reserve_capacity'] = fuel_reserve_capacity
        item['colors'] = colors
        item['starter'] = starter
        item['electrical'] = electrical
        item['url'] = response.url

        yield item
