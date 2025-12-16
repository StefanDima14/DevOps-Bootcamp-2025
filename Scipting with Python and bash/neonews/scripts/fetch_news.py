import requests

url = 'https://newsdata.io/api/1/latest?apikey=pub_1e47f19aa7e34cf69b7c9081919a62a3&country=ro&language=ro&category=business&removeduplicate=1'
response = requests.get(url)
data = response.json()
print(data)