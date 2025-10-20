# %%
import pandas as pd
import matplotlib.pyplot as plt
import polars as pl

# %%
# Reading data from a csv file
# You can read data from a CSV file using the `read_csv` function. By default, it assumes that the fields are comma-separated.

# We're going to be looking at some cyclist data from Montréal. Here's the [original page](http://donnees.ville.montreal.qc.ca/dataset/velos-comptage) (in French), but it's already included in this repository. We're using the data from 2012.

# This dataset is a list of how many people were on 7 different bike paths in Montreal, each day.

broken_df = pd.read_csv("../data/bikes.csv", encoding="ISO-8859-1")

# TODO: please load the data with the Polars library (do not forget to import Polars at the top of the script) and call it pl_broken_df
pl_broken_df = pl.read_csv("../data/bikes.csv", encoding="ISO-8859-1")
# %%
# Look at the first 3 rows
print( "Pandas Data Frame first 3 rows:")
print(broken_df[:3])

# TODO: do the same with your polars data frame, pl_broken_df
print( "Polars Data Frame first 3 rows:")
pl_broken_df.slice(0,3)
# %%
# You'll notice that this is totally broken! `read_csv` has a bunch of options that will let us fix that, though. Here we'll

# * change the column separator to a `;`
# * Set the encoding to `'latin1'` (the default is `'utf8'`)
# * Parse the dates in the 'Date' column
# * Tell it that our dates have the day first instead of the month first
# * Set the index to be the 'Date' column

fixed_df = pd.read_csv(
    "../data/bikes.csv",
    sep=";",
    encoding="latin1",
    parse_dates=["Date"],
    dayfirst=True,
    index_col="Date",
)
fixed_df[:3]

# TODO: do the same (or similar) with polars
pl_fixed_df = pl.read_csv(
    "../data/bikes.csv",
    separator=";", 
    encoding="latin1")
pl_fixed_df = pl_fixed_df.with_columns(pl.col("Date").str.to_date("%d/%m/%Y")) # Parsing dates with day first formatted by converting the string to date
pl_fixed_df.slice(0,3) # Displaying first 3 rows

# %%
# Selecting a column
# When you read a CSV, you get a kind of object called a `DataFrame`, which is made up of rows and columns. You get columns out of a DataFrame the same way you get elements out of a dictionary.

# Here's an example:
fixed_df["Berri 1"]

# TODO: how would you do this with a Polars data frame?
pl_fixed_df.select("Berri 1")

# %%
# Plotting is quite easy in Pandas
print("Plotting with Pandas:")
fixed_df["Berri 1"].plot()

# TODO: how would you do this with a Polars data frame?
# Since matplotlib is in the pip list and Polars documentation/forums do not show a direct way to plot like pandas, I am going to cheat and convert the dataframe into Pandas for plotting.
# Well I tried that but it didn't work directly, my mistake was I did not include the x and y parameters and was using the select function to select the column instead.
print("Plotting with Polars:")
pl_fixed_df.plot.line(x="Date", y="Berri 1")

# %%
# We can also plot all the columns just as easily. We'll make it a little bigger, too.
# You can see that it's more squished together, but all the bike paths behave basically the same -- if it's a bad day for cyclists, it's a bad day everywhere.

fixed_df.plot(figsize=(15, 10))

# TODO: how would you do this with a Polars data frame? With Polars data frames you might have to use the Seaborn library and it mmight not work out of the box as with pandas.
import seaborn as sns
import matplotlib.pyplot as plt

# Converting from Polars to Pandas for easier plotting suggest by forums
pd_pl_fixed_df = pl_fixed_df.to_pandas().set_index("Date")

df_melted = pd_pl_fixed_df.reset_index().melt(id_vars="Date", var_name="Pathway", value_name="Count") #Melting the dataframe as we saw in the lecture slides 2
print(df_melted.head())

plt.clf() 
sns.lineplot(data=df_melted, x="Date", y="Count", hue="Pathway")
plt.title("Bike counts for all pathways using Seaborn")
plt.show()
# %%
