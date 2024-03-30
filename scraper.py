import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify

app = Flask(__name__)

def scrape_website(url, all_data):
    # Send a GET request to the URL
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        border_elements = soup.find_all(class_='border-b border-gray-lighter py-6')

        # Loop through each border element
        for border_element in border_elements:
            # Find the nested element with the class name 'block justify-between md:flex'
            nested_element = border_element.find(class_='block justify-between md:flex')
            

            if nested_element:
                # Find the <h4> element within the nested element
                h4_element = nested_element.find('h4')
                stars_span = nested_element.find('span', class_='inline-flex')

                if h4_element:
                    # Print the text of the <h4> element

                    reviews_detail = {}
                    svg_elements = stars_span.find_all('svg')
                    stars_count = 0
                    for svg in svg_elements:
                        # Check if the <path> element within the <svg> has class 'text-gray-lighter'
                        path = svg.find('path', class_='text-gray-lighter fill-current')
                        if not path:
                            stars_count += 1

                    # this should be in JSON object as Review
                    
                    review = h4_element.text.strip()
                    
                    # print("Comment:", review)
                    reviews_detail['Review'] = review

                    # this should be in JSON object as Stars
                    # print( ' Number of star: ', stars_count)
                    reviews_detail['Stars'] = stars_count

                    response2 = requests.get(url + '/images')

                    if response2.status_code == 200:
                        # Parse the HTML content using BeautifulSoup
                        soup = BeautifulSoup(response2.content, 'html.parser')

                        images =[]

                        findImages = soup.find_all(class_='absolute inset-0 h-full w-full rounded-lg object-cover fade-in')
                        
                        numberOfImages = 0
                        for image in findImages: 
                            if numberOfImages > 4:
                                break

                            numberOfImages += 1

                            # this should be in JSON object as img link
                            picture = image.get('src')
                            images.append(picture)

                            # print('link: ', picture)
                        
                        reviews_detail['images'] = images
                    
                    all_data.append(reviews_detail)

                else:
                    print("No <h4> element found within nested element")
            else:
                print("No nested element with class 'block justify-between md:flex' found")
        
        
    else:
        print(f"Failed to fetch data from {url}")
    
    # return all_data
    # print(all_data)

def get_morphData():
    url = 'https://3883826a-2ad0-4b24-b764-554a6231791f.beta-api.morphdb.io/v0/data-api/record/query'
    headers = {
        'Content-Type': 'application/json',
        'X-API-KEY': 'YH6D79dTr7SLlyufqthfEqUE68H53OidKfpCf79r'
    }
    data = {
        'select': [
            "room_url"
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()["items"]  

# Define the endpoint to return the scraped data
@app.route('/scrape', methods=['GET'])
def scrape():
    all_data = []
    
    # Get room URLs from the API
    morph_data_items = get_morphData()
    room_urls = [item["room_url"] for item in morph_data_items]
    
    # Scrape each room URL
    for url in room_urls:
        scrape_website(url, all_data)
    
    # Return the scraped data as JSON
    return jsonify(all_data)

if __name__ == '__main__':
    app.run(debug=True)  





