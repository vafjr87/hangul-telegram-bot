#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
import json
import os


def check_users(max=0):
    with open('bot/logs/activity_log.txt', mode='r', encoding='utf-8') as file:
        log_list = []
        for line in file:
            log_list.append(json.loads(line))

    users = []

    if __name__ == '__main__':
        for line in reversed(log_list):
            first = line['message']['chat'].get('first_name')
            last = line['message']['chat'].get('last_name')
            username = line['message']['chat'].get('username')

            user = '{:20}\t{:20}\t{:20}'.format(first if first else '-', last if last else '-',
                username if username else '-')

            if user not in users:
                users.append(user)

            print('Total users:\t {}\n'.format(len(users)))

            print('{:20}\t{:20}\t{:20}'.format('First Name', 'Last Name', 'Username'))

            for user in users:
                print(user)

            print()
    else:
        ids = set()

        for line in reversed(log_list):
            id = line['message']['chat'].get('id')
            first = line['message']['chat'].get('first_name')
            last = line['message']['chat'].get('last_name')
            username = line['message']['chat'].get('username')
            date = datetime.fromtimestamp(line['message'].get('date'))

            user = {'id': id, 'first': first, 'last': last, 'username': username,
            'date': date}

            if id not in ids:
                    users.append(user)
                    ids.add(id)

        if max != 0:
            if max < 0:
                max *= -1

            return (users[:max], len(users))

        return (users, len(users))


def check_directory(directory):
    try:
        os.stat(directory)
    except OSError:
        os.mkdir(directory)


def log_activity(update):
    directory = 'logs'
    check_directory(directory)

    with open(directory + '/activity_log.txt', 'a') as file:
        file.write(update.to_json() + '\n')
    print('log OK. User:', update.message.chat.first_name)


if __name__ == '__main__':
    check_users()
