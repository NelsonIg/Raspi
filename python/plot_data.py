import pandas as pd
import matplotlib.pyplot as plt

sensor_data = pd.read_csv("sensorData.csv")
data_slice = sensor_data[sensor_data.index%12==0]  # pick one sample per minute

t = range(0,len(data_slice['temperature'].values),1) # t in 1 min interval
ax = data_slice.plot(y=['temperature', 'humidity'], label=["temperature [°C]", "humidity [%]"])
ax.set_xticks(data_slice.index.values)
ax.set_xticklabels(t)
plt.title('Small Window half opened')
plt.xlabel('time [min]')
plt.show()
