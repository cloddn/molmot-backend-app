import csv #csv파일을 다루기 위한 라이브러리를 import 합니다.
import requests
import json
import os


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "molmot_server.settings")
import django
django.setup()

with open('support_2022.csv','r+', encoding='utf-8-sig') as csv_file:
    rows = csv.reader(csv_file, delimiter = ',')
    print(rows)
    for row in rows:
        print(row[0])