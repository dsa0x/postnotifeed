from random import choice
import json
import requests
from bs4 import BeautifulSoup

USER_AGENTS = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36']

class IGScraper:


    def __init__(self, url, UA=None):
        self.url = url
        self.UA = UA

    def __random_agent(self):
        if self.UA and isinstance(self.UA, list):
            return choice(self.UA)
        return choice(USER_AGENTS)

    
    def __request_url(self):
        try:
            response = requests.get(
                self.url,headers={'User-Agent':self.__random_agent()}
            )
            response.raise_for_status
        except requests.HTTPError:
            raise requests.HTTPError('Received non-200 status code')
        except requests.RequestException:
            raise requests.RequestException
        else:
            return response.text

    @staticmethod
    def extract_json(html):
        soup = BeautifulSoup(html,'html.parser')
        body = soup.find('body')
        script_tag = body.find('script')
        raw_string = script_tag.text.strip().replace('window._sharedData =', '').replace(';','')
        return json.loads(raw_string)

    def post_metrics(self):
        results = []
        try:
            response = self.__request_url()
            json_data = self.extract_json(response)
            metrics = json_data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']
        except Exception as e:
            raise e
        else:
            for node in metrics:
                node = node.get('node')
                if node and isinstance(node,dict):
                    results.append(node)
        return results

#Define the URL for the profile page.

#Initiate a scraper object and call one of the methods.


#Iterate through the metrics and write them to database.
def linkget(username):
    url = 'https://www.instagram.com/{}'.format(username)
    instagram = IGScraper(url)
    metrics = instagram.post_metrics()
    links = []
    for m in metrics:
        i_id = str(m['shortcode'])
        links.append(i_id)
    link = 'https://www.instagram.com/p/' + links[0] + '/'
    linkdict = {
        'link':link
    }
    return linkdict
