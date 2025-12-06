"""
Simple Matplotlib Dashboard for Customer Churn Monitoring
Run this after making predictions to see your monitoring dashboard
"""
import json
import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path

def load_metrics():
    """Load metrics from log file"""
    metrics_file = Path("logs/metrics.json")
    
    if not metrics_file.exists():
        print("❌ No metrics file found!")
        print("Make sure you have:")
        print("1. Created the logs directory")
        print("2. Made some predictions using the API")
        return []
    
    metrics = []
    with open(metrics_file, 'r') as f:
        for line in f:
            try:
                metrics.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    
    return metrics

def create_dashboard():
    """Create simple matplotlib dashboard"""
    metrics = load_metrics()
    
    if not metrics:
        print("❌ No metrics data available.")
        print("\nTo generate metrics:")
        print("1. Start your Flask API")
        print("2. Make predictions: curl -X POST http://localhost:5000/predict -d @input.json")
        print("3. Run this script again")
        return
    
    print(f"✅ Loaded {len(metrics)} metric entries")
    
    # Extract data
    timestamps = [datetime.fromisoformat(m['timestamp']) for m in metrics]
    avg_probs = [m['avg_churn_probability'] for m in metrics]
    total_preds = [m['total_predictions'] for m in metrics]
    high_risk_pcts = [m['high_risk_percentage'] for m in metrics]
    
    # Get latest metrics
    latest = metrics[-1]
    
    # Create 2x2 dashboard
    fig = plt.figure(figsize=(14, 10))
    fig.suptitle('Customer Churn Monitoring Dashboard', fontsize=18, fontweight='bold')
    
    # Plot 1: Average Churn Probability Over Time (Top Left)
    ax1 = plt.subplot(2, 2, 1)
    ax1.plot(timestamps, avg_probs, marker='o', linewidth=2, markersize=6, color='#2E86AB')
    ax1.set_title('Average Churn Probability Over Time', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Probability')
    ax1.set_ylim(0, 1)
    ax1.grid(True, alpha=0.3)
    ax1.tick_params(axis='x', rotation=45)
    
    # Add current value annotation
    if avg_probs:
        ax1.annotate(f'{avg_probs[-1]:.2%}', 
                    xy=(timestamps[-1], avg_probs[-1]),
                    xytext=(10, 10), textcoords='offset points',
                    bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7),
                    fontsize=10, fontweight='bold')
    
    # Plot 2: Risk Distribution (Top Right)
    ax2 = plt.subplot(2, 2, 2)
    risk_data = [
        latest['low_risk_customers'],
        latest['medium_risk_customers'],
        latest['high_risk_customers']
    ]
    risk_labels = [
        f"Low Risk\n({latest['low_risk_customers']})",
        f"Medium Risk\n({latest['medium_risk_customers']})",
        f"High Risk\n({latest['high_risk_customers']})"
    ]
    colors = ['#06D6A0', '#FFD166', '#EF476F']
    
    wedges, texts, autotexts = ax2.pie(risk_data, labels=risk_labels, autopct='%1.1f%%',
                                         colors=colors, startangle=90,
                                         textprops={'fontsize': 10})
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    ax2.set_title('Current Risk Distribution', fontsize=12, fontweight='bold')
    
    # Plot 3: Key Metrics (Bottom Left)
    ax3 = plt.subplot(2, 2, 3)
    ax3.axis('off')
    
    # Create metrics display
    metrics_text = f"""
    📊 KEY METRICS (Latest)
    
    Total Predictions: {latest['total_predictions']}
    
    Average Churn Probability: {latest['avg_churn_probability']:.1%}
    
    High Risk Customers: {latest['high_risk_customers']} ({latest['high_risk_percentage']:.1f}%)
    
    Medium Risk Customers: {latest['medium_risk_customers']}
    
    Low Risk Customers: {latest['low_risk_customers']}
    
    ⏱ Last Updated: {latest['timestamp'][:19]}
    """
    
    ax3.text(0.1, 0.5, metrics_text, fontsize=11, family='monospace',
             verticalalignment='center', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.3))
    
    # Plot 4: High Risk Trend (Bottom Right)
    ax4 = plt.subplot(2, 2, 4)
    ax4.plot(timestamps, high_risk_pcts, marker='s', linewidth=2, 
             markersize=6, color='#EF476F', label='High Risk %')
    ax4.axhline(y=50, color='red', linestyle='--', alpha=0.5, label='50% Threshold')
    ax4.set_title('High Risk Customer Trend', fontsize=12, fontweight='bold')
    ax4.set_xlabel('Time')
    ax4.set_ylabel('Percentage (%)')
    ax4.set_ylim(0, 100)
    ax4.grid(True, alpha=0.3)
    ax4.legend()
    ax4.tick_params(axis='x', rotation=45)
    
    # Adjust layout
    plt.tight_layout()
    
    # Save dashboard
    output_file = Path("logs/dashboard.png")
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"\n✅ Dashboard saved to: {output_file}")
    
    # Show dashboard
    plt.show()
    
    # Print summary
    print("\n" + "="*50)
    print("MONITORING SUMMARY")
    print("="*50)
    print(f"Total Metric Entries: {len(metrics)}")
    print(f"Average Churn Probability: {latest['avg_churn_probability']:.1%}")
    print(f"High Risk Customers: {latest['high_risk_customers']} ({latest['high_risk_percentage']:.1f}%)")
    
    # Check for concerning trends
    if latest['high_risk_percentage'] > 40:
        print("\n⚠️  WARNING: High proportion of at-risk customers!")
    if len(avg_probs) > 1 and avg_probs[-1] > avg_probs[0] * 1.2:
        print("⚠️  WARNING: Churn probability increasing over time!")
    
    print("="*50)

if __name__ == "__main__":
    print("="*50)
    print("Customer Churn Monitoring Dashboard")
    print("="*50)
    create_dashboard()
