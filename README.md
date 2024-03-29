# trading

A simple repository of helpful trading tools.

## oa-positions-parser.py


__UPDATE: The Oct 15, 2022 release is so awesome--1 minute intervals and so many other enhancements and improvements!  
        But sadly, it broke this script. I'm working on a fix but give me a few days or a week or so; I've got other commitments. 
        A few hours later: so while there is new data available on the closed positions page (the exact time of position 
        closing (e.g. Oct 13, 2022 at 1:00pm) there are crucial pieces of info now missing, especially if 
        you plan to use the data for external analysis in a spreadsheet: 1) the quantity, 2) the opening credit (or debit). Unless 
        OA adds them back this script may not be worth keeping up. As such, I'm stopping development on this for now.
        If things change let me know and I may resurrect it.__

This script is for those users with an [OptionAlpha](https://optionalpha.com) subscription who would like to 
download the trades their bot or bots have made into Excel or Sheets. Several of us are eagerly awaiting a Download
button on the Positions page but until then you can use this script.  If you trade options systematically
and don't have an account and want the help of automating much of the mundane parts of your option 
trading, check them out!

Additional prerequisites before you can run this script:

A) Before you can use this script you will need Python 3 installed.
You can check if Python is installed by following this: https://blog.finxter.com/how-to-check-your-python-version/
If you don't have it installed, install Python by visiting https://www.python.org/downloads/ and finding the Download button/link.
Additionally, after you've installed python, you'll need the beautifulsoup library.
Open a Terminal or CMD and run:

```pip install beautifulsoup4```


B) You'll need to save the file 'oa-positions-parser.py' on your computer somewhere and remember where you put it.
I'd recommend putting in your home directory (~ on Mac or %USERPROFILE% on Windows) since this is where you'll be
when you open Terminal or CMD to run the script.

C) You'll need to produce the HTML file to pass to the script. 
  1) Visit your bot's positions page (e.g. https://app.optionalpha.com/bots/bot/BOTXXXXX/positions),
  2) Scroll down and click "Load More" until all positions are on screen
  3) Then save that page as an html file (File|Save Page as...). 
  4) Choose a filename with no spaces (maybe save as the my-bot-name.html) to make things easier later when you run the script.

**NOTE: There's a [bug in Chromium-based browsers (including Chrome, Brave and Edge)](https://support.google.com/chrome/thread/4239329/chrome-webpage-save-as-for-webpage-html-only-option-no-longer-works?hl=en)
where you must save as "Webpage, Complete" in order to get the HTML file saved 
properly (you can't use "Webpage, HTML Only" until they fix the bug).**

Note: Since this is a "screen scraper" script the only data available is what's visible
on that positions page. For instance, there's no opening date of the trade (or times)
on that page.**


### Usage
python oa-positions-parser.py -h
```
usage: oa-positions-parser.py [-h] [--csv] [--fees CENTS] file

Parses the closed positions found on the positions page of an OptionAlpha bot.

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

positional arguments:
  file          HTML file saved from OA bots positions page

optional arguments:
  -h, --help    show this help message and exit
  --csv         Output CSV instead of the default TSV (tab-separated values)
  --fees CENTS  Trading fees per contract in cents (e.g. --fees 35, would mean 35 cents/contract)

usage: oa-positions-parser.py [-h] [--csv] file

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
```

### Sample usage: showing TSV output
```
$ python oa-positions-parser.py files/tc0dte.html
tradeno	bot	sym	exp	strat	postext	status	closedate	qty	cost	costdesc	pnl
1	TC 0DTE	SPY	7/5	Short Call Spread	-381, +386	Closed	Jul 5	13	195	Credit	-312
2	TC 0DTE	SPY	7/5	Short Put Spread	-368, +363	Closed	Jul 5	13	312	Credit	299
3	TC 0DTE	SPY	7/1	Short Put Spread	-372, +367	Closed	Jul 1	13	377	Credit	364
4	TC 0DTE	SPY	7/1	Short Call Spread	-384, +389	Closed	Jul 1	12	168	Credit	144
5	TC 0DTE	SPY	6/30	Short Call Spread	-382, +387	Closed	Jun 30	12	300	Credit	180
6	TC 0DTE	SPY	6/30	Short Put Spread	-367, +362	Closed	Jun 30	12	156	Credit	144
7	TC 0DTE	SPY	6/29	Short Call Spread	-386, +391	Closed	Jun 29	12	180	Credit	180
8	TC 0DTE	SPY	6/29	Short Put Spread	-373, +368	Closed	Jun 29	12	324	Credit	288
9	TC 0DTE	SPY	6/27	Short Call Spread	-395, +400	Closed	Jun 27	11	198	Credit	187
10	TC 0DTE	SPY	6/27	Short Put Spread	-382, +377	Closed	Jun 27	11	209	Credit	187
11	TC 0DTE	SPY	6/24	Short Put Spread	-377, +372	Closed	Jun 24	12	216	Credit	192
12	TC 0DTE	SPY	6/24	Short Call Spread	-388, +393	Closed	Jun 24	12	252	Credit	-636
13	TC 0DTE	SPY	6/22	Short Put Spread	-365, +360	Closed	Jun 22	12	180	Credit	168
14	TC 0DTE	SPY	6/22	Short Call Spread	-378, +383	Closed	Jun 22	12	264	Credit	-864
15	TC 0DTE	SPY	6/21	Short Call Spread	-380, +385	Closed	Jun 21	12	132	Credit	120
16	TC 0DTE	SPY	6/21	Short Put Spread	-367, +362	Closed	Jun 21	12	204	Credit	192
17	TC 0DTE	SPY	6/17	Short Put Spread	-360, +355	Closed	Jun 17	12	252	Credit	216
18	TC 0DTE	SPY	6/17	Short Call Spread	-376, +381	Closed	Jun 17	12	252	Credit	228
19	TC 0DTE	SPY	6/15	Short Put Spread	-366, +361	Closed	Jun 15	12	324	Credit	-36
20	TC 0DTE	SPY	6/15	Short Call Spread	-389, +394	Closed	Jun 15	12	408	Credit	168
```

### Sample usage: exporting to file (including estimated fees of $0.461/contract)
NOTE: there are two additional columns at the end: fees and netpnl (netpnl is the sum of pnl and fees)
```
$ python oa-positions-parser.py --fees 46.1 ~/Downloads/tc0dte-margin.html
$ head -16 tc0dte-margin.tsv
tradeno	bot	sym	exp	strat	postext	status	closedate	qty	cost	costdesc	pnl	fees	netpnl
1	TC 0DTE	SPY	8/22	Short Call Spread	-421, +426	Expired	Aug 22	11	165	Credit	165	-10.142	154.858
2	TC 0DTE	SPY	8/22	Short Put Spread	-412, +407	Closed	Aug 22	11	143	Credit	-10	-20.284	-30.284
3	TC 0DTE	SPY	8/19	Short Call Spread	-429, +434	Expired	Aug 19	11	99	Credit	99	-10.142	88.858
4	TC 0DTE	SPY	8/19	Short Put Spread	-419, +414	Closed	Aug 19	11	132	Credit	99	-20.284	78.716
5	TC 0DTE	SPY	8/17	Short Call Spread	-431, +436	Expired	Aug 17	11	154	Credit	154	-10.142	143.858
6	TC 0DTE	SPY	8/17	Short Put Spread	-421, +416	Canceled	Aug 17	0	0	Credit	0	0	0
7	TC 0DTE	SPY	8/15	Short Put Spread	-421, +416	Canceled	Aug 15	0	0	Credit	0	0	0
8	TC 0DTE	SPY	8/15	Short Call Spread	-429, +434	Closed	Aug 15	12	216	Credit	-480	-22.128	-502.128
9	TC 0DTE	SPY	8/12	Short Put Spread	-418, +413	Expired	Aug 12	12	180	Credit	180	-11.064	168.936
10	TC 0DTE	SPY	8/12	Short Call Spread	-426, +431	Closed	Aug 12	12	180	Credit	-192	-22.128	-214.128
11	TC 0DTE	SPY	8/10	Short Call Spread	-423, +428	Closed	Aug 10	11	121	Credit	110	-20.284	89.716
12	TC 0DTE	SPY	8/10	Short Put Spread	-412, +407	Closed	Aug 10	11	110	Credit	99	-20.284	78.716
13	TC 0DTE	SPY	8/8	Short Call Spread	-421, +426	Expired	Aug 8	11	121	Credit	121	-10.142	110.858
14	TC 0DTE	SPY	8/8	Short Put Spread	-412, +407	Closed	Aug 8	11	198	Credit	-209	-20.284	-229.284
15	TC 0DTE	SPY	8/5	Short Call Spread	-416, +421	Expired	Aug 5	11	154	Credit	154	-10.142	143.858
$
```

### Export to a file (Step by step)
You wisely saved 'my-bot-name.html' (no spaces) in the default download directory and now want to 
copy/import those trades into Excel or Sheets.  

Step 0:
Open a terminal (see Open a Terminal down below if you're unfamiliar)

Step 1:
Run the appropriate command below 
**NOTE: the command ends with a file redirection ("> filename.tsv"). This is important. Be sure not to edit that out
when you change the filename to your file**

```python oa-positions-parser.py %USERPROFILE%/Downloads/my-bot-name.html > my-bot-name.tsv``` (Windows)

```python oa-positions-parser.py ~/Downloads/my-bot-name.html > my-bot-name.tsv``` (Mac)

Step 2:
Open the newly created file in Excel or Sheets (in this case, my-bot-name.tsv)

Alternatively, you can save CSV files if you'd like.

```python oa-positions-parser.py --csv %USERPROFILE%/Downloads/my-bot-name.html > my-bot-name.csv``` (Windows)

```python oa-positions-parser.py --csv ~/Downloads/my-bot-name.html > my-bot-name.csv``` (Mac)

NOTE: The default separator that Excel/Sheets uses when you paste into a sheet
is the tab character. That's the reason the script's default is TSV output.


### Open a Terminal
If you're unfamiliar with running commands like this, try these useful articles:

Open Terminal on Windows: https://docs.microsoft.com/en-us/windows/terminal/
Open CMD on Windows: https://www.lifewire.com/how-to-open-command-prompt-2618089

Open Terminal on Mac: https://support.apple.com/guide/terminal/open-or-quit-terminal-apd5265185d-f365-44cb-8b09-71a064a42125/mac

### Advanced Usage
If you're savvy at the command line or aspire to be you're either aware of or can 
learn about the tools to capture the standard output and copy it to the clipboard. 
NOTE: Using clip on Windows may be problematic (John told me he found it inserts 
an extra newline between trades in essence, "double-spacing" your trades when 
pasted into Excel, but capturing standard out to a file appears to not have this issue.
I myself am unsure how this can be; appears contradictory).

(Windows) clip: https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/clip

(Mac) pbcopy: https://osxdaily.com/2007/03/05/manipulating-the-clipboard-from-the-command-line/
