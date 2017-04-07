import executor #pip install executor
import requests
import time

def ask_for_sort(url, file_name):
    files = {"file": open(file_name)}
    start = time.time()
    response = requests.post(url, files=files)
    time_spend = time.time() - start
    return [response, time_spend]
    
def _print(tab, print_data):
    print(str(tab[1]) + " sekund!")
    print(tab[0].text.split('\n')[0] + " stevilo elementov!")
    if(print_data != 0):
        print(tab[0].text)
    return

url = "https://zzrs-server-kristanm1.c9users.io/nalozi"
file_name = "./int_50x.txt"
tab = ask_for_sort(url, file_name)
_print(tab, 1)