# Sean McGlincy
import math
import numpy as np
import pandas as pd
from scipy import spatial
from datetime import datetime
import sys
import warnings
if not sys.warnoptions:
    warnings.simplefilter("ignore")


def reformat_data(weather_data):
    '''  Seperates the Date and Time.  Time is added a a new column in the data frame '''
    '''  The colins (:) are removed from the time stamp for comparing to Sunrise and Sunset'''
    assert (len(weather_data) != 0)
    for key, value in weather_data.items():
        value["DATE"], value["TIME"] = value["DATE"].str.split("\s+", 1).str
        value["TIME"] = value["TIME"].str.replace(':', '').astype(int)
    return weather_data

def check_date(d):

    '''   This checks the date to insure that it's valid   '''
    '''    Cite: https://stackoverflow.com/questions/18539266/how-to-validate-a-specific-date-and-time-format-using-python  '''
    try:
        datetime.strptime(d, '%m/%d/%y')
        return True
    except ValueError:
        return False


def avg_temp(data, date):
    assert (len(data) != 0)
    assert (check_date(date))

    '''   Returns a dict structure of AVG & STD of the Bulb Temp between sunrise and sunset.  '''
    results = {}
    results["TEMP_AVG"] = {}
    results["TEMP_STD"] = {}

    ''' Get just the dates being used and the time of Sunset and Sunrise'''
    df = data.loc[date == data["DATE"]]
    sunrise = min(df["DAILYSunrise"])
    sunset = max(df["DAILYSunset"])

    '''   Returns a dataframe for time between Sunrise and Sunset'''
    df = df.loc[(df["TIME"] > sunrise) & (df["TIME"] < sunset)]

    '''   Convert column data to a long and replace NaN with Zero'''
    df["HOURLYDRYBULBTEMPF"] = pd.to_numeric(df["HOURLYDRYBULBTEMPF"], errors='coerce').fillna(0)
    df["HOURLYDRYBULBTEMPC"] = pd.to_numeric(df["HOURLYDRYBULBTEMPC"], errors='coerce').fillna(0)

    '''  Add data to dictionary'''
    results["TEMP_AVG"]["FAHRENHEIT"] = df["HOURLYDRYBULBTEMPF"].mean()
    results["TEMP_AVG"]["CELSIUS"]    = df["HOURLYDRYBULBTEMPC"].mean()
    results["TEMP_STD"]["FAHRENHEIT"] = df["HOURLYDRYBULBTEMPF"].std()
    results["TEMP_STD"]["CELSIUS"]    = df["HOURLYDRYBULBTEMPC"].std()
    return results

def wind_chill_equation(temp, velocity):
    ''''  WindChill Equation for USA 2001:  https://en.wikipedia.org/wiki/Wind_chill '''

    '''  Formats the numbers to floats before replacing NaN with Zero '''
    velocity = float(velocity)
    if math.isnan(velocity):
        velocity = 0
    temp = float(temp)
    if math.isnan(temp):
        temp = 0
    assert (isinstance(temp, float))
    assert (isinstance(velocity, float))

    '''  Calculates the Wind Chill Index and returns rounded to the nearest tenth'''
    velocity = velocity ** 0.16
    WC = 35.74 + 0.6215 * temp - 35.75 * velocity + 0.4275 * temp * velocity
    return round(WC, 1)

def wind_chill(data, date):
    assert (len(data) != 0)
    assert (check_date(date))

    ''''  Removes unwanted data'''
    data = data.loc[(date == data["DATE"])]

    '''  Gets the Hours for when the Dry Bulb Air Tempature dropped below 40 degrees.
         NaN tempature values are set to 1000 degrees to ensure they are not picked for wind chill measurments
         The Hourly Wind Speed is formated to longs and NaN is replaced with Zeros
         I pick Wind Speed over Wind Gust because Wind Gusts are full of mostly NaN
    '''
    data = data.loc[(pd.to_numeric(data["HOURLYDRYBULBTEMPF"], errors='coerce').fillna(1000).astype(np.int64) < 40)]
    data["HOURLYWindSpeed"] = pd.to_numeric(data["HOURLYWindSpeed"], errors='coerce').fillna(0)

    '''  Create an array of Zero.  If there are no tempatures below 40 degrees return an array with 0.0
         If there is data, replace the array with an array of wind chill measurements
    '''
    WC = [0.0]
    if data.shape[0] > 0:
        WC = data.apply(lambda x: wind_chill_equation(x["HOURLYDRYBULBTEMPF"], x["HOURLYWindSpeed"]), axis=1)
    return list(WC)



def cos(x,y):
    if x is None or y is None:
        return 0.0
    '''  This function returns the distance.  Subtract 1 to calculate the cosine similarity'''
    cos = 1 - spatial.distance.cosine(x, y)

    if np.isfinite(cos):
        return cos
    return 0.0



def process_data(df, date):
    assert (len(df) != 0)
    assert (check_date(date))

    '''  Call Methods 1 & 2 for temp during the day and windchill   '''
    temp_data  =  avg_temp(df, date)
    wc = wind_chill(df, date)

    '''  Remove all columns from dataframe except the ones we want
         The data is then converted to floats and the mean is taken for each column.  
         NaN is replaced with Zeros
         This will insure that each dat has the same number of indexes   '''

    df = df.loc[:, ["HOURLYVISIBILITY" , "HOURLYDRYBULBTEMPF", "HOURLYWETBULBTEMPF", "HOURLYRelativeHumidity", "HOURLYWindSpeed", "HOURLYWindDirection", "HOURLYWindGustSpeed", "DAILYSunrise", "DAILYSunset"]]
    df["HOURLYVISIBILITY"] = pd.to_numeric(df["HOURLYVISIBILITY"], errors='coerce')
    df["HOURLYDRYBULBTEMPF"] = pd.to_numeric(df["HOURLYDRYBULBTEMPF"], errors='coerce')
    df["HOURLYWETBULBTEMPF"] = pd.to_numeric(df["HOURLYWETBULBTEMPF"], errors='coerce')
    df["HOURLYRelativeHumidity"]  = pd.to_numeric(df["HOURLYRelativeHumidity"], errors='coerce')
    df["HOURLYWindSpeed"] = pd.to_numeric(df["HOURLYWindSpeed"], errors='coerce')
    df["HOURLYWindDirection"] = pd.to_numeric(df["HOURLYWindDirection"], errors='coerce')
    df["HOURLYWindGustSpeed"] = pd.to_numeric(df["HOURLYWindGustSpeed"], errors='coerce')
    df["HOURLYWindGustSpeed"] = pd.to_numeric(df["DAILYSunrise"], errors='coerce')
    df["HOURLYWindGustSpeed"] = pd.to_numeric(df["DAILYSunset"], errors='coerce')

    '''  Create an array of statistical data:  Tempature:  Min, Max, Day_TEMP, Day_STD,  Windchile: Mean & STD < 40 degrees   '''
    row = [date]
    row.append(max(df["HOURLYDRYBULBTEMPF"]))
    row.append(min(df["HOURLYDRYBULBTEMPF"]))
    row.append(temp_data["TEMP_AVG"]["FAHRENHEIT"])
    row.append(temp_data["TEMP_STD"]["FAHRENHEIT"])
    row.append(np.mean(wc))
    row.append(np.std(wc))

    row.extend(df.fillna(0).as_matrix().mean(axis=0))
    return row


def similar_days(atl, tx, date):
    assert (len(weather_data) != 0)
    assert (check_date(date))

    ''''  This funcion will calculate the similarity between a day in ATL and all the days in Canada
          The function uses cosine similarity to compare the data between the two days and sorting the most similar days to the front of the list. 
          Before the cosine function can be called, the data will be reformed into arrays of a standard size and sequence.
    '''

    '''  Get all unique dates from data frame and iterate over them  '''
    similiarity = []
    X =  process_data( atl.loc[(date == atl["DATE"])], date)
    list_of_dates = tx['DATE'].unique()
    for i in range(len(list_of_dates)):

        '''   Removes all data except the target date.  Then calls a helper function  '''
        data = tx.loc[(list_of_dates[i] == tx["DATE"])]
        Y = process_data(data, list_of_dates[i])

        '''   Calls cosine similarity and the results are sorted as tuples in defending order.   (Similarity, Date)
              The most similar city is returned  
        '''
        C = cos(X[1:], Y[1:])
        similiarity.append((C, list_of_dates[i] ))
    similiarity.sort(key=lambda tup: tup[0], reverse=True)
    return similiarity[0][1]





if __name__ == "__main__":
    FILE_1 = "./data/1089419.csv"
    FILE_2 = "./data/1089441.csv"

    ''' Assert the files have more then two rows '''
    assert (sum(1 for row in FILE_1) > 2)
    assert (sum(1 for row in FILE_2) > 2)


    '''  Reads data in and stores it in a dict '''
    weather_data = {}
    weather_data["TX"] = pd.read_csv(FILE_1)
    weather_data["ATL"] = pd.read_csv(FILE_2)

    '''  Reformats Date and Time  '''
    weather_data = reformat_data(weather_data)


    '''  Method 1 '''
    temp_data = avg_temp(weather_data["ATL"], "10/3/17")
    print ("Method 1 Results:")
    print (temp_data["TEMP_AVG"]["FAHRENHEIT"])
    print (temp_data["TEMP_AVG"]["CELSIUS"])
    print (temp_data["TEMP_STD"]["FAHRENHEIT"])
    print (temp_data["TEMP_STD"]["CELSIUS"])

    '''  Method 2 '''
    print ("\nMethod 2 Results:")
    wc_tx   = wind_chill(weather_data["TX"], "1/1/08")
    wc_atl = wind_chill(weather_data["ATL"], "1/1/08")
    print (wc_tx)
    print (wc_atl)

    '''  Method 3 '''
    tx_day =similar_days(weather_data["ATL"], weather_data["TX"], "10/3/17")
    print ("\nMethod 3 Results:")
    print(tx_day)
    exit (0)


