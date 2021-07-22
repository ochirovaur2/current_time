from utilities.classes.Instagram import Instagram


def handle_get_followers(sessionid, login):
	insta_api = Instagram(sessionid, login)
	user_id_data = insta_api.get_user_id()
	if user_id_data['status'] == 200:
		user_id = user_id_data['msg']

	elif user_id_data['status'] == 204:
		return ("user not found", 204)
	else:
		return ("need new sessionid", 429)
	variables_for_first_recursion = '{"id":"' + user_id + '","include_reel":true,"fetch_mutual":true,"first":24}'	
	followers = { "query_hash": '37479f2b8209594dde7facb0d904896a',
				"dict_key": 'edge_followed_by'}

	final_list_of_followers = insta_api.get_users([], variables_for_first_recursion, followers)

	
	return (final_list_of_followers, 200)