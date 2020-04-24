import yaml
import json
import logging
import time
import requests
from io import StringIO
from enum import Enum
import uuid
import os

#logging.basicConfig(filename='/var/log/Main_App/se_service_perf_data.log',format='%(message)s',level=logging.DEBUG)

class grafana_report:
	def __init__(self, headers=None, disable_ssl=False):
		super().__init__()
		data=yaml.load(open('config.yaml','r'), Loader=yaml.FullLoader)
		self.host = data['GRAFANA_INFO']['host']
		self.port = data['GRAFANA_INFO']['port']
		self.key_name = (uuid.uuid4().hex.lower()[0:8])
		self.KeyRole = {'VIEWER':'Viewer', 'EDITOR':'Editor', 'ADMIN' : 'Admin'}
		self.user = data['login_creds']['user']
		self.password = data['login_creds']['password']
		self.time_frame = data['time_frame']
		self.pdf_filename = data['pdf_filename']
		print(self.pdf_filename)	
		
	def get_base_headers(self):
		headers = {}
		headers["Accept"] = "application/json"
		headers["Content-Type"] = "application/json"
		return(headers)
	
	def get_auth_headers(self, api_token):
		headers = get_base_headers()
		headers['Authorization'] = 'Bearer {0}'.format(api_token)
		return headers

	def dashboards_list(self):
		response = requests.get('{0}/api/search?folderIds=0&query=&starred=false'.format(self.url),
			verify=self.ssl_verification,
			headers=self.headers)
		print(response.text)
		#print(response.status_code)

	def get_cookies(self):
		login_uri = 'http://{0}:{1}/login'.format(self.host, self.port)
		payload = {'user': self.user, 'password': self.password} 
		r = requests.post(login_uri, data=payload)
		if r.status_code == requests.codes.ok:
			return r.cookies
		return None
	def create_admin_api_token(self):
		cookies = self.get_cookies()
		uri = 'http://{0}:{1}/api/auth/keys'.format(self.host, self.port)
		payload = {'name': self.key_name, 'role': self.KeyRole['ADMIN'] }
		r = requests.post(uri, cookies=cookies, data=payload)
		return (r.status_code, r.text)
	
	def get_api_token(self):
		global API_TOKEN
		#if API_TOKEN is None:
		result = self.create_admin_api_token()
		if result[0] == requests.codes.ok:
			io = StringIO(result[1])
			res = json.load(io)
			API_TOKEN = res.get("key")
			print(API_TOKEN)
		return(API_TOKEN)
	
	def report_pdf(self):
		self.API_TOKEN = self.get_api_token()
		print(self.API_TOKEN)	
		cmd = ('grafana-reporter -cmd_enable=1 -cmd_apiKey {0}  -ip {1}:{2} -cmd_dashboard CGw-HgoWz -cmd_ts {3} -cmd_o alambeg.pdf'.format(self.API_TOKEN, self.host, self.port, self.time_frame))
		os.system(cmd)

p1=grafana_report()
#p1.dashboards_list()
#p1.get_api_token()
p1.report_pdf()
