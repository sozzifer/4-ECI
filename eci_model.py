import numpy as np
import pandas as pd
import scipy.stats as stat
import statsmodels.stats.proportion as statmod

# Generate dataframes for quantitative and qualitative datasets from csv
df_quant = pd.read_csv("data/happy_quant.csv")
df_qual = pd.read_csv("data/happy_qual.csv")

# y-axis ranges for different quantitative variables
quant_y_range = {"Total_happiness": 130,
                "Height": 115,
                "Weight": 80,
                "Age": 400,
                "Difficulty_score_1": 310,
                "Difficulty_score_2": 310,
                "BMI": 80}


# Filter quantitative dataframe based on user's dropdown selection
# Returns filtered dataframe, mean and confidence interval for user-entered confidence level
def get_df_quant(value, conf_level):
    df = df_quant[value].dropna().reset_index(drop=True)
    mean = np.mean(df)
    sem = stat.sem(df)
    conf_int = stat.norm.interval(confidence=conf_level,
                                  loc=mean,
                                  scale=sem)
    return df, mean, conf_int


# Filter qualitative dataframe based on user's dropdown and category radio button selection
# Returns x/y data for bar chart creation and confidence interval for user-entered confidence level
def get_df_qual(value, conf_level, category):
    df1 = df_qual[value][(df_qual[value] == category)].dropna().reset_index(drop=True)
    df2 = df_qual[value][(df_qual[value] != category)].dropna().reset_index(drop=True)
    cat1 = df1[0]
    cat2 = df2[0]
    x = ["Observed proportions", "Equal proportions"]
    y1 = df1.count()
    y2 = df2.count()
    expected_y = (y1+y2)/2
    y1_values = [y1, expected_y]
    y2_values = [y2, expected_y]
    conf_int = statmod.proportion_confint(y1, y1+y2, 1-conf_level, "normal")
    return x, y1, y2, y1_values, y2_values, cat1, cat2, conf_int
