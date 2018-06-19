import re
import numpy as np
import pandas as pd



def reformat_data(weather_data):
    for key, value in weather_data.items():
        value["DATE"], value["TIME"] = value["DATE"].str.split("\s+", 1).str
        value["TIME"] = value["TIME"].str.replace(':', '').astype(int)
    #    todo check time for NAN pd.to_numeric(data["HOURLYDRYBULBTEMPF"], errors='coerce').fillna(1000).astype(np.int64) < 40.0)]

    return weather_data


def avg_temp(date):
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


def wind_chill(date):
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


if __name__ == "__main__":
    # todo perform checks on input data
    weather_data = {}
    weather_data["TX"] = pd.read_csv("./data/1089419.csv")
    weather_data["ATL"] = pd.read_csv("./data/1089441.csv")

    # Reformat Data
    weather_data = reformat_data(weather_data)


    # Method 1
    temp_data = avg_temp("10/3/17")
    print (temp_data["ATL"]["TEMP_AVG"]["FAHRENHEIT"])
    print (temp_data["ATL"]["TEMP_AVG"]["CELSIUS"])
    print (temp_data["ATL"]["TEMP_STD"]["FAHRENHEIT"])
    print (temp_data["ATL"]["TEMP_STD"]["CELSIUS"])

    # Method 2
    wc_data = wind_chill("1/1/08")
    print (wc_data["TX"])
    print (wc_data["ATL"])

    # Method 3






