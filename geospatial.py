#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 31 13:56:15 2020

@author: holdenbruce
"""

# conda install geopandas
# dependencies of geopandas:
# conda install -c conda-forge shapely
# conda install -c conda-forge fiona
# conda install -c conda-forge pyproj
# conda install -c conda-forge rtree
# conda install -c conda-forge geopy
# conda install -c conda-forge descartes
# conda install -c anaconda mapclassify

import geopandas as gpd
import pandas as pd


url = 'https://raw.githubusercontent.com/uber-web/kepler.gl-data/master/nyctrips/data.csv'
nyc_taxi = pd.read_csv(url)
nyc_taxi.head()
nyc_taxi.columns


gdf = gpd.GeoDataFrame(nyc_taxi, geometry = gpd.points_from_xy(
    nyc_taxi.pickup_longitude,
    nyc_taxi.pickup_latitude)
)














# https://towardsdatascience.com/visualizing-data-at-the-zip-code-level-with-folium-d07ac983db20
# visualizing data at the zip code level with folium and geojson

import pandas as pd
import re
from datetime import datetime
from dateutil.parser import parse
#conda install -c conda-forge missingno
import missingno as msno #https://www.geeksforgeeks.org/python-visualize-missing-values-nan-values-using-missingno-library/
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt
import json

inspect_ms_data = pd.read_excel('ms_data.xlsx', skiprows=0, header=2)
inspect_ms_data = inspect_ms_data.drop([26,27,28,29,30])
inspect_ms_data.sort_values(by=['School'])

inspect_ms_data.shape #there are 26 middle schools in fairfax
#https://www.fcps.edu/schools-centers?f%5B0%5D=school_center_school_type%3A75
#but the fcps website tells me there are only 23
#compare my list to their list and drop any middle schools that are not on the fcps site
#drop: Hayfield SS, Lake Braddock, Robinson SS,
# inspect_ms_data = inspect_ms_data.drop([19,5,23])
# inspect_ms_data.shape #now we have our 23 schools, as expected
#actually, upon further research, these 3 schools are "Secondary Schools" but 
#still considered Middle Schools in the FCPS
inspect_ms_data.shape
#so we actually have 26 middle schools in the FCPS 


middle_schools = inspect_ms_data['School'].unique()

inspect_ms_data.head()
inspect_ms_data.dtypes

inspect_ms_data.Grades.min()
inspect_ms_data.columns


def dateobj(str):
    return datetime.strptime(str, '%Y-%m-%dT%H:%M:%S')
# inspect_ms_data['Date Opened'] = inspect_ms_data['Date Opened'].apply(dateobj)




# GeoJSON data is zipcode areas
# i should layer on top of that the average household income census data per zipcode 
# 'MeanZIP.xlsx' is Census data from 2006-2010 compiled by UMich from the ACS
# https://www.psc.isr.umich.edu/dis/census/Features/tract2zip/
# it contains every zip code in the United States and its corresponding average income
zip_income = pd.read_excel('MeanZIP.xlsx', header=0)
zip_income.head
zip_income.columns
zip_income.iloc[0]
zip_income['Zip']



#load GeoJSON
with open('ZIP_Codes.geojson','r') as jsonFile:
    data = json.load(jsonFile)
tmp = data


#remove zipcodes not in our dataset
geozips = []
# for i in range(len(tmp['features'])):
#     if tmp['features'][i]['properties']['name'] in list(geo_agg['facility_zip'].unique()):
#         geozips.append(tmp['features'][i])
# not actually relevant here because this geojson is for fairfax county, which is 
# the same county from the middle school data, so they perfectly align 
for i in range(len(tmp['features'])):
    geozips.append(tmp['features'][i])



#creating new JSON object
new_json = dict.fromkeys(['type','features'])
new_json['type'] = 'FeatureCollection'
new_json['features'] = geozips


#save JSON object as updated-file 
open('updated-file.json','w').write(
    json.dumps(new_json, sort_keys=True, indent=4, separators=(',', ': '))
)
# this returned an output of: Out[390]: 15841315
# what does that mean?



x = 'average_score'
print((' ').join(x.split('_')).title())


# conda install -c conda-forge folium
import folium

# table = main table/data frame we read from (pandas DataFrame)
# zips = column name where ZIP codes are (string)
# mapped_feature = column name for feature we want to visualize (string)
# add_text = any additional commentary to be added in the map legend (string)

def create_map(table, zips, mapped_feature, add_text = ''):
    # reading of the updated GeoJSON file
    fcZip_geo = r'updated-file.json'
    
    # initiating a Folium map with Fairfax County's longitude and latitude
    m = folium.Map(location = [38.908500671, -77.240501404], zoom_start = 11)
    
    # creating a choropleth map
    m.choropleth(
        geo_data = fcZip_geo,
        fill_opacity = 0.7,
        line_opacity = 0.2,
        data = table,
        # refers to which key within the GeoJSON to map the ZIP code to
        key_on = 'feature.properties.name',
        # first element contains location information, second element contains feature of interest
        columns = [zips, mapped_feature],
        fill_color = 'RdYlGn',
        legend_name = (' ').join(mapped_feature.split('_')).title() + ' ' + add_text + ' Across Fairfax County'
    )
    folium.LayerControl().add_to(m)
    # save map with filename based on the feature of interest
    m.save(outfile = mapped_feature + '_map.html')

create_map(zip_income, 'Zip', 'Mean')







# Tuesday, January 5th 
# For TJAAG, apparently, I only need to find the median household income for each middle 
# school region. So, I think it will make sense to first identify which zip codes correspond 
# to which middle schools. Then, compare the census data on median household income over time, 
# grouping by these zipcodes. 

#identify which zip codes correspond to which middle schools 













# ## Zillow 
# they have an API 
# use that to search by school region / houses that serve that school
# then look at Zestimate to determine general population's wealth
# maybe also look at renters vs. homeowners?
# i'm not sure how best to do this but i'll have to create some estimate for 
# determining the general wealth of those micro-communities 









# I have data on the family/household income per town in Fairfax County, VA.
# I'm interested in looking at the median income of families so that I can estimate
# the wealth of Middle School families per each middle school in the county.
# This data is for 2017 and is an average of the past 5 years (I think?) meaning
# that we don't have year-by-year data to match the admissions statistics for TJ

# Once I have this data loaded in I will need to figure out how to approximate the 
# wealth of each middle school where there are multiple middle schools per town...
# How will I do this? Zillow had an interesting region tracker that showed housing
# prices for middle school regions but that data isn't readily available and does 
# not have direct information on the ~income~ of the families, which is what we 
# are really looking for.

fairfax_towns = pd.read_csv('family_income_fairfax_towns.csv', header=0, index_col=0)
# tysons = pd.read_csv('family_income_fairfax_towns_just_tysons.csv', header=0, index_col=0)
# fairfax_towns = pd.concat([fairfax_towns,tysons], axis=1)

fairfax_towns.columns #loc[:,'Families']
fairfax_towns.iloc[0] #indexing this way searches by row, so the [0] is the first row of the
        #pandas dataframe, which is 'Families' ... every columns gets returned 
fairfax_towns.iloc[0][0] #adding the second number allows you to index into the specific column (in this case, the column at index 0 = Fairfax County, Virginia!!Estimate)

# https://en.wikipedia.org/wiki/List_of_Fairfax_County_Public_Schools_middle_schools
towns = {
    0: 'Alexandria',
    4: 'Annandale',
    8: 'Burke',
    12: 'Centreville',
    16: 'Chantilly',
    20: 'Clifton',
    24: 'Dunn Loring',
    28: 'Fairfax',
    32: 'Falls Church',
    36: 'Fort Hunt',
    40: 'Herndon',
    44: 'Hybla Valley',
    48: 'Lincolnia',
    52: 'Lorton',
    56: 'McLean',
    60: 'Merrifield',
    64: 'Reston',
    68: 'Rose Hill',
    72: 'Springfield',
    76: 'Tysons Corner', 
    80: 'West Springfield',
}
#there are 21 towns/sub-regions listed here...Vienna not listed, Tysons Corner added
#great falls not listed, Hybla Valley and Lincolnia added
#used specificity here to designate where middle schools are located

# while this is a good start, it might make sense to add every single region in fairfax
# county and then simply group by locations of elementary schools that feed to the middle
# schools so that i create my own regions to analyze 

fairfax_towns.iloc[11][76]
median_family_income = fairfax_towns.iloc[11] #the mean amount a family (households occupied by 2+ people related by birth, marrigae, adoption) is pulling in 
mean_family_income = fairfax_towns.iloc[12] #the average amount a family (households occupied by 2+ people related by birth, marrigae, adoption) is pulling in 
per_capita_income = fairfax_towns.iloc[13] #the average income earned by each person in a given area

# maybe i could consider families twice the national average in income 
# as well as families below the federal poverty line?

median_family_income[52]

towns[52]

num_families_in_town_dict = {}
median_family_income_dict = {}
mean_family_income_dict = {}
per_capita_income_dict = {}

# median_family_income_dict[towns[88]] = 
# median_family_income[]

for i in range(0, 84, 4):
    # print(towns[i])
    print("# of Families in {}:".format(towns[i]), fairfax_towns.iloc[0][i])
    num_families_in_town_dict[towns[i]] = int(fairfax_towns.iloc[0][i].replace(',',''))
    print("Median Family Income in {}:".format(towns[i]), fairfax_towns.iloc[11][i])
    median_family_income_dict[towns[i]] = int(median_family_income[i].replace(',',''))
    print("Mean Family Income in {}:".format(towns[i]), fairfax_towns.iloc[12][i])
    mean_family_income_dict[towns[i]] = int(mean_family_income[i].replace(',',''))
    print("Per Capita Income in {}:".format(towns[i]), fairfax_towns.iloc[13][i])
    per_capita_income_dict[towns[i]] = int(per_capita_income[i].replace(',',''))


# Sort:
# import operator
# num_families_in_town = sorted(num_families_in_town.items(), key=operator.itemgetter(1), reverse=True)
# median_family_income = sorted(median_family_income.items(), key=operator.itemgetter(1), reverse=True)
# mean_family_income = sorted(mean_family_income.items(), key=operator.itemgetter(1), reverse=True)
# per_capita_income = sorted(per_capita_income.items(), key=operator.itemgetter(1), reverse=True)
# Ok, now I have this town-specific information sorted from highest to lowest


# Liberty Middle School is in Chantilly, which only has 85 families, but the MS 
# has over 1100 kids...so clearly they are bringing in students from surrounding
# neighborhoods. 
# Rocky Run is another example of a school that needs to be given some more thought
# since it is on the border of a bunch of different town lines and draws students
# from many locations. 
# Estimating average wealth for these middle schools is going to be difficult. 





MS_TJ_2017 = pd.read_csv('2017_MS_TJ_admissions.csv', header=0)
MS_TJ_2017.head()
MS_TJ_2017 = MS_TJ_2017.rename(columns={'Unnamed: 0': "School"}) 
col = ['School', 'Total Admitted']
MS_TJ_2017_admitted = MS_TJ_2017[col]
# Sort: 
# MS_TJ_2017_admitted = sorted(MS_TJ_2017_admitted.items(), key=operator.itemgetter(1), reverse=True)
# MS_TJ_2017_admitted 
MS_TJ_2017_admitted_ordered = MS_TJ_2017_admitted.sort_values(by=['Total Admitted'], ascending=False, ignore_index=True)


# It might be interesting to see a graph showing the middle schools with the highest
# rates of acceptance to TJ alongside a grpah showing the richest towns in the county


# Total Students Admitted to TJ by Middle School
# https://benalexkeen.com/bar-charts-in-matplotlib/
import matplotlib.pyplot as plt
plt.style.use('ggplot')

x = MS_TJ_2017_admitted_ordered.loc[:,'School']
y = MS_TJ_2017_admitted_ordered.loc[:,'Total Admitted']

x_pos = [i for i, _ in enumerate(x)]

plt.bar(x, y, color='green')
plt.xlabel('Schools')
plt.ylabel('Total Students Admitted to TJ')
plt.title('Total Students Admitted to TJ by Middle School')
plt.xticks(x_pos,x, rotation='vertical')
plt.show()










#alternatively
plt.bar(range(len(MS_TJ_2017_admitted_ordered)), list(MS_TJ_2017_admitted_ordered['Total Admitted']), align='center')
plt.xticks(range(len(MS_TJ_2017_admitted_ordered)), list(MS_TJ_2017_admitted_ordered['School']), rotation='vertical')
plt.title('# of TJ Admitted Students by Middle School in 2017')
plt.show()



# Median Family Income
# https://stackoverflow.com/questions/16010869/plot-a-bar-using-matplotlib-using-a-dictionary
plt.bar(range(len(median_family_income_dict)), list(median_family_income_dict.values()), align='center', color='orange')
plt.xticks(range(len(median_family_income_dict)), list(median_family_income_dict.keys()), rotation='vertical')
plt.title('Median Family Income of Fairfax County Families')
plt.show()









# Right, now I need to group the Middle Schools by Town and then plot that 
# against the family income data I have for each of those towns 
# Maybe the left-y could be the income that corresponds to a bar chart displaying
# both the Median and Mean (or per capita) income per town 
# then the right-y could be the number of students accepted from the MS that is
# represented by that town... this would require me making a new dataframe where
# I group by town and combine the admissions numbers of middle schools that are 
# in the same town, then I would be able to add the line graph on top of the 
# bar chart so that yo could visualize the income per town on top of the admissions
# rates for those towns 

# https://stackoverflow.com/questions/32474434/trying-to-plot-a-line-plot-on-a-bar-plot-using-matplotlib

N = len(median_family_income_dict)
list(median_family_income_dict.values())
list(per_capita_income_dict.values())

ind = np.arange(N)
width = 0.35
plt.bar(ind, list(median_family_income_dict.values()), width, label = 'Median Family Income')
plt.bar(ind+width, list(per_capita_income_dict.values()), width, label = 'Per Capita Income (family)')

plt.ylabel('$')
plt.rcParams['figure.figsize']=[10,10]


plt.xticks(ind+width/2, list(median_family_income_dict.keys()), rotation='vertical')
plt.legend(loc = 'best')
plt.title('Bar Plot of Median and Per Capita Income for Families in Fairfax County Towns')
plt.show()




# Now I need to combine the admissions data, grouping by town 
# https://pandas.pydata.org/pandas-docs/stable/user_guide/groupby.html
    #Group by: split-apply-combine
MS_TJ_2017
MS_TJ_2017_admitted
MS_TJ_2017_admitted_ordered


#aggregate
grouped_town = MS_TJ_2017.groupby('Town')
grouped_town_and_school = MS_TJ_2017.groupby(['Town','School'])

grouped_town.aggregate(np.sum) #this only looks at towns and sums the values...this is what i want to plot
grouped_town_and_school.aggregate(np.sum) #this does not sum values and just couples the schools with their towns
    #this will be helpful to just see in a chart, not that helpful for plotting

admitted_by_town = grouped_town.aggregate(np.sum).sort_values(by=['Total Admitted'], ascending=False)['Total Admitted']


grouped_towns = list(admitted_by_town.index)

#currently admitted_by_town (and grouped_towns) is sorted from highest admitted rate to lowest
#however, median_family_income is sorted alphabetically
#i'd like to sort median_family_income the same way admitted_by_town is sorted

# Z = [x for _,x in sorted(zip(grouped_towns,median_family_income.keys()))]




median_dict_grouped_by_town = {key: median_family_income_dict[key] for key in grouped_towns}
median_dict_grouped_by_town
per_capita_dict_grouped_by_town = {key: per_capita_income_dict[key] for key in grouped_towns}
per_capita_dict_grouped_by_town 



# https://stackoverflow.com/questions/32474434/trying-to-plot-a-line-plot-on-a-bar-plot-using-matplotlib
# the x-axis NEEDS to be pulling the exact same data, which means that the 
# ordering of the towns MUST be the same 
plt.figure()       
# grouped_towns = list(admitted_by_town.index)
N = len(grouped_towns)
medians = list(median_dict_grouped_by_town.values())

median_dict_grouped_by_town.keys()
admitted_by_town.index
per_capita_dict_grouped_by_town.keys()

width = 0.35
per_capitas = list(per_capita_dict_grouped_by_town.values())
ind = np.arange(N)
plt.ylim(0.0, 250000)
# len(ind), len(medians), len(width)
plt.bar(ind, medians, width, color='r', label='Median Family Income')
plt.bar(ind+width, per_capitas, width, color='y', label='Per Capita Income')
plt.ylabel('Bar Plot of Median and Per Capita Income for Families in Fairfax County Towns')

x = admitted_by_town.index
y = admitted_by_town
x_pos = [i for i, _ in enumerate(x)]

plt.xticks(ind+width/2, x, rotation='vertical')
plt.legend(loc = 'upper right')



# plt.title('Admissions ')

axes2 = plt.twinx()
axes2.plot(x, y, color='k', label='Number of Admitted Students to TJ by Town')
axes2.set_ylim(0.0, 70.0)
axes2.set_ylabel('Line plot of Number of Admitted Students to TJ by Town')

plt.legend(loc = 'upper left')
plt.rcParams['figure.figsize']=[20,10]
plt.show()







# Alright
# it might be helpful to look at (plot) mean family income because higher 
# values will indicate that ultra rich people are living there, which might
# be an indication of the value those families place on the school district





















# MJ TJ Admissions Class of 2017-2021
MS_TJ_admissions = pd.read_csv('MS_TJ_admissions.csv', header=0)
MS_TJ_admissions.head()
MS_TJ_admissions = MS_TJ_admissions.rename(columns={'Unnamed: 0': "School"}) 
MS_TJ_admissions.head()




#this works:
MS_TJ_admissions = pd.read_csv('MS_TJ_admissions.csv', header=0, index_col=0)
MS_TJ_admissions.head()
MS_TJ_admissions = MS_TJ_admissions.T 
MS_TJ_admissions 

MS_TJ_admissions.plot(legend=True)
plt.figure(figsize=[20,20])
plt.show()



#plotly - use this 
import plotly.express as px
#load data into the figure
fig = px.line(MS_TJ_admissions, title='TJ Admissions by Middle School for Class of 2017-2021')
# Show plot 
fig.show()








MS_TJ_admissions.columns
admissions_columns = ['Total Admitted 2017', 'Total Admitted 2018', 'Total Admitted 2019', 'Total Admitted 2020', 'Total Admitted 2021']
schools = MS_TJ_admissions['School']
MS_TJ_admissions['Total Admitted 2017']

# now create a dataframe from that data
d = {col: MS_TJ_admissions[col] for col in admissions_columns} #pivot the data
df = pd.DataFrame(data=d) #create a new dataframe using this new data ... https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html
df = df.set_index(schools) #set the index so that the school names show 
df.head()

lines = df.plot.line()

[school for school in MS_TJ_admissions['School']]

for school in range(len(MS_TJ_admissions)):
    print(MS_TJ_admissions['School'][school])


d = {school: MS_TJ_admissions['School'][school] for school in range(len(MS_TJ_admissions))}
df = pd.DataFrame(data=d)


d = {school: MS_TJ_admissions['School'] for school in MS_TJ_admissions['School']} #pivot the data
df = df.set_index([col for col in admissions_columns]) #set the index so that the school names show 



df = pd.DataFrame({
    'pig': [20, 18, 489, 675, 1776],
    'horse': [4, 25, 281, 600, 1900]
    }, index=[1990, 1997, 2003, 2009, 2014])
#        pig  horse
# 1990    20      4
# 1997    18     25
# 2003   489    281
# 2009   675    600
# 2014  1776   1900





# Time-Series
urbpop=df[['country','date','pcturb']] #urbpop just keeps 3 columns from the "df" dataframe: country, date, and pcturb.
urbpopwide=urbpop.pivot(index='date',columns='country',values='pcturb')
#the arguments to the "pivot" function do the following
## assigns the column "date" as the index 
## converts country data from rows to columns
## applies this transformation to the 'pcturb' variable.
urbpopwide.plot.line(title='Percent of Total Population living in Urban Areas')
urbpop=df[['country','date','pcturb']] 
urbpopwide=urbpop.pivot(index='date',columns='country',values='pcturb')
urbpopwide.plot.line(title='Percent of Total Population living in Urban Areas')









