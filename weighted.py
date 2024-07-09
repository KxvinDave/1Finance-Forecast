import pandas as pd
def computeWeighted(agriGVA, serviceGVA, industryGVA, startYear, weights):
    """
    Computes the weighted GVA.
    """
    agriGVA.set_index('Date', inplace=True)
    serviceGVA.set_index('Date', inplace=True)
    industryGVA.set_index('Date', inplace=True)

    combinedGVA = pd.concat([agriGVA, serviceGVA, industryGVA], axis=1)
    combinedGVA = combinedGVA[combinedGVA.index.year >= startYear]

    combinedGVA['Weighted GVA'] = (
        combinedGVA.iloc[:, 0] * weights['AgriGVA'] + 
        combinedGVA.iloc[:, 1] * weights['ServiceGVA'] +
        combinedGVA.iloc[:, 2] * weights['IndustryGVA']
    )
    return combinedGVA
    