import asyncio
from pyppeteer import *
import copy

class Psr:
    '''

    '''

    def __init__(self, uri, parse_rule):
        self.base = "https://www.redfin.com"
        self.uri = uri
        # TODO(chun074@usc.edu): this rule should be loaded from external settings, ie. json format in github.
        self.parse_rule = {
            'basic': {
                'home_id': '//meta[@name="twitter:app:url:iphone"]/@content',
                'Redfin Estimate': '//div[@class="info-block avm"]//div[1]/text()',
                'Street Address': '//div[@class="HomeInfo inline-block"]//span[@class="street-address"]/text()',
                'county': '//div[@class="HomeInfo inline-block"]//span[@class="locality"]/text()',
                'state': '//div[@class="HomeInfo inline-block"]//span[@class="region"]/text()',
                'zipcode': '//div[@class="HomeInfo inline-block"]//span[@class="postal-code"]/text()',
                'Last Sold Price': '//div[@class="info-block price"]//div[1]/text()',
                'Beds': '//div[@class="HomeMainStats float-right"]//div[3]//div//text()',
                'Baths': '//div[@class="HomeMainStats float-right"]//div[4]//div//text()',
                'Sq. Ft.': '//div[@class="info-block sqft"]//span//span[1]//text()',
                'Built': '//span[@data-rf-test-id="abp-yearBuilt"]//span[@class="value"]/text()',
                'lat-long': '/html/head/meta[10]/@content',
            },
            'Overview': {
                'Hoa Dues': '//div[@class="keyDetailsList"]//div[1]//span[2]/text()',
                'Style': '//div[@class="keyDetailsList"]//div[2]//span[2]/text()',
                'Property Type': '//div[@class="keyDetailsList"]//div[3]//span[2]/text()',
                'View': '//div[@class="keyDetailsList"]//div[4]//span[2]/text()',
                'Community': '//div[@class="keyDetailsList"]//div[5]//span[2]/text()',
                'County': '//div[@class="keyDetailsList"]//div[6]//span[2]/text()',
                'MLS#': '//div[@class="keyDetailsList"]//div[7]//span[2]/text()',
            },
            'Listing Details': {
                'rawdata': '//*[@id="content"]/div[17]/div/node()'
            },
            'Property History': {
                'table': '//*[@id="content"]/div[19]/div/node()'
            },
            'Public Facts': {
                'Taxable Value - Land': '//*[@id="public-records-scroll"]'
                                        + '/div/div/div[1]/div[1]/div/div/table/tbody/tr[1]/td[2]/text()',
                'Taxable Value - Additions':
                    '//*[@id="public-records-scroll"]/div/div/div[1]/div[1]/div/div/table/tbody/tr[2]/td[2]/text()',
                'Tax Record Year':
                    '//*[@id="public-records-scroll"]/div/div/div[1]/div[2]/div/div/table/tbody/tr/td[1]/text()',
                'Tax Record':
                    '//*[@id="public-records-scroll"]/div/div/div[1]/div[2]/div/div/table/tbody/tr/td[2]/text()',
                'Home Facts - Beds': '//*[@id="basicInfo"]/div[2]/div[1]/div[1]/div/text()',
                'Home Facts - Baths': '//*[@id="basicInfo"]/div[2]/div[1]/div[2]/div/text()',
                'Home Facts - Sqft': '//*[@id="basicInfo"]/div[2]/div[1]/div[3]/div/text()',
                'Home Facts - Stories': '//*[@id="basicInfo"]/div[2]/div[1]/div[4]/div/text()',
                'Home Facts - Lot Size': '//*[@id="basicInfo"]/div[2]/div[1]/div[5]/div/text()',
                'Home Facts - Style': '//*[@id="basicInfo"]/div[2]/div[1]/div[6]/div/text()',
                'Home Facts - Year Built': '//*[@id="basicInfo"]/div[2]/div[1]/div[7]/div/text()',
                'Home Facts - Year Renovated': '//*[@id="basicInfo"]/div[2]/div[1]/div[8]/div/text()',
                'Home Facts - County': '//*[@id="basicInfo"]/div[2]/div[1]/div[9]/div/text()',
                'Home Facts - APN': '//*[@id="basicInfo"]/div[2]/div[1]/div[10]/div/text()',
            },
            'Activity': {
                'Views': '//*[@id="activity-scroll"]/div/div/table/tbody/tr/td[1]/div/div[2]/div/span[1]/text()',
                'Favorites': '//*[@id="activity-scroll"]/div/div/table/tbody/tr/td[2]/div/div[2]/div/span[1]/text()',
                'X-Outs': '//*[@id="activity-scroll"]/div/div/table/tbody/tr/td[3]/div/div[2]/div/span[1]/text()',
                'Redfin Tours': '//*[@id="activity-scroll"]/div/div/table/tbody/tr/td[4]/div/div[2]/div/span[1]/text()',
            },
            'Schools': {
                'Serving This Home': '//tr[@class="schools-table-row"]/node()',
                'Elementary': '//tr[@class="schools-table-row"]/node()',
                'Middle': '//tr[@class="schools-table-row"]/node()',
                'High': '//tr[@class="schools-table-row"]/node()'
            },
            'Neighborhood': {
                'Car-Dependent':
                    '//*[@id="neighborhood-info-scroll"]/div/div[2]/div[1]/div/div[1]/div[1]/div/span[1]/text()',
                'Good Transit':
                    '//*[@id="neighborhood-info-scroll"]/div/div[2]/div[1]/div/div[2]/div[1]/div/span[1]/text()',
                'Bikeable': '//*[@id="neighborhood-info-scroll"]/div/div[2]/div[1]/div/div[3]/div[1]/div/span[1]/text()',
            },
            'Nearby Similar Homes': {
                'connected': '//*[@id="content"]/div[25]/div//a[@class="bottom link-override"]/@href'
            },
            'Nearby Recently Sold Homes': {
                'connected': '//*[@id="lsis-solds"]//a[@class="bottom link-override"]/@href'
            },
        }

        # load parse rules

    async def parse(self):
        browser = await launch(headless=True)
        context = await browser.createIncognitoBrowserContext()
        page = await context.newPage()
        await page.goto('{}/{}'.format(self.base, self.uri))
        information = copy.deepcopy(self.parse_rule)
        uri = '{}/{}'.format(self.base, self.uri)
        uri_list = list()
        uri_list.append(uri)
        information["basic"]["uri"] = uri_list
        print('{}/{}'.format(self.base, self.uri))
        preloads = [
            '#propertyHistory-expandable-segment > div.sectionBottomLinkContainer > div > span',
            '#lsis-nearby-homes > div.action.clickable.nearby-homes-show-more',
        ]
        interactives = [
            '#schools-scroll > div > div.main-content > div > div.scrollable.tabs > div:nth-child(2) > button',
            '#schools-scroll > div > div.main-content > div > div.scrollable.tabs > div:nth-child(3) > button',
            '#schools-scroll > div > div.main-content > div > div.scrollable.tabs > div:nth-child(4) > button',
        ]

        for preload in preloads:
            try:
                if await page.querySelector(preload) is not None:
                    await page.waitForSelector(preload, {'timeout': 10000})
                    await page.click(preload)
            except TimeoutError as t:
                print(t)
        for category in self.parse_rule:
            for label in self.parse_rule[category]:
                try:
                    information[category][label] = list()
                    if category == 'Schools':  # TODO(chun074@usc.edu): should refactor this.
                        elements = await page.xpath(self.parse_rule[category][label])
                        for content in elements:
                            text_content = await page.evaluate('(content) => content.textContent', content)
                            # print(label + ": " + text_content)
                            information[category][label].append(text_content)

                        for interactive in interactives:
                            try:
                                if await page.querySelector(interactive) is not None:
                                    await page.waitForSelector(interactive, {'timeout': 10000})
                                    await page.click(interactive)
                            except TimeoutError as e:
                                print(e)
                    else:
                        elements = await page.xpath(self.parse_rule[category][label])
                        for content in elements:
                            text_content = await page.evaluate('(content) => content.textContent', content)
                            # print(label + ": " + text_content)
                            information[category][label].append(text_content)
                except Exception as e:
                    print("[error: " + label + "]: ")
                    print(e)
                    information[category][label].append(None)
                    # fill with error val and mark it on scheduler(work-queue) to re-fetch.
        print(information)
        return information
