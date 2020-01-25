from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from requests.compat import quote_plus
from . import models

# Create your views here.

BASE_CRAIGLISTS_URL = 'https://kaiserslautern.craigslist.org/search/?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'

def home(request):
    return render(request, 'search/base.html')

def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url = BASE_CRAIGLISTS_URL.format(quote_plus(search)) #add the plus sign between the search words
    response = requests.get(final_url)
    data = response.text

    soup = BeautifulSoup(data, features='html.parser')

    post_listings = soup.find_all('li', {'class': 'result-row'}) #list class name of craigslist

    final_posting = []

    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')

        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'

        if post.find(class_='result-image').get('data-ids'):
            post_image = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1] #get the post image name/id in a list form
            post_image_url = BASE_IMAGE_URL.format(post_image)
        else:
            post_image_url = 'https://www.insidehighered.com/sites/default/server_files/styles/large/public/media/barber_question_0.jpg'

        #post_text = new_soup.find(id='postingbody').text

        final_posting.append((post_title, post_url, post_price, post_image_url))

    # print(post_title) #gets the link of first search result from craigslist
    # print(post_url)
    # print(post_price)

    search_for_frontend = {
        'search': search,
        'final_posting': final_posting,
    }

    return render(request, 'search/new_search.html', search_for_frontend)


