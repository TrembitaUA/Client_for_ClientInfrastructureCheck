#!/usr/bin/python3
import argparse
from datetime import datetime

from XRoad import XClient


class Check(XClient):
    def __init__(self, ss, **kwargs):
        if not kwargs.get('service'):
            if 'SEVDEIR-TEST/' in kwargs.get('client'):
                s = {
                    'service': '/'.join((
                        'SEVDEIR-TEST',
                        'GOV',
                        '11110014',
                        'SUB_prod',
                        'ClientInfrastructureCheck'
                    ))
                }
            else:
                s = {
                    'service': '/'.join((
                        'SEVDEIR',
                        'GOV',
                        '11110015',
                        'TestSub15',
                        'ClientInfrastructureCheck'
                    ))
                }
            kwargs.update(s)
        super().__init__(ss, **kwargs)


def check(ss, client, service=None):
    print('Утиліта перевірки доступності вузлів трембіти')
    print("")
    print('Починаємо перевірку......')
    print('Ваш локальний ШБО.................:', ss)
    print('Ваша підсистема.........:', client)

    c = Check(ss, client=client, service=service)
    body = c.request(DateTimeSend=datetime.now()).get('body' or {})
    try:
        response = body.get('ClientInfrastructureCheckResult' or {})
    except Exception as err:
        print(err)
    else:
        GeneratedTime = response.get('GeneratedTime')
        ReceivedTime = response.get('ReceivedTime')
        print("")
        print('Все пройшло добре!')
        print("")
        print('Відправили запит.........:', ReceivedTime)
        print('Сервіс відпрацював запит.:', GeneratedTime)
        print('Отримали відповідь.......:', datetime.now())
        print('')
        print('Час на все...............:', datetime.now() - ReceivedTime)
        print()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Утиліта перевірки доступності вузлів трембіти',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        'host', metavar='SECURITY_SERVER',
        help='URL вашого локального ШБО')
    parser.add_argument(
        '--client', '-c', metavar='URL_CLIENT',
        help='Адреса вашої підсистеми ')
    parser.add_argument(
        '--service', '-s', metavar='URL_SERVISE',
        help='не обовьязково, адреса сервісу ClientInfrastructureCheck')
    args = parser.parse_args()

    if not args.client:
        parser.print_help()
        exit(1)

    check(args.host, args.client, args.service)
