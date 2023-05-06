import pandas as pd

def sort_periods(df_timeline):
    periodos_dict={
    "II PERIODO de 2010":0,
    "I PERIODO DE 2011":1,
    "II PERIODO DE 2011":2,
    "I PERIODO DE 2012":3,
    "II PERIODO DE 2012":4,
    "I PERIODO DE 2013":5,
    "II PERIODO DE 2013":6,
    "I PERIODO DE 2014":7,
    "II PERIODO DE 2014":8,
    "I PERIODO DE 2015":9,
    "II PERIODO DE 2015":10,
    "I PERIODO DE 2016":11,
    "II PERIODO DE 2016":12,
    "I PERIODO DE 2017":13,
    "II PERIODO DE 2017":14,
    "I PERIODO DE 2018":15,
    "II PERIODO DE 2018":16,
    "I PERIODO DE 2019":17,
    "II PERIODO DE 2019":18,
    "I PERIODO DE 2020":19,
    "II PERIODO DE 2020":20,
    "I PERIODO DE 2021":21,
    "II PERIODO DE 2021":22,
    "I PERIODO DE 2022":23,
    "II PERIODO DE 2022":24,
    }
    df_timeline['Period'] = pd.Categorical(df_timeline['Period'], categories=periodos_dict, ordered=True)
    return  df_timeline