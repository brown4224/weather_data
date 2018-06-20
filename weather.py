import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from scipy import spatial
import sys
import warnings
if not sys.warnoptions:
    warnings.simplefilter("ignore")


def reformat_data(weather_data):
    for key, value in weather_data.items():
        value["DATE"], value["TIME"] = value["DATE"].str.split("\s+", 1).str
        value["TIME"] = value["TIME"].str.replace(':', '').astype(int)
    #    todo check time for NAN pd.to_numeric(data["HOURLYDRYBULBTEMPF"], errors='coerce').fillna(1000).astype(np.int64) < 40.0)]

    return weather_data


def avg_temp(weather_data, date):
    # todo perform check on dates
    results = {}
    for key, value in weather_data.items():
        results[key] = {}
        results[key]["TEMP_AVG"] = {}
        results[key]["TEMP_STD"] = {}

        data = value.loc[date == value["DATE"]]
        sunrise = min(data["DAILYSunrise"])
        sunset = max(data["DAILYSunset"])
        data = data.loc[(data["TIME"] > sunrise) & (data["TIME"] < sunset)]
        results[key]["TEMP_AVG"]["FAHRENHEIT"] = data["HOURLYDRYBULBTEMPF"].mean()
        results[key]["TEMP_AVG"]["CELSIUS"]    = data["HOURLYDRYBULBTEMPC"].mean()
        results[key]["TEMP_STD"]["FAHRENHEIT"] = data["HOURLYDRYBULBTEMPF"].std()
        results[key]["TEMP_STD"]["CELSIUS"]    = data["HOURLYDRYBULBTEMPC"].std()
    return results


def wind_chill_equation(temp, velocity):
    #  Cite US Windchill 2001:  https://en.wikipedia.org/wiki/Wind_chill
    # assert (temp.isnumeric())
    # assert (velocity.isnumeric())
    velocity = float(velocity)
    temp = float(temp)
    velocity = velocity ** 0.16
    WC = 35.74 + 0.6215 * temp - 35.75 * velocity + 0.4275 * temp * velocity
    return round(WC, 1)


def wind_chill(weather_data, date):
    # todo perform check on dates
    results = {}
    WC = []
    for key, value in weather_data.items():
        data = value.loc[(date == value["DATE"]) ]
        data = data.loc[(pd.to_numeric(data["HOURLYDRYBULBTEMPF"], errors='coerce').fillna(1000).astype(np.int64) < 40)]
        if data.shape[0] > 0:
            WC = data.apply(lambda x: wind_chill_equation(x["HOURLYDRYBULBTEMPF"], x["HOURLYWindSpeed"]), axis=1)
        results[key] = list(WC)
    return results



def cos(x,y):
    if x is None or y is None:
        return 0.0
    cos = 1 - spatial.distance.cosine(x, y)
    if np.isfinite(cos):
        return cos
    return 0.0



def process_data(df, date):
    #     todo assert data frame
    row = []
    row.append(date)
    df = df.loc[:, ["HOURLYVISIBILITY" , "HOURLYDRYBULBTEMPF", "HOURLYWETBULBTEMPF", "HOURLYRelativeHumidity", "HOURLYWindSpeed", "HOURLYWindDirection", "HOURLYWindGustSpeed"]]

    df["HOURLYVISIBILITY"] = pd.to_numeric(df["HOURLYVISIBILITY"], errors='coerce')
    df["HOURLYDRYBULBTEMPF"] = pd.to_numeric(df["HOURLYDRYBULBTEMPF"], errors='coerce')
    df["HOURLYRelativeHumidity"]  = pd.to_numeric(df["HOURLYRelativeHumidity"], errors='coerce')
    df["HOURLYWindSpeed"] = pd.to_numeric(df["HOURLYWindSpeed"], errors='coerce')
    df["HOURLYWindDirection"] = pd.to_numeric(df["HOURLYWindDirection"], errors='coerce')
    df["HOURLYWindGustSpeed"] = pd.to_numeric(df["HOURLYWindGustSpeed"], errors='coerce')

    # matrix = df.fillna(0).as_matrix().mean(axis=0)
    row.extend(df.fillna(0).as_matrix().mean(axis=0))
    return row






def similar_days(weather_data, date):
    similiarity = []
    atl = weather_data["ATL"]
    tx = weather_data["TX"]

    X =  process_data( atl.loc[(date == atl["DATE"])], date)
    list_of_dates = tx['DATE'].unique()
    for i in range(len(list_of_dates)):
        data = tx.loc[(list_of_dates[i] == tx["DATE"])]
        Y = process_data(data, list_of_dates[i])
        C = cos(X[1:], Y[1:])
        similiarity.append((C, list_of_dates[i] ))
    similiarity.sort(key=lambda tup: tup[0], reverse=True)
    return similiarity[0][1]





if __name__ == "__main__":
    # todo perform checks on input data
    weather_data = {}
    weather_data["TX"] = pd.read_csv("./data/1089419.csv")
    weather_data["ATL"] = pd.read_csv("./data/1089441.csv")

    # Reformat Data
    weather_data = reformat_data(weather_data)


    # # Method 1
    temp_data = avg_temp(weather_data, "10/3/17")
    print ("Method 1 Results:")
    print (temp_data["ATL"]["TEMP_AVG"]["FAHRENHEIT"])
    print (temp_data["ATL"]["TEMP_AVG"]["CELSIUS"])
    print (temp_data["ATL"]["TEMP_STD"]["FAHRENHEIT"])
    print (temp_data["ATL"]["TEMP_STD"]["CELSIUS"])

    # Method 2
    print ("\nMethod 2 Results:")
    wc_data = wind_chill(weather_data, "1/1/08")
    print (wc_data["TX"])
    print (wc_data["ATL"])

    # Method 3
    tx_day =similar_days(weather_data, "10/3/17")
    print ("\nMethod 3 Results:")
    print(tx_day)






