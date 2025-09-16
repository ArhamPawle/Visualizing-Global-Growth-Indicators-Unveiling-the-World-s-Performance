import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.animation import FuncAnimation

# Load your CSV data into Pandas DataFrames
df_gdp = pd.read_csv('total-gdp-vs-gdp-per-capita.csv')
df_gdp_deflator = pd.read_csv('GDP_Deflator.csv')

melted_df = df_gdp_deflator.melt(id_vars=['Country Name'], var_name='Year', value_name='GDP deflator')
melted_df = melted_df.rename(columns={'Country Name': 'Entity'})
# Display the reshaped DataFrame
print(melted_df.head())
# Merge the DataFrames by country and year
melted_df['Year'] = melted_df['Year'].astype(int)
merged_df = pd.merge(df_gdp, melted_df, on=['Entity', 'Year'])

print(merged_df)
