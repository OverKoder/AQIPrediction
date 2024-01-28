import os
import datetime
from prophet.serialize import model_from_json

def load_models():
    model_dict = {}
    for model in os.listdir('./forecast'):

        # Load model
        with open('./forecast/' + model, 'r') as f:
            model_dict[model] = model_from_json(f.read())

    return model_dict

def get_forecast(model_dict):
    
    today = datetime.datetime.now()
    last_training_day = datetime.datetime(2024,1,25)

    forecast_dict = {}
    for key, model in model_dict.items():

        # Get prediction of the following 4 days
        future = model.make_future_dataframe(periods=(today - last_training_day).days + 4).iloc[-4:,:]
        forecast_values = model.predict(future)['yhat'].values

        # Round each number and prepare dict for html context
        for suffix, number in zip(['_1', '_2', '_3', '_4'], [round(number) for number in forecast_values]):
            name = key.split('.')[0] + suffix
            forecast_dict[name] = number

    
    return forecast_dict
