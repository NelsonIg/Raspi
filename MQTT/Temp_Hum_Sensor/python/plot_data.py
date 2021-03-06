import pandas as pd
import matplotlib.pyplot as plt
import datetime as date
import numpy as np
now = date.datetime.now()

sensor_data = pd.read_csv(f'{now.year}-{now.month}-{now.day}-sensor_data.csv')

# compute average
WINDOW_SIZE = 6
WINDOW_TYPE = None # None, 'triang'
# Weight data according to window and take the mean
moving_average = sensor_data.rolling(WINDOW_SIZE, win_type=WINDOW_TYPE).mean()
# Slice data if necessary
STEP = 1
data_slice = moving_average[::STEP]

# plot raw data and mean in one figure
fig, axis = plt.subplots(1,1)
ax = data_slice.plot(y=['temperature', 'humidity'], label=["temperature mean [°C]", "humidity mean [%]"], ax=axis)
ax2 = sensor_data.plot(y=['temperature', 'humidity'], label=["temperature [°C]", "humidity [%]"], ax=axis)
plt.title('Random Test')
plt.xlabel(f'Window: ({WINDOW_SIZE}, {WINDOW_TYPE})')


# data_slice.hist(bins=50)
# sensor_data.hist(bins=50)
plt.show()