import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.animation as animation 
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np

Gross_Capital_Formation = pd.read_csv('GDP_Deflator.csv')
CO2_emission = pd.read_csv('owid-co2-data.csv')
Exports = pd.read_csv('exports-of-goods-and-services-constant-2015-us.csv')
GDP = pd.read_csv('GDP(US)diff_for.csv')

melted_df = Gross_Capital_Formation.melt(id_vars=['Country Name'], var_name='Year', value_name='Gross capital formation (current US$)')
melted_df = melted_df.rename(columns={'Country Name': 'Entity'})

# Display the reshaped DataFrame
#print(melted_df.head())
# Merge the DataFrames by country and year
melted_df['Year'] = melted_df['Year'].astype(int)
merged_df = pd.merge(Exports, CO2_emission, on=['Entity', 'Year'])
merged_df = pd.merge(merged_df, melted_df, on=['Entity', 'Year'])
merged_df = pd.merge(merged_df, GDP, on=['Entity', 'Year'])
print(merged_df)

# List of income categories to filter out
high_middle_income = ['High-income countries', 'Middle-income countries', 'East Asia and Pacific (WB)', 'Upper-middle-income countries','Europe and Central Asia (WB)', 
                      'North America (WB)','European Union (27)','Lower-middle-income countries','Latin America and Caribbean (WB)',
                      'South Asia (WB)','Middle East and North Africa (WB)','Sub-Saharan Africa (WB)']

# Filtering the DataFrame to remove high-income and middle-income countries
filtered_df = GDP[~GDP['Entity'].isin(high_middle_income)]

# Filter data for the year 2021
df_2021 = filtered_df[filtered_df['Year'] == 2021]

# Get top 10 GDP countries for the year 2021
top_10_gdp_2021 = df_2021.nlargest(10, 'GDP (constant 2015 US$)')

# Extract the top 10 country names
top_10_countries = top_10_gdp_2021['Entity'].unique()
top_10_countries = top_10_countries[top_10_countries != 'World']
# Calculate world GDP for each year
world_gdp = GDP[GDP['Entity'] == 'World'].groupby('Year')['GDP (constant 2015 US$)'].sum()

# Calculate top 10 countries' GDP for each year
top_10_gdp = GDP[GDP['Entity'].isin(top_10_countries)].groupby('Year')['GDP (constant 2015 US$)'].sum()

# Subtract top 10 countries' GDP from world GDP for each year
rest_of_world_gdp = world_gdp - top_10_gdp


# Print or use the 'rest_of_world_gdp' Series as needed
print(rest_of_world_gdp)

#values_to_append = np.array(['Rest_World'])
#top_10_countries = np.concatenate((top_10_countries, values_to_append))
xyz = ['World']
GDP = GDP[~GDP['Entity'].isin(xyz)]

# Create subplots for the animation
fig, ax = plt.subplots(figsize=(10, 6))

# Create empty lines for each country
lines = [ax.plot([], [], label=Entity)[0] for Entity in top_10_countries]
ax.legend()

# Function to initialize the plot
def init():
    ax.set_xlim(filtered_df['Year'].min(), filtered_df['Year'].max())
    ax.set_ylim(filtered_df['GDP (constant 2015 US$)'].min(), filtered_df['GDP (constant 2015 US$)'].max()/2.5)
    return lines

# Animation function: update the plot for each frame
def animate(i):
    # Filter data up to the current year
    data = filtered_df[filtered_df['Year'] <= filtered_df['Year'].min() + i]

    for j, line in enumerate(lines):
        # Get country data based on the current line (Entity)
        country_data = data[data['Entity'] == top_10_countries[j]]
        
        # Update line data for the current country if data exists
        if not country_data.empty:
            line.set_data(country_data['Year'], country_data['GDP (constant 2015 US$)'])

    return lines

# Create the animation
ani = FuncAnimation(fig, animate, frames=filtered_df['Year'].nunique(), init_func=init, interval=100, blit=True)
plt.show()
#ani.save("TLI.gif", dpi=250, writer=PillowWriter(fps=25))
#ani.save("TLI.gif", dpi=300, writer='pillow', fps=25, quantizer='nq')
pd.set_option('display.max_rows', None)
print(rest_of_world_gdp)