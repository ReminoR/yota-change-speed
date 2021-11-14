
"""
TODO
Реализовать вызов справки
Реализовать получение статуса
Реализовать получение актуальных тарифов
Реализовать max speed, min speed
Реализовать выбор тарифов
Реализовать ошибки и обработку исключений
(нет подключения, не получил страницу, не авторизовался, не изменил скорость и т.д.)
Парсинг аргументов командной строки
Дописать получение логина и пароля из файла .env
Дописать функцию создания файла с логином и паролем
"""
import json
import requests
import time


def make_headers(auth=False):
    headers = {
        'Accept': 'application/json',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) \
                    Chrome/87.0.4280.66 Safari/537.36',
    }
    if auth:
        headers['authorization'] = 'Basic bmV3X2xrX3Jlc3Q6cGFzc3dvcmQ='
    return headers


# Получаем execution
def access_token():
    url = 'https://id.yota.ru/sso/oauth2/access_token?skipAutoLogin=true'
    data = {
        'client_id': 'yota_mya',
        'client_secret': 'password',
        'realm': '/customer',
        'service': 'dispatcher',
        'grant_type': 'urn:roox:params:oauth:grant-type:m2m',
        'response_type': 'token cookie'
    }

    s = session.post(url, data, headers=make_headers())

    if s.ok:
        print('Execution получен успешно:', s.status_code)
        return s.json()['execution']
    else:
        print('Execution. Ошибка получения.', s.text)


def auth(username, password, execution):
    url = 'https://id.yota.ru/sso/oauth2/access_token?skipAutoLogin=true'
    auth_data = {
        'execution': execution,
        'username': username,
        'password': password,
        '_eventId': 'next',
        'response_type': 'token cookie',
        'client_id': 'yota_mya',
        'client_secret': 'password',
        'service': 'dispatcher',
        'grant_type': 'urn:roox:params:oauth:grant-type:m2m',
        'realm': '/customer',
    }

    s = session.post(url, auth_data, headers=make_headers())

    if s.ok:
        print('Авторизация прошла успешно:', s.status_code, s.text)
        # print('auth ' + json.dumps(s.json(), indent=4, sort_keys=True))
        return s.json()['access_token'], s.json()['refresh_token']
    else:
        print('Ошибка авторизации', s.text)


# def get_token_info():
#     url = 'https://my.yota.ru/wa/v1/auth/tokenInfo'
#     s = session.post(url, headers=make_headers(auth=True))
#     if s.ok:
#         print('Информация о токене:', s.text)
#         print(s.json()['at'])
#         return s.json()['at']
#     else:
#         print('Ошибка получения информации о токене', s.status_code, s.text)


def statusLegal():
    url = 'https://my.yota.ru/wa/v1/profile/statusLegal'
    s = session.get(url, headers=make_headers(auth=True))
    if s.ok:
        print('Статус пользователя легален:', s.text)
    else:
        print('Ошибка получения статуса пользователя', s.status_code, s.text)


# def setTokenInCookie(token):
#     url = 'https://my.yota.ru/wa/v1/auth/setTokenInCookie'
#     data = {'token': token}
#     s = session.post(url, data, headers=make_headers(auth=True))
#     if s.ok:
#         print('Установка токена в Cookie прошла успешно', s.text)
#     else:
#         print('Ошибка установки токена в Cookie', s.status_code, s.text)


def get_config():
    url = 'https://my.yota.ru/data/config.json'
    data = {
        'v': round(time.time() * 1000)
    }
    s = session.get(url, data, headers=make_headers(auth=True))
    if s.ok:
        print('Время успешно установлено')
    else:
        print('Ошибка установки времени', s.status_code, s.text)


def get_info():
    url = 'https://my.yota.ru/wa/v1/profile/info'
    s = session.get(url, headers=make_headers(auth=True))

    if s.ok:
        print('\r\nИнформация пользователя:',
              '\r\nuserId:', s.json()['userId'],
              '\r\nstatus:', s.json()['status'],
              '\r\nphone:', s.json()['phone'],
              '\r\nemail:', s.json()['email'])
    else:
        print('Ошибка получения информации пользователя')

    url = 'https://my.yota.ru/wa/v1/devices/devices'
    s = session.get(url, headers=make_headers(auth=True))
    print('\r\nИнформация о тарифе: ') if s.ok else print('Ошибка получения списка тарифов')
    print('Тариф: ', s.json()['devices'][0]['slider']['currentProduct']['speed'] + ' ' + s.json()['devices'][0]['slider']['currentProduct']['speedType'])
    print('Стоимость текущего тарифа: ', str(s.json()['devices'][0]['product']['price']['amount']) + ' ' + s.json()['devices'][0]['product']['price']['currencyCode'])
    print('Оставшийся период: ', s.json()['devices'][0]['slider']['currentProduct']['remain'])
    print('Текущий регион: ', s.json()['currentRegion'])
    productCode = s.json()['devices'][0]['product']['productOfferingCode']
    currentTariffId = s.json()['devices'][0]['product']['productId']
    print('ID текущего тарифа', currentTariffId)

    return currentTariffId


def get_tariffs():
    url = 'https://my.yota.ru/wa/v1/devices/devices'
    s = session.get(url, headers=make_headers(auth=True))

    if s.ok:
        print('Список тарифов')
        tariffs = s.json()['devices'][0]['slider']['steps']
        for tariff in tariffs:
            print(tariff['code'], tariff['remain'], tariff['speed'])
        # print('get_tariffs ' + json.dumps(s.json(), indent=4, sort_keys=True))
    else:
        print('Ошибка получения списка тарифов', s.text)


def change_tariff(currentTariffId, desired_tariff, at, reft):
    url = 'https://my.yota.ru/wa/v1/devices/changeOffer/change'

    tariff_data = {
        "currentProductId": currentTariffId,
        "offerCode": desired_tariff,
        "disablingAutoprolong": 'false',
        "resourceID": {"key": "0103073473", "type": "ICCID"}
    }

    headers = {
        # 'authority': 'my.yota.ru',
        # 'method': 'POST',
        # 'path': '/wa/v1/devices/changeOffer/change',
        # 'scheme': 'https',
        # 'accept': 'application/json, text/plain, */*',
        # 'accept-encoding': 'gzip, deflate, br',
        # 'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'authorization': 'Basic bmV3X2xrX3Jlc3Q6cGFzc3dvcmQ=',
        # 'content-length': '136',
        'content-type': 'application/json',
        # 'cookie': ('at=' + at + '; ' + 'reft=' + reft + '; '
        # 'YOTA_REGION_CODE=O_71;username=sahajatomsk%40gmail.com;'
        # 'authLevel=2;userId=6048860332;'),
        # # rt=40a79051-cc89-4797-991a-cc5048b5bbe9;
        # 'origin': 'https://my.yota.ru',
        # 'referer': 'https://my.yota.ru/devices',
        # 'sec-fetch-dest': 'empty',
        # 'sec-fetch-mode': 'cors',
        # 'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
        # x-transactionid: 3c6c066a-bbe2-48f6-bd19-811a24e234c7
    }

    cookies = {
        'at':at,
        'reft': reft,
        'YOTA_REGION_CODE': 'O_71',
        'username': 'sahajatomsk%40gmail.com',
        'authLevel': '2',
        'userId': '6048860332'
    }

    print(headers)

    s = session.post(url,
                     tariff_data,
                     headers=headers, cookies=cookies)

    print('\r\nЖелаемый тариф:', desired_tariff, 'ID установленного тарифа:', currentTariffId)
    if s.ok:
        print('Тариф успешно изменен на ', desired_tariff) 
    else:
        print('Ошибка изменения тарифа:', s.status_code, s.text)
        # print(s.headers)
        print(s.reason)


def get_balance():
    url = 'https://my.yota.ru/wa/v1/finance/getBalance'
    s = session.get(url, headers=make_headers(auth=True))
    print('Баланс:', s.json()['amount'], s.json()['currencyCode']) if s.ok else print('Ошибка получения баланса')


with requests.Session() as session:
    at, reft = auth('sahajatomsk@gmail.com', '05may1970', access_token())
    # get_token_info()
    # statusLegal()
    # setTokenInCookie(get_token_info())
    # get_config()
    # get_balance()
    # get_tariffs()
    currentTariffId = get_info()
    # time.sleep(3)
    # statusLegal()
    change_tariff(currentTariffId, 'POS-MA15-0010', at, reft)
