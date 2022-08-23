from bs4 import BeautifulSoup
from decimal import Decimal
import argparse
import csv
import sys
 
msg = """Parses the closed positions found on the positions page of an OptionAlpha bot.

Optionally, you can specify the trading fees/contract you pay to give a rough idea
of how much you'll pay to trade for a given bot. It handles positions with a status of Closed, 
Expired, and Canceled and works with any kind of OA supported strategy; spreads, ICs, IBs,
long calls/puts or stock.  For instance, if you trade Iron Condors it will correctly calculate
the fees for four options for each condor you trade.  Stock positions, unlike option strategies, 
are assumed to have zero fees, even though that's not actually accurate. I chose 'fees' instead
of 'commissions' language since it seems we are moving commissions--including options 
commissions--towards zero, so fees really means anything you pay to trade including the sum of 
commissions, ORF, Exchange fees for index options, SEC fee, etc.

Works and tested in Chrome, Brave and Edge browsers.
"""
epilog_msg = """usage: oa-positions-parser.py [-h] [--csv] file

Parses the closed positions found on the positions page of an OptionAlpha bot.

positional arguments:
  file        HTML file saved from OA bots positions page

optional arguments:
  -h, --help  show this help message and exit
  --csv       Output CSV instead of the default TSV (tab-separated values)

Examples:

(Windows): python oa-positions-parser.py %USERPROFILE%/Downloads/my-bot-name.html
or
(Mac)    : python oa-positions-parser.py ~/Downloads/my-bot-name.html

The above commands print the output to the console in the default TSV output.
You can also output to a TSV or CSV file.
In this example, we're on Windows and create both a TSV and CSV file instead of printing to the console.

python oa-positions-parser.py %USERPROFILE%/Downloads/my-bot-name.html > my-bot-name.tsv
python oa-positions-parser.py --csv %USERPROFILE%/Downloads/my-bot-name.html > my-bot-name.csv

You can also specify trading fees you pay per contract. Specify the fees as cents; in this example
the trading fees are specified as 45.09 cents ($0.4509/contract):

python oa-positions-parser.py --csv --fees 45.09 %USERPROFILE%/Downloads/my-bot-name.html > my-bot-name.csv
"""
parser = argparse.ArgumentParser(description=msg, epilog=epilog_msg,
                                 formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("--csv", help="Output CSV instead of the default TSV (tab-separated values)", action="store_true")
parser.add_argument('--fees', type=Decimal, default=0, help='Trading fees per contract in cents (e.g. --fees 35, would mean 35 cents/contract)', metavar="CENTS")
parser.add_argument("file", help="HTML file saved from OA bots positions page")

args = parser.parse_args()
config = vars(args)

delim = ',' if args.csv else '\t'
per_contract_fee = args.fees/Decimal(100) if args.fees != 0 else 0

chars_to_remove = [u' ', u'$', u',']
def remove_chars(subj, chars):
    sc = set(chars)
    return ''.join([c for c in subj if c not in sc])

def clean_number(text):
    if text is None or "--" in text:
        return 0    # not sure why OA puts -- for zero or a N/A (canceled or override orders) so we fix it here
    return remove_chars(text, chars_to_remove)

with open(args.file) as fp:
    soup = BeautifulSoup(fp, 'html.parser')
    # One thing: I wrote this script so it will "blow up" and give a good error message if it ever fails.
    # For example, "bot = title[0].string" if title is None or a zero-length array then it will choke
    # on this exact line telling us exactly why.
    # Another example: "costdiv.div.span.string".  Accessing this string after doing a 'find' for costdiv
    # implies there's a costdiv then a div then a span and that span has some text node.  If any of those are None
    # then again it will choke on that line with an error message telling us mostly what's wrong.
    # One more: "title = soup.select("#bots-bot hd.title-editor h1.title a.edit-title")"
    # Starting in reverse, we're looking an <a> tag with class="edit-title" within a
    # an <h1> with class "title" within an <hd> with class "title-editor" within
    # an element (doesn't matter what type element) with an id of "bots-bot". If we wanted to specify
    # we could do "view#bots-bot" if the element was a <view>.
    title = soup.select("#bots-bot hd.title-editor h1.title a.edit-title")
    bot = title[0].string
    closedpos = soup.find(id="bots-bot-positions-closedpos")
    bd = closedpos.find_all('bd', class_="dim-scroller")
    rows = bd[0].find_all("row", class_="pos")
    writer = csv.writer(sys.stdout, delimiter=delim, quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["tradeno", "bot", "sym", "exp", "strat", "postext", "status", "closedate", "qty",
                    "cost", "costdesc", "pnl", "fees", "netpnl"])
    tradeno = 1;
    for row in rows:
        symdiv = row.bd.find("div", class_="symbol")
        sym = symdiv.find("span", class_="sym").string
        exp = symdiv.find("span", class_="exp").string
        strat = symdiv.find("span", class_="strat").string
        postext = symdiv.find("span", class_="postext").string

        closedatediv = row.bd.find("div", class_="closeDate")
        status = closedatediv.div.span.string
        closedate = closedatediv.desc.string

        qtydiv = row.bd.find("div", class_="quantity")
        qty = clean_number(qtydiv.span.string)

        costdiv = row.bd.find("div", class_="cost")
        cost = clean_number(costdiv.div.span.string)
        costdesc = costdiv.desc.string

        pnldiv = row.bd.find("div", class_="pnl")
        pnl = clean_number(pnldiv.span.string)

        if per_contract_fee != 0 and qty != 0:
            strat_qty = 0  #contract quantity for a strategy
            if 'Spread' in strat:
                strat_qty = 2
            elif 'Iron' in strat:
                strat_qty = 4
            elif 'Long Call' in strat or 'Long Put' in strat:
                strat_qty = 1
            fees = -1 * Decimal(qty) * Decimal(strat_qty) * per_contract_fee
            #if position was closed, then we have roughly double the fees, otherwise it expired and no closing fees
            fees = fees * 2 if "Closed" in status else fees
            netpnl = Decimal(pnl) + fees
        else:
            fees = 0
            netpnl = pnl

        writer.writerow([tradeno, bot, sym, exp, strat, postext, status, closedate, qty, cost, costdesc, pnl, fees, netpnl])
        tradeno += 1
