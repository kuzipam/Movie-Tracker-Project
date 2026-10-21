import pathlib
import sys
import csv
import os
import pandas as pd
import json
from dotenv import load_dotenv
#python -m _01_movie_data_project_2026.movie_data_code

SUBDIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SUBDIR)
SCRIPTS_PATH = os.path.join(PROJECT_ROOT, "_02_scripts")
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

load_dotenv()
credential_filename = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "key.json")
KEY_PATH = os.path.join(PROJECT_ROOT, credential_filename)


from _02_scripts.movie_entry_script import movie_entry
from _02_scripts.data_sync_script import data_sync

#Setting up the connection to google sheets using my json key.
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
creds = service_account.Credentials.from_service_account_file(KEY_PATH, scopes=SCOPES)
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")

CSV_PATH = os.path.join(PROJECT_ROOT, "_01_movie_data_project_2026", "movie.csv")


service = build('sheets', 'v4', credentials=creds)

sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range='MovieWatchlist2026!A:G').execute()
sheet_name ='"MovieWatchlist2026'

#Included menu for the movie tracker.
while True:
    print("------MOVIE TRACKER------")
    print("\n Hello welcome to the Movie Tracker.")
    print("1.Log in a Movie")
    print("2.Update local csv file from google sheets")
    print("3 to x-1 .Work in progress")
    print("x.Exit Program")
    choice = int(input("\nWhat would you like to do today?(Choose between option 1 - x): "))

    if choice == 1:
        movie_entry(sheet, SPREADSHEET_ID,CSV_PATH)
        
    elif choice == 2:
        
        movie_file_load = pd.read_csv(CSV_PATH)
        row_count_local= len(movie_file_load)
        rows = result.get('values', [])
        row_count_cloud = len(rows)-1

        if row_count_local != row_count_cloud:
            print(f"\nYour local cvs file has {row_count_local} entries and the Google Sheet has {row_count_cloud} entries.")
            print("Updating local csv file now.")
            data_sync(rows, row_count_cloud,CSV_PATH)
            print("\nThank you.Exiting Program.")
            break
        else:
            print("\nLocal csv file and Google sheets are both up-to-date with your entries.")
            break

                