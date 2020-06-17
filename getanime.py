import requests, json, json
from bs4 import BeautifulSoup
from io import StringIO


def search(search):
  query = '''
  query ($id: Int, $page: Int, $perPage: Int, $search: String) {
      Page (page: $page, perPage: $perPage) {
          pageInfo {
              total
              currentPage
              lastPage
              hasNextPage
              perPage
          }
          media (id: $id, search: $search, type: ANIME, sort: SEARCH_MATCH) {
              id
              title {
                  romaji
              }
          }
      }
  }
  '''
  variables = {
      'search': search,
      'page': 1,
      'perPage': 1,
      'type': 'ANIME'
  }
  url = 'https://graphql.anilist.co'

  response = requests.post(url, json={'query': query, 'variables': variables})
  io = StringIO(response.text)
  results = json.load(io)
  result_list = results['data']['Page']['media']
  final_result = []
  title = result_list[0]['title']['romaji']
  return title



def gogo_api_ani_list(method, query):
	romaji = search(query)
	base_url = f'https://gogoanime.now.sh/api/v1/{method + romaji}'.lower().replace(' ', '%20')
	io = StringIO(requests.get(f'{base_url}').text)
	io = json.load(io)
	return io


def gogo_api(method, query):
	base_url = f'https://gogoanime.now.sh/api/v1/{method + query}'.lower().replace(' ', '%20')
	io = StringIO(requests.get(f'{base_url}').text)
	io = json.load(io)
	return io

