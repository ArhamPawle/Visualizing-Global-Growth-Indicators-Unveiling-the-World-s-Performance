import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.animation import FuncAnimation
import numpy as np
import country_converter as coco

# Load your CSV data into Pandas DataFrames
df_gdp = pd.read_csv('GDP(US)diff_for.csv')
df_gdp_per_capita = pd.read_csv('GDP(Percapita)Diff_for.csv')
df_gdp_deflator = pd.read_csv('GDP_Deflator.csv')
melted_df = df_gdp_deflator.melt(id_vars=['Country Name'], var_name='Year', value_name='GDP deflator')
melted_df = melted_df.rename(columns={'Country Name': 'Entity'})

# Display the reshaped DataFrame
#print(melted_df.head())
# Merge the DataFrames by country and year
melted_df['Year'] = melted_df['Year'].astype(int)
melted_df.info()
merged_df = pd.merge(df_gdp, df_gdp_per_capita, on=['Entity', 'Year'])
merged_df.info()
merged_df = pd.merge(merged_df, melted_df, on=['Entity', 'Year'])
print(merged_df.head())
merged_df.dropna(subset=['GDP (constant 2015 US$)_x'], inplace=True)
#merged_df.to_csv('your_file.csv', index=False)
print('hi')
#scaler = StandardScaler()
#merged_df['GDP (constant 2015 US$)_x'] = scaler.fit_transform(merged_df[['GDP (constant 2015 US$)_x']])
# Convert GDP values to billions
merged_df['GDP (constant 2015 US$)_x'] = merged_df['GDP (constant 2015 US$)_x'] / 1e9  # Dividing by 1 billion
merged_df['GDP (constant 2015 US$)_x'] = np.log(merged_df['GDP (constant 2015 US$)_x'])
merged_df['GDP (constant 2015 US$)_y'] = merged_df['GDP (constant 2015 US$)_y'] / 1000
print('df created')
#merged_df['GDP (constant 2015 US$)_y'] = np.log(merged_df['GDP (constant 2015 US$)_y'])
# Add a column for continents using country_converter
#merged_df['Continent'] = merged_df['Entity'].apply(lambda x: coco.convert(names=x, to='continent', not_found=None))
merged_df = pd.read_csv('continent.csv') 
# Filter out rows where continent information is missing
merged_df.dropna(subset=['Continent'], inplace=True)

# Initialize colors for continents
colors = {'Asia': 'red', 'Europe': 'blue', 'Africa': 'green', 'America': 'orange', 'Oceania': 'purple'}

# Create a scatter plot for each continent
fig, ax = plt.subplots()
scatters = {}

for continent, color in colors.items():
    df_continent = merged_df[merged_df['Continent'] == continent]
    scatters[continent] = ax.scatter([], [], s=[], alpha=0.5, color=color, label=continent)

# Set fixed x-axis limit and logarithmic y-axis scale (remains the same)
ax.set_xlim(0, merged_df['GDP (constant 2015 US$)_y'].max() / 1.5)
ax.set_ylim(0, merged_df['GDP (constant 2015 US$)_x'].max())

# Add labels to x and y axes
ax.set_xlabel('GDP per Capita (constant 2015 US$)')
ax.set_ylabel('GDP (constant 2015 US$) (log scale)')

# Add legend with larger marker size
ax.legend(loc='upper right', scatterpoints=1, markerscale=1.5)

# Function to update scatter plots for each continent
def update(year):
    year_data = merged_df[merged_df['Year'] == year]
    for continent, scatter in scatters.items():
        continent_data = year_data[year_data['Continent'] == continent]
        scatter.set_offsets(continent_data[['GDP (constant 2015 US$)_y', 'GDP (constant 2015 US$)_x']])
        scatter.set_sizes(continent_data['GDP deflator'] * 3)
    ax.set_title(f'Year: {year}')

# Define the years for the animation and sort them
years = np.sort(merged_df['Year'].unique())

# Create the animation with sorted years
ani = FuncAnimation(fig, update, frames=years, interval=500)
plt.show()