from __future__ import absolute_import, unicode_literals
from MapSnatch import MapSnatchLogic
import click

@click.command()
@click.option('--domain', default=None, help='Domain to perform reconaissance on.')
@click.option('--mapsubs', default=False, help='Enable to pull all URLs on sub domain pages')
def start_mapping(domain, mapsubs):
	"""Lightweight recon program. Used to assess status of a (sub)domain and snatch all URLs."""
	print('[*] Starting with domain - {0}'.format(domain))
	start = MapSnatchLogic(domain, mapsubs)
	start.get_subs()
	start.get_statuses()
	start.harvest_links(domain)
