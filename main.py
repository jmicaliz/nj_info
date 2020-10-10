import csv
import os
import sys
import datetime

import requests
from dotenv import load_dotenv

# Loads from a .env file
load_dotenv()

DISTANCE_API_KEY = os.getenv("DISTANCE_API_KEY")
if (not DISTANCE_API_KEY) or (DISTANCE_API_KEY) == "":
  raise ValueError("Missing DISTANCE_API_KEY")
  
DISTANCE_URL = os.getenv("DISTANCE_URL", "https://maps.googleapis.com/maps/api/distancematrix/json")
NJ_CSV_INPUT = os.getenv("NJ_CSV_INPUT", "nj_list.csv")
NJ_CSV_OUTPUT = os.getenv("NJ_CSV_OUTPUT", "nj_list.csv")


def _read_csv(input_csv):
  csv_dict_list = []

  with open(input_csv, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      csv_dict_list.append(row)

  return csv_dict_list

def _write_csv(csv_dict_list, output_csv):

  with open(output_csv, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=list(csv_dict_list[0].keys()))
    writer.writeheader()
    for row in csv_dict_list:
      writer.writerow(row)

def get_travel_time(origin, url, api_key):
  payload = {
    "origins": f"{origin}+NJ",
    "destinations": "Penn+Station+NY",
    "mode": "transit",
    "arrival_time": int(datetime.datetime(2020, 10, 30, 13, 30, tzinfo=datetime.timezone.utc).timestamp()),
    "key": api_key
  }
  print(f"Getting info for: {origin}")
  r = requests.get(url, params=payload)
  result_obj = r.json()['rows'][0]['elements'][0]

  if result_obj['status'] == 'ZERO_RESULTS':
    return 'No Results'

  return result_obj['duration']['text']

def fill_travel():
  csv_dict_list = _read_csv(NJ_CSV_INPUT)
  for i in range(len(csv_dict_list)):
    csv_dict_list[i]['travel_time'] = get_travel_time(csv_dict_list[i]['Municipality'], DISTANCE_URL, DISTANCE_API_KEY)

  _write_csv(csv_dict_list, NJ_CSV_OUTPUT)


if __name__ == "__main__":
  fill_travel()
