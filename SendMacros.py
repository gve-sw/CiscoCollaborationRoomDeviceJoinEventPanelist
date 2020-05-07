"""
Copyright (c) 2020 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

import requests
import base64
import csv
from multiprocessing.pool import ThreadPool
import datetime

#CSV file which contains the IP addresses of all TP codecs
filename = 'TP_List.csv'

#log path. configure complete path along with filename

Logfile = "TP_codec_config_update_report.txt"
with open(Logfile, "a+") as text_file:
    text_file.write('\n' + datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p") + '\n')
    text_file.write("==========================" + '\n')

rows = []

try:
    with open(filename, 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)

        # extracting field names through first row
        fields = next(csvreader)  # python3

        # extracting each data row one by one
        for row in csvreader:
            rows.append(row)

        # get total number of rows
        print("Total no. of rows: %d" % (csvreader.line_num))
        lines = int(csvreader.line_num)
except FileNotFoundError:
    print(filename + " Input file not found in current directory")



fieldindex = fields.index('IP Address')
codecIPs = []

for row in rows:
    codecIPs.append(row[fieldindex])

print("codecIPs are {}".format(codecIPs))

username,password=input("Username: "), input("Password: ")

xml_file = 'macros-enable.xml'
xml_file_2 = 'macros-joinevent.xml'

# This function is where the magic happens. I am using request to open the xml file and then posting the content
# to the url of each TP endpoint based on the IP address obtained from the CSV file
# NB that http needs to be enabled on the TP endpoint otherwise you will get a 302 error.
def do_upload(ip):

        try:
            payload=open(xml_file, "r").read()
            url = "http://{}/putxml".format(ip)
            userpass = username + ':' + password
            encoded_u = base64.b64encode(userpass.encode()).decode()
            headers = {
                'Content-Type': 'text/xml',
                'Authorization': 'Basic '+encoded_u,
                'Content-Type': 'text/plain'
            }
            print('-'*40)
            print('Enabling Macros on {}'.format(ip))
            response = requests.request("POST", url, headers=headers, data=payload, verify=False)
            print(response.text)

            with open(Logfile, "a+") as text_file:
                text_file.write("The Status of Macros enabling on codec IP {} |---->>>".format(ip) + '\n')
                text_file.write(response.text)

            payload2=open(xml_file_2, "r").read()
            print('-' * 40)
            print('Configuring In-Room Control and Macros on {}'.format(ip))

            response = requests.request("POST", url, headers=headers, data=payload2, verify=False)
            print(response.text)
            with open(Logfile, "a+") as text_file:
                text_file.write("The Status of In-Room Control and Macros Config on codec {} |---->>".format(ip) + '\n')
                text_file.write(response.text)


        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
            text_file.write('Http error talking to {} : {}'.format(ip, errh))
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
            text_file.write('failed to connect to {} : {}'.format(ip, errc))
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
            text_file.write('timeout connecting to {} : {}'.format(ip, errt))
        except requests.exceptions.RequestException as err:
            print("Other Error: ", err)
            text_file.write('Other error trying to send to {} : {}'.format(ip, err))



def main():
    ''' This Section uses multi-threading to send config to ten TP endpoint at a time'''
    pool = ThreadPool(10)
    results = pool.map(do_upload, codecIPs)
    pool.close()
    pool.join()
    return results

main()