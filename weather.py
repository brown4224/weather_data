import re
import numpy as np
import pandas as pd



def avg_temp(date):
    # todo perform check on dates
    data = atl.loc[date == atl["DATE"]]
    sunrise = min(data["DAILYSunrise"])
    sunset = max(data["DAILYSunset"])
    # m = data["HOURLYDRYBULBTEMPF"].mean()
    # data.loc[(data['column_name'] == some_value) & data['other_column'].isin(some_values)]
    data_sanatized = data.loc[(data["TIME"] > sunrise) & (data["TIME"] < sunset)]
    m = m["HOURLYDRYBULBTEMPF"].mean()
    print(m)

    # print ([temp for temp in data["HOURLYDRYBULBTEMPF"] if data["TIME"] > sunrise])

    # change time format data["TIME"] :   6:35 -> 635
    # test = data['TIME'].astype(int)
    # test = data['TIME'].str.replace('0', '')
    # print (data['TIME'].replace('0', '', regex=False, inplace=True))

    # print(test)
    # data = data.loc[data["TIME"] > sunrise &  data["TIME"] < sunrise]
    # print (data)

    # print (data.loc[(data["TIME"] > sunrise) &  (data["TIME"] < sunrise)])



    # temp["FAHRENHEIT"], temp["CELSIU"] =  data["HOURLYDRYBULBTEMPF"]
    # data = data.loc[data["TIME"] > sunrise &&  data["TIME"] < sunrise]
    # print (re.sub(':', '', date["TIME"]).str)
    # print(date["TIME"].str.replace(':', ''))
    # print (test.values)
    # print(list(atl.rows.values))
    # print(test["TIME"] ," ", test["DAILYSunset"])
    # print (test["DAILYSunrise"])

    # print (test["DAILYSunrise"])
    # data['TIME'] = data['TIME'].map(lambda x: x.strip(":"))
    # data['T'] = data['TIME'].apply(lambda x: x.strip(":"))
    # print ([data['TIME'] > sunrise])
    # data['TIME'] = data['TIME'].strip(":")

    # print (pd.to_numeric(data['TIME']))


#      HOURLYDRYBULBTEMPF
if __name__ == "__main__":
    # todo perform checks on input data
    tx = pd.read_csv("./data/1089419.csv")
    atl = pd.read_csv("./data/1089441.csv")

    # Reformat Data
    atl["DATE"], atl["TIME"] = atl["DATE"].str.split("\s+", 1).str
    atl["TIME"] = atl["TIME"].str.replace(':', '').astype(int)

    # Call Function
    avg_temp("10/3/17")


