import pandas as pd
import sys

# python3 -m venv venv
# . venv/bin/activate
# pip install pandas
# python compute_winrate.py <file>
#
# To deactivate virtualenv:
# deactivate

# Example: This is Lee's AUTO UP DB9 bot as of 2024-05-25
# (venv) ➜  $ python compute_winrate.py ~/Downloads/BOT_AUTO_UP_DB9-20240525-7a7a1b.csv
#               type  wins  num_trades  avg_daysInTrade    min_trade_date    max_trade_date     avg_PnL  sum_PnL  win_rate
# 0          longput    75         184        20.711957  01-12-2023 10:15  12-15-2023 16:15  -17.983696    -3309  0.407609
# 1    longputspread    46          59         9.745763  01-14-2022 11:45  12-22-2022 12:45   28.949153     1708  0.779661
# 2  shortcallspread    73          74         9.716216  01-14-2022 11:45  12-28-2022 11:16  600.810811    44460  0.986486
# 3   shortputspread     5           6        34.000000  03-10-2023 13:00   12-15-2022 9:45   72.500000      435  0.833333

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
