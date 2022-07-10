
from bs4 import BeautifulSoup
from lxml import etree
import argparse
import csv
import sys
 
msg = "Parses the closed positions found on the positions page of an OptionAlpha bot."
epilog_msg = """usage: oa-positions-parser.py [-h] [--csv] file

Parses the closed positions found on the positions page of an OptionAlpha bot.

positional arguments:
  file        HTML file saved from OA bots positions page

optional arguments:
  -h, --help  show this help message and exit
  --csv       Output CSV instead of the default TSV (tab-separated values)

Examples (copies script output to clipboard):

(Windows): python oa-position-parser.py %USERPROFILE%/Downloads/my-bot-name.html|clip
or
(MAC): python oa-position-parser.py ~/Downloads/my-bot-name.html|pbcopy

Then open Excel/Sheets and paste.  Done.

You can also export as CSV but it doesn't play as nice with Excel or Sheets by default:
python oa-position-parser.py --csv ~/Downloads/my-bot-name.html
"""
parser = argparse.ArgumentParser(description=msg, epilog=epilog_msg,
                                 formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("--csv", help="Output CSV instead of the default TSV (tab-separated values)", action="store_true")
parser.add_argument("file", help="HTML file saved from OA bots positions page")

args = parser.parse_args()
config = vars(args)

delim = ',' if args.csv else '\t'

chars_to_remove = [u' ', u'$', u',']

def remove_chars(subj, chars):
    sc = set(chars)
    return ''.join([c for c in subj if c not in sc])

with open(args.file) as fp:
    soup = BeautifulSoup(fp, 'html.parser')
    dom = etree.HTML(str(soup))
    #bot name is under the <a class="edit-title"> of the SECOND <h1 class="title">
    h1s = soup.find_all("h1", class_="title") #xpath from Chrome Dev Tools: '//*[@id=bots-bot]/hd/ct[2]/h1/a'
    if h1s and len(h1s) == 2:
        a = h1s[1].find("a", class_="edit-title")
        bot = a.string if a else ""
    else:
        bot = ""
    closedpos = soup.find(id="bots-bot-positions-closedpos")
    bd = closedpos.find_all('bd', class_="dim-scroller")
    rows = bd[0].find_all("row", class_="pos")

    writer = csv.writer(sys.stdout, delimiter=delim,
                        quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["tradeno", "bot", "sym", "exp", "strat", "postext", "status", "closedate", "qty",
                    "cost", "costdesc", "pnl"])
    tradeno = 1;
    for row in rows:
        symdiv = row.bd.find("div", class_="symbol")
        sym = symdiv.find("span", class_="sym").string
        exp = symdiv.find("span", class_="exp").string
        strat = symdiv.find("span", class_="strat").string
        postext = symdiv.find("span", class_="postext").string

        closedatediv = row.bd.find("div", class_="closeDate")
        status = closedatediv.div.string
        closedate = closedatediv.desc.string

        qtydiv = row.bd.find("div", class_="quantity")
        qty = qtydiv.string

        costdiv = row.bd.find("div", class_="cost")
        cost = remove_chars(costdiv.div.string, chars_to_remove)
        costdesc = costdiv.desc.string

        pnldiv = row.bd.find("div", class_="pnl")
        pnl = remove_chars(pnldiv.string, chars_to_remove)   # You'd need to strip commas and $ character to compute commissions

        writer.writerow([tradeno, bot, sym, exp, strat, postext, status, closedate, qty, cost, costdesc, pnl])
        tradeno += 1
