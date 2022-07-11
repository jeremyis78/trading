from bs4 import BeautifulSoup
import argparse
import csv
import sys
 
msg = """Parses the closed positions found on the positions page of an OptionAlpha bot.
Works and tested in Chrome, Brave and Edge browsers"""
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

def clean_number(text):
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
        cost = clean_number(costdiv.div.span.string)
        costdesc = costdiv.desc.string

        pnldiv = row.bd.find("div", class_="pnl")
        pnl = clean_number(pnldiv.span.string)

        writer.writerow([tradeno, bot, sym, exp, strat, postext, status, closedate, qty, cost, costdesc, pnl])
        tradeno += 1
