import matplotlib.pyplot as plt

from data import load_solar_data
from simulation import run_simulation, validate_model

def set_aesthetic_theme():
    # Canvas and background colors (Soft off-white)
    plt.rcParams['figure.facecolor'] = '#FDFCF0' 
    plt.rcParams['axes.facecolor'] = '#FDFCF0'
    
    # Text and label colors (Soft charcoal and grays)
    plt.rcParams['text.color'] = '#333333'
    plt.rcParams['axes.labelcolor'] = '#555555'
    plt.rcParams['xtick.color'] = '#777777'
    plt.rcParams['ytick.color'] = '#777777'
    
    # Grid and borders (Minimalist floating look)
    plt.rcParams['axes.grid'] = True
    plt.rcParams['grid.color'] = '#EAEAEA'
    plt.rcParams['grid.linestyle'] = '--'
    plt.rcParams['axes.edgecolor'] = '#EAEAEA'
    plt.rcParams['axes.spines.top'] = False
    plt.rcParams['axes.spines.right'] = False

def create_dashboard():
    # --- VALIDATION ---
    print("Running simulation validation...")
    validate_model()

    # --- GET REAL DATA ---
    print("Loading data and running simulations...")
    solar_data = load_solar_data()
    
    # Run all three simulations
    altitudes_min, days_min = run_simulation(70)
    altitudes_max, days_max = run_simulation(230)
    altitudes_real, days_real = run_simulation(solar_data)

    # --- BUILD VISUALIZATION ---
    set_aesthetic_theme()
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))

    # Plot 1 - Solar Activity
    ax1.plot(solar_data.index, solar_data.values, color='#F4A261')
    ax1.set_title('Solar Activity (F10.7)', fontweight='bold')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('F10.7 Index')

    # Plot 2 - Altitude Decay: Three Scenarios
    days_min_axis = range(len(altitudes_min))
    days_max_axis = range(len(altitudes_max))
    days_real_axis = range(len(altitudes_real))

    ax2.plot(days_min_axis, altitudes_min, 
             color='#2A9D8F', label=f'Solar min (f107=70): {days_min} days')
    ax2.plot(days_max_axis, altitudes_max, 
             color='#E76F51', label=f'Solar max (f107=230): {days_max} days')
    ax2.plot(days_real_axis, altitudes_real, 
             color='#4A824A', linewidth=2.5, label=f'Real solar data: {days_real} days')
    
    ax2.axhline(y=120, color='#333333', linestyle=':', label='Re-entry threshold')
    ax2.set_title('Altitude Decay: Three Scenarios', fontweight='bold')
    ax2.set_xlabel('Days')
    ax2.set_ylabel('Altitude (km)')
    # Adding fontsize=9 shrinks it down nicely
    ax2.legend(loc='upper right', fontsize=7, frameon=False)
    # Forces the Y-axis to start at 100 instead of 120, giving you a 20km "padding" at the bottom
    ax2.set_ylim(bottom=100)

    # Plot 3 - Bar Chart
    bars = ax3.bar(['Solar Min', 'Solar Max'], 
                   [days_min, days_max], 
                   color=['#2A9D8F', '#E76F51'], width=0.6)
    ax3.bar_label(bars, padding=5, fontweight='bold', color='#333333')
    ax3.set_title('Satellite Lifetime', fontweight='bold')
    ax3.set_ylabel('Total Days')
    
    # Clean up bar chart axes
    ax3.spines['left'].set_visible(False)
    ax3.spines['bottom'].set_visible(False)
    ax3.set_yticks([])

    # Polish, Save, and Show
    plt.tight_layout()
    plt.savefig('output.png', dpi=150, bbox_inches='tight')
    print("Success! Dashboard saved as output.png")
    
    
    plt.show()


if __name__ == "__main__":
    create_dashboard()
