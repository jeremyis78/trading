# trading

A simple repository of helpful trading tools.

## oa-positions-parser.py
This script is for those users with an [OptionAlpha](https://optionalpha.com) subscription who would like to 
download the trades their bot or bots have made into Excel or Sheets. Several of us are eagerly awaiting a Download
button on the Positions page but until then you can use this script.  If you trade options systematically
and don't have an account and want the help of automating much of the mundane parts of your option 
trading, check them out!

Additional prerequisites before you can run this script:

A) Before you can use this script you will need Python 3 installed.
You can check if Python is installed by following this: https://blog.finxter.com/how-to-check-your-python-version/
If you don't have it installed, install Python by visiting https://www.python.org/downloads/ and finding the Download button/link.
Additionally, after you've installed python, you'll need the beautifulsoup4 and lxml libraries.
Open a Terminal or CMD and run:

```pip install beautifulsoup4```

and

```pip install lxml```


B) You'll need to save the file 'oa-positions-parser.py' on your computer somewhere and remember where you put it.
I'd recommend putting in your home directory (~ on Mac or %USERPROFILE% on Windows) since this is where you'll be
when you open Terminal or CMD to run the script.

C) You'll need to produce the HTML file to pass to the script. 
  1) Visit your bot's positions page (e.g. https://app.optionalpha.com/bots/bot/BOTXXXXX/positions),
  2) Scroll down and click "Load More" until all positions are on screen
  3) Then save that page as an html file (File|Save Page as...). 
  4) Choose a filename with no spaces (maybe save as the my-bot-name.html) to make things easier later when you run the script.
Note: there's a [bug in Chrome](https://support.google.com/chrome/thread/4239329/chrome-webpage-save-as-for-webpage-html-only-option-no-longer-works?hl=en)
where you must save as "Webpage, Complete" in order to get the HTML file saved 
properly (you can't use "Webpage, HTML Only" until they fix the bug). 
Note: since this is a "screen scraper" script the only data available is what's visible
on that positions page. For instance, there's no opening date of the trade (or times)
on that page.


### Usage
python oa-positions-parser.py -h
```usage: oa-positions-parser.py [-h] [--csv] file

Parses the closed positions found on the positions page of an OptionAlpha bot.

positional arguments:
file        HTML file saved from OA bots positions page

optional arguments:
-h, --help  show this help message and exit
--csv       Output CSV instead of the default TSV (tab-separated values)

Examples (copies script output to clipboard):
(Windows): python oa-positions-parser.py %USERPROFILE%/Downloads/my-bot-name.html|clip
or
(MAC): python oa-positions-parser.py ~/Downloads/my-bot-name.html|pbcopy

Then open Excel/Sheets and paste.  Done.

You can also export as CSV but it doesn't play as nice with Excel or Sheets by default:
python oa-positions-parser.py --csv ~/Downloads/my-bot-name.html
```

### Sample usage showing TSV output
```
python oa-positions-parser.py files/tc0dte.html
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


### Import trades to Excel or Sheets (using clip or pbcopy)
You wisely saved 'tc0dte.html' (no spaces) in the default download directory and now want to 
copy/import those trades into Excel or Sheets.  

Step 0:
Open a terminal (see Open a Terminal down below if you're unfamiliar)

Step 1:
Run the appropriate command below 
**Note the command ends with |clip or |pbcopy. This is important. Be sure not to edit that out
when you change the filename to your file**

```python oa-positions-parser.py %USERPROFILE%/Downloads/tc0dte.html|clip``` (Windows)

```python oa-positions-parser.py ~/Downloads/tc0dte.html|pbcopy``` (Mac)

Step 2:
Open Excel or Sheets file you want to use

Step 3:
Windows: Ctrl + V    (Paste)
Mac    : Command + V (Paste)

Step 4:
Voila!  All your trades from the bot are pasted into the active sheet.

### Open a Terminal
If you're unfamiliar with running commands like this, try these useful articles:

Open Terminal on Windows: https://docs.microsoft.com/en-us/windows/terminal/
Open CMD on Windows: https://www.lifewire.com/how-to-open-command-prompt-2618089

Open Terminal on Mac: https://support.apple.com/guide/terminal/open-or-quit-terminal-apd5265185d-f365-44cb-8b09-71a064a42125/mac

clip: https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/clip
pbcopy: https://osxdaily.com/2007/03/05/manipulating-the-clipboard-from-the-command-line/