import requests
import json
from types import SimpleNamespace

f = open('config.json')
cfg = json.load(f, object_hook=lambda d: SimpleNamespace(**d))

def searchemote(command_query):
    url = "https://7tv.io/v3/gql"
    query = {
                "variables": {
                    "query": command_query,
                    "limit": 10,
                    "page": 1,
                    "filter": {
                        "case_sensitive": cfg.SevenTV_case_sensitive,
                        "category": cfg.SevenTV_category,
                        "exact_match": cfg.SevenTV_exact_match,
                        "ignore_tags": cfg.SevenTV_ignore_tags,
                    },
                },
                "extensions": {},
                "operationName": 'SearchEmotes',
                "query":'query SearchEmotes($query: String!, $page: Int, $sort: Sort, $limit: Int, $filter: EmoteSearchFilter) {\n  emotes(query: $query, page: $page, sort: $sort, limit: $limit, filter: $filter) {\n    count\n    items {\n      id\n      name\n      listed\n      trending\n      owner {\n        id\n        username\n        display_name\n        style {\n          color\n          paint_id\n          __typename\n        }\n        __typename\n      }\n      flags\n      host {\n        url\n        files {\n          name\n          format\n          width\n          height\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}'
            }

    response = requests.post(url, json=query)
    info = json.loads(response.text, object_hook=lambda d: SimpleNamespace(**d))

    if info.data:
        return info.data.emotes.items
    else: return None