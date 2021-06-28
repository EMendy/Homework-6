#!/usr/bin/env python
# coding: utf-8

# # Homework 6, Part Two: A dataset about dogs.
# 
# Data from [a FOIL request to New York City](https://www.muckrock.com/foi/new-york-city-17/pet-licensing-data-for-new-york-city-23826/)

# ## Do your importing and your setup

# In[1]:


import pandas as pd


# In[2]:


import matplotlib.pyplot as plt


# ## Read in the file `NYC_Dog_Licenses_Current_as_of_4-28-2016.xlsx` and look at the first five rows

# In[3]:


df = pd.read_excel('NYC_Dog_Licenses_Current_as_of_4-28-2016.xlsx')


# ## How many rows do you have in the data? What are the column types?
# 
# If there are more than 30,000 rows in your dataset, go back and only read in the first 30,000.

# In[4]:


df.shape[0]


# In[5]:


df.shape[1]


# In[6]:


df.dtypes


# In[7]:


df.head()


# ## Describe the dataset in words. What is each row? List two column titles along with what each of those columns means.
# 
# For example: “Each row is an animal in the zoo. `is_reptile` is whether the animal is a reptile or not”

# In[11]:


# Each row represents a single dog.  
#The dataset gives demographic details about each one of the dogs such as their breed, color, 
#medical details, age, etc. For example, Animal Birth is the date the dog was born, and 
# Vaccinated details Yes or No about the dogs vaccination status.


# # Your thoughts
# 
# Think of four questions you could ask this dataset. **Don't ask them**, just write them down in the cell below. Feel free to use either Markdown or Python comments.

# 1. Which zip codes have the most dogs registered within them?
# 2. What percentage of the dataset of dogs is a trained or guard dog?
# 3. Do most dogs have only one breed or are most dogs a mix?
# 4. What percentage of female dogs are spayed? males nutered?

# # Looking at some dogs

# ## What are the most popular (primary) breeds of dogs? Graph the top 10.

# In[37]:


df['Primary Breed'].value_counts().dropna().head(10)


# ## "Unknown" is a terrible breed! Graph the top 10 breeds that are NOT Unknown

# In[69]:


# df['Primary Breed' != 'Unknown'].value_counts().dropna().head(10)
# this is not working for some reason 


# df['Primary Breed'].ne['Unknown'].value_counts().dropna().head(10)
# also does not work for some reason

# df[df['Primary Breed'] != 'Unknown'].value_counts().head(10)
# also does not work, don't understand why not

# referencing https://pandas.pydata.org/pandas-docs/version/0.24.2/reference/api/pandas.DataFrame.ne.html 


# ## What are the most popular dog names?

# In[45]:


df['Animal Name'].value_counts().head()


# ## Do any dogs have your name? How many dogs are named "Max," and how many are named "Maxwell"?

# In[48]:


df[df['Animal Name'] == 'Emily']


# In[53]:


df[df['Animal Name'] == 'Max']['Animal Name'].count()


# In[52]:


df[df['Animal Name'] == 'Maxwell']['Animal Name'].count()


# ## What percentage of dogs are guard dogs?
# 
# Check out the documentation for [value counts](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.value_counts.html).

# In[54]:


df['Guard or Trained'].value_counts(normalize = True)


# ## What are the actual numbers?

# In[55]:


df['Guard or Trained'].value_counts()


# ## Wait... if you add that up, is it the same as your number of rows? Where are the other dogs???? How can we find them??????
# 
# Use your `.head()` to think about it, then you'll do some magic with `.value_counts()`

# In[59]:


df['Guard or Trained'].count()
#rows = 81937


# In[60]:


df.head()


# In[61]:


df['Guard or Trained'].value_counts(dropna = False)


# ## Fill in all of those empty "Guard or Trained" columns with "No"
# 
# Then check your result with another `.value_counts()`

# In[64]:


df['Guard or Trained'].fillna('No').value_counts()


# ## What are the top dog breeds for guard dogs? 

# In[67]:


df[df['Guard or Trained'] == 'Yes']['Primary Breed'].value_counts().head()


# ## Create a new column called "year" that is the dog's year of birth
# 
# The `Animal Birth` column is a datetime, so you can get the year out of it with the code `df['Animal Birth'].apply(lambda birth: birth.year)`.

# In[68]:


df['year'] = df['Animal Birth'].apply(lambda birth: birth.year)


# ## Calculate a new column called “age” that shows approximately how old the dog is. How old are dogs on average?

# In[72]:


# referencing this https://www.geeksforgeeks.org/convert-birth-date-to-age-in-pandas/ 

# from datetime import datetime, date

# maybe we are not supposed to go this in depth?  


# In[73]:


df['age'] = 2021 - df['year']


# In[75]:


df['age'].mean().round()


# # Joining data together

# ## Which neighborhood does each dog live in?
# 
# You also have a (terrible) list of NYC neighborhoods in `zipcodes-neighborhoods.csv`. Join these two datasets together, so we know what neighborhood each dog lives in. **Be sure to not read it in as `df`, or else you'll overwrite your dogs dataframe.**

# In[76]:


df_zip = pd.read_csv('zipcodes-neighborhoods.csv')
df_zip


# In[78]:


df.merge(df_zip, left_on='Owner Zip Code', right_on='zip')


# In[79]:


df = df.merge(df_zip, left_on='Owner Zip Code', right_on='zip')


# ## What is the most popular dog name in all parts of the Bronx? How about Brooklyn? The Upper East Side?

# In[94]:


df[df['borough'] == 'Bronx']['Animal Name'].value_counts().head(1)


# In[95]:


df[df['borough'] == 'Brooklyn']['Animal Name'].value_counts().head(1)


# In[105]:


df[df['neighborhood'] == 'Upper East Side']['Animal Name'].value_counts().head(1)


# ## What is the most common dog breed in each of the neighborhoods of NYC?

# In[119]:


df.groupby(by='neighborhood')['Primary Breed'].value_counts().head(1)
# I am not sure how to get it to print for each neighborhood rather than simply printing the single one on top


# In[122]:


df.groupby(by='neighborhood')['Primary Breed'].value_counts()


# ## What breed of dogs are the least likely to be spayed? Male or female?

# In[129]:


df.groupby(by = 'Primary Breed')['Spayed or Neut'].value_counts(normalize = True).round(2)


# In[132]:


df[df.groupby(by = 'Primary Breed')['Spayed or Neut'].value_counts(normalize = True).round(2)][['Spayed or Neut' == 'Yes'] < ['Spayed or Neut' == 'No']]
# Not sure how to write this one.


# In[ ]:





# ## Make a new column called monochrome that is True for any animal that only has black, white or grey as one of its colors. How many animals are monochrome?

# In[134]:


#df['monochrome'] = 
#df.monochrome.count()
df[[df['Animal Dominant Color']|df['Animal Secondary Color']|df['Animal Third Color']] == ['Black'|'White'|'Grey', case = False]]
# I don't see what it means about the syntax error here.  It's pointing to the y? 


# ## How many dogs are in each borough? Plot it in a graph.

# In[137]:


df.borough.value_counts()


# In[141]:


import matplotlib.pyplot as plt

df.borough.value_counts().plot.barh()
plt.xlabel('Number of Dogs')
plt.ylabel('Borough of NYC')
plt.title('By Borough ')
plt.suptitle("Dogs of NYC")


# ## Which borough has the highest number of dogs per-capita?
# 
# You’ll need to merge in `population_boro.csv`

# In[ ]:





# ## Make a bar graph of the top 5 breeds in each borough.
# 
# How do you groupby and then only take the top X number? You **really** should ask me, because it's kind of crazy.

# In[ ]:





# ## What percentage of dogs are not guard dogs?

# In[ ]:




