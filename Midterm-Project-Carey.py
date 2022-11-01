#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 22 16:48:49 2022

@author: brettcarey
"""

import json
import urllib.request
import urllib.error
import pandas
import csv
import sqlite3

API_key = "1c7484c74099"
domain = "http://api.joshuaproject.net"
#search_params = input("Parameters: ")
url = domain+"/v1/countries.json?api_key="+API_key+"&continents=AFR"
output_type = input("Output file type: ")
# exception handling structure (credit to https://api.joshuaproject.net/getting_started)
try:
    # request the API
    request = urllib.request.urlopen(url)
except urllib.error.HTTPError as e:
    print('The server couldn\'t fulfill the request.')
    print('Error code: ', e.code)
    exit
except urllib.error.URLError as e:
    print('We failed to reach a server.')
    print('Reason: ', e.reason)
    exit
else:
    # Everything worked
    # decode the response
    response = request.read().decode("utf8")
    # load the JSON
    jsondata = json.loads(response)
    # modify columns
    for data in jsondata:
        # add a new column
        data["PercentNotChristianity"]=str(100-data["PercentChristianity"])
        # delete columns with missing data
        del data["RLG4Primary"]
        del data["ROL3SecondaryLanguage"]
        del data["AreaSquareMiles"]
        del data["ReligionDataYear"]
        del data["LiteracyRate"]
        del data["LiteracySource"]
        del data["HDIYear"]
        del data["HDIValue"]
        del data["HDIRank"]
        del data["StateDeptReligiousFreedom"]
        del data["UNMap"]
        del data["PrayercastVideo"]
        del data["WINCountryProfile"]
        del data["CntPeoplesLR"]
    # convert API response to dataframe
    df = pandas.json_normalize(jsondata)
    # give a summary of the data
    print("There are", str(df.shape[0]), "rows and",str(len(df.columns)),
          "columns in this data")
    # create csv file
    if output_type == "csv":
        data_file = open('african_countries.csv', 'w', newline='')
        csv_writer = csv.writer(data_file)
        count = 0
        for data in jsondata:
            # create csv header out of json keys
            if count == 0:
                header = data.keys()
                csv_writer.writerow(header)
                count += 1
            # write the data contained in the values
            csv_writer.writerow(data.values())
        data_file.close()
    # create sql database file
    elif output_type == "sql":
        # establish sql connection
        conn = sqlite3.connect('african_countries.db')
        # convert dataframe to sql table in database
        pandas.DataFrame.to_sql(df, name='african_countries', 
                                if_exists='replace', con=conn)
    # if user fails to give the correct input, tell them their options
    else:
        print("Invalid output type. Valid types are csv or sql.")
        

