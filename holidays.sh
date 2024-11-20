#!/bin/bash
# Compute US Federal Holidays, indicating the actual weekday a holiday is observed if it falls on a weekend
# Requires ncal command and MacOS/BSD-specific date command.
#
# Usage: holidays.sh YYYY [+output_fmt]
# Example 1: ./holidays.sh 2022
# Example 2: ./holidays.sh 2024 "+%a, %b %d %Y %z"
# Example 3: ./holidays.sh 2027 "+%Y-%m-%d"
# Example 4: for yr in $(seq 2021 2028); do ./holidays.sh $yr "+%a, %Y-%m-%d" ;  done;
# See man date(1) for +output_fmt.
#
# The default output is in CSV format and the columns would be:
# observed-weekday,day-of-week,month-name,day-of-month,actual-holiday-offset
# Example rows:
# 2021-12-31, Fri, Dec, 31, -1         (observed weekday is Friday, actual holiday is Saturday)
# 2022-01-17, Mon, Jan, 17, 0          (no adjustment needed)
# 2027-07-05, Mon, Jul, 05, +1         (observed weekday is Monday, actual holiday is Sunday
#
# The inclusion of redundant date data in the default CSV output provides flexibility and helps
# to explain/understand the calculation behind the scenes and offer the ability to input to a
# an external tool, like a spreadsheet.
# For instance, this script should never produce Sat or Sun in the day-of-week column as its sole
# purpose is computing the weekday date that is observed to recognize a holiday that occurs on
# Sat or Sun.
#
# This script also properly handles the case where an observed holiday can occur in the previous
# month or even the previous month of the previous year.
# For example, New Year's Day in 2022 fell on Saturday so the holiday was observed
# on Friday, Dec 31, 2021; this script would indicate "2021-12-31, Fri, Dec, 31, -1"
# where the actual-holiday-offset (in days) is non-zero to indicate this is an observed holiday,
# not the actual date of the holiday which would be 2021-12-31 - (-1) = 2022-01-01 (Saturday).
#
# To see dates in a custom format, use an appropriate output_fmt, for instance, as seen in Example 2.
#
# Bugs:
# 1) Presently, all holidays as of 2021 are listed; calling this with the year
# 2020 would still list Juneteenth which was not officially recognized until 2021.
#
# 2) When calling this script for just a single year, it's possible the following New Year's holiday
# will be observed in the current year.  For instance, requesting only the year 2021, would not
# indicate that Dec 31, 2021 is the observed weekday of New Year's day for the following year.  To correctly
# list all observed holidays over a span of dates be sure to include the surrounding or following
# years as demonstrated by Example 4.
#
# 3) It does not (yet) compute market half days where the market closes
# at 1pm ET instead of 4pm ET  (e.g., day before Thanksgiving or other market half days).
#
# 4) The actual-holiday-offset is only available when using the default format.

YEAR=${1}  # YYYY format (e.g. 2022)
OUTPUT_FMT=${2} #e.g., "+%a, %d %b %Y %z"
DEFAULT_FMT="+%Y-%m-%d, %a, %b, %d"

display_date(){   # params: ISO_DATE (YYYY-MM-DD)
  d=$1
  yyyy=${d:0:4}   # YYYY
  mm=${d:5:2}     # MM
  dd=${d:8:2}     # DD
  msg=$2          # e.g. (observed) or blank
  #echo "${yyyy} ${mm} ${dd} '$OUTPUT_FMT'"
  dt=$(date -j -v${mm}m -v${dd}d -v${yyyy}y "$OUTPUT_FMT")
  echo $dt $MSG
}

# Compute the observed holiday from an absolute or fixed date.
observe_date(){ # params yyyy, mm, dd
  month=$1
  day=$2
  year=$3

  dow=$(date -j -v"${month}"m -v"${day}"d -v"${year}"y '+%a')  # Sat, Sun, Mon, etc

  adj_days=0
  case $dow in
  Sun) adj_days=+1; ;; # move to Monday
  Sat) adj_days=-1; ;; # move to Friday
  esac

  if [ "$adj_days" -ne "0" ] ;
  then # adjust the date by adj_days
    if [ "$OUTPUT_FMT" = "" ] ;
      then date -v"${year}"y -v"${month}"m -v"${day}"d -v${adj_days}d "$DEFAULT_FMT, ${adj_days}";
      else date -v"${year}"y -v"${month}"m -v"${day}"d -v${adj_days}d "$OUTPUT_FMT";
    fi
  else
    if [ "$OUTPUT_FMT" = "" ] ;
      then date -v"${year}"y -v"${month}"m -v"${day}"d "$DEFAULT_FMT, 0";
      else date -v"${year}"y -v"${month}"m -v"${day}"d "$OUTPUT_FMT";
    fi
  fi
}

# Compute the relative date given: month, ordinal, day of week
#    Example args: Nov 3rd Mon -> 3rd Monday in November
#                  May Lst Thu -> Last Thursday in May
compute_date(){
  month=$1
  ordinal=$2
  dow=$3
  year=$4

  ordinal_no=${ordinal:0:1}
  field=$((ordinal_no+1))
  dow_days=$(ncal "$month" "$year"| grep "^${dow:0:2}"|tr -s " ")

  if [ "$ordinal" = "Lst" ]
  then
    day=$(echo "$dow_days"|awk -F' ' '{print $NF}')
  else
    day=$(echo "$dow_days"|cut -d' ' -f "$field")
  fi

  if [ "$OUTPUT_FMT" = "" ] ;
    then date -v"${year}"y -v"${month}"m -v"${day}"d "$DEFAULT_FMT, 0";
    else date -j -f "%d-%b-%Y" "${day}-${month}-${year}" "$OUTPUT_FMT";
  fi
}

observe_date "Jan" 1 "$YEAR"           # Abs: New Year's Day
compute_date "Jan" "3rd" "Mon" "$YEAR" # Rel: MLK Jr Day: 3rd Monday in January
compute_date "Feb" "3rd" "Mon" "$YEAR" # Rel: Washington's Birthday/President's Day: 3rd Monday in February
compute_date "May" "Lst" "Mon" "$YEAR" # Rel: Memorial Day: Last Monday in May
observe_date "Jun" 19 "$YEAR"          # Abs: Juneteenth National Independence Day
observe_date "Jul" 4 "$YEAR"           # Abs: Independence Day
compute_date "Sep" "1st" "Mon" "$YEAR" # Rel: Labor Day
compute_date "Oct" "2nd" "Mon" "$YEAR" # Rel: Columbus / Indigenous Peoples Day: Second Monday in October
observe_date "Nov" 11 "$YEAR"          # Abs: Veterans' Day
compute_date "Nov" "4th" "Thu" "$YEAR" # Rel: Thanksgiving Day
observe_date "Dec" 25 "$YEAR"          # Abs: Christmas
