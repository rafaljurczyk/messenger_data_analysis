import os
import json
import pandas as pd

from .parameters import getParam

FILE_PATH = getParam('all_msg_path')
USER = getParam('user')


def get_one_chat(chat_name, chat_path, user: str = USER):
    with open(chat_path, encoding='utf-8', errors='ignore') as json_file:
        conversation = json.load(json_file)
        participants = list(conversation['participants'])
        messages = pd.DataFrame(conversation['messages'])
        messages['chat_with'] = chat_name
        messages['participants_number'] = len(participants)
        messages['date'] = pd.to_datetime(messages['timestamp_ms']*int(1e6), errors='ignore').dt.tz_localize('UTC').dt.tz_convert('Europe/Warsaw').dt.strftime('%Y-%m-%d')
        messages['hour'] = pd.to_datetime(messages['timestamp_ms']*int(1e6), errors='ignore').dt.tz_localize('UTC').dt.tz_convert('Europe/Warsaw').dt.strftime('%H')
        messages['minutes'] = pd.to_datetime(messages['timestamp_ms']*int(1e6), errors='ignore').dt.tz_localize('UTC').dt.tz_convert('Europe/Warsaw').dt.strftime('%M')
        return messages


def create_dataframe(folder_with_messages: str = FILE_PATH):
    dataFrames = []

    for directory in os.listdir(folder_with_messages):
        chat_name = directory.split('_')[0]
        for chat in os.listdir(os.path.join(folder_with_messages, directory)):
            if chat.startswith('message'):
                dataFrames.append(get_one_chat(chat_name, os.path.join(folder_with_messages, directory, chat)))
    print('Merging messages...')
    fullDataFrame = pd.concat(dataFrames, ignore_index=True)
    # print(fullDataFrame)

    return fullDataFrame


def get_messages():
    print('getting all messages...')
    return create_dataframe()