from uagents import Agent, Context
import pandas as pd
from prophet import Prophet
from io import StringIO


# Create an agent named Alice
predict_usage = Agent(name="predict_usage", seed="a214e140-147f-4173-85de-dc3d3139ad8e", port=8000, endpoint=["http://localhost:8000/submit"])

prediction = pd.DataFrame()

@predict_usage.on_event("startup")
async def introduce_agent(ctx: Context):
    global prediction
    ctx.logger.info(f"Hello, I'm agent {predict_usage.name} and my address is {predict_usage.address}.")

    data = pd.read_csv(
        'pv_profiles/pv_profile_2023_06_PPE_1_prosument.csv',
        header=0,
        names=['ds', 'production', 'consumption']
    )
    data_production = data[['ds', 'production']].rename({'ds': 'ds', 'production': 'y'}, axis='columns')
    data_consumption = data[['ds', 'consumption']].rename({'ds': 'ds', 'consumption': 'y'}, axis='columns')

    model_production = Prophet()
    model_production.fit(data_production)
    future_production = model_production.make_future_dataframe(periods=24, freq='h')  # Predicting 30 hours into the future
    forecast_production = model_production.predict(future_production)

    # Plot the forecast
    model_production.plot_components(forecast_production).savefig('results/forecast_production.png')


    model_consumption = Prophet()
    model_consumption.fit(data_consumption)
    future_consumption = model_consumption.make_future_dataframe(periods=24, freq='h')  # Predicting 30 hours into the future
    forecast_consumption = model_consumption.predict(future_consumption)

    # Plot the forecast
    model_consumption.plot_components(forecast_consumption).savefig('results/forecast_consumption.png')

    forecast_production['production'] = forecast_production['yhat']
    forecast_consumption['consumption'] = forecast_consumption['yhat']

    prediction = pd.merge(forecast_production[['ds', 'production']], forecast_consumption[['ds', 'consumption']], on='ds')

    prediction.to_csv('results/prediction.csv', index=False)


# Define a periodic task for Alice
@predict_usage.on_interval(period=2.0)
async def say_hello(ctx: Context):
    ctx.logger.info(f'hello, my name is {predict_usage.name}')

    csv_string = StringIO()
    prediction.head(5).to_csv(csv_string, index=False)
    csv_output = csv_string.getvalue()

    ctx.logger.info(f'My First 5 predictions: \n{csv_output}')



# Run the agent
if __name__ == "__main__":
    predict_usage.run()