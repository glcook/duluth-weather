#!/usr/bin/env python
# coding: utf-8


from bs4 import BeautifulSoup
import requests
import datetime


# Create list of dates in url query format for almanac.com from Jan 1 1990 to May 31 2022

start_date = datetime.datetime(1990, 1, 1, 0, 0, 0, 0)
# end_date = datetime.datetime(2022, 6, 1, 0, 0, 0, 0) # Use June 1 as end bc loop will not execute last for last date
end_date = datetime.datetime(1990, 1, 3, 0, 0, 0, 0) # Use June 1 as end bc loop will not execute last for last date

delta = end_date - start_date
num_days = delta.days

date_list = []

for i in range(num_days):
    cur_date = start_date + datetime.timedelta(days=i)
    date_list.append(cur_date.strftime('%Y-%m-%d'))

# Scrape data for each date from almanac.com and store in dictionary

# Create text file to write data to; write headers
with open('weather_data.txt', 'w') as f:
    f.write('date,min_temp,mean_temp,max_temp,total_precip,visibilty,snow_depth,mean_wind_spd,max_sus_wind_spd\n')

# Searh url for almanac.com weather history, will append date to end
base_url = "https://www.almanac.com/weather/history/MN/Duluth/"
day = 0 # Counter for loop

strt_stmp = datetime.datetime.now() # Start timestamp of scraping

for d in date_list:
    # Get current day data from url, store in dictionary
    url = base_url + d
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")

    cur_headers = []
    for header in doc.find_all('th'):
        if (header.h3 is not None):
            cur_headers.append(header.contents[0].string)

    cur_data = []
    for i in doc.find_all('td'):
        cur_data.append(i.p.contents[0].string)

    weather_data = {}
    for hdr, dta in zip(cur_headers, cur_data):
        weather_data[hdr] = dta

    # Append data from dictionary to text csv file
    with open('weather_data.txt', 'a') as f:
        write_str = d + ','
        write_str += weather_data['Minimum Temperature'] + ','
        write_str += weather_data['Mean Temperature'] + ','
        write_str += weather_data['Maximum Temperature'] + ','
        write_str += weather_data['Total Precipitation'] + ','
        write_str += weather_data['Visibility'] + ','
        write_str += weather_data['Snow Depth'] + ','
        write_str += weather_data['Mean Wind Speed'] + ','
        write_str += weather_data['Maximum Sustained Wind Speed'] + '\n'
        f.write(write_str)

    # Print scraping status and increment counter
    pct_complete = float(day / num_days)
    tmstmp = datetime.datetime.now()
    run_time = tmstmp - strt_stmp
    day += 1

    print(f"{d} data fetched ###### {pct_complete:.2%} complete ###### elapsed time: {run_time}")
