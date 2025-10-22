# Made by: Hunter Davis

from pybaseball import pitching_stats
import matplotlib.pyplot as plt

def calculate_efficiency_index(df):
    """
    Calculates a custom pitcher efficiency index based on Z-scores of K-BB% and SIERA.
    The index is scaled so 100 is the league average.
    """
    df = df[df['IP'] > 0]
    
    avg_k_bb_percent = df['K-BB%'].mean()
    std_k_bb_percent = df['K-BB%'].std()
    
    avg_siera = df['SIERA'].mean()
    std_siera = df['SIERA'].std()
    
    df['k_bb_zscore'] = (df['K-BB%'] - avg_k_bb_percent) / std_k_bb_percent
    df['siera_zscore'] = (avg_siera - df['SIERA']) / std_siera
    
    siera_weight = 0.6
    k_bb_weight = 0.4
    
    df['Efficiency_Index'] = (df['siera_zscore'] * siera_weight + df['k_bb_zscore'] * k_bb_weight)
    
    final_index_scaled = 100 + (df['Efficiency_Index'] * 10)
    df['Efficiency_Index'] = final_index_scaled

    return df

def visualize_data(top_pitchers, year, num_pitchers=15):
    """
    Creates a horizontal bar chart to visualize the top N pitchers
    using a sequential color palette, with the darkest color for the most efficient pitcher.
    """
    plot_data = top_pitchers.head(num_pitchers).copy()
    
    pitcher_names = plot_data['Name']
    efficiency_scores = plot_data['Efficiency_Index']

    norm = plt.Normalize(efficiency_scores.min(), efficiency_scores.max())
    cmap = plt.get_cmap('Blues')
    colors = cmap(norm(efficiency_scores))

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.barh(
        pitcher_names,
        efficiency_scores,
        color=colors,         
        edgecolor='darkblue', 
        linewidth=1,          
    )
    
    ax.set_title(f'Top {num_pitchers} Most Efficient Starters in {year}', fontsize=16, weight='bold')
    ax.set_xlabel('Custom Efficiency Index (100 = League Average)', fontsize=12, weight='bold')
    ax.set_ylabel('Pitcher', fontsize=12, weight='bold')

    for index, value in enumerate(efficiency_scores):
        ax.text(value + 1, index, f'{value:.2f}', va='center')
        
    ax.set_xlim(left=95, right=max(efficiency_scores) + 5)
    
    ax.invert_yaxis()
    
    plt.tight_layout()
    plt.show()

def find_top_pitchers(year, min_ip, num_pitchers=20):
    """
    Fetches pitcher data for a given year, calculates the custom efficiency
    index, and returns a sorted list of the top performers.
    """
    print(f"Fetching pitcher data for the {year} season from FanGraphs...")
    
    raw_stats = pitching_stats(year)
    
    qualified_pitchers = raw_stats[raw_stats['IP'] >= min_ip].copy()
    
    if qualified_pitchers.empty:
        print("No qualified pitchers found. Check year and minimum IP.")
        return
        
    print(f"Calculating efficiency index for {len(qualified_pitchers)} qualified pitchers...")
    
    pitchers_with_index = calculate_efficiency_index(qualified_pitchers)
    
    top_pitchers = pitchers_with_index.sort_values(by='Efficiency_Index', ascending=False)
    
    print(f"\nTop {num_pitchers} Most Efficient Pitchers in {year} (min {min_ip} IP):")
    display_cols = ['Name', 'Team', 'IP', 'K-BB%', 'SIERA', 'Efficiency_Index']
    print(top_pitchers[display_cols].head(num_pitchers).to_string(index=False))

    visualize_data(top_pitchers, year, num_pitchers)

if __name__ == "__main__":
    current_year = 2025
    minimum_innings_pitched = 150
    find_top_pitchers(current_year, minimum_innings_pitched)




