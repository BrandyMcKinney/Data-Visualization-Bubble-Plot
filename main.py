import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Standardizes currency to USD values so that we can better compare results
def format_currency(dataset):
  url = "https://api.exchangerate-api.com/v4/latest/USD"

  # Requests data from API
  response = requests.get(url)
  data = response.json()

  def convert_currency(row):
    rate = data["rates"][row["Unit Code"]]
    return row["Value"] / rate

  #row of data in dataset
  for index, row in dataset.iterrows():
    dataset.at[index, "Unit Code"] = "USD"
    dataset.at[index, "Value"] = convert_currency(row)
  return dataset


# ADD CODE: Pandas dataframes

wage = pd.read_csv("wage.csv", delimiter=",")
happiness = pd.read_csv("happiness.csv", delimiter=",")

wage_usd = format_currency(wage)
wage_and_happiness = wage.merge(happiness)

wage_and_happiness_by_country = wage_and_happiness.groupby("Country")
# print(wage_and_happiness_by_country)
wage_average_per_country = wage_and_happiness_by_country["Value"].mean()
# print(wage_average_per_country)
happiness_average_per_country = wage_and_happiness_by_country[
  "Happiness score"].mean()

fig = sns.scatterplot(x="Value",
                      y="Happiness score",
                      hue="Happiness score",
                      size="Happiness score",
                      sizes=(20, 180),
                      data=wage_and_happiness)

plt.title("Annual Salary and Happiness")
plt.xlabel("Annual Salary of Full-Time Workers (USD)")
plt.ylabel("Happiness Scores of Citizens")
fig.set_facecolor("#E5E5E5")
plt.savefig("salary_happiness2.png")
# print("Countries With the Highest Average wages are:", wage_average_per_country.nlargest(10))
# print("Countries With the Lowest Average wages are:", wage_average_per_country.nsmallest(10))
# print("Countries With the Highest Happiness Scores are:", happiness_average_per_country.nlargest(10))
# print("Countries With the Lowest Happiness Scores are:", happiness_average_per_country.nsmallest(10))
