from typing import List
import pandas as pd

def SectorGVA(arr: List[pd.DataFrame]):
    for i in range(len(arr)):
        arr[i].columns = arr[i].iloc[1]
        arr[i] = arr[i].iloc[6:, :]
        arr[i].rename(columns={"Description ": "Date"}, inplace=True)
        if len(arr[i].columns) > 2:
            if 'OBICUS' not in arr[i].columns[1]:
                print("Removing NaN in Agriculture GVA")
                arr[i].drop(arr[i].columns[0], axis=1, inplace=True)
            else:
                print("Removing OBICUS column!")
                arr[i].drop(arr[i].columns[1], axis=1, inplace=True)
        for column in arr[i].columns:
            if column != 'Date':
                arr[i][column] = pd.to_numeric(arr[i][column], errors='coerce')
    
    #re-assigning list as individual GVAs.
    AgriGVA = arr[0]
    ServiceGVA = arr[1]
    IndustryGVA = arr[2]
    return AgriGVA, ServiceGVA, IndustryGVA

def IndiaGVA(path: str):
    GVA = pd.read_excel(path)
    GVA.columns = GVA.iloc[0]
    GVA = GVA.iloc[6:, :]
    GVA.rename(columns={"Description ": "Date"}, inplace=True)
    GVA['Date'] = pd.to_datetime(GVA['Date'], errors='coerce')
    for cols in GVA.columns:
        if cols!= 'Date':
            GVA[cols] = pd.to_numeric(GVA[cols], errors='coerce')
    return GVA