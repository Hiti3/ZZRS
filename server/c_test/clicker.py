import requests
import time


url = 'https://zzrs-server-kristanm1.c9users.io/nalozi'
files = {'file': open('./int_50000x.txt')}
start = time.time()
response = requests.post(url, files=files)
end = time.time()

print(end - start)
#print(response.text)
