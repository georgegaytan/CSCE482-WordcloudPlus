from lxml import html
import requests

def get_data(site_address):
	page = requests.get(site_address)
	return page.content