import os
import json
import logging
import pathlib
from pprint import pprint

from notion_client import Client
from notion_client import APIErrorCode, APIResponseError

database_id = ""
csv_file_name = ""
tags = [""]

auth_json_f = open('notion_auth.json')
auth_json = json.load(auth_json_f)

notion = Client(auth=auth_json['secret'])

def export_to_csv(query_result):
    current_path = pathlib.Path(__file__).parent.resolve()
    f = open(str(current_path) + "/" + "".join(csv_file_name) + ".csv", "w")

    for result in query_result['results']:
        title_name = result['properties']['Title']['title'][0]['plain_text'].lstrip().rstrip()
        artist_name = result['properties']['Artist']['rich_text'][0]['plain_text'].lstrip().rstrip()

        #print(title_name + "," + artist_name)
        f.write(title_name + "," + artist_name + "\n")

def filter_generator(tags_string):
    and_list = []
    for tag in tags_string:
        and_list.append(
        {
            "property": "Tags",
            "multi_select": 
            {
                "contains": tag
            }
        })
    return and_list

def query_database(tags):
    try:
        my_page = notion.databases.query(
            **{
                "database_id": database_id,
                "filter": {
                    "and": filter_generator(tags)
                }
            }
        )

        return my_page
    except APIResponseError as error:
        if error.code == APIErrorCode.ObjectNotFound:
            ...  # For example: handle by asking the user to select a different database
        else:
            # Other error handling code
            logging.error(error)

query_result = query_database(tags)
export_to_csv(query_result)