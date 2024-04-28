# from google.auth.transport.requests import AuthorizedSession
# from google.oauth2 import service_account

def get_disaster_warnings(coordinates):
	print(coordinates)
	return str({
		"flood_data": "The nearest flood is at coordinats 40 -122 with a certainty of 75%.",
		"fire_data": "Fire detected in San Francisco.",
		"earth_data": "There was an 7.2 earthquake 3 minutes ago in Vacaville, CA.",
		"wind_advisory": "There is a wind advisory warning in the area.",
		"heat_advisory": "There is a heat advisory warning in the area."
	})

# credentials = service_account.Credentials.from_service_account_file(KEY)
# scoped_credentials = credentials.with_scopes(
#     ['https://www.googleapis.com/auth/cloud-platform'])

# session = AuthorizedSession(scoped_credentials)

# url = 'https://earthengine.googleapis.com/v1alpha/projects/earthengine-public/assets/LANDSAT'

# response = session.get(url)

# from pprint import pprint
# import json
# pprint(json.loads(response.content))