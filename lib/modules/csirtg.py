from csirtgsdk.client import Client
from csirtgsdk.search import Search

from common import get_apikey


def run(query):
    result = None
    key = get_apikey('csirtg')

    try:
        client = Client(remote='https://csirtg.io/api', token=key)
        search = Search(client)
        result = search.search(query)
    except:
        pass

    return result


def main(artifact, artifact_type=None):
    result = run(artifact)
    return result
