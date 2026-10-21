import marimo

__generated_with = "0.24.2"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    from pathlib import Path
    import numpy as np

    file_path = r"C:\Users\IDEAPAD\Desktop\Movie Tracker Project\_01_movie_data_project_2026\movie.csv"
                                                                                                                        
    df = pd.read_csv(file_path)

    mo.ui.table(df)
    return (df,)


@app.cell
def _(df):
    df["release_year"].describe()
    return


@app.cell
def _(df):
    df["my_rating"].describe()
    return


if __name__ == "__main__":
    app.run()
