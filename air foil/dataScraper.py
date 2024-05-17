import requests
from bs4 import BeautifulSoup as bs4
import json

# Airfoil Coordinates Database URL Starter
URL_START = "https://m-selig.ae.illinois.edu/ads/"

# airfoil json data file structure 
#   airfoil_data = {
#                   "code":{
#                     "x": [
#                       1, 2, 3, 4,...
#                     ],
#                     "y": [
#                       1, 2, 3, 4,...
#                     ]
#                   },
#               }


# Get Foil urls and data
class AirfoilDataScraper:
    def __init__(self, url):
        self.url = url # Existing in main file
        self.data_links = [] 
        self.airfoil_data = {} # For save in the json file

    def scrape_data(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            soup = bs4(response.content, 'html.parser')
            links = soup.find_all('a') # Thses are a html "a" tags
            for link in links:
                coord_direction = link.get('href')
                # Get the real url existed in href atributes
                if isinstance(coord_direction, str) and coord_direction.startswith("coord/"):
                    data_link = URL_START + coord_direction
                    self.data_links.append(data_link)
                    # Get coord dat file
                    response = requests.get(data_link)
                    # Collect airfoil codes
                    foil_code = coord_direction[6:-4]
                    if response.status_code == 200:
                        content = response.text
                        lines = content.splitlines()
                        # Declare x and y points lists
                        x = []
                        y = []
                        for line in lines:
                            all_xandy = line.split()
                            # Ignoring lines that more than to two block of text
                            if len(all_xandy) == 2:
                                try:
                                    # Except finding points > 1
                                    if -1 <= float(all_xandy[0]) <= 1 and -1 <= float(all_xandy[1]) <= 1:
                                        x.append(float(all_xandy[0]))
                                        y.append(float(all_xandy[1]))
                                except ValueError:
                                    # Skip lines that cannot be converted to floats (e.g., headers)
                                    pass
                        response.close() # Cloes Airfoil Coordinates Database request

                        new_foil = {"x": x, "y": y} # Initialize lists of x and y coordinates
                        self.airfoil_data[foil_code] = new_foil # Add air foil codes
        # Failure message  
        else:
            print(f"error code {response.status_code}")
        response.close()

    def save_data_as_json(self, filename):
        with open(filename, 'w') as json_file:
            json.dump(self.airfoil_data, json_file, indent=4)
            json_file.close()
