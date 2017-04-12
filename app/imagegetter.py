import requests
from bs4 import BeautifulSoup
import urlparse


def getimages():
   url = "https://www.walmart.com/ip/54649026"
   result = requests.get(url)
   soup = BeautifulSoup(result.text, "html.parser")

   imagelisting = []

   # This will look for a meta tag with the og:image property
   og_image = (soup.find('meta', property='og:image') or
	                    soup.find('meta', attrs={'name': 'og:image'}))
   if og_image and og_image['content']:
       imagelisting.append(og_image['content'])

   # This will look for a link tag with a rel attribute set to 'image_src'
   thumbnail_spec = soup.find('link', rel='image_src')
   if thumbnail_spec and thumbnail_spec['href']:
       imagelisting.append(thumbnail_spec['href'])

   for img in soup.findAll("img", src=True):
       if img["src"] not in imagelisting: # removes duplication of urls
           imagelisting.append(img['src'])
   return imagelisting
