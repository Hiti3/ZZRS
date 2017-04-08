import requests
import time
from threading import Thread

def ask_for_sort(url, file_name):
    files = {"file": open(file_name)}
    start = time.time()
    response = requests.post(url, files=files)
    time_spent = time.time() - start
    _print([response, time_spent], 0)
    return [response, time_spent]
    
def _print(tab, print_data):
    num_elements = tab[0].text.split('\n')[0]
    total_time = round(tab[1], 3)
    print(num_elements + " elements " + str(total_time) + " s")
    if(print_data != 0):
        print(tab[0].text)
    return

c9_username = ""
c9_workspace_name = ""
url = "https://" + c9_workspace_name + "-" + c9_username + ".c9users.io/nalozi"
file_name = "inputs/int_10000.txt"
num_threads = 50

for i in range(num_threads):
    t = Thread(target=ask_for_sort, args=(url, file_name))
    t.start()
