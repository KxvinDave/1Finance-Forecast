import pandas as pd
from load import loadData
from preprocess import SectorGVA, IndiaGVA
from weighted import computeWeighted
from mergePredict import mergeGVA, forecastFuture, createFutureDF, buildSARIMAX
import plotly.graph_objects as go

ServicePath = ""
IndexPath = ""
AgriPath = ""
GVAPath = ""

AgriGVA, ServiceGVA, IndustryGVA, _ = loadData(ServicePath, IndexPath, AgriPath, GVAPath)

dataframes = [AgriGVA, ServiceGVA, IndustryGVA]
try:
    AgriGVA, ServiceGVA, IndustryGVA = SectorGVA(AgriGVA, ServiceGVA, IndustryGVA)
    GVA = IndiaGVA(GVAPath)
except Exception as e:
    print(f"Pre-processing failed. {e}")

Weights = {
    'AgriGVA': 0.15,
    'ServiceGVA': 0.60,
    'IndustryGVA': 0.25
}
StartYear = pd.to_datetime('2012').year
combinedGVA = computeWeighted(AgriGVA, ServiceGVA, IndustryGVA, StartYear, Weights)
combined = mergeGVA(GVA, combinedGVA, StartYear)
estimators, weightedGVA = forecastFuture(combined, Weights)

lastKnown = combined.index[-1]
tempFuture, futureRange = createFutureDF(estimators, weightedGVA, lastKnown)

estimatedWeighted = pd.DataFrame(weightedGVA, columns=['WeightedGVA'], index=futureRange)
Phase2 = combined[['WeightedGVA', 'GVA']].copy()
Phase2 = pd.concat([Phase2, estimatedWeighted], axis=0)

combined = pd.concat([combined, tempFuture], sort=False).combine_first(combined)
#Build and fit the sarimax
bestModel, bestParams, bestSeasonal = buildSARIMAX(Phase2, lastKnown)

#Forecast future GVA
PredX = Phase2[Phase2.index > lastKnown].drop('GVA', axis=1)
futureGVA = bestModel.get_forecast(steps=4, exog=PredX)
forecastedGVA = futureGVA.predicted_mean
forecastGVAConfInt = futureGVA.conf_int()

ActualGVA = combined['GVA'].dropna()
forecastedGVAseries = pd.Series(forecastedGVA, index=futureRange)
completeGVA = pd.concat([ActualGVA, forecastedGVAseries])

#Plot YoY
YoYGrowth = completeGVA.pct_change(4) * 100
YoYActual = YoYGrowth[:-4]
YoYPred = YoYGrowth[-4:]

figure = go.Figure()

figure.add_trace(go.Scatter(
    x = YoYGrowth.index,
    y = YoYActual,
    name = 'Actual YoY Growth',
    line = dict(color = 'cornflowerblue')
))
figure.add_trace(go.Scatter(
    x = YoYGrowth.index,
    y = YoYPred,
    name = 'Predicted YoY Growth',
    line = dict(color = 'firebrick')
))
figure.update_layout(
    title='YoY GVA (Actual & Predicted)',
    xaxis_title='Date',
    yaxis_title='YoY Growth (%)',
    legend_title = 'Reference'
)
figure.show()