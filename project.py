import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("IMDB Dataset.csv")

if df['Runtime'].dtype == 'object':
    df['Runtime'] = df['Runtime'].str.replace(' min', '', regex=False).astype(float)

votes_col = 'No_of_Votes' if 'No_of_Votes' in df.columns else 'Votes'
if votes_col in df.columns and df[votes_col].dtype == 'object':
    df[votes_col] = df[votes_col].str.replace(',', '', regex=False).astype(float)

print(df.head(3))
print(df.tail(3))

df.info()

print(df.isnull().sum())
print(df.isnull().values.any())

subset_df = df.iloc[41:76]
print(subset_df)

max_votes_idx = df[votes_col].idxmax()
print(df.loc[max_votes_idx])

plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
sns.boxplot(y=df['IMDB_Rating'])
plt.title('IMDB_Rating')
plt.subplot(1, 2, 2)
sns.boxplot(y=df['Runtime'])
plt.title('Runtime')
plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 5))
plt.scatter(df['Runtime'], df['IMDB_Rating'])
plt.xlabel('Runtime')
plt.ylabel('IMDB_Rating')
plt.title('Runtime vs IMDB_Rating')
plt.show()

plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
sns.histplot(df['IMDB_Rating'], kde=True)
plt.title('Distribution of IMDB_Rating')
plt.subplot(1, 2, 2)
sns.histplot(df['Runtime'].dropna(), kde=True)
plt.title('Distribution of Runtime')
plt.tight_layout()
plt.show()

rating_col = 'Certificate' if 'Certificate' in df.columns else 'Rating' if 'Rating' in df.columns else 'IMDB_Rating'
plt.figure(figsize=(10, 5))
sns.countplot(data=df, x=rating_col)
plt.xticks(rotation=45)
plt.show()