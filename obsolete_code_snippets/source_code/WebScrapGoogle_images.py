# PWP course 2021 University of Oulu
# Applied by Merja Kreivi-Kauppinen

# WebScrapGoogle_images.py

# The code for scrabing images from Google search image
# Downloads 80 images at once - limit is set by Google

# -------------------------------------------------------------------------------------
# The main parts of this code has been created by Goutam Borthakur
# He has GitHub site available at https://github.com/goutamborthakur555

# For explanation of this code, you can check YouTube video: https://www.youtube.com/watch?v=8AyKJxBxx0M&t=172s
# Or check GitHub site
# https://github.com/goutamborthakur555/WebScraping-with-and-without-proxy/blob/master/WebScraping-Google-Images-Bulk-Downloader.py

# -------------------------------------------------------------------------------------

# Before run the check 'User-Agent request header' on your browser !!!

# The User-Agent request header contains a characteristic string 
# that allows the network protocol peers to identify the application type, 
# operating system, and software version of the requesting software user agent.

# write: 'my user agent' in your browser to get your browser user agent details
# my user agent details presented below:
# Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36
# add 'User-Agent' details to u_agnt dict in code

# --------------------------------------------------------------------------------------

# Create empty folder at the same path than this file,
# and define the folder later in the code

# Run on python - python WebScrapGoogle_images.py

# Define input as search keyword or keywords,
# and define required image count - 80 is maximum

# --------------------------------------------------------------------------------------

import os
# pip install requests (to sent GET requests)
import requests
# BeautifulSoup (to parse html and getting data out from html, xml or other markup languages)
from bs4 import BeautifulSoup

# download images from google search image
Google_Image = 'https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&'

# needed for google search
u_agnt = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive',
} 

# folder at the same path than this file
Image_Folder = 'ImageDownload'

def main():
    if not os.path.exists(Image_Folder):
        os.mkdir(Image_Folder)
    download_images()

def download_images():
    data = input('Enter your search keyword(s): ')
    num_images = int(input('Enter the amount of images you want: '))
    
    print('Searching Images....')
    
    search_url = Google_Image + 'q=' + data #'q=' because its a query
    
    # request url, without u_agnt the permission gets denied
    response = requests.get(search_url, headers=u_agnt)
    html = response.text #To get actual result i.e. to read the html data in text mode
    
    # find all img where class='rg_i Q4LuWd'
    b_soup = BeautifulSoup(html, 'html.parser') #html.parser is used to parse/extract features from HTML files
    results = b_soup.findAll('img', {'class': 'rg_i Q4LuWd'})
    
    #extract the links of requested number of images with 'data-src' attribute and appended those links to a list 'imagelinks'
    #allow to continue the loop in case query fails for non-data-src attributes
    count = 0
    imagelinks= []
    for res in results:
        try:
            link = res['data-src']
            imagelinks.append(link)
            count = count + 1
            if (count >= num_images):
                break
            
        except KeyError:
            continue
    
    print(f'Found {len(imagelinks)} images')
    print('Start downloading...')

    for i, imagelink in enumerate(imagelinks):
        # open each image link and save the file
        response = requests.get(imagelink)
        
        imagename = Image_Folder + '/' + data + str(i+1) + '.jpg'
        with open(imagename, 'wb') as file:
            file.write(response.content)

    print('Download Completed!')
    

if __name__ == '__main__':
    main()