# import packages
import httplib2
import json


# define functions
def findlocation(searchstring, google_api_key):
    """
    Description: This function helps users to find the coordinates of one location by using google geocode APIs.
                
    Parameters: -searchstring: the location that users want to know the coordinate
                -google_api_key: the google geocode API key
    
    Returns: This function will returns a list. The first element in this list is latitude. The second element 
            in this list is longtitude
    """
    # the google geocode API endpoints
    url = ('https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}'.format(searchstring, google_api_key))
    
    # use httplib2 packages to get the response from google geocode API
    h = httplib2.Http()
    response, content = h.request(url, 'GET')
    
    # parse the response and extract the latitude and longtitude
    result = json.loads(content)
    longtitude = result['results'][0]['geometry']['location']['lng']
    latitude = result['results'][0]['geometry']['location']['lat']
    
    return(latitude, longtitude)


def retrive_restaurant_inf(foursquare_client_id, foursquare_client_secret, latitude, longitude):
    """
    Description: This function helps users to find restaurants close to one location by using foursquare APIs.
                
    Parameters: -foursquare_client_id: the foursquare API ID
                -foursquare_client_secret: the foursquare API password
                -latitude: the latitude of the location that users want to find restaurants
                -longitude: the longitude of the location that users want to find restaurants

    Returns: This function will returns a dictionery. This dictionart will contain the restaurant's name, 
            the restaurant's address, and the restaurant's photos.
    """
    # define the searching area (meter)
    radius = '10000'
    
    # define the search type for the foursquare APIs
    search_type = 'restaurant'
    
    # the foursquare API endpoints
    url = ('https://api.foursquare.com/v2/venues/search?client_id={}&client_secret={}&v=20130815&ll={},{}&radius={}&query={}'.format(foursquare_client_id, foursquare_client_secret, latitude, longitude, radius, mealType))
    
     # use httplib2 packages to get the response from foursquare API
    h = httplib2.Http()
    text_response, text_content = h.request(url, 'GET')
    text_results = json.loads(text_content)
    
    # parse the response 
    restaurant_text_result = text_results['response']['venues']
    
    for i in range(0, len(restaurant_text_result)):
        venue_id = restaurant_text_result[i]['id']
        restaurant_name = restaurant_text_result[i]['name']
        restaurant_address = restaurant_text_result[i]['location']['formattedAddress']

        url = ('https://api.foursquare.com/v2/venues/{}/photos?client_id={}&v=20150603&client_secret={}'.format(venue_id,foursquare_client_id,foursquare_client_secret))
        photo_response, photo_content = h.request(url,'GET')
        photo_result = json.loads(photo_content)
               
        if photo_result['response']['photos']['count'] != 0:
            photo_result = photo_result['response']['photos']['items'][0]
            photo_url = photo_result['prefix'] + str(photo_result['width']) + str(photo_result['height']) + photo_result['suffix']
        
        elif photo_result['response']['photos']['count'] == 0:
            photo_url = 'This restaurant does not provide photos.'
            
        restaurant_dict[str(i)] = {'name': restaurant_name, 'addr': restaurant_address, 'img_url': photo_url}
    
    return restaurant_dict
	
	
# settings
google_key = 'your google API key'

foursquare_id = 'your foursquare API ID'
foursquare_password = 'your foursquare API password'


if __name__ == '__main__':
	
	restaurant_coordinate = findlocation('taipei', google_key)
	restaurant_inf_dict = retrive_restaurant_inf(foursquare_id, foursquare_password, restaurant_coordinate[0], restaurant_coordinate[1])
