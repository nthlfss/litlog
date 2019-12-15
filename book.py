import sys
from apiclient.discovery import build

# For this example, the API key is provided as a command-line argument.
api_key = 'AIzaSyD3EAagT7dIAfMal8iAXF6mgyimS_BD6vI'

# The apiclient.discovery.build() function returns an instance of an API service
# object that can be used to make API calls. The object is constructed with
# methods specific to the books API. The arguments provided are:
#   name of the API ('books')
#   version of the API you are using ('v1')
#   API key
service = build('books', 'v1', developerKey=api_key)

# The books API has a volumes().list() method that is used to list books
# given search criteria. Arguments provided are:
#   volumes source ('public')
#   search query ('android')
# The method returns an apiclient.http.HttpRequest object that encapsulates
# all information needed to make the request, but it does not call the API.
search = input('search: ')
request = service.volumes().list(source='public', q=search)

# The execute() function on the HttpRequest object actually calls the API.
# It returns a Python object built from the JSON response. You can print this
# object or refer to the Books API documentation to determine its structure.
response = request.execute()


# Accessing the response like a dict object with an 'items' key returns a list
# of item objects (books). The item object is a dict object with a 'volumeInfo'
# key. The volumeInfo object is a dict with keys 'title' and 'authors'.
print ('Found %d books:' % len(response['items']))
for book in response.get('items', []):
  print ('Title: %s, Authors: %s' % (
    book['volumeInfo']['title'],
    book['volumeInfo']['authors'])) 