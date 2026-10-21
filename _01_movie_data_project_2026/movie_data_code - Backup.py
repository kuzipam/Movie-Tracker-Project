import csv
import os
from datetime import datetime, date
import pandas as pd

sheet_id = "1q-4ns4Zt1z7uW-Zlo8ARcu6rioBHYggqvDg0EKLtaR0"

#Setting up the connection to google sheets using my json key.
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'key.json'
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
SPREADSHEET_ID = "1q-4ns4Zt1z7uW-Zlo8ARcu6rioBHYggqvDg0EKLtaR0"

service = build('sheets', 'v4', credentials=creds)

sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range='MovieWatchlist2026!A:G').execute()
sheet_name ='"MovieWatchlist2026'

#Function that pulls data from Sheets to update local csv file when an entry is made online lol.
def update_local_csv_file_from_sheets(rows, rows_count_cloud):
            try:
                if not rows:
                    print("No data was found in the Google sheet!")
                    return

                with open("movie.csv", "w", newline = "", encoding="utf-8") as a:
                    movie_writer1 = csv.writer(a)
                    movie_writer1.writerows(rows)
                print(f"\nSuccessfully updated the local csv file:{"movie.csv"} with {row_count_cloud} rows.")

            except Exception as e:
                print(f"An error has occured: {e}")

#Empty dictionary that will be used for entries.
movie = {}

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
        #All the data collected for each movie. Plan to use data analysis tool once learnt.
        #Updated the inputs with validation code to prevent crashes.

        title = input("Please enter the title of the movie you wacthed: \n").strip()

        date_watched_choice = int(input(f"Please select an option to enter the date {title} was watched:\n1.Manually enter date\n2.Auto-fill current date\n"))
        date_watched = int(0)
        if date_watched_choice == 1:
            date_watched = str(input(f"Please enter the date {title} was watched(YYYY-MM-DD and include hypen too): \n"))
        elif date_watched_choice == 2:
            date_watched = str(date.today()).strip()
        else:
            print("Invalid input. Please choose between 1 and 2.\n")
            
        platform = input(f"Please enter the platform you watched {title} on: \n").strip()

        while True:
            try:
                my_rating = int(input(f"Please enter your rating of {title} (1-10): \n")) 
                if 1<= my_rating <= 10:
                    break
                print("Please Enter a number between 1 and 10. \n")
            except ValueError:
                print("Invalid input!")

        while True:
            try:
                runtime_mins = int(input(f"Please enter the runtime of {title} in minutes: \n"))
                if runtime_mins > 0:
                    break
                print("Runtime has to be greater than zero.\n")
            except ValueError:
                print("Runtime has to be a whole number.")

        genre = input("Please enter the genre of the movie: \n").strip()

        while True:
            try:
                release_year = int(input(f"Please enter the release year of {title}: \n"))
                if 1885 <= release_year <= date.today().year+2:
                    break
                print("Invalid release year!")
            except ValueError:
                print("Invalid input!")

        #Filling the dictionary.
        movie = {"title":title, "date_watched": date_watched, "platform":platform, "my_rating":my_rating, "runtime_mins":runtime_mins, "genre": genre, "release_year":release_year}
        print(movie)

        #Used to make the rows in the csv file.
        fields = ["title", "date_watched", "platform", "my_rating", "runtime_mins", "genre", "release_year"]

        #Checked if the csv file was empty and was used to create the rows when the csv file was empty
        file_empty = not os.path.exists("movie.csv") or os.stat("movie.csv").st_size == 0

        with open("movie.csv", 'a', newline = "") as movie_csv:
            
            movie_writer = csv.DictWriter(movie_csv, fieldnames=fields)

            if file_empty:
                movie_writer.writeheader()

            movie_writer.writerow(movie)

        movie_row = [title, date_watched, platform, my_rating, runtime_mins, genre, release_year]

        sheet.values().append(
            spreadsheetId=SPREADSHEET_ID,
            range='MovieWatchlist2026!A:G',
            valueInputOption = 'USER_ENTERED',
            body={'values':[movie_row]}
        ).execute()

        print("Successfully added movie to Google Sheets!")
        
    elif choice == 2:
        movie_file_load = pd.read_csv("movie.csv")
        row_count_local= len(movie_file_load)
        rows = result.get('values', [])
        row_count_cloud = len(rows)-1

        if row_count_local != row_count_cloud:
            print(f"\nYour local cvs file has {row_count_local} entries and the Google Sheet has {row_count_cloud} entries.")
            print("Updating local csv file now.")
            update_local_csv_file_from_sheets(rows, row_count_cloud)
            print("\nThank you.Exiting Program.")
            break
        else:
            print("\nLocal csv file and Google sheets are both up-to-date with your entries.")
            break

                