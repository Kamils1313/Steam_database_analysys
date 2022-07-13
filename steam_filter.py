# -*- coding: utf-8 -*-
"""
Created on Sun Nov 14 09:17:08 2021

@author: kamil
"""
import pandas as pd
import math
df = pd.read_csv('steam_data.csv')
dfn = pd.DataFrame(None, columns=df.columns)
for row in df.iterrows():
    try:
        if "soundtrack" in row[1]["Title"] or "Soundtrack" in row[1]["Title"]:
            pass
        else:
            if "Utilities" in row[1]["Genre"]:
                pass
            else:
                if "Movie" in row[1]["Tags"] and math.isnan(row[1]["Genre"]):   #zauważyłem, że filmy nigdy nie mają gatunku, a interaktywne filmy mają (a je można uznać za gry)
                    pass
                else:
                    if row[1]["DLC"] == "DLC":
                        pass
                    else:
                        dfn=dfn.append([row[1]])
    except Exception as e:
        print(e)
        print(row[1]["id"])
dfn.to_csv('./games.csv', index=False)