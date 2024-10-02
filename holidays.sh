#!/bin/bash
# Compute US Federal Holidays
# Requires ncal command and MacOS/BSD-specific date command.
#
# Usage: holidays.sh YYYY [+output_fmt]
# Example 1: ./holidays.sh 2022
# Example 2: ./holidays.sh 2024 "+%a, %b %d %Y %z"
# Example 3: for yr in $(seq 2021 2028); do ./holidays.sh $yr "+%a, %Y-%m-%d" ;  done;
# See man date(1) for +output_fmt.
#
# The default output is "+%a, %b %d" for relative dates (e.g., last Monday in May).
# The last Monday in May would produce a line like "Mon, May 30" leaving out the year.
# If the holiday is an absolute date (e.g. Jan 1st, Jul 4th) and it falls on a weekend
# then " %Y $adj_days" would be appended, adding the year as well as the number of days
# adjusted (+/-adj_days).
#
# It properly handles the case where an observed holiday can occur in the previous
# month or even the previous month of the previous year.
# For example, New Year's Day in 2022 fell on Saturday so the holiday was observed
# on Friday, Dec 31, 2021; this script would indicate "Fri, Dec 31 2021 -1"
# including the year as well as the relative offset to indicate this is an observed
# holiday, not the actual date of the holiday.
#
# Bugs: Presently, all holidays as of 2021 are listed; calling this with the year
# 2020 would still list Juneteenth which was not officially recognized until 2021.
# TODO: make the output format configurable/machine-readable/ISO format with a
# TODO: second argument

YEAR=${1}  # YYYY format (e.g. 2022)
OUTPUT_FMT=${2} #e.g., "+%a, %d %b %Y %z"
DEFAULT_FMT="+%a, %d %b %Y"

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
      then date -v"${day}"d -v"${month}"m -v"${year}"y -v${adj_days}d "$DEFAULT_FMT ${adj_days}";
      else date -v"${day}"d -v"${month}"m -v"${year}"y -v${adj_days}d "$OUTPUT_FMT";
    fi
  else
    if [ "$OUTPUT_FMT" = "" ] ;
      then echo "$dow, $month $day";
           #date -v"${day}"d -v"${month}"m -v"${year}"y "$DEFAULT_FMT";
      else date -v"${day}"d -v"${month}"m -v"${year}"y "$OUTPUT_FMT";
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
    then echo "$dow, $month $day";
    else date -v"${day}"d -v"${month}"m -v"${year}"y "$OUTPUT_FMT";
  fi
  #date -v"${day}"d -v"${month}"m -v"${year}"y "$OUTPUT_FMT"
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
