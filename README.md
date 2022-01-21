# Motivation
Obsidian is a great productivity tool that I use to keep my thoughts and ideas in place. One area I want to log and review are movies. When I sat down and listed all my favourite movies, it came down to a list of more than 100 movies! Trying to search through the cast and directors for all these movies is time consuming and I just want to get a quick summary of the movie before trying to write my own thoughts on them. So I decided to use Python to automate this for me. 

# Requirements
You need to install Python and its required packages for this to work. To install these, type `pip install requirements.txt`. 

# How this works
1. Input all the movies to search into the csv `movies_to_search.csv`. 
2. The script makes use of the [`imdb` package](https://imdbpy.github.io/) to download the metadata from IMDB. This does not require you to have an IMDB api account. You can check out their documentations on what data is available to adjust as required. I created a function that allows me to down the information regarding:
- title
- plot
- genre
- country
- cover url
- director
- kind
- rating
- synopsis
- year

```python
from imdb import IMDb

def movie_search(my_title):
    """
    Given a string (movie title), find the metadata for that movie (or the closest
    one matching that name).

    Parameters
    ----------
    my_title : string

    returns a dictionary of metadata
    """
    # create a dictionary to store data
    information = dict()

    # create an instance of the IMDb class
    ia = IMDb()

    # search for a movie
    lookups = ia.search_movie(my_title)

    # use the first search result to return the id
    try:
        # Test if any movies are found
        movie_id = lookups[0].movieID

        # get a movie
        movie = ia.get_movie(movie_id)

        # RETRIEVE DATA
        # Get the movie title searched for
        t = movie['title']
        information['title'] = t
        print(f'Retrieving data for {t}')

        # Get the plot outline
        try:
            information['plot'] = movie['plot outline']
        except:
            print('plot outline not available')
            try:
                information['plot'] = movie['plot'][0]
            except:
                print('plot also not available')
                information['plot'] = ''

        # Get the genre
        try:
            information['genre'] = ','.join(movie['genre'])
        except:
            print('no information on genre')
            information['genre'] = ''

        # Get the country
        try:
            information['country'] = ','.join(movie['countries'])
        except:
            print('no information on country')
            information['country'] = ''

        # Get the director
        # Extract the names in each Person object
        try:
            director_names = [d['name'] for d in movie['directors']]
            information['director'] = ','.join(director_names)
        except:
            print('director information not available')
            information['director'] = ''

        # Get the cast
        # Extract the top 5 names in cast (if it exists)
        try:
            cast_names = [d['name'] for d in movie['cast']]
            if len(cast_names) >5:
                cast_names = cast_names[0:5]
            information['cast'] = ','.join(cast_names)
        except:
            print('No information on cast')
            information['cast'] = ''
        
        # Get the rating
        try:
            information['rating'] = movie['rating']
        except:
            print('rating info is not available')
            information['rating'] = 'N/A'

        # Get the year
        try:
            information['year'] = movie['year']
        except:
            print('no information on year')
            information['year'] = ''

        # Get the type
        try:
            information['kind'] = movie['kind']
        except:
            print('type not available')
            information['kind'] = ''

        # Get the cover url
        try:
            information['cover url'] = movie['cover url']
        except:
            print('cover url not available')
            information['cover url'] = ''

        # Get sypnosis
        try:
            information['synopsis'] = movie['synopsis'][0]
        except:
            print('no synopsis')
            information['synopsis'] = ''
    except:
        print('NO RESULTS FOUND FOR {my_title}')
        information['title'] = my_title
        information['plot'] = ''
        information['genre'] = ''
        information['country'] = ''
        information['cover url'] = ''
        information['director'] = ''
        information['kind'] = ''
        information['rating'] = ''
        information['synopsis'] = ''
        information['year'] = ''

    return(information)
```

3. Obsidian reads markdown pages so I automate the creation of markdown pages using python using [mdutils](https://pypi.org/project/mdutils/). I create a function to automate the creation of a standard template filled in with the new metadata:

```python
def create_markdown_page(myresults):
    """
    Given a dataframe containing all the information about movies, 
    we can create individual pages

    Parameters
    ----------
    myresults : DataFrame
        Contains essential headers: title, year, rating, genre, country, director
        cast, synopsis and plot
    """
    # Create iterations
    for index, row in myresults.iterrows():
        # Create a file
        mdFile = MdUtils(file_name=row['title'])

        # Create a metadata section
        mdFile.new_line(text='---\n')
        facts = ['year', 'rating','genre', 'country', 'director', 'cast']
        for f in facts:
            mdFile.new_line(text=f'{f.title()}: {row[f]}')
        mdFile.new_line(text='Type: Review')
        mdFile.new_line(text='')
        mdFile.new_line(text='---\n')

        # Create a title
        mdFile.new_header(level=1, title=row['title'])

        # Create a cover
        # i could use new_inline_image but the text wraps at 20 characters
        # creating a break. Hence, I code my own image line and unwrap it
        cover_link = '!['+ row['title'] + '](' + row['cover url'] + ')'
        mdFile.write(text = cover_link, wrap_width=0)

        # Create a section for the plot
        mdFile.new_header(level=1, title="Plot")

        # Clean up plot text
        plot_text = row['plot']
        plot_text = ' '.join(plot_text.split())
        plot_text = plot_text.replace('\ ','')
        mdFile.new_line(text=plot_text, wrap_width=0)

        # Create my own review section
        mdFile.new_header(level=1, title="My own thoughts")

        # Create markdown
        mdFile.create_md_file()
```

You can drag and drop these newly created markdown sheets into Obsidian. 
