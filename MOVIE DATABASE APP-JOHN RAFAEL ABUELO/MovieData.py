#importing modules
import requests
import tmdbsimple as tmdb
import urllib.request
from urllib.error import HTTPError, URLError
from PIL import Image

#importing API key
API_KEY = '62c29c67169d49f5b6d44ae275e236c5'

#importing tmdb API database
tmdb.API_KEY = API_KEY
tmdb.REQUESTS_TIMEOUT = 5
tmdb.REQUESTS_SESSION = requests.Session()

#class for storing and referencing movie details, description, and poster image
class MovieObject:
    def __init__(self, title, poster, description, rating, language, id, release):
        self.title = title
        self.poster = poster
        self.description = description
        self.rating = rating
        self.id = id
        self.language = language
        self.release_date = release
        


#creating function for downloading movie poster image from tmdb API database
def download_img(url, id):
    try:
        img_name = f"posters/{id}.jpg"
        urllib.request.urlretrieve(f"{url}", img_name)
    except (HTTPError, URLError):
        return "default_movie.jpg"
    
#setting image appearance
    basewidth = 320
    img = Image.open(img_name).convert('RGB')
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((basewidth, hsize))
    img.save(img_name)
    return img_name

#creating function for pulling the movie information from tmdb API database
def get_movie_data(query):
    search = tmdb.Search()
    search.movie(query=f"{query}")
    obj_list = []
    for result in search.results:
        try:
            result['release_date']
   
            obj_list.append(MovieObject(result['original_title'], result['poster_path'], result['overview']
                                        , result['vote_average'], result['original_language'], result['id'],
                                        result['release_date']))
        except KeyError:
            obj_list.append(MovieObject(result['original_title'], result['poster_path'], result['overview']
                                    , result['vote_average'], result['original_language'], result['id'],
                                        "Not Found"))
    return obj_list

    