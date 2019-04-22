from pyppeteer import *


class Crawler:
    """
    class Crawler gets list of URIs from zip_code and page information.
    """

    # TODO(chun074@usc.edu): check style guide for constant values and keep them in separate module if possible.
    LINKS = '//*[@class="HomeCardContainer"]/div/div/div/a/@href'
    BASE_URL = 'https://www.redfin.com'

    def __init__(self, page, zip_code, filter_options, debug):
        self.page = page
        self.zip_code = zip_code
        self.filter_options = filter_options
        self.debug = debug

    # TODO(chun074@usc.edu): separate this method to util class.
    def get_redfin_url_by_zipcode(self):
        """ Configure URI based on zip_code and page and make complete URL.
        Returns complete url. (string) """
        return self.BASE_URL + '/zipcode/{}/recently-sold/page-{}'.format(self.zip_code, self.page)

    async def crawl(self):
        """
        crawls target and returns list of (leaf nodes to explore).
        :return: list() of uri string.
        """
        url = self.get_redfin_url_by_zipcode()
        self.debug.console(url)

        browser = await launch()
        context = await browser.createIncognitoBrowserContext()
        page = await context.newPage()
        await page.goto(url)

        tst = await page.xpath(self.LINKS)
        uris = list()
        for t in tst:
            uris.append(await page.evaluate('(t) => t.textContent', t))
        self.debug.console(uris)

        await browser.close()
        return uris
