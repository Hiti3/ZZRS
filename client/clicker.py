import requests
import time
from threading import Thread
from requests_throttler import BaseThrottler
import logging

c9_username = "kristanm1"
c9_workspace_name = "zzrs-server"
url = "https://" + c9_workspace_name + "-" + c9_username + ".c9users.io/nalozi"
data_type = "int"
input_size = 50000
num_clients = 5
num_files = 2
wait_for_response = True
request_delay = 0.5
file_list = ["inputs/"+data_type+"_"+str(input_size)+"/"+data_type+"_"+str(input_size)+"_"+str(i)+".txt" for i in range(num_files)]
threads = []

times = [0.0] * num_clients

def ask_for_sort(url, file_name):
    files = {"file": open(file_name)}
    start = time.time()
    response = requests.post(url, files=files)
    time_spent = time.time() - start
    return [response, time_spent]
    
def _print(response, client_id, file_id, print_data):
    num_elements = response.text.split('\n')[0]
    total_time = response.elapsed.total_seconds()
    times[int(client_id)] += float(total_time)
    print("client: {:d} file: {:d} elements: {:s} time: {:.3f} s".format(client_id, file_id, num_elements, total_time))

def sort_file_list(url, file_list, wait_for_response, request_delay, client_id):
    if wait_for_response:
        for i, file in enumerate(file_list):
            response = requests.post(url, files={"file": open(file)})
            _print(response, client_id, i, 0)
    else:
        reqs = [requests.Request(method="POST", url=url, files={"file": open(file_name)}) for file_name in file_list]
        with BaseThrottler(name='base-throttler', delay=request_delay) as bt:
            throttled_requests = bt.multi_submit(reqs)
        for i, tr in enumerate(throttled_requests):
            _print(tr.response, client_id, i, 0)
    return

logging.disable(logging.WARNING)
for i in range(num_clients):
    threads.append(Thread(target=sort_file_list, args=(url, file_list, wait_for_response, request_delay, i)))
    threads[i].start()

sum = 0.0;
for i in range(num_clients):
    threads[i].join()
    sum = sum + float(times[i]/num_files)

print("Povprecen cas: " + str(sum/num_clients))
print("Stevilo odjemalcev: " + str(num_clients))
print("Stevilo podatkov v datoteki: " + str(input_size))
print("Stevilo razlicnih datotek: " + str(num_files))