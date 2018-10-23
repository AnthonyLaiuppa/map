from __future__ import absolute_import, unicode_literals
from MapSnatch import MapSnatchLogic
import click

@click.command()
@click.option('--domain', default=None, help='Domain to perform reconaissance on.')
@click.option('--substatus', default=False, help='Enable to pull all status codes of sub domain pages.', type=bool)
@click.option('--mapsubs', default=False, help='Enable to pull all URLs found on sub domain pages.', type=bool)
def start_mapping(domain, mapsubs, substatus):
	"""
		Lightweight recon program. Used to assess status of a (sub)domain and map all URLs.
	    This will help identify targets and points of interest.
	"""
	print('[*] Starting with domain - {0}'.format(domain))
	msl = MapSnatchLogic(domain)

	if substatus:
		msl.get_subs()
		msl.get_statuses()

	msl.spider_links()





