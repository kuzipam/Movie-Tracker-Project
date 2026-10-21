import csv
import os
import pandas as pd
from datetime import datetime, date


#Empty dictionary that will be used for entries.
movie = {}

def movie_entry(sheet,SPREADSHEET_ID,CSV_PATH):
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
              if 1900 <= release_year <= date.today().year+2:
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
      file_empty = not os.path.exists(CSV_PATH) or os.stat(CSV_PATH).st_size == 0
      
      with open(CSV_PATH, 'a', newline = "") as movie_csv:
      
          movie_writer = csv.DictWriter(movie_csv, fieldnames=fields)
      
          if file_empty:
              movie_writer.writeheader()
      
          movie_writer.writerow(movie)
      
      movie_row = [title, date_watched, platform, my_rating, runtime_mins, genre, release_year]

      #Also includes the entry made in the program to sheets
      sheet.values().append(
          spreadsheetId=SPREADSHEET_ID,
          range='MovieWatchlist2026!A:G',
          valueInputOption = 'USER_ENTERED',
          body={'values':[movie_row]}
      ).execute()
      
      print("Successfully added movie to Google Sheets!")
      