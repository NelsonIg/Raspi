import pandas as pd
import matplotlib.pyplot as plt
import datetime as date
import numpy as np
now = date.datetime.now()

sensor_data = pd.read_csv(f'{now.year}-{now.day}-sensor_data.csv')

# compute average
WINDOW_SIZE = 6
WINDOW_TYPE = 'gaussian'  # None, 'triang'
moving_average = sensor_data.rolling(WINDOW_SIZE).mean()
STEP = 1
data_slice = moving_average[::STEP]

fix, axis = plt.subplots(1,1)
ax = data_slice.plot(y=['temperature', 'humidity'], label=["temperature mean [°C]", "humidity mean [%]"], ax=axis)
ax2 = sensor_data.plot(y=['temperature', 'humidity'], label=["temperature [°C]", "humidity [%]"], ax=axis)
plt.title('Random Test')
plt.xlabel(f'Window: ({WINDOW_SIZE}, {WINDOW_TYPE})')
plt.show()
