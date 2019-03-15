import requests
from bs4 import BeautifulSoup
import time

session = requests.Session()
headers = {
	'Connection': 'keep-alive',
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}
domain = 'https://my.yota.ru'
url_tariff_page = 'https://my.yota.ru/selfcare/devices'
tariffs = {
	'0': 'POS-MA15-0001',
	'300': 'POS-MA15-0002',
	'350': 'POS-MA15-0003',
	'400': 'POS-MA15-0004',
	'450': 'POS-MA15-0005',
	'500': 'POS-MA15-0006',
	'550': 'POS-MA15-0007',
	'600': 'POS-MA15-0008',
	'650': 'POS-MA15-0009',
	'700': 'POS-MA15-0010',
	'750': 'POS-MA15-0011',
	'800': 'POS-MA15-0012',
	'850': 'POS-MA15-0013',
	'900': 'POS-MA15-0014',
	'950': 'POS-MA15-1015',
	'1000': 'POS-MA15-1016'
}


def main(tariff):
	auth_url = get_auth_page()
	time.sleep(1)
	auth(auth_url, 'sahajatomsk@gmail.com', '05may1970')
	time.sleep(1)
	page_tariff = get_tariff_page()
	time.sleep(1)
	change_tariff(page_tariff, tariff)


def get_auth_page():
	url = 'https://my.yota.ru'
	r = requests.get(url, headers=headers)
	soup = BeautifulSoup(r.text, 'html.parser')
	form = soup.find(class_="b-b2c-auth__tab")
	action = form.get('action')

	print('страница авторизации получена')
	return action


def auth(url, login, password):
	auth_data = {
		'IDToken1': '6048860332',
		'IDToken2': password,
		'goto': 'https%3A%2F%2Fmy.yota.ru%3A443%2Fselfcare%2FloginSuccess',
		'gotoOnFail': 'https%3A%2F%2Fmy.yota.ru%3A443%2Fselfcare%2FloginError',
		'org': 'customer',
		'ForceAuth': 'true',
		'login': login, #'sahajatomsk%40gmail.com'
		'password': password
	}
	session.post(url, auth_data, headers=headers)
	print('авторизация прошла успешно')


def get_tariff_page():
	r = session.get(url_tariff_page, headers=headers)
	print('страница с тарифами получена')
	return r.text


def change_tariff(html, tariff):
	soup = BeautifulSoup(html, 'html.parser')
	form = soup.find(class_="tariff-choice-form")
	url_change_tarif = domain + form.get('action')
	tarif_data = {
		'product': form.select('input[name="product"]')[0].get('value'),
		'offerCode': tariff,
		'areOffersAvailable': form.select('input[name="offerCode"]')[0].get('value'),
		'period': form.select('input[name="period"]')[0].get('value'),
		'status': form.select('input[name="status"]')[0].get('value'),
		'autoprolong': form.select('input[name="autoprolong"]')[0].get('value'),
		'isSlot': form.select('input[name="isSlot"]')[0].get('value'),
		'finished': form.select('input[name="finished"]')[0].get('value'),
		'blocked': form.select('input[name="blocked"]')[0].get('value'),
		'freeQuotaActive': form.select('input[name="freeQuotaActive"]')[0].get('value'),
		'pimpaPosition': form.select('input[name="pimpaPosition"]')[0].get('value'),
		'specialOffersExpanded': form.select('input[name="resourceId"]')[0].get('value'),
		'resourceId': form.select('input[name="specialOffersExpanded"]')[0].get('value'),
		'currentDevice': form.select('input[name="currentDevice"]')[0].get('value'),
		'username': '',
		'isDisablingAutoprolong': 'false'
	}

	tarif = session.post(url_change_tarif, tarif_data, headers=headers)
	print('смена тарифа на ' + tariff + ' успешно')