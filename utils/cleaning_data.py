from ..database.database import df_for_clean, engine_1

df = df_for_clean


def clean_data():
    global df
    # Analyzing the columns in oder to determine if is important to delete the rows with missing values
    df = df.dropna(subset=["industry","city","gender","race","job_title","education_level"])

    # annual_salary has values that has a different format, in this case deleting the ","
    df.loc[:, "annual_salary"] = df["annual_salary"].str.replace(",","")

    # As the DataBase is taking into account only information from works, the annual_salary couldn´t be less than 1000 dolars a year, so deleting the rows that has this values on annual_salary
    df = df[~df["annual_salary"].isin(["0","00","1","100"])]

    # Deleting the spaces at the end of all the columns from the DataFrame
    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

    # Converting the column annual_salary into float
    df.loc[:,"annual_salary"] = df["annual_salary"].astype("float")

    # Converting all the column country to lowercase
    df["country"] = df["country"].str.lower()

    # Checking the column country from the DataFrame and converting the different forms the people from the survey answer into unique format
    df["country"] = df["country"].replace({"usa": "united states", "us": "united states", "u.s.": "united states","united states of america": "united states", "u.s.a.": "united states","u.s": "united states","america": "united states", "united state": "united states", "unites states": "united states", "united stated": "united states", "u.s.a": "united states", "u. s.": "united states", "united sates": "united states", "the united states": "united states", "united state of america": "united states", "🇺🇸": "united states", " unitedstates": "united states"})
    df["country"] = df["country"].replace({"uk": "united kingdom","england": "united kingdom","u.k.":"united kingdom", "england, uk": "united kingdom", "wales": "united kingdom", "scotland": "united kingdom", "england, united kingdom": "united kingdom"})
    df["country"] = df["country"].replace({"the netherlands": "netherlands"})
    df["country"] = df["country"].replace({"nz": "new zealand"})

    # Deleting any row that has less than 5 equal names, after checking the main rows from the DF
    value_count_country = df["country"].value_counts()
    no_values_country = value_count_country[value_count_country >= 5].index
    df = df[df["country"].isin(no_values_country)]

    # Converting all the column city to lowercase
    df.loc[:,"city"] = df["city"].str.lower()

    # Checking the column city from the DataFrame and converting the different forms the people from the survey answer into unique format
    df.loc[:,"city"] = df["city"].replace({"new york city": "new york", "nyc": "new york"})
    df.loc[:,"city"] = df["city"].replace({"washington, dc": "washington", "washington dc": "washington", "dc": "washington"})

    # Deleting any row that has less than 5 equal names, after checking the main rows from the DF
    value_count_city = df["city"].value_counts()
    no_values_city = value_count_city[value_count_city >= 5].index
    df = df[df["city"].isin(no_values_city)]

    # Converting the df_final_state into df_final, that is going to be the last df.
    df_final = df

    # Creating a column in order to have a count for each row, as an id
    df_final = df_final.assign(id=range(1, len(df_final) + 1))

    # uploading the clean DataFrame into the instance SQL transforming it into a sql document.
    df_final.to_sql("final_data_andres", con=engine_1, if_exists="replace")

