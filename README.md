# trading

A simple repository of helpful trading tools.

## oa-positions-parser.py
This script is for those users with an [OptionAlpha](https://optionalpha.com) subscription who would like to download the
trades their bot or bots have made into Excel or Sheets. Several of us are eagerly awaiting a Download
button on the Positions page but until then you can use this script.  If you trade options systematically
and don't have an account and want to automate your option trades, check them out!

Additional prerequisites before you can run this script:
A) Before you can use this script you will need Python 3 installed.
You can check if Python is installed by following this: https://blog.finxter.com/how-to-check-your-python-version/
If you don't have it installed, install Python by visiting https://www.python.org/downloads/ and finding the Download button/link.

B) You'll need to save the file 'oa-positions-parser.py' on your computer somewhere and remember where you put it.
I'd recommend putting in your home directory (~ on Mac or %USERPROFILE% on Windows) since this is where you'll be
when you open Terminal or CMD to run the script.

C) You'll need to produce the HTML file to pass to the script. 
  1) Visit your bot's positions page (e.g. https://app.optionalpha.com/bots/bot/BOTXXXXX/positions),
  2) Scroll down and click "Load More" until all positions are on screen
  3) Then save that page as an html file (File|Save Page as...). 
  4) Choose a filename with no spaces (maybe save as the name-of-your-bot.html) to make things easier later when you run the script.
Note: there's a [bug in Chrome](https://support.google.com/chrome/thread/4239329/chrome-webpage-save-as-for-webpage-html-only-option-no-longer-works?hl=en)
where you must save as "Webpage, Complete" in order to get the HTML file saved 
properly (you can't use "Webpage, HTML Only" until they fix the bug). 
Note: since this is a "screen scraper" script the only data available is what's visible on that positions page. For instance,
we only get the close date of the trade--there's no close time or opening date/time--so the script can't compute things like 
Days or Minutes in Trade.


### Usage
python oa-positions-parser.py -h
```usage: oa-positions-parser.py [-h] file

Parses the closed positions found on the positions page of an OptionAlpha bot (produces TSV output suitable for import to Excel or Sheets).

positional arguments:
  file        HTML file saved from OA bots positions page

optional arguments:
  -h, --help  show this help message and exit

Example: python tc0dte-positions.html
```

### Sample usage showing TSV output
```
python oa-positions-parser.py files/tc0dte-beautified.txt
tradeno	bot	sym	exp	strat	postext	status	closedate	qty	cost	costdesc	pnl
1	unknown	SPY	7/5	Short Call Spread	-381, +386	Closed	Jul 5	13	195	Credit	-312
2	unknown	SPY	7/5	Short Put Spread	-368, +363	Closed	Jul 5	13	312	Credit	299
3	unknown	SPY	7/1	Short Put Spread	-372, +367	Closed	Jul 1	13	377	Credit	364
4	unknown	SPY	7/1	Short Call Spread	-384, +389	Closed	Jul 1	12	168	Credit	144
5	unknown	SPY	6/30	Short Call Spread	-382, +387	Closed	Jun 30	12	300	Credit	180
6	unknown	SPY	6/30	Short Put Spread	-367, +362	Closed	Jun 30	12	156	Credit	144
7	unknown	SPY	6/29	Short Call Spread	-386, +391	Closed	Jun 29	12	180	Credit	180
8	unknown	SPY	6/29	Short Put Spread	-373, +368	Closed	Jun 29	12	324	Credit	288
9	unknown	SPY	6/27	Short Call Spread	-395, +400	Closed	Jun 27	11	198	Credit	187
10	unknown	SPY	6/27	Short Put Spread	-382, +377	Closed	Jun 27	11	209	Credit	187
11	unknown	SPY	6/24	Short Put Spread	-377, +372	Closed	Jun 24	12	216	Credit	192
12	unknown	SPY	6/24	Short Call Spread	-388, +393	Closed	Jun 24	12	252	Credit	-636
13	unknown	SPY	6/22	Short Put Spread	-365, +360	Closed	Jun 22	12	180	Credit	168
14	unknown	SPY	6/22	Short Call Spread	-378, +383	Closed	Jun 22	12	264	Credit	-864
15	unknown	SPY	6/21	Short Call Spread	-380, +385	Closed	Jun 21	12	132	Credit	120
16	unknown	SPY	6/21	Short Put Spread	-367, +362	Closed	Jun 21	12	204	Credit	192
17	unknown	SPY	6/17	Short Put Spread	-360, +355	Closed	Jun 17	12	252	Credit	216
18	unknown	SPY	6/17	Short Call Spread	-376, +381	Closed	Jun 17	12	252	Credit	228
19	unknown	SPY	6/15	Short Put Spread	-366, +361	Closed	Jun 15	12	324	Credit	-36
20	unknown	SPY	6/15	Short Call Spread	-389, +394	Closed	Jun 15	12	408	Credit	168
```


### Copy results to clipboard
You wisely saved 'tc0dte.html' (no spaces) in the default download directory and now want to 
copy those trades into Excel or Sheets.  Run the appropriate command and then paste the results into
your spreadsheet.

```python oa-positions-parser.py ~/Downloads/tc0dte.html|pbcopy``` (Mac)

```python oa-positions-parser.py %USERPROFILE%/Downloads/tc0dte.html|clip``` (Windows)
