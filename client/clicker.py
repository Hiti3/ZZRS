#INSTALLATION: sudo pip install RequestsThrottler

import requests
import time
from threading import Thread
from requests_throttler import BaseThrottler
import logging
import math

c9_username = "zkokelj"
c9_workspace_name = "newzzrs"
#url = "https://" + c9_workspace_name + "-" + c9_username + ".c9users.io/nalozi"
url = "http://46.101.220.240:8080/nalozi"
print(url)
data_type = "int"
input_size = 30000
num_clients = 10
num_files = 5
wait_for_response = True
request_delay = 0.5
file_list = ["inputs/"+data_type+"_"+str(input_size)+"/"+data_type+"_"+str(input_size)+"_"+str(i)+".txt" for i in range(num_files)]
#print(file_list)
threads = []

err = False
times = [0.0] * num_clients

def ask_for_sort(url, file_name):
    files = {"file": open(file_name)}
    start = time.time()
    response = requests.post(url, files=files)
    time_spent = time.time() - start
    return [response, time_spent]

def _print(response, client_id, file_id, print_data):
    num_elements = response.text.split('\n')[0]
    if not isinstance(num_elements, int):
        error = True
    total_time = response.elapsed.total_seconds()
    times[int(client_id)] += float(total_time)
    print("client: {:3d} file: {:3d} elements: {:6s} time: {:.3f} s".format(client_id, file_id, num_elements, total_time))

def sort_file_list(url, file_list, wait_for_response, request_delay, client_id):
    if wait_for_response:
        for i, file in enumerate(file_list):
            response = requests.post(url, files={"file": open(file)})
            #print(response.text)
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
    sum = sum + float(times[i])

sd = 0.0 # std deviation
mean = (sum/num_clients) # avg time per 1 user over all his files
for i in range(num_clients):
    sd = sd + math.pow(times[i] - mean, 2)
sd = math.sqrt(sd / (num_clients))

#output test logs
mean_str = "Povprecen cas cakanja klientov preko vseh zahtevanih datotek: " + str(mean)
num_clients_str = "Stevilo odjemalcev: " + str(num_clients)
input_size_str = "Stevilo podatkov v datoteki: " + str(input_size)
num_files_str = "Stevilo razlicnih datotek: " + str(num_files)
sd_str = "Standardna deviacija preko vseh zahtevanih datotek na klienta: " + str(sd)
error_str = "Prislo do napake: " + str(err)

print(input_size_str)
print(mean_str)
print(num_clients_str)
print(num_files_str)
print(sd_str)
print(error_str)

test_file = open("../testi/Test_" + str(input_size) + "_" + str(num_clients) + "_" + str(num_files) + ".txt", "w+")
test_file.write(input_size_str+'\n')
test_file.write(mean_str+'\n')
test_file.write(num_clients_str+'\n')
test_file.write(num_files_str+'\n')
test_file.write(sd_str+'\n')
test_file.write(error_str+'\n')
