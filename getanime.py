import requests
from io import StringIO
import json, re

def search_anilist(search, max_results=10):
	query = """
	query ($id: Int, $page: Int, $search: String, $type: MediaType) {
		Page (page: $page, perPage: 10) {
			media (id: $id, search: $search, type: $type) {
				id
				idMal
				description(asHtml: false)
				title {
					english
					romaji
				}
				coverImage {
					extraLarge
				}
				bannerImage
				averageScore
				meanScore
				status
				genres
				episodes
				externalLinks {
					url
					site
				}
				nextAiringEpisode {
					timeUntilAiring
				}
			}
		}
	}
	"""
	variables = {
		'search': search,
		'page': 1,
		'perPage': max_results,
		'type': 'ANIME',
		'sort': 'SEARCH_MATCH'
	}
	url = 'https://graphql.anilist.co'

	response = requests.post(url, json={'query': query, 'variables': variables})
	io = StringIO(response.text)
	results = json.load(io)['data']['Page']['media'][0]

	res = {
		'desc': re.sub(r"\<(.*?)\>", '', results['description']),
		'title': results['title']['english'],
		'link': 'https://anilist.co/anime/{}'.format(results['id']),
		'img': results['coverImage']['extraLarge'],
		'status': results['status'],
		'genres': results['genres'],
		'totalEpisodes': results['episodes']
		}
	return res
