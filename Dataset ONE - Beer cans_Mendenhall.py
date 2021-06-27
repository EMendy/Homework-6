#!/usr/bin/env python
# coding: utf-8

# # Homework 6, Part One: Lots and lots of questions about beer

# ### Do your importing and your setup

# In[1]:


import pandas as pd


# ## Read in the file `craftcans.csv`, and look at the first first rows

# In[2]:


df = pd.read_csv('craftcans.csv', na_values = ['Does not apply'])


# ## How many rows do you have in the data? What are the column types?

# In[3]:


df.shape[0]


# In[4]:


df.shape[1]


# In[5]:


df


# In[6]:


df.dtypes


# # Checking out our alcohol

# ## What are the top 10 producers of cans of beer?

# In[7]:


df.Brewery.value_counts().head(10)


# ## What is the most common ABV? (alcohol by volume)

# In[8]:


# why does the code below give me an answer despite ABV being an object rather than an int?

df.ABV.mode()


# ## Oh, weird, ABV isn't a number. Convert it to a number for me, please.
# 
# It's going to take a few steps!
# 
# ### First, let's just look at the ABV column by itself

# In[9]:


df.ABV


# ### Hm, `%` isn't part of  a number. Let's remove it.
# 
# When you're confident you got it right, save the results back into the `ABV` column.
# 
# - *Tip: In programming the easiest way to remove something is to *replacing it with nothing*.
# - *Tip: "nothing" might seem like `NaN` sinc we talked about it a lot in class, but in this case it isn't! It's just an empty string, like ""*
# - *Tip: `.replace` is used for replacing ENTIRE cells, while `.str.replace` is useful for replacing PARTS of cells (see my New York example)*

# In[10]:


df.ABV = df.ABV.str.replace('%','')


# In[11]:


df.ABV


# ### Now let's turn `ABV` into a numeric data type
# 
# Save the results back into the `ABV` column (again), and then check `df.dtypes` to make sure it worked.
# 
# - *Tip: We used `.astype(int)` during class, but this has a decimal in it...*

# In[12]:


df.ABV.astype(float)


# In[13]:


df.ABV = df.ABV.astype(float)


# In[14]:


df.dtypes


# ## What's the ABV of the average beer look like?
# 
# ### Show me in two different ways: one command to show the `median`/`mean`/etc, and secondly show me a chart

# In[15]:


df.ABV.mean().round(2)


# In[16]:


df.ABV.hist()


# In[17]:


df.ABV.plot(kind = 'barh', x = 'ABV', y = 'Beer')
#This is not a good visual option for this. The Hist is the best option, 


# ### We don't have ABV for all of the beers, how many are we missing them from?
# 
# - *Tip: You can use `isnull()` or `notnull()` to see where a column is missing data.*
# - *Tip: You just want to count how many `True`s and `False`s there are.*
# - *Tip: It's a weird trick involving something we usually use to count things in a column*

# In[18]:


df.ABV.isnull().value_counts()


# # Looking at location
# 
# Brooklyn used to produce 80% of the country's beer! Let's see if it's still true.

# ## What are the top 10 cities in the US for canned craft beer?

# In[19]:


# I assume that means "What are the top ten highest producing cities in the US?" i.e. which cities produce the most beer?

#df.groupby(by = 'Location').Beer.value_counts(ascending = False).head(10)
#first instinct was too complex.  I can achieve what I need with less. 

df.Location.value_counts(ascending = False).head(10)


# ## List all of the beer from Brooklyn, NY

# In[20]:


df[df.Location == 'Brooklyn, NY']


# ## What brewery in Brooklyn puts out the most cans of beer?

# In[21]:


df[df.Location == 'Brooklyn, NY'].Brewery.value_counts(ascending = False).head(1)


# ## What are the five most popular styles of beer produced by Sixpoint?

# In[22]:


df[(df.Location == 'Brooklyn, NY') & (df.Brewery == 'Sixpoint Craft Ales')].Style.value_counts(ascending = False).head()


# ## List all of the breweries in New York state.
# 
# - *Tip: We want to match *part* of the `Location` column, but not all of it.*
# - *Tip: Watch out for `NaN` values! You might be close, but you'll need to pass an extra parameter to make it work without an error.*

# In[23]:


import numpy as np

df[df.Location.str.contains("NY", na=False)].Brewery.drop_duplicates()


# ### Now *count* all of the breweries in New York state

# In[24]:


df[df.Location.str.contains("NY", na=False)].Brewery.drop_duplicates().count()


# # Measuring International Bitterness Units
# 
# ## Display all of the IPAs
# 
# Include American IPAs, Imperial IPAs, and anything else with "IPA in it."
# 
# IPA stands for [India Pale Ale](https://www.bonappetit.com/story/ipa-beer-styles), and is probably the most popular kind of beer in the US for people who are drinking [craft beer](https://www.craftbeer.com/beer/what-is-craft-beer).

# In[25]:


df[df.Style.str.contains("IPA", na=False)]


# IPAs are usually pretty hoppy and bitter. IBU stands for [International Bitterness Unit](http://www.thebrewenthusiast.com/ibus/), and while a lot of places like to brag about having the most bitter beer (it's an American thing!), IBUs don't necessary *mean anything*.
# 
# Let's look at how different beers have different IBU measurements.

# ## Try to get the average IBU measurement across all beers

# In[26]:


#df.IBUs = df.IBUs.replace("N.S.", np.nan)
df.IBUs.isnull().value_counts()


# In[30]:


#df[df.IBUs.isnull()]


# In[29]:


#df.IBUs.value_counts()


# ### Oh no, it doesn't work!
# 
# It looks like some of those values *aren't numbers*. There are two ways to fix this:
# 
# 1. Do the `.replace` and `np.nan` thing we did in class. Then convert the column to a number. This is boring.
# 2. When you're reading in your csv, there [is an option called `na_values`](http://pandas.pydata.org/pandas-docs/version/0.23/generated/pandas.read_csv.html). You can give it a list of **numbers or strings to count as `NaN`**. It's a lot easier than doing the `np.nan` thing, although you'll need to go add it up top and run all of your cells again.
# 
# - *Tip: Make sure you're giving `na_values` a LIST, not just a string*
# 
# ### Now try to get the average IBUs again

# In[34]:


df.IBUs.mean().round(2)


# ## Draw the distribution of IBU measurements, but with *twenty* bins instead of the default of 10
# 
# - *Tip: Every time I ask for a distribution, I'm looking for a histogram*
# - *Tip: Use the `?` to get all of the options for building a histogram*
# - *Tip: Make sure your `matplotlib` thing is set up right!*

# In[57]:


import matplotlib.pyplot as plt


# In[68]:


df.IBUs.hist(bins=20)
plt.xlabel('IBUs')
plt.ylabel('Frequency')
plt.title('IBU Spread ')
plt.suptitle("Beers of America")


# ## Hm, Interesting distribution. List all of the beers with IBUs above the 75th percentile
# 
# - *Tip: There's a single that gives you the 25/50/75th percentile*
# - *Tip: You can just manually type the number when you list those beers*

# In[88]:


# df.IBUs.quantile(.75j).Beer

# This doesn't work. DOn't understand what I'm supposed to do here. I've tried to write it six or seven different ways that all give very long errors


# In[ ]:





# ## List all of the beers with IBUs below the 25th percentile

# In[89]:


# df.IBUs.quantile(.25i).Beer
# Same thing. No idea here. This is how it looks in documentations.


# ## List the median IBUs of each type of beer. Graph it.
# 
# Put the highest at the top, and the missing ones at the bottom.
# 
# - Tip: Look at the options for `sort_values` to figure out the `NaN` thing. The `?` probably won't help you here.

# In[92]:


df.groupby(by='Style').IBUs.median()


# In[97]:


# df.groupby(by='Style').IBUs.median().sort_values(ascending = False, na = False)  
    #doesn't work for some reason

df.groupby(by='Style').IBUs.median().sort_values(ascending = False)

#It appears that it automatically puts the Nan Vlaues last?  Is that the case 


# ## Hmmmm, it looks like they are generally different styles. What are the most common 5 styles of high-IBU beer vs. low-IBU beer?
# 
# - *Tip: You'll want to think about it in three pieces - filtering to only find the specific beers beers, then finding out what the most common styles are, then getting the top 5.*
# - *Tip: You CANNOT do this in one command. It's going to be one command for the high and one for the low.*
# - *Tip: "High IBU" means higher than 75th percentile, "Low IBU" is under 25th percentile*

# In[98]:


#df.groupby(by='Style').IBUs.median().sort_values(ascending = False).dropna()
#  I couldn't get the percentiles to work so I won't be able to do this one.


# In[ ]:





# ## Get the average IBU of "Witbier", "Hefeweizen" and "American Pale Wheat Ale" styles
# 
# I'm counting these as wheat beers. If you see any other wheat beer categories, feel free to include them. I want ONE measurement and ONE graph, not three separate ones. And 20 to 30 bins in the histogram, please.
# 
# - *Tip: I hope that `isin` is in your toolbox*

# In[101]:


df[(df.Style == "Witbier")|(df.Style == "Hefeweizen")|(df.Style == "American Pale Wheat Ale")].IBUs.mean().round(2)


# ## Draw a histogram of the IBUs of those beers

# In[104]:


df[(df.Style == "Witbier")|(df.Style == "Hefeweizen")|(df.Style == "American Pale Wheat Ale")].IBUs.hist()
plt.xlabel("IBUs")
plt.ylabel("Frequency")


# ## Get the average IBU of any style with "IPA" in it (also draw a histogram)

# In[106]:


df[df.Style.str.contains("IPA", na=False)].IBUs.mean().round(2)


# In[108]:


df[df.Style.str.contains("IPA", na=False)].IBUs.hist()
plt.xlabel("IBUs")
plt.ylabel("Frequency")


# ## Plot those two histograms on top of one another
# 
# To plot two plots on top of one another, you do two steps.
# 
# 1. First, you make a plot using `plot` or `hist`, and you save it into a variable called `ax`.
# 2. You draw your second graph using `plot` or `hist`, and send `ax=ax` to it as a parameter.
# 
# It would look something like this:
# 
# ```python
# ax = df.plot(....)
# df.plot(ax=ax, ....)
# ``` 
# 
# (...except totally different)

# In[110]:


ax = df[df.Style.str.contains("IPA", na=False)].IBUs.hist()


# In[111]:


df[df.Style.str.contains("IPA", na=False)].IBUs.hist(ax=ax)
plt.xlabel("IBUs")
plt.ylabel("Frequency")


# In[ ]:


# Seems that I followed as it is mentioned but I am getting this long error.


# ## Compare the ABV of wheat beers vs. IPAs : their IBUs were really different, but how about their alcohol percentage?
# 
# Wheat beers might include witbier, hefeweizen, American Pale Wheat Ale, and anything else you think is wheaty. IPAs probably have "IPA" in their name.

# In[112]:


df[(df.Style == "Witbier")|(df.Style == "Hefeweizen")|(df.Style == "American Pale Wheat Ale")].ABV.mean().round(2)


# In[114]:


df[df.Style.str.contains("IPA", na=False)].ABV.mean().round(2)


# In[ ]:





# ## Good work!
# 
# If you made it this far you deserve a drink.

# In[115]:


#I couldn't figure out at least three of them, so I wouldn't say I made it whole. 


# In[ ]:




