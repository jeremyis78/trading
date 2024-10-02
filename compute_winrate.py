import pandas as pd
import sys

# python3 -m venv venv
# . venv/bin/activate
# pip install pandas
# python compute_winrate.py <file>

# Example: python compute_winrate.py ~/Downloads/BOT92831316391850954728831-20231020-d02fbd.csv

def compute_win_rate(file):
    """
    Compute the stats, win rate, avg PnL, etc for each type of trade in the given CSV file.
    CSV files need at minimum the following columns: type,openDate,closeDate,daysInTrade,pnl
    Inspired by
    https://stackoverflow.com/questions/73619241/calculate-win-rates-in-python-using-groupby-and-lambda-functions
    """
    trades = pd.read_csv(file)

    #print(trades)

    return ((trades.assign(is_winner=trades['pnl'].gt(0))
             .groupby('type', sort=False, as_index=False))
            .agg(**{'wins': ('is_winner', 'sum'),
                    'num_trades': ('type', 'size'),
                    'avg_daysInTrade': ('daysInTrade', 'mean'),
                    'min_trade_date': ('openDate', 'min'),
                    'max_trade_date': ('closeDate', 'max'),
                    'avg_PnL': ('pnl', 'mean'),
                    'sum_PnL': ('pnl', 'sum'),
                    'win_rate': ('is_winner', 'mean')}))


if __name__ == "__main__":
    csv_file = sys.argv[1] if len(sys.argv) > 1 else "BOT-something.csv"
    wr = compute_win_rate(csv_file)
    print(wr)
