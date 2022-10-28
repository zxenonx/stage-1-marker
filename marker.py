#!/usr/bin/python

import csv
import sys
from typing import Any

import requests

def read_csv(file):
    with open(file, 'r') as f:
        reader = csv.reader(f)
        next(f, None)
        urls = []

        for row in reader:
            print("row", row[2] , row[len(row) - 1])
            url = {"username": row[2], "endpoint": row[len(row) - 1]}
            urls.append(url)
        print(urls)
        print(len(urls))    
        return urls

def is_valid(response: dict[str, Any]) -> bool:
    if not isinstance(response["slackUsername"], str) or not isinstance(response["backend"], bool) or not isinstance(response["age"], int) or not isinstance(response["bio"], str):
        return False
    return True

def write_to_csv(urls: list, type: str):
    types = {"passed": "passed-interns.csv", "failed": "failed-interns.csv"}
    with open(types[type], 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["slackUsername"])

        for url in urls:
            writer.writerow([url["username"]])
        file.close()    

def marker(urls: list[dict[str, Any]]) -> None:
    failed = []
    passed = []
    for url in urls:
        try:
            # sending get request and saving the response as response object
            response = requests.get(url=url["endpoint"])
            print(response.status_code)

            if response.status_code != 200:
                failed.append(url)
            else:
                if not is_valid(response.json()):
                    failed.append(url)
                else:
                    passed.append(url)    
                    print(response.json())                
        except Exception:
            failed.append(url)
            print("error")    
    write_to_csv(passed, "passed")
    write_to_csv(failed, "failed")
    print("passed", passed)
    print("failed", failed)

if __name__ == '__main__':
    urls = read_csv(sys.argv[1])
    marker(urls)
