#!/bin/bash
# Compute US Federal Holidays

YEAR=$1  # YYYY format (e.g. 2024)
OUTPUT_FMT="+%a, %d %b %Y %z"

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

# Compute the observed holiday from a fixed date.
observed_date(){ # params yyyy, mm, dd
  YYYY=$1
  MM=$2
  DD=$3
  HOLIDAY=${YEAR}-${MM}-${DD}
  DOW=$(date -j -v${MM}m -v${DD}d -v${YYYY}y '+%a')  # Sat, Sun, Mon, etc

  # echo -n "$HOLIDAY is on $DOW; observed on "

  case $DOW in

    Sun)
      # Add one day to $holiday
      OBSERVED_DD=$((DD+1))
      printf "%d-%02d-%02d (observed)" ${YEAR} ${MM} ${OBSERVED_DD}
      ;;

    Sat)
      # Subtract one day to $holiday
      OBSERVED_DD=$((DD-1)) 
      printf "%d-%02d-%02d (observed)" ${YEAR} ${MM} ${OBSERVED_DD}   
      ;;

    *)
      echo -n "$HOLIDAY"
      ;;
  esac
}

# New Year's Day is always Jan 1st, observed holiday may be day before or after
#actual="$YEAR-01-01"
#observed=$(observed_date $YEAR 01 01)
echo "Jan1: $(observed_date $YEAR 01 01)"


# MLK Jr Day: 3rd Monday in January
MM=1
echo 3MJan: Jan $(ncal $MM $YEAR| grep "^Mo"|tr -s " "|cut -d' ' -f 4) 
#                     \            \     \___________________\/    
#                   Jaunary      All Mondays               3rd Monday only

# Washington's Birthday/President's Day: 3rd Monday in February
MM=2
echo 3MFeb: Jan $(ncal $MM $YEAR| grep "^Mo"|tr -s " "|cut -d' ' -f 4)
#                     \            \      \___________________\/
#                   February      All Mondays               3rd Monday only

# Memorial Day: Last Monday in May
MM=5
echo LMMay: May $(ncal $MM $YEAR| grep "^Mo"|tr -s " "|awk -F' ' '{print $NF}')
#                     \            \    \___________________\/
#                     May      All Mondays               Last one (aka last field) 

# Juneteenth is always June 19th, observed holiday may be day before or after
MM=6
#observed=$(observed_date $YEAR $MM 19)
echo "Jun19: $(observed_date $YEAR $MM 19)" 

# Independence Day is always July 4th, observed holiday may be day before or after
MM=7
#observed=$(observed_date $YEAR $MM 4)
echo "Jul4: $(observed_date $YEAR $MM 4)"
 
# Labor Day: First Monday in Sep
MM=9
echo 1MSep: Sep $(ncal $MM $YEAR| grep "^Mo"|tr -s " "|cut -d' ' -f 2)
#                     \            \       \___________________\/
#                   September  All Mondays                   1st one

# Columbus / Indigenous Peoples Day: Second Monday in October
MM=10
echo 2MOct: Oct $(ncal $MM $YEAR| grep "^Mo"|tr -s " "|cut -d' ' -f 3)
#                     \            \         \___________________\/
#                   October      All Mondays                  2nd one

# Veterans' Day is always Nov 11th, observed holiday may be day before or after
MM=11
echo "Nov11: $(observed_date $YEAR $MM 11)"

# Thanksgiving Day: Fourth Thursday in November
echo 4TNov: Nov $(ncal $MM $YEAR| grep "^Th"|tr -s " "|cut -d' ' -f 5)
#                     \            \        \___________________\/
#                   November    All Thursdays               4th one

# Christmas Day is always Dec 25th, observed holiday may be day before or after
echo "Dec25: $(observed_date $YEAR 12 25)"
