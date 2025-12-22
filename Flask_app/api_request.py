#GET
#
# import requests
#
# url = 'http://127.0.0.1:5000/'
# response = requests.get(url)
#
# print(response.status_code) # Prints the HTTP status code (e.g., 200 for OK)
# print(response.text)        # Prints the raw content of the response in unicode
# print(response.json())      # Parses JSON content into a Python dictionary or list


#POST

import requests

url = 'http://127.0.0.1:5000/jobs'
payload ={
    'title':'Python Developer',
    'company':'Google',
    'location':'Hyderabad'
}

# Use the 'data' parameter for form-encoded data
# Use the 'json' parameter for JSON data (requests handles serialization and headers)
response = requests.post(url, json=payload)

print(response.json())
