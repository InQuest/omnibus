from csirtgsdk.client import Client
from csirtgsdk.search import Search

from common import get_apikey


class Plugin(object):
    def __init__(self, artifact):
        self.artifact = artifact
        self.artifact['data']['csirtg'] = None
        self.api_key = get_apikey('csirtg')


    def run(self):
        try:
            client = Client(remote='https://csirtg.io/api', token=self.api_key)
            search = Search(client)
            data = search.search(self.artifact['name'])
            if len(data['feed']['indicators']) > 0:
                self.artifact['data']['csirtg'] = search.search(self.artifact['name'])
        except:
            pass


def main(artifact):
    plugin = Plugin(artifact)
    plugin.run()
    return plugin.artifact
