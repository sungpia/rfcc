import asyncio
import crawler
import psr  # TODO(chun074@usc.edu): investigate why import parser references internal module, but calling external one.
import time
import debug
import sys
import formatter
import exporter
parse_rule = {
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
                'Bikeable':
                    '//*[@id="neighborhood-info-scroll"]/div/div[2]/div[1]/div/div[3]/div[1]/div/span[1]/text()',
            },
            'Nearby Similar Homes': {
                'connected': '//*[@id="content"]/div[25]/div//a[@class="bottom link-override"]/@href'
            },
            'Nearby Recently Sold Homes': {
                'connected': '//*[@id="lsis-solds"]//a[@class="bottom link-override"]/@href'
            },
        }


if __name__ == '__main__':
    global page, zip_code, is_debug
    # sys.argv = ['1', '90015', '1']
    # TODO(chun074@usc.edu): type check command line arguments.
    try:
        page = int(sys.argv[0])
        zip_code = int(sys.argv[1])
        is_debug = int(sys.argv[2])
        if not isinstance(page, int):
            raise TypeError
        if not isinstance(zip_code, int):
            raise TypeError
        if not isinstance(is_debug, int):
            raise TypeError
    except TypeError:
        raise TypeError

    # crawl
    crawler = crawler.Crawler(page, zip_code, {}, debug.Debug(1))
    uris = asyncio.get_event_loop().run_until_complete(crawler.crawl())
    debug.Debug(1).console(uris)

    # parse
    parsers = list()
    formatter = formatter.Formatter()

    dataset = list()
    for uri in uris:
        parsers.append(psr.Psr(uri, parse_rule))

    for parser in parsers:
        data = asyncio.get_event_loop().run_until_complete(parser.parse())
        formatted = formatter.format(data)
        dataset.append(formatter.flatten(data))
        time.sleep(2)  # randomize time

    exporter = exporter.Exporter()
    exporter.toCSV('./test.csv', dataset)
