import pandas as pd
import pmdarima as pm
from statsmodels.tsa.statespace.sarimax import SARIMAX
import itertools

def mergeGVA(gva, combinedGVA, startYear):
    combined = gva.copy()
    combined.set_index('Date', inplace=True)
    combined = combined[combined.index.year >= startYear]

    #merging the two
    combined = combined.merge(combinedGVA, left_index=True, right_index=True)
    combined = combined.rename(columns={
        'GVA at basic prices: Base year 2011-12: At constant prices ': 'GVA',
        'GVA at basic prices: Agriculture, forestry and fishing: Base year 2011-12: At constant prices ': 'AgriGVA',
        'GVA at basic prices: Services: Base year 2011-12: At constant prices ': 'ServiceGVA',
        'GVA at basic prices: Industry: Base year 2011-12: At constant prices ': 'IndustryGVA'
    })
    return combined

def forecastFuture(combined, weights):
    estimators = {}
    names = [col for col in combined.columns if col!= 'GVA' or col != 'WeightedGVA']
    for pred in names:
        data = combined[pred].dropna()
        Model = pm.auto_arima(data, m=4, d=None, start_p=0, start_q=0,
                              max_p=5, max_q=5, max_P=2, max_Q=2, trace=False, error_action='ignore', suppress_warnings=True, stepwise=True)
        forecast = Model.predict(n_periods=4)
        estimators[pred] = forecast

    weightedGVA = [0] * 4
    for name, forecast in estimators.items():
        weightedGVA = [WGF + F * weights[name] for WGF, F in zip(weightedGVA, forecast)]
    return estimators, weightedGVA

def createFutureDF(estimators, weightedGVA, lastKnown):
    futureRange = pd.date_range(lastKnown + pd.offsets.MonthBegin(1), periods=4, freq='Q')
    tempFutureDF = pd.DataFrame(index=futureRange)
    for pred, forecast in estimators.items():
        tempFutureDF[pred] = forecast
    tempFutureDF['WeightedGVA'] = weightedGVA
    return tempFutureDF, futureRange

def buildSARIMAX(DF, lastKnown):
    PredX = DF[DF.index <= lastKnown].drop('GVA', axis=1)
    target = DF[DF.index <= lastKnown]['GVA']

    p=d=q = range(0, 5)
    P=D=Q = range(0, 2)
    pdq = [(x[0], x[1], x[2]) for x in list(itertools.product(p, d, q))]
    PDQ = [(x[0], x[1], x[2], 4) for x in list(itertools.product(P, D, Q))]

    bestAIC = float('inf')
    bestParams = None
    bestSeasonal = None
    bestModel = None

    for param in pdq:
        for seasonalParam in PDQ:
            try:
                model = SARIMAX(target, order=param, seasonal_order=seasonalParam, enforce_stationarity=False, enforce_invertibility=False)
                results = model.fit()
                if results.aic < bestAIC:
                    bestAIC = results.aic
                    bestParams = param
                    bestSeasonal = seasonalParam
                    bestModel = results
            except Exception as e:
                print(f"An error occurred: {e}")
    print("The best SARIMAX model is: SARIMAX{bestParams}X{bestSeasonal}")
    return bestModel, bestParams, bestSeasonal