import pandas as pd

df_quant = pd.read_csv("data/happy_quant.csv")
df_qual = pd.read_csv("data/happy_qual.csv")
quant_y_range = {"Total_happiness": 130,
                "Height": 115,
                "Weight": 80,
                "Age": 400,
                "Difficulty_score_1": 310,
                "Difficulty_score_2": 310,
                "BMI": 80}


def get_df_qual(value, category):
    df1 = df_qual[value][(df_qual[value] == category)].dropna().reset_index(drop=True)
    df2 = df_qual[value][(df_qual[value] != category)].dropna().reset_index(drop=True)
    cat1 = df1[0]
    cat2 = df2[0]
    x = ["Observed proportions", "Equal proportions"]
    y1 = df1.count()
    y2 = df2.count()
    expected_y = (y1+y2)/2
    return x, y1, y2, expected_y, cat1, cat2


def get_df_quant(value):
    df = df_quant[value].dropna().reset_index(drop=True)
    return df

