# from scipy.spatial.distance import cosine
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from scipy import spatial


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
    # if x is None or y is None:
    #     return 0.0
    print ("Cos Function")
    # x = np.array(x)
    # y = np.array(y)
    print(x)
    print(y)
    # Uses distance, subtract 1 for similarity
    cos = 1 - spatial.distance.cosine(x, y)
    # cos = cosine(np.array(x), np.array(y))

    # if w2v:
    #     cos = cosine(np.array(x), np.array(y))
    # else:
    #     cos = cosine(x.toarray()[0], y.toarray()[0])
    # cos = cosine_similarity(x, y)
    print (cos)
    if np.isfinite(cos):
        return cos
    return 0.0



def process_data(df, date):
    #     todo assert data frame
    row = []
    row.append(date)
    df = df.loc[:, ["HOURLYVISIBILITY" , "HOURLYDRYBULBTEMPF", "HOURLYWETBULBTEMPF", "HOURLYRelativeHumidity", "HOURLYWindSpeed", "HOURLYWindDirection", "HOURLYWindGustSpeed"]]

    # df["HOURLYVISIBILITY"] = pd.to_numeric(df["HOURLYVISIBILITY"])
    # print (df["HOURLYDRYBULBTEMPF"])
    # # df["HOURLYDRYBULBTEMPF"] = pd.to_numeric(df["HOURLYDRYBULBTEMPF"].extract('(\d+)', expand=True).astype(int))
    # # df["HOURLYDRYBULBTEMPF"] = pd.to_numeric(df["HOURLYDRYBULBTEMPF"].str.replace(r"[D]",value=r''))
    # print("Temp")
    # print (df["HOURLYDRYBULBTEMPF"])
    #
    # df["HOURLYWETBULBTEMPF"] = pd.to_numeric(df["HOURLYWETBULBTEMPF"])
    # df["HOURLYRelativeHumidity"]  = pd.to_numeric(df["HOURLYRelativeHumidity"])
    # df["HOURLYWindSpeed"] = pd.to_numeric(df["HOURLYWindSpeed"])
    # df["HOURLYWindDirection"] = pd.to_numeric(df["HOURLYWindDirection"])
    # df["HOURLYWindGustSpeed"] = pd.to_numeric(df["HOURLYWindGustSpeed"])


    df["HOURLYVISIBILITY"] = pd.to_numeric(df["HOURLYVISIBILITY"], errors='coerce')
    df["HOURLYDRYBULBTEMPF"] = pd.to_numeric(df["HOURLYDRYBULBTEMPF"], errors='coerce')
    df["HOURLYRelativeHumidity"]  = pd.to_numeric(df["HOURLYRelativeHumidity"], errors='coerce')
    df["HOURLYWindSpeed"] = pd.to_numeric(df["HOURLYWindSpeed"], errors='coerce')
    df["HOURLYWindDirection"] = pd.to_numeric(df["HOURLYWindDirection"], errors='coerce')
    df["HOURLYWindGustSpeed"] = pd.to_numeric(df["HOURLYWindGustSpeed"], errors='coerce')

    matrix = df.fillna(0).as_matrix().mean(axis=0)
    print(matrix)
    row.extend(matrix)
    return row

    #
    #
    # # pd.to_numeric(df["HOURLYVISIBILITY"], errors='coerce')
    # # pd.to_numeric(df["HOURLYDRYBULBTEMPF"], errors='coerce')
    # # pd.to_numeric(df["HOURLYWETBULBTEMPF"], errors='coerce')
    # # pd.to_numeric(df["HOURLYRelativeHumidity"], errors='coerce')
    # # pd.to_numeric(df["HOURLYWindSpeed"], errors='coerce')
    # # pd.to_numeric(df["HOURLYWindDirection"], errors='coerce')
    # # pd.to_numeric(df["HOURLYWindGustSpeed"], errors='coerce')
    #
    #
    # # print("Temp")
    # # print (df["HOURLYDRYBULBTEMPF"])
    # # df = df.fillna(0.0)
    # # print(df.dtypes)
    # # print(df)
    #
    #
    #
    # # exit (0)
    # # matrix = pd.to_numeric(df, errors='coerce').fillna(0).astype(np.int64)
    # # matrix = df.fillna(0)
    # # matrix = df.fillna(0).values()
    # # print(matrix)
    # # matrix = df.fillna(0).as_matrix()
    # # matrix = pd.to_numerics(matrix)
    # # matrix = matrix.astype(float)
    # # matrix = float(matrix)
    # # print(matrix)
    #
    #
    #
    # df["mean"] = np.array(df.mean(axis=0))
    #
    # # matrix = np.array(df.mean(axis=0)).reshape(1, df.shape[1])
    # # matrix = list(df.mean(axis=0))
    # # matrix = df.mean(axis=0).values()
    # print (df["mean"])
    # # print (matrix)
    # exit(0)
    # # matrix = matrix.mean(axis=0)
    # # matrix = matrix.sum(axis=0)
    #
    # # print (matrix)
    # row.extend(matrix)
    # # row.extend( matrix.astype(float).mean(axis=0))
    # # np.mean()
    # # print(row)
    # # row.extend( df.fillna(0).as_matrix().flatten('F'))
    # return row



def similar_days(weather_data, date):
    atl = weather_data["ATL"]
    tx = weather_data["TX"]


    # atl_data =  process_data( atl.loc[(date == atl["DATE"])], date)

    # print( atl.loc[(date == atl["DATE"])], date)

    X =  process_data( atl.loc[(date == atl["DATE"])], date)
    # print(X)

    tx_matrix = []
    list_of_dates = tx['DATE'].unique()
    for i in range(len(list_of_dates)):
        data = tx.loc[(list_of_dates[i] == tx["DATE"])]
        # tx_matrix.append( process_data(data, list_of_dates[i]))
        Y = process_data(data, list_of_dates[i])
        # results = cosine_similarity(X[1:], Y[1:])
        print(Y[1:])
        # exit(0)
        results = cos(X[1:], Y[1:])
        exit(0)
        break





if __name__ == "__main__":
    # todo perform checks on input data
    weather_data = {}
    weather_data["TX"] = pd.read_csv("./data/1089419.csv")
    weather_data["ATL"] = pd.read_csv("./data/1089441.csv")

    # Reformat Data
    weather_data = reformat_data(weather_data)


    # # Method 1
    # temp_data = avg_temp(weather_data, "10/3/17")
    # print (temp_data["ATL"]["TEMP_AVG"]["FAHRENHEIT"])
    # print (temp_data["ATL"]["TEMP_AVG"]["CELSIUS"])
    # print (temp_data["ATL"]["TEMP_STD"]["FAHRENHEIT"])
    # print (temp_data["ATL"]["TEMP_STD"]["CELSIUS"])
    #
    # # Method 2
    # wc_data = wind_chill(weather_data, "1/1/08")
    # print (wc_data["TX"])
    # print (wc_data["ATL"])

    # Method 3
    similar_days(weather_data, "10/3/17")






