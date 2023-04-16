# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt

# Defined function to extract specific values in the water temperature dataframe later
def string_exterminator(cell):
    cell = str(cell)
    cell = cell.split("/")
    if len(cell) >= 2:
        return cell[1]
    else:
        return ""

# Specify the order of the months
month_order = ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']

# Import and clean the water temperature data
df_wt = pd.read_html('https://www.weather.gov/buf/Hist_LakeTemps')
df_wt = df_wt[1]
df_wt = df_wt.applymap(string_exterminator)
df_wt = df_wt.apply(pd.to_numeric, errors='coerce')
df_wt = pd.DataFrame.from_records({'Jul': df_wt[7].mean(),
                     'Aug':df_wt[8].mean(),
                     'Sep':df_wt[9].mean(),
                     'Oct':df_wt[10].mean(),
                     'Nov':df_wt[11].mean(),
                     'Dec':df_wt[12].mean(),
                     'Jan':df_wt[1].mean(),
                     'Feb':df_wt[2].mean(),
                     'Mar':df_wt[3].mean(),
                     'Apr':df_wt[4].mean(),
                     'May':df_wt[5].mean(),
                     'Jun':df_wt[6].mean()}, 
                                     index=[0])
df_wt = df_wt.T
df_wt['Month'] = df_wt.index
df_wt['Temp'] = df_wt.iloc[:, 0]
df_wt = df_wt.append(df_wt.iloc[0])
df_wt.reset_index(inplace=True,drop=True)
df_wt.loc[12, "Temp"] = round(df_wt.loc[12, "Temp"], 0)
df_wt = df_wt.drop(0, axis=1)
df_wt.reset_index(inplace=True,drop=True)
df_wt.loc[12, "Temp"] = round(df_wt.loc[12, "Temp"], 0)
df_wt['Month'] = pd.Categorical(df_wt['Month'], categories=month_order, ordered=True)
df_wt.sort_values(by='Month', inplace=True)
df_wt = df_wt.append(df_wt.iloc[0])
df_wt = df_wt.drop(index=[0])
df_wt.loc[12, "Temp"] = round(df_wt.loc[12, "Temp"], 0)
df_wt = df_wt.append(df_wt.iloc[0])
df_wt = df_wt.reset_index()
df_wt['Index'] = df_wt.index

# Import and clean the air temperature data 
df = pd.read_html('https://www.weather.gov/buf/BUFtemp')
df = df[7]
df.reset_index(drop=True, inplace=True)
df = df.drop(labels=[0], axis=0)
df = df.apply(pd.to_numeric)
df_t = pd.DataFrame.from_records({'Jul': df[7].mean(),
                     'Aug':df[8].mean(),
                     'Sep':df[9].mean(),
                     'Oct':df[10].mean(),
                     'Nov':df[11].mean(),
                     'Dec':df[12].mean(),
                     'Jan':df[1].mean(),
                     'Feb':df[2].mean(),
                     'Mar':df[3].mean(),
                     'Apr':df[4].mean(),
                     'May':df[5].mean(),
                     'Jun':df[6].mean()}, 
                                 index=[0])
df_t = df_t[['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']]
df_t = df_t.T
df_t['Month'] = df_t.index
df_t['Temp'] = df_t.iloc[:, 0]
df_t = df_t.drop(0, axis=1)
df_t = df_t.append(df_t.iloc[0])
df_t.reset_index(inplace=True, drop=True)
df_t.loc[12, "Temp"] = round(df_t.loc[12, "Temp"], 0)

# Fixing the order and labels to plot on the x- and y-axes
nums = [0,1,2,3,4,5,6,7,8,9,10,11,12]
y_label = []
y_tick = range(20, 105, 5)
for i in nums:
    df_t.iloc[i, 0] = i
    
for i in y_tick:
    if i % 10 != 0:
        y_label.append("")
    else:
        y_label.append(i)
  
# Plot the data     
fig, ax = plt.subplots()
ax.plot(df_wt.index, df_wt['Temp'], color = 'blue', label = 'Water',zorder=3)
ax.plot(df_t['Month'], df_t['Temp'], color = 'red', linestyle = '--', label = 'Air',zorder=3)

# Plot vertical line
ax.axvline(x=0.75, color='black',zorder=1)
ax.axvline(x=3.65, color='black',zorder=1)
ax.axvline(x=6.625, color='black',zorder=1)
ax.axvline(x=7.8, color='black',zorder=1)

# Plot text labels on the figure 
ax.text(1.15, 85, f'Lake-effect \nRain Season', fontsize=10, zorder=2)
ax.text(4, 75, f'Lake-effect \nSnow Season', fontsize=10,zorder=2)
ax.text(6.65, 65, f'Frozen \nLake', fontsize=10,zorder=2)
ax.text(8.75, 75, f'Lake-effect \nStable Season', fontsize=10,zorder=2)
ax.text(0.75, 101, '──────── Lake Warmer Than Air ────────', fontsize=9,zorder=2)
ax.text(8, 101, '────── Lake Colder ────', fontsize=9,zorder=2)

# Extra plot information
ax.grid(color='gray', axis='x', linestyle='--', zorder=0)
ax.set_xticks(nums, ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun','Jul'],zorder=1)
ax.set_xlabel('Month')
ax.set_ylabel('Temperature (°F)')
ax.set_yticks(y_tick, y_label)
plt.xlim(0,12)
plt.setp(ax.get_xticklabels())
plt.legend()
plt.show()
