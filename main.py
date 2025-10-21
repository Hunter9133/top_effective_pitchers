# This small script will find and display the 20 most efficient QUALIFIED pitchers 
# in the 2025 MLB regular season through the use of the pybaseball library and pandas. 
# Efficiency is defined as taking on a large workload while maintaining high effectiveness.
# Pitchers who can work deep into games while keeping runs off the board will be 
# ranked the highest. 

# A simple efficiency score metric will be defined as:
# ((K% - BB%) x IP) / SIERA)

# !! Hightlight in post that this is not everything that goes into evaluating a pitcher !!

import pybaseball as pyb
import matplotlib.pyplot as plt
import numpy as np

# Get pitching data for the 2025 MLB season
pitching_data = pyb.pitching_stats(2025)

# Filter for qualified pitchers (minimum 162 innings pitched)
qualified_pitchers = pitching_data[pitching_data['IP'] >= 162]

# Calculate K% and BB%
qualified_pitchers['K%'] = (qualified_pitchers['SO'] / qualified_pitchers['TBF']) * 100
qualified_pitchers['BB%'] = (qualified_pitchers['BB'] / qualified_pitchers['TBF']) * 100
# Calculate the efficiency score
qualified_pitchers['Efficiency_Score'] = ((qualified_pitchers['K%'] - qualified_pitchers['BB%']) * qualified_pitchers['IP']) / qualified_pitchers['SIERA']


# Sort pitchers by efficiency score in descending order
sorted_pitchers = qualified_pitchers.sort_values(by='Efficiency_Score', ascending=False)
# Select the top 20 most efficient pitchers
top_20_efficient_pitchers = sorted_pitchers.head(20)
# Display the results
print(top_20_efficient_pitchers[['Name', 'Team', 'IP', 'K%', 'BB%', 'SIERA', 'Efficiency_Score']])

# 1) Horizontal bar chart of the top 20 by Efficiency_Score
bars = top_20_efficient_pitchers.sort_values("Efficiency_Score", ascending=True)

plt.figure(figsize=(10, 8))
plt.rcParams["font.family"] = "DejaVu Sans" 
plt.barh(bars["Name"], bars["Efficiency_Score"])
plt.xlabel("Efficiency Score = ((K% - BB%) × IP) / SIERA")
plt.ylabel("Pitcher")
plt.title("Top 20 Most Efficient Qualified Pitchers (2025)")
plt.tight_layout()
plt.savefig("efficiency_top20_bar.png", dpi=200)
plt.show()


