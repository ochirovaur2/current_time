import requests
import json
import urllib
import random
import time


class Instagram:
	"""docstring for Instagram"""
	def __init__(self, sessionid, login):
		
		self.login = login
		self.base_url = 'https://www.instagram.com'
		self.headers = {"cookie": f"sessionid={sessionid}"}
		self.user_id = None
		
	def get_user_id(self):
		url = f'{self.base_url}/web/search/topsearch/?context=blended&query={self.login}&rank_token=0.8575941298483327&include_reel=true'

		result = requests.get(url=url, headers=self.headers)

		if result.status_code == 429:
			return {'msg': "Need new sessionid", 'status': result.status_code}
		
		users = json.loads(result.text)["users"]

		if len(users) > 0:
			self.user_id = users[0]["user"]["pk"] 
			return {'msg': users[0]["user"]["pk"], 'status': 200} 
		else:
			return {'msg': "User not found", 'status': 204}


	def get_users(self, final_list, variables, query_data):
		try:
			
			url = f'{self.base_url}/graphql/query/?query_hash={query_data["query_hash"]}&variables={urllib.parse.quote(variables)}'

			result = requests.get(url=url, headers=self.headers)

			if result.status_code > 400:
				time.sleep(3)
				result = requests.get(url=url, headers=self.headers)

				if result.status_code > 400:
					return final_list


			data =  json.loads(result.text)

			edge_followed_data = data["data"]["user"][query_data['dict_key']]

			users = [user["node"]["username"] for user in edge_followed_data["edges"]] 

			final_list = [*final_list, *users]

			print(len(final_list))

			page_info = edge_followed_data["page_info"]
			has_next_page = page_info['has_next_page']
			end_cursor = page_info['end_cursor']

			if has_next_page:

				random_num_to_sleep = random.uniform(1.5, 3.3)

				#print('sleep for:',random_num_to_sleep)

				time.sleep(random_num_to_sleep)

				variables = '{"id":"' + self.user_id + '","include_reel":true,"fetch_mutual":false,"first":13,"after":"'+f'{end_cursor}'+'"}'

				return self.get_users(final_list, variables, query_data)
			else:
				return final_list	
		except:
			return final_list
