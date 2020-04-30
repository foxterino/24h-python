import wbdata
import matplotlib.pyplot as plt
import datetime

# countries = [i['id'] for i in wbdata.get_country(incomelevel="HIC", display=False)]
countries = ["UA", "RU", "POL", "MDA", "HUN", "SVK", "BLR", "ROU"]
indicators = {"NY.GDP.PCAP.KD.ZG": "gpd"}
date_range = (datetime.datetime(2000, 1, 1), datetime.datetime(2018, 1, 1))

df = wbdata.get_dataframe(indicators, country=countries,
                          convert_date=True, data_date=date_range)

dfu = df.unstack(level=0)

dfu.plot()
plt.legend(loc='best')
plt.title("GDP of Ukraine and Its neighborhoods")
plt.xlabel('Time')
plt.ylabel('GDP growth (annual %)')

plt.show()
