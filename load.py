import pandas as pd
def loadData(servicePath: str, indexPath: str, agriPath: str, gvaPath: str):
    AgriGVA = pd.read_excel(agriPath, sheet_name='Quarterly')
    ServiceGVA = pd.read_excel(servicePath, sheet_name='GVA-Quarterly')
    IndustryGVA = pd.read_excel(indexPath, sheet_name='Sheet3')
    GVA = pd.read_excel(gvaPath)

    return AgriGVA, ServiceGVA, IndustryGVA, GVA