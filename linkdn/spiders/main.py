import scrapy
from linkdn.items import LinkdnItem
from lxml import html
import json
import requests

# class LinkdnSpider(scrapy.Spider):
class LinkdnSpider(scrapy.Spider):
    name = "linkdn"
    # start_urls = [
    #     "https://www.linkedin.com",
    # ]

    def start_requests(self):
        profile_urls = [
            'bushra-dhanani-76450224b',
            'bushra-dhanani-76450224b',
            'sharina-perez',
            'zohairar',
            'senda-j-21b04962',
            'mr-abdul-hameed-3501b2135',
            'niyas-kadambot-hydrose-35abbb107',
            'sharook-kt-420665230',
            'sherry-ann-ligayo-34936559'
            # 'ket-how-tey-a1567896',
            # 'muhliscm',
            # 'arjun-tv-a2671118a',
            # 'stefia-david',
            # 'betsy-joseph-098979219',
            # 'sreejith-t-a23844206',
            # 'jeena-abraham-ba376012a',
            # 'itsmeshalini',
            # 'naman-agarwal-bbb9b6158',
            # 'pranit-mohanty-629381182',
            # 'chethan-kumar-vu-32268124b',
            # 'krishnan-v-934156a7',
            # 'sandheep-gopalan-658684234',
            # 'jasmin-j-709615159',
            # 'mirna-ibrahim-a99844235'
            ]
        cookies = {
            'li_at': 'AQEDAQcfXvwDkE1IAAABlJwBaOsAAAGUwA3s61YAf549Kpn8iRXD0GiabxO3-BO4xrCo3gNLSgxWC7ARu0ispFEqPB_iFROte6hu3n9Z-EQXPr_MysYMqm1jBpW8Aj2yWXx3_0tjCHvczweupw2wYFPK',
        }

        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,ml;q=0.7',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'priority': 'u=0, i',
            'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        }

        for profile_url_slug in profile_urls:
            url = f'https://www.linkedin.com/in/{profile_url_slug}'
            meta = {
                'profile_url': url,
                'profile_url_slug': profile_url_slug,
                'cookies': cookies,
                'headers': headers
            }
            yield scrapy.Request(
                url=url, callback=self.parse, cookies=cookies, headers=headers, meta=meta
                )
            # break

    def parse(self, response):
        meta_data = response.meta
        parser = html.fromstring(response.text)
        # print(parser.xpath("//span[text()= 'About']//parent::h2//parent::div//parent::div//parent::div//parent::div//following-sibling::div//span//text()"))
        profile_slug = meta_data.get('profile_url_slug')
        profile_xpath = f"//code[contains(@id, 'bpr-guid')][contains(text(), '{profile_slug}')]//text()"
        profile_items = parser.xpath(profile_xpath)
        profile_data = json.loads(
            "".join(profile_items[0]).strip().replace(' ', '').replace('//', '').replace('\\u003D', '').strip()).get('included', []
        )
        for item in profile_data:
            publicIdentifier = item.get('publicIdentifier')
            if publicIdentifier and publicIdentifier in response.url:
                headline = item.get('headline', None)
                first_name = item.get('firstName', None)
                last_name = item.get('lastName', None)
                about_api_key = item.get("entityUrn")
                meta_data['about_api_key'] = about_api_key
                meta_data['first_name'] = first_name
                meta_data['headline'] = headline
                meta_data['last_name'] = last_name
                meta_data['publicIdentifier'] = publicIdentifier
                show_more_profile_urls = None

                if item.get('entityUrn'):
                    show_more_profile_urls = (
                        f'https://www.linkedin.com/in/{profile_slug}/overlay/browsemap-recommendations/?isPrefetched=true&profileUrn={item.get("entityUrn")}'
                    )
                    meta_data['show_more_profile_urls'] = show_more_profile_urls
                    yield scrapy.Request(
                        url=show_more_profile_urls, callback=self.show_more_profile, cookies=meta_data.get('cookies'), headers=meta_data.get('headers'), meta=meta_data
                    )

    def show_more_profile(self, response):
        cookies = {
            'lang': 'v=2&lang=en-us',
            'li_at': 'AQEDAQcfXvwFoVp2AAABlK3xkiUAAAGU0f4WJU4AN4FLfebPE72-XDSXKgeSAvAsstHcR-1JrQZyGmTnX5nIsruFNVO-ywWERZe89DusZDlx3AbCuf2l30yFlRCwouPGBGV9Zhxg6LN5HKggV2463U75',
            'JSESSIONID': '"ajax:7930250182375445394"'
        }

        headers = {
            'accept': 'application/vnd.linkedin.normalized+json+2.1',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,ml;q=0.7',
            'cache-control': 'no-cache',
            'csrf-token': 'ajax:7930250182375445394',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://www.linkedin.com/in/mishel-john-56223156/',
            'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'x-li-lang': 'en_US',
            'x-li-page-instance': 'urn:li:page:d_flagship3_profile_view_base;oBmXUY8DQ1GqfL4Sswt+cA==',
            'x-li-pem-metadata': 'Voyager - Profile=profile-tab-initial-cards',
            'x-li-track': '{"clientVersion":"1.13.29542","mpVersion":"1.13.29542","osName":"web","timezoneOffset":5.5,"timezone":"Asia/Calcutta","deviceFormFactor":"DESKTOP","mpName":"voyager-web","displayDensity":1,"displayWidth":1920,"displayHeight":1080}',
            'x-restli-protocol-version': '2.0.0',
        }
        parser = html.fromstring(response.text)
        meta_data = response.meta
        show_more_profile_data_xpath = "//code[contains(text(), 'More profiles for you')]//text()"
        show_more_profile_data = parser.xpath(show_more_profile_data_xpath)

        show_more_profile_items = json.loads("".join(show_more_profile_data)).get('data', {}).get('data', {}).get('identityDashProfileComponentsBySectionType', {}).get('elements', [])
        show_more_profile_get = show_more_profile_get_items(show_more_profile_items)

        encoded_url = meta_data.get("about_api_key").replace(':', '%3A')
        about_api = (
            f'https://www.linkedin.com/voyager/api/graphql?variables=(profileUrn:{encoded_url})&queryId=voyagerIdentityDashProfileCards.477a15aef40d846236e0ad896b84f7e0'
        )
        # about_api = 'https://www.linkedin.com/voyager/api/graphql?includeWebMetadata=true&variables=(profileUrn:urn%3Ali%3Afsd_profile%3AACoAAAvHtNoBEyGzBjx0xD1rn4-BMkRRnkMStoo)&queryId=voyagerIdentityDashProfileCards.e832334bfcc658dc78dcdc9492d65ea1'
        headers['referer'] = f'{meta_data.get("profile_url")}'
        res = requests.get(about_api, headers=headers, cookies=cookies)
        for item in res.json().get('included', []):
            if item.get('topComponents'):
                for item_data in item.get('topComponents'):
                    try:
                        causes = item_data.get('components', {}).get('headerComponent', None).get('title', None).get('text')
                    except Exception as error:
                        causes = None
                    if causes and causes == 'About':
                        about = get_about(item.get('topComponents', []))
                        meta_data['about'] = about
                    if causes and causes == 'Causes':
                        Causes = get_about(item.get('topComponents', []))
                        meta_data['Causes'] = Causes
        data = {
            'profile_url': meta_data.get('profile_url', None),
            'profile_url_slug': meta_data.get('profile_url_slug', None),
            'first_name': meta_data.get('first_name', None),
            'last_name': meta_data.get('last_name', None),
            'headline': meta_data.get('headline', None),
            'publicIdentifier': meta_data.get('publicIdentifier', None),
            'show_more_profile_urls': meta_data.get('show_more_profile_urls', None),
            'about': meta_data.get('about', None),
            'Causes': meta_data.get('Causes', None),
            'show_more_profile': show_more_profile_get
        }
        yield LinkdnItem(**data)


def get_about(data):
    about_list = []
    for item in data:
        if item.get('components', {}).get('textComponent'):
            about_list.append(
                item.get('components', {}).get('textComponent').get('text').get('text').strip()
            )
    return "".join(about_list).strip() if about_list else None


def show_more_profile_get_items(show_more_profile_items):
    item_lists = []
    for item in show_more_profile_items:
        item_profile = item.get('components', {}).get('fixedListComponent', {}).get('components', [])
        for get_profile in item_profile:
            profile_items = get_profile.get('components', {}).get('entityComponent', {})
            name = profile_items.get('titleV2', {}).get('text', {}).get('text', '')
            subtitle = profile_items.get('subtitle', {}).get('text', '')
            profile_url = profile_items.get('textActionTarget', '')
            datas = {
                'name': name,
                'subtitle': subtitle,
                'profile_url': profile_url
            }
            item_lists.append(datas)
    return item_lists if item_lists else []
