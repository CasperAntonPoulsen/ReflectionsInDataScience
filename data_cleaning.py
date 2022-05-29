import pandas as pd
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
#%%
#read json file and create dataframe
json_file = 'at_postData_secondbatch.json'
df = pd.read_json(json_file, lines=True)
#%%
#function for getting number of days 
def td_days(td):
    return td.days
#group by id and experimental status
id_group = df.groupby(["id","isExperimental"])
#create list for 
df_list = []
i = 0
for (post_id, isexperimental), group_df in id_group:
    first_time = group_df['datetime'].min()
    time_passed = group_df['datetime'] - first_time
    days_passed = np.array(time_passed.apply(td_days))
    if 7 in days_passed:
        group_df['days_passed'] = days_passed
        group_df = group_df.drop_duplicates(subset=['id', 'days_passed'], keep = 'first')
        group_df = group_df[group_df['days_passed'] <= 7][1:]
        df_list.append(group_df)
    i += 1
    if i % 100 == 0:
        print(i)
#%%
all_df = pd.concat(df_list)
all_df.to_csv('second_batch_wdays.csv', sep = ';', index = False)
