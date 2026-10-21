import pandas as pd
from pathlib import Path

file_path= r"C:\Users\IDEAPAD\Desktop\Movie Tracker Project\_01_movie_data_project_2026\movie.csv"

df = pd.read_csv(file_path)
df.index = df.index + 1

# print(df.head(15))
print(df)

