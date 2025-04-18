# -*- coding: utf-8 -*-
"""
HEALTHCARE ANALYSIS - DATA PREPROCESSING

"""


# Import Libraries

import pandas as pd
import numpy as np

from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import OneHotEncoder

import seaborn as sns
import scipy.stats as stats
import pylab


# Import the data

from sqlalchemy import create_engine
from urllib.parse import quote_plus

# loading the excel file
healthcare_data = pd.read_csv(r"E:\ArborAcademy\Project_HCA\healthcare_dataset.csv")

# Credentials to connect to Database
user = 'navya'  # user name
pw = 'mysql@12'  # password
pw = quote_plus(pw) # to be used in case of error
db = 'arbor'  # database name
engine = create_engine(f"mysql+pymysql://{user}:{pw}@localhost/{db}")

# to_sql() - function to push the dataframe onto a SQL table.
healthcare_data.to_sql('healthcare', con = engine, if_exists = 'replace', chunksize = 1000, index = False)

sql = 'select * from healthcare;'
df = pd.read_sql_query(sql, engine)

# Reading the data
df.head()
df.info()
df.describe()
df.shape


#------ IMPUTATION ------#
# Checking for missing values
df.isna().sum()


#------ TYPECASTING ------#
# Converting date columns to datetime format
df['Date of Admission'] = pd.to_datetime(df['Date of Admission'], dayfirst=True, errors='coerce')
df['Discharge Date'] = pd.to_datetime(df['Discharge Date'], dayfirst=True, errors='coerce')

# Verifying the data types
print(df.dtypes)

# Ensuring proper datetime format for saving or displaying
df['Date of Admission'] = df['Date of Admission'].dt.strftime('%Y-%m-%d')
df['Discharge Date'] = df['Discharge Date'].dt.strftime('%Y-%m-%d')


#------ HANDLING DUPLICATES ------#
# Detecting duplicate rows
duplicate = df.duplicated()
count = 0
for i in duplicate: 
    if i == True:
        count += 1
print("Total duplicate rows are: ", count)

# Duplicates in Columns
df.corr(numeric_only = True)


#------ OUTLIERS TREATMENT ------#
# Detecting Outliers
sns.boxplot(df.Age)
sns.boxplot(df["Billing Amount"])


#------ DISCRETIZATION ------#
df.columns

# Discretizing Age column
df["age_label"] = pd.cut(df["Age"], bins=3, labels=["Young Adult", "Middle Aged", "Old Adult"])

print(df[["Age", "age_label"]].head())


#------ ENCODING ------#
# Perform one-hot encoding on 'Gender'
encoder = OneHotEncoder(drop='first', sparse_output=False)
encoded_gender = encoder.fit_transform(df[['Gender']])

df['gender_encoded'] = encoded_gender.flatten()

print(df[["Gender", "gender_encoded"]].head())


#------ NORMALIZATION ------#
# Noramilzing Billing Amount column
min_max_scaler = MinMaxScaler()
df[["bill_normalized"]] = min_max_scaler.fit_transform(df[["Billing Amount"]])

print(df[["Billing Amount", "bill_normalized"]].head())


#------ Q-Q PLOT ------#
stats.probplot(df["Billing Amount"], dist = "norm", plot = pylab)
stats.probplot(np.log(df["Billing Amount"]), dist = "norm", plot = pylab)
stats.probplot(pow(df["Billing Amount"], 1/2) , dist = "norm", plot = pylab)


# Saving processed data
df.to_sql('healthcare_processed', con = engine, if_exists = 'replace', chunksize = 1000, index = False)

df.to_csv("healthcare_processed.csv", index = False)
print("Processed file saved successfully!")









