import csv
import json

# Data from preload/benchmark/eyewitness_results_b111.md
DATA = [
    {"model": "claude-haiku", "hot_acc": 0.987, "cold_acc": 0.053, "hot_cost": 0.0066, "cold_cost": 0.0009},
    {"model": "claude-opus", "hot_acc": 0.987, "cold_acc": 0.067, "hot_cost": 0.1272, "cold_cost": 0.0222},
    {"model": "sonar-pro", "hot_acc": 0.980, "cold_acc": 0.093, "hot_cost": 0.0144, "cold_cost": 0.0034},
    {"model": "gemini-flash", "hot_acc": 0.947, "cold_acc": 0.120, "hot_cost": 0.0007, "cold_cost": 0.0002},
    {"model": "gemini-pro", "hot_acc": 0.940, "cold_acc": 0.087, "hot_cost": 0.0061, "cold_cost": 0.0016},
    {"model": "gpt-4o", "hot_acc": 0.933, "cold_acc": 0.087, "hot_cost": 0.0106, "cold_cost": 0.0015},
    {"model": "sonar", "hot_acc": 0.920, "cold_acc": 0.073, "hot_cost": 0.0041, "cold_cost": 0.0003},
    {"model": "gpt-4o-mini", "hot_acc": 0.893, "cold_acc": 0.113, "hot_cost": 0.0006, "cold_cost": 0.0001},
]

def run_analysis():
    total_hot_cost = sum(d['hot_cost'] for d in DATA) * 75
    total_cold_cost = sum(d['cold_cost'] for d in DATA) * 75
    
    # Pooled ratio calculation
    pooled_ratio = total_hot_cost / total_cold_cost
    
    # Export to CSV
    with open('r10_efficiency_analysis.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['model', 'hot_acc', 'cold_acc', 'hot_cost', 'cold_cost', 'efficiency_score'])
        for d in DATA:
            eff = d['hot_acc'] / d['hot_cost']
            writer.writerow([d['model'], d['hot_acc'], d['cold_acc'], d['hot_cost'], d['cold_cost'], eff])
            
    print(f"Total Inference Spend (75q): ${total_hot_cost + total_cold_cost:.4f}")
    print(f"Pooled HOT:COLD Cost Ratio: {pooled_ratio:.2f}x")

if __name__ == '__main__':
    run_analysis()