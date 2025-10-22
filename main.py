# Made by: Hunter Davis

from pybaseball import pitching_stats
import matplotlib.pyplot as plt

def calculate_PSI(df):
    """
    Calculates a custom pitcher performance and skill index (PSI) based on Z-scores of K-BB% and SIERA.
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
    
    df['PSI'] = (df['siera_zscore'] * siera_weight + df['k_bb_zscore'] * k_bb_weight)
    
    final_index_scaled = 100 + (df['PSI'] * 10)
    df['PSI'] = final_index_scaled

    return df

def visualize_data(top_pitchers, year, num_pitchers):
    """
    Creates a horizontal bar chart to visualize the top N pitchers
    using a sequential color palette, with the darkest color for the most effective pitcher.
    """
    plot_data = top_pitchers.head(num_pitchers).copy()
    
    pitcher_names = plot_data['Name']
    PSI_scores = plot_data['PSI']

    norm = plt.Normalize(PSI_scores.min(), PSI_scores.max())
    cmap = plt.get_cmap('Blues')
    colors = cmap(norm(PSI_scores))

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.barh(
        pitcher_names,
        PSI_scores,
        color=colors,         
        edgecolor='darkblue', 
        linewidth=1,          
    )
    
    ax.set_title(f'Top {num_pitchers} Most Effective Starters in {year}', fontsize=16, weight='bold')
    ax.set_xlabel('Performance and Skill Index (100 = League Average)', fontsize=12, weight='bold')
    ax.set_ylabel('Pitcher', fontsize=12, weight='bold')

    for index, value in enumerate(PSI_scores):
        ax.text(value + 1, index, f'{value:.2f}', va='center')
        
    ax.set_xlim(left=95, right=max(PSI_scores) + 5)
    
    ax.invert_yaxis()
    
    plt.tight_layout()
    filename = f'top_{num_pitchers}_pitchers_{year}.png'
    plt.savefig(filename, dpi=300)
    plt.show()

def find_top_pitchers(year, min_ip, num_pitchers=20):
    """
    Fetches pitcher data for a given year, calculates the PSI
    and returns a sorted list of the top performers.
    """
    print(f"Fetching pitcher data for the {year} season from FanGraphs...")
    
    raw_stats = pitching_stats(year)
    
    qualified_pitchers = raw_stats[raw_stats['IP'] >= min_ip].copy()
    
    if qualified_pitchers.empty:
        print("No qualified pitchers found. Check year and minimum IP.")
        return
        
    print(f"Calculating PSI for {len(qualified_pitchers)} qualified pitchers...")
    
    pitchers_with_index = calculate_PSI(qualified_pitchers)
    
    top_pitchers = pitchers_with_index.sort_values(by='PSI', ascending=False)
    
    print(f"\nTop {num_pitchers} Most Efficient Pitchers in {year} (min {min_ip} IP):")
    display_cols = ['Name', 'Team', 'IP', 'K-BB%', 'SIERA', 'PSI']
    print(top_pitchers[display_cols].head(num_pitchers).to_string(index=False))

    visualize_data(top_pitchers, year, num_pitchers)

if __name__ == "__main__":
    current_year = 2024
    minimum_innings_pitched = 150
    find_top_pitchers(current_year, minimum_innings_pitched)




