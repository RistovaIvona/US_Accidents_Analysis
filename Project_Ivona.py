# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 18:22:06 2020

@author: USER
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('US_Accidents_Dec19.csv')
print(df.shape)

#First we can view the percentage of missing values
percentage = (df.isnull().sum()/df.isnull().count()).sort_values(ascending=False)*100
#print(percentage)
print(df.info())

df.columns.values
df.describe()

#to_datetime (start_time and end_time) to use lately  
df['Start_Time'] = pd.to_datetime(df['Start_Time'])
df['End_Time'] = pd.to_datetime(df['End_Time'])
print(df.info())

#finding values with nan and null values 
#null
df.isnull().sum()
#nan
df.isna().sum()

#Cleaning the dataset

df['TMC'] = df['TMC'].fillna(df['TMC'].median())
df['End_Lat'] = df['End_Lat'].fillna(df['End_Lat'].mean())
df['End_Lng'] = df['End_Lng'].fillna(df['End_Lng'].mean())
df['Number'] = df['Number'].fillna(df['Number'].mean())
df['City'] = df['City'].fillna(df['City'].mode()[0])
df['Zipcode'] = df['Zipcode'].fillna(df['Zipcode'].mode()[0])
df['Timezone'] = df['Timezone'].fillna(df['Timezone'].mode()[0])
df['Airport_Code'] = df['Airport_Code'].fillna(df['Airport_Code'].mode()[0])
df['Weather_Timestamp'] = df['Weather_Timestamp'].fillna(df['Weather_Timestamp'].mode()[0])
df['Temperature(F)'] = df['Temperature(F)'].fillna(df['Temperature(F)'].mean())
df['Wind_Chill(F)'] = df['Wind_Chill(F)'].fillna(df['Wind_Chill(F)'].mean())
df['Humidity(%)'] = df['Humidity(%)'].fillna(df['Humidity(%)'].median())
df['Pressure(in)'] = df['Pressure(in)'].fillna(df['Pressure(in)'].median())
df['Visibility(mi)'] = df['Visibility(mi)'].fillna(df['Visibility(mi)'].median())
df['Wind_Direction'] = df['Wind_Direction'].fillna(df['Wind_Direction'].mode()[0])
df['Wind_Speed(mph)'] = df['Wind_Speed(mph)'].fillna(df['Wind_Speed(mph)'].median())
df['Precipitation(in)'] = df['Precipitation(in)'].fillna(df['Precipitation(in)'].median())
df['Weather_Condition'] = df['Weather_Condition'].fillna(df['Weather_Condition'].mode()[0])

df['Description'] = df['Description'].fillna(df['Description'].mode()[0])
df['Sunrise_Sunset'] = df['Sunrise_Sunset'].fillna(df['Sunrise_Sunset'].mode()[0])
df['Civil_Twilight'] = df['Civil_Twilight'].fillna(df['Civil_Twilight'].mode()[0])
df['Nautical_Twilight'] = df['Nautical_Twilight'].fillna(df['Nautical_Twilight'].mode()[0])
df['Astronomical_Twilight'] = df['Astronomical_Twilight'].fillna(df['Nautical_Twilight'].mode()[0])

df.isnull().sum()
df.isna().sum()
df.nunique()

print(df.info())
print(df.isna().sum())

#Data processing and manipulation
#Find the state that has the most accidents
acc_state_max = df.groupby('State')['ID'].count()
acc_state_max = acc_state_max.reset_index()
print(acc_state_max)
mask = (acc_state_max['ID'] == acc_state_max['ID'].max())
acc_state = acc_state_max.loc[mask]
print(acc_state)

#acc_per_state = df.groupby('State')['ID'].count().reset_index()
#print(acc_per_state)    
#acc_per_state.index[acc_per_state['ID'] == acc_per_state['ID'].max()].tolist()
#acc_per_state.reset_index()
#acc_per_state['ID'] == acc_per_state['ID'].max()

#Find the state that has the most number of most severe
#accidents

df_t = df[df['Severity'] == 4]
most_severe_acc = df_t.groupby(['State'])['ID'].count()
most_severe_acc = df_t.groupby(['State'])['ID'].count().sort_values(ascending = False)

most_severe_acc = most_severe_acc.reset_index()
print(most_severe_acc)

mask = (most_severe_acc['ID'] == most_severe_acc['ID'].max())
severe_acc = most_severe_acc.loc[mask]

print(severe_acc)

#Find the most common hour at which accidents have
#occurred
df['hour'] = df['Start_Time'].dt.hour
hour_acc_occured = df.groupby('hour')['ID'].count()
hour_acc_occured = hour_acc_occured.reset_index()
print(hour_acc_occured)

mask = (hour_acc_occured['ID'] == hour_acc_occured['ID'].max())
hour_acc = hour_acc_occured.loc[mask]

print(hour_acc)

#Find the average duration of an accident
df['duration'] = df['End_Time'] - df['Start_Time']
print(df['duration'])

avg_acc_duration = df['duration'].mean()
print(avg_acc_duration)

#Find the average number of yearly accidents per city
df['year'] = df['Start_Time'].dt.year
yearly_avg = df.groupby(['City','year'])['ID'].count()
yearly_avg = yearly_avg.reset_index()

print(yearly_avg)
yearly_avg = yearly_avg.groupby(['City'])['ID'].mean()
yearly_avg = yearly_avg.reset_index()

print(yearly_avg)

#Examine the relationship between accident severity and other accident
#information such as time, weather and location

#weather condition
weather_condition = df.groupby('Weather_Condition').count() 

plt.figure(figsize=(30, 10))
plt.title('Number of Accidents due to Weather_Conditions')
plt.bar(weather_condition.index, weather_condition.Number, color='r')
plt.xlabel('Weather Conditions')
plt.ylabel('Number of Accidents')
plt.xticks(weather_condition.index, rotation='vertical', size=10)
plt.show()

print('Weather condititon were accident occures the most: ',weather_condition.Number.idxmax())
print('Rank States: ',weather_condition['Number'].sort_values(ascending=False))

#state
state = df.groupby('State').count() 

plt.figure(figsize=(30, 10))
plt.title('Number of Accidents per State')
plt.bar(state.index, state.Number, color='r')
plt.xlabel('State')
plt.ylabel('Number of Accidents')
plt.xticks(state.index, rotation='vertical', size=10)
plt.show()

print('The State were accident occures: ',state.Number.idxmax())
print('Rank States: ',state['Number'].sort_values(ascending=False))

state_accident_count=df.groupby(['State'],as_index=False)['ID'].count().sort_values(by = "ID",ascending=False)
f, ax = plt.subplots(figsize=(18, 8))
ax = sns.lineplot(x="State", y="ID", data=state_accident_count)
ax.set(ylabel='Total no of accidents')
plt.show()

#Lng Lat 
#Different way to visualize by some state 
#Map of accident color code by country 

# Set state
state='PA'

# Select the state of Pennsylvania
df_state=df.loc[df.State==state].copy()
df_state.drop('State',axis=1, inplace=True)
df_state.info()

sns.scatterplot(x='Start_Lng', y='Start_Lat', data=df_state, hue='County', legend=False, s=20)
plt.show()



#Severity
severity = df.groupby('Severity').count() 
print(severity)

plt.figure(figsize=(5, 10))
plt.title('Number of Accidents per Severity')
plt.bar(severity.index, severity.Number, color='r')
plt.xlabel('Severity')
plt.ylabel('Number of Accidents')
plt.xticks(severity.index, rotation='vertical', size=10)
plt.show()

print('Severity most occures: ',severity.Number.idxmax())
print('Severity Rank: ',severity['Number'].sort_values(ascending=False))

#accident per hour
time_hour = df.groupby('hour').count() 

plt.figure()
plt.title('Number of Accidents per Time')
plt.bar(time_hour.index, time_hour.Number, color='r')
plt.xlabel('Hour of day')
plt.ylabel('Number of Accidents')
plt.xticks(time_hour.index, rotation='vertical', size=10)
plt.show()

print('The Hour were accident occures the most: ',time_hour.Number.idxmax())
print('Rank States: ',time_hour['Number'].sort_values(ascending=False))

#accident per day
df['day'] = df['Start_Time'].dt.day
acc_day = df.groupby('day').count()

plt.figure()
plt.title('Number of Accidents per Day')
plt.bar(acc_day.index, acc_day.Number, color='r')
plt.xlabel('Hour of day')
plt.ylabel('Number of Accidents')
plt.xticks(acc_day.index, rotation='vertical', size=10)
plt.show()
