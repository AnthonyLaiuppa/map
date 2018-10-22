from __future__ import absolute_import, unicode_literals
from bs4 import BeautifulSoup
from time import sleep
import sublist3r
import requests


class MapSnatchLogic(object):

	def __init__(self, domain=None, mapsubs=False, statuses={}, links={}):
		self.domain=domain
		self.mapsubs=mapsubs
		self.statuses=statuses
		self.links=links

	def get_subs(self):
		"""We're using sublist3r to get us the subdomains"""
		output = self.domain + '_subdomains.txt'
		subdomains = sublist3r.main(
			self.domain, 
			40,
			output, 
	 		ports= None, 
			silent=False, 
			verbose= False, 
	 		enable_bruteforce= False, 
	 		engines=None
	 )
		for sub in subdomains:
			print('[!] Found subdomain - {0}'.format(sub))
		print('[*] Successfully retrieved subdomains')
		self.subdomains = subdomains

	def get_statuses(self):
		#We check the top level domain first
		self.check_status(self.domain)
		#Then we check the subs
		for sub in self.subdomains:
			self.check_status(sub)

		print('[*] Successfully populated statuses')

		for k,v in self.statuses.items():
			print('[-] {0} : {1}'.format(k,v))

	def check_status(self, url):
		sleep(1)
		getter='https://'+url
		print('[-] Checking status of: {0}'.format(url))
		try:
			r = requests.get(getter)
			self.statuses[url] = r.status_code
		except Exception as exc:
			self.statuses[url] = 'Failed to establish new connection'

	def harvest_links(self,url):
		getter =' https://'+url
		r = requests.get(getter)
		print('[-] Harvesting Links from: {0}'.format(url))
		links = []
		content = r.content
		#Get all the links from the page with Bs4
		soup = BeautifulSoup(content,'html.parser')
		soup_links = soup.find_all('a')
		#Populate our list of links
		for link in soup_links:
			links.append(link.get('href'))
		#NoneTypes could ruin our day, filter it
		links = list(filter(None,links))
		#Clean our links of out of scope stuff
		out_of_scope = []
		for link in links:
			if link[0] is not '/':
				out_of_scope.append(link)
		clean_links = [link for link in links if link not in out_of_scope]
		#Store our links in a dict url:[links]
		self.links[url] = clean_links
		print('[*] Links harvested from: {0}'.format(url))
		for k,v in self.links.items():
			print('[-] {0} : {1}'.format(k,v))





