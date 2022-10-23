import os
import json
import logging
import pathlib
from pprint import pprint

from notion_client import Client
from notion_client import APIErrorCode, APIResponseError

# Database must be shared with the integration
# https://developers.notion.com/docs/getting-started

database_id = ""
csv_name = "New in apir"

auth_json_f = open('notion_auth.json')
auth_json = json.load(auth_json_f)

notion = Client(auth=auth_json['secret'])

def import_from_csv():
    current_path = pathlib.Path(__file__).parent.resolve()
    f = open(str(current_path) + "/" + "".join(csv_name) + ".csv", "r")

    for line in f.readlines():
        line = line.replace("\n", "")
        comma_index = line.rindex(",")
        song_name = line[:comma_index].strip()
        artist_name = line[comma_index+1:].strip()
        

        new_page_props = {
            'Title': {'title': [{'text': {'content': f"{song_name}"}}]},
            'Artist': {'rich_text': [{'text': {'content': f"{artist_name}"}}]},
        }

        notion_page = notion.pages.create(
            parent={ 'database_id': database_id },
            properties=new_page_props
        )

        if notion_page['object'] == 'error':
            print("ERROR", notion_page['message'])
            print (song_name + " " + artist_name)
            continue

import_from_csv()