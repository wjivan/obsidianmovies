import pandas as pd
import utils
import importlib
import pickle
from alive_progress import alive_bar

# %load_ext autoreload
# %autoreload 2
importlib.reload(utils)
from utils import movie_search, create_markdown_page

# Import a list of movie names to search
to_search = pd.read_csv('movies_to_search.csv')

# Using the function to fill up the csv
results = []
my_search = to_search['Movies'].tolist()

with alive_bar(len(my_search)) as bar:
    for m in my_search:
        info = movie_search(m)
        results.append(info)
        bar()

myresults = pd.DataFrame(results)

# Save a copy of myresults
myresults.to_pickle('download_results.pkl')
myresults.to_csv('myresult.csv')

## OPTION1: CREATING INDIVIDUAL MARKDOWN FILES
# Create small markdown pages
create_markdown_page(myresults)

## OPTION 2: CREATE A MAIN MARKDOWN PAGE
# Add obsidian links to the title
myresults['title'] = '[['+myresults['title']+']]'

## OPTION 3: FILTER OUT JUST THE FACTS
facts = ['title', 'year', 'rating','genre', 'country', 'director', 'cast']
simpleresults = myresults[facts]

## SAVE OUT AS TEXT
with open('movie_main.txt','w') as file_out:
    simpleresults.to_markdown(buf=file_out)

