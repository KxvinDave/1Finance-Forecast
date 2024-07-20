### 1 Finance MacroEconomic Forecast

### Overview:
The primary objective of this project is to develop a forecasting model to predict the Gross Domestic Product (GDP) using various economic indicators and historical data. This model aims to provide accurate and reliable GDP forecasts to assist in economic planning and decision-making.

### Features:
* Data Loading: Load and preprocess historical economic data from various sources
* Data preprocessing: Clean and transform the data to make it suitable for modelling
* Model evaluation: Assess the performance of the models using appropriate metrics (MAPE, MAE)
* Prediction: Combine different datasets and produce a final forecast.

### Modules:
#### load.py:
  * Description: Loads raw economic data.
  * Main function: loadData() which returns `pd.DataFrame`
#### preprocess.py:
  * Description: Cleans and performs basic preprocessing on the data
#### mergePredict.py:
  * Description: Merge different datasets and produces a final GDP forecast/prediction
#### weighted.py:
  * Description: Apply different weights to different GVA columns
#### main.py:
  * Description: Main script to execute the workflow from data loading to model training and prediction.

### Installation:
1). Clone the repository: `git clone https://github.com/KxvinDave/1Finance-Forecast/`
2). Navigate to the project dir: `cd <path>`
3). Create a virtual environment (optional): `python -m venv venv` and then run `venv\Scripts\activate`
4). install the requirements: `pip install -r requirements.txt.txt`


### Usage:
To run the GDP forecast model;
You will have to specify the paths to the following:
- Service GVA,
- Industry GVA,
- Agricultural GVA &
- GVA

Then after navigating to the root directory, please execute, `python main.py`.
