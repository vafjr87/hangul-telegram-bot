#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pickle
import requests

class Naver(object):
    def __init__(self):
        self.url = {
            'translate': 'https://openapi.naver.com/v1/language/translate',
            'encyc':     'https://openapi.naver.com/v1/search/encyc',
            'voice':     'https://openapi.naver.com/v1/voice/tts.bin'
        }

    def translate(self, source, target, text):
        """Translation using Naver API"""
        if text == '':
            return ''

        with open('token', 'rb') as token:
            token = pickle.load(token)

        params = {
            'source': source,
            'target': target,
            'text': text
        }

        response = requests.post(
            self.url.get('translate'),
            data = params,
            headers = token.get('naver'))

        
        if response.status_code == requests.codes.ok:
            data = response.json()
            return data.get('message').get('result').get('translatedText')
        else:
            data = response.json()
            print(f'Status code: {response.status_code}')
            print(f'Message: {data["errorMessage"]}')
            print(f'API code: {data["errorCode"]}')
            return ''

if __name__ == '__main__':
    naver = Naver()
    print(naver.translate('ko', 'en', '나는 친구를 없어요'))
