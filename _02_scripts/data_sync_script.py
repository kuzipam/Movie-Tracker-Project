import csv
import os
import pandas as pd


#Function that pulls data from Sheets to update local csv file when an entry is made online lol.
def data_sync(rows, rows_count_cloud, CSV_PATH):
    try:
        if not rows:
            print("No data was found in the Google sheet!")
            return

        with open(CSV_PATH, "w", newline = "", encoding="utf-8") as a:
            movie_writer1 = csv.writer(a)
            movie_writer1.writerows(rows)
            print(f"\nSuccessfully updated the local csv file:{CSV_PATH} with {rows_count_cloud} rows.")

    except Exception as e:
        print(f"An error has occured: {e}")
