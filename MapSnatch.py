from __future__ import absolute_import, unicode_literals
from bs4 import BeautifulSoup
from time import sleep
import sublist3r
import requests


class MapSnatchLogic(object):

	def __init__(self, domain=None, statuses={}, mapped_links={}, links=[], alive=[]):
		self.domain=domain
		self.statuses=statuses
		self.mapped_links=mapped_links
		self.links=links
		self.alive=alive


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

		for k,v in self.statuses.items():
			print('[-] {0} : {1}'.format(k,v))

		print('[*] Successfully populated statuses')


	def check_status(self, url):

		#Take a url and return a status code
		getter = url
		if 'https://' not in url:
			getter ='https://'+url
		print('[-] Checking status of: {0}'.format(url))

		try:
			r = requests.get(getter)
			self.statuses[url] = r.status_code
			#We need to know what hosts are up incase we need their urls too
			if r.status_code == 200:
				self.alive.append(url)

		except Exception as exc:
			#Unreachable
			self.statuses[url] = 0


	def harvest_links(self,url):

		links = []
		getter = url
		if 'https://' not in url:
			getter ='https://'+url
			
		r = requests.get(getter)
		content = r.content
		if r.status_code == 404:
			return links
		#print('[-] Harvesting Links from: {0}'.format(url))

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
		#Alternate approach using set
		#clean_links = list(set(links) - set(out_of_scope))

		#print('[*] Links harvested from: {0}'.format(url))
		return clean_links


	def map_links(self,url,clean_links):

		#Store our links in a dict url:[links]
		self.mapped_links[url] = clean_links

		print('[*] Mapped found links to page {0}'.format(url))




	def spider_links(self):
		#Gets a tremendous amount of links starting from the top level 
		#Get links, map links
		clean_links = self.harvest_links(self.domain)
		self.map_links(self.domain,clean_links)
		
		#Form a queue
		self.links = self.links + clean_links
		urls = []
		done = []

		#Get all of the links from top level and all top level relative paths
		for link in self.links:
			if link not in done:
				print('[-] Doing work with link: {0}'.format(link))
				url = self.domain + link
				urls.append(url)
				clean_links = self.harvest_links(url)
				self.map_links(url, clean_links)

				#Merge lists, remove dupes, pop
				self.links = self.links + clean_links
				self.links = list(set(self.links))
				done.append(link)

		#Form an evolving queue to burrow down and get the rest
		keys = list(self.mapped_links.keys())
		for key in keys:
			#Get the nested list so we can look for new pages to scrape
			nested_links = self.mapped_links[key]
			for link in nested_links:
				url = self.domain+link
				#If we already have this URL in our keys its been mapped so skip
				if url in keys:
					pass
				else:
					clean_links = self.harvest_links(url)
					self.map_links(url, clean_links)