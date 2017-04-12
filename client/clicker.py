import requests
import time
from threading import Thread

c9_username = "kristanm1"
c9_workspace_name = "zzrs-server"
url = "https://" + c9_workspace_name + "-" + c9_username + ".c9users.io/nalozi"
data_type = "int"
input_size = 100000
num_clients = 10
num_files = 2
file_list = ["inputs/"+data_type+"_"+str(input_size)+"/"+data_type+"_"+str(input_size)+"_"+str(i)+".txt" for i in range(num_files)]
threads = []

times = [0.0] * num_clients

def ask_for_sort(url, file_name):
    files = {"file": open(file_name)}
    start = time.time()
    response = requests.post(url, files=files)
    time_spent = time.time() - start
    return [response, time_spent]
    
def _print(tab, client_id, file_id, print_data):
    num_elements = tab[0].text.split('\n')[0]
    total_time = str(round(tab[1], 3))
    times[int(client_id)] += float(total_time)
    print("client: " + client_id + " file: " + file_id + " elements: " + num_elements + " time: " + total_time + " s")
    if(print_data != 0):
        print(tab[0].text)
    return

def sort_file_list(url, file_list, client_id):
    for i, file in enumerate(file_list):
        data = ask_for_sort(url, file)
        _print(data, str(client_id), str(i), 0)
    return

for i in range(num_clients):
    threads.append(Thread(target=sort_file_list, args=(url, file_list, i)))
    threads[i].start()

sum = 0.0;
for i in range(num_clients):
    threads[i].join()
    sum = sum + float(times[i]/num_files)

print("Povprecen cas: " + str(sum/num_clients))
print("Stevilo odjemalcev: " + str(num_clients))
print("Stevilo podatkov v datoteki: " + str(input_size))
print("Stevilo razlicnih datotek: " + str(num_files))