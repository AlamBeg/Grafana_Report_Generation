import json
import requests
import yaml

API_TOKEN=None

class api_token:
	def get_token(user, password):
	login_uri = 'http://{0}:{1}/login'.format(GRAFANA_INFO['host'], GRAFANA_INFO['port'])
	payload = {'user': user, 'password': password, 'email': ''} 
	r = requests.post(login_uri, data=payload)
	if r.status_code == requests.codes.ok:
		return r.cookies
	return None
