
from bs4 import BeautifulSoup
import sys
from lxml import etree
from decimal import Decimal
import argparse
 
msg = "Parses the closed positions found on the positions page of an OptionAlpha bot (produces TSV output suitable for import to Excel or Sheets)."
epilog_msg = "Example:  python tc0dte-positions.html"
parser = argparse.ArgumentParser(description=msg, epilog=epilog_msg,
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
#parser.add_argument("-c", "--commissions", help="Commissions per contract", default=0)
parser.add_argument("file", help="HTML file saved from OA bots positions page")
args = parser.parse_args()
config = vars(args)

chars_to_remove = [u' ', u'$', u',']

def remove_chars(subj, chars):
    sc = set(chars)
    return ''.join([c for c in subj if c not in sc])

commpercontract = 0   # Decimal(config['commissions'])
with open(config['file']) as fp:
    soup = BeautifulSoup(fp, 'html.parser')
    dom = etree.HTML(str(soup))
    #bot name is under the <a class="edit-title"> of the SECOND <h1 class="title">
    botH1s = soup.find_all("h1", class_="title") #xpath from Chrome Dev Tools: '//*[@id=bots-bot]/hd/ct[2]/h1/a'
    bot = botH1s[1].find("a", class_="edit-title").string
    closedpos = soup.find(id="bots-bot-positions-closedpos")
    bd = closedpos.find_all('bd', class_="dim-scroller")
    rows = bd[0].find_all("row", class_="pos")
    #print("tradeno\tbot\tsym\texp\tstrat\tpostext\tstatus\tclosedate\tqty\tcost\tcostdesc\tcomm\tpnl")
    print("tradeno\tbot\tsym\texp\tstrat\tpostext\tstatus\tclosedate\tqty\tcost\tcostdesc\tpnl")
    tradeno = 1;
    for row in rows:
        #print(type(pos.bd.div.div))
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
         
        if "Canceled" == status: continue  # Skip Canceled orders

        strat_qty = 0  #contract quantity for a strategy
        if 'Spread' in strat:
            strat_qty = 2
        elif 'Iron' in strat:
            strat_qty = 4
        elif 'Long Call' in strat or 'Long Put' in strat:
            strat_qty = 1

        # Assuming commissions for both open and close positions
        # Expired positions are not accounted for so comms will be generated as if the there was a closing trade (todo: could fix this)
        # Equity positions assume 0 commissions
        # No ORF/SEC/TRF,etc fees are included in this amount
        #Note: no commissions are calculated currently; can't get a number extracted from beautifulsoup; what I am doing wrong?
        comm = Decimal(strat_qty) * Decimal(qty) * Decimal(2) * commpercontract
        #netpnl = Decimal(pnl) - comm
        print("{:d}\t{:s}\t{:s}\t{:s}\t{:s}\t{:s}\t{:s}\t{:s}\t{:s}\t{:s}\t{:s}\t{:s}"
              .format(tradeno, bot, sym, exp, strat, postext, status, closedate, qty, cost, costdesc, pnl))
        tradeno += 1
