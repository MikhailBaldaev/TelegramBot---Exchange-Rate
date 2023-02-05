import pandas as pd
import matplotlib.pyplot as plt


def chrt(dict):
    new_list = {}
    for i in dict:
        for key, value in i.items():
            key = pd.to_datetime(key)
            value = float(value.replace(',', '.'))
            new_list.setdefault(key, value)
    print(new_list)
    ts = pd.Series(data=new_list, index=pd.date_range('2022-11-12', '2022-12-26', periods=1))
    ts = ts.cumsum()
    plt.figure()
    ts.plot()
    plt.show()


dicts = [{'09.12.2022': '62,5722'}, {'11.12.2022': '62,3813'}, {'26.12.2022': '68,6760'}, {'22.12.2022': '70,5256'}, {'03.12.2022': '61,7749'}, {'25.12.2022': '68,6760'}, {'12.12.2022': '62,3813'}, {'20.12.2022': '66,3474'}, {'18.12.2022': '64,6078'}, {'23.12.2022': '72,1306'}, {'06.12.2022': '62,1849'}, {'28.12.2022': '69,9346'}, {'17.12.2022': '64,6078'}, {'14.12.2022': '63,2120'}, {'04.12.2022': '61,7749'}, {'01.12.2022': '60,8803'}, {'07.12.2022': '62,9103'}, {'15.12.2022': '63,3590'}, {'30.12.2022': '71,9778'}, {'30.11.2022': '61,0742'}]
dicts_temp = {}
for i in dicts:
    for k, v in i.items():
        k = f'{k[6:]}-{k[3:5]}-{k[:2]}'
        dicts_temp.setdefault(k, v)
#print(dicts_temp)
#chrt(dicts)
new_list = {}
for key, value in dicts_temp.items():
    key = pd.to_datetime(key)
    value = float(value.replace(',', '.'))
    new_list.setdefault(key, value)
dates = [i for i in new_list.keys()]

#print(sorted(dates))
#values = [i for i in new_list.values()]
ts = pd.Series(data=new_list, index=sorted(dates))
plt.figure(figsize=(15, 6))
ax = ts.plot()
fig = ax.get_figure()
plt.xticks(sorted(dates))
fig.savefig('graph.png')
#ts.plot()

plt.show()
#plt.savefig('graph.png')
