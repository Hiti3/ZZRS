import requests
import time
from threading import Thread

def ask_for_sort(url, file_name):
    files = {"file": open(file_name)}
    start = time.time()
    response = requests.post(url, files=files)
    time_spent = time.time() - start
    return [response, time_spent]
    
def _print(tab, client_id, file_id, print_data):
    num_elements = tab[0].text.split('\n')[0]
    total_time = str(round(tab[1], 3))
    print("client: " + client_id + " file: " + file_id + " elements: " + num_elements + " time: " + total_time + " s")
    if(print_data != 0):
        print(tab[0].text)
    return

def sort_file_list(url, file_list, client_id):
    for i, file in enumerate(file_list):
        data = ask_for_sort(url, file)
        _print(data, str(client_id), str(i), 0)
    return

c9_username = ""
c9_workspace_name = ""
url = "https://" + c9_workspace_name + "-" + c9_username + ".c9users.io/nalozi"
data_type = "int"
input_size = 10000
num_files = 10
file_list = ["inputs/" + data_type + "_" + str(input_size) + "_" + str(i) + ".txt" for i in range(num_files)]
num_clients = 10

for i in range(num_clients):
    t = Thread(target=sort_file_list, args=(url, file_list, i))
    t.start()
