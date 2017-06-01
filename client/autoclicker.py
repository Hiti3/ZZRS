#INSTALLATION: sudo pip install RequestsThrottler

import requests
import time
from threading import Thread
from requests_throttler import BaseThrottler
import logging
import math
#Frankfurt 512/1
url = "http://139.59.132.145:8080/nalozi"

#San Francisco 512/1
#url = "http://138.197.200.63:8080/nalozi"

#Frankfurt 2gb/2
#url ="http://138.68.77.140:8080/nalozi"

print(url)
data_type = "int"
input_size = [50000]
num_clients = [40,50,60,70,80]
num_files = 5
wait_for_response = True
request_delay = 0.5

#print(file_list)



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
    #print("client: {:3d} file: {:3d} elements: {:6s} time: {:.3f} s".format(client_id, file_id, num_elements, total_time))

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

for iix in input_size:
    file_list = ["inputs/"+data_type+"_"+str(iix)+"/"+data_type+"_"+str(iix)+"_"+str(i)+".txt" for i in range(num_files)]
    for ix in num_clients:
        threads = []
        err = False
        times = [0.0] * ix

        logging.disable(logging.WARNING)
        for i in range(ix):
            threads.append(Thread(target=sort_file_list, args=(url, file_list, wait_for_response, request_delay, i)))
            threads[i].start()

        sum = 0.0;
        for i in range(ix):
            threads[i].join()
            sum = sum + float(times[i])

        sd = 0.0 # std deviation
        mean = (sum/ix) # avg time per 1 user over all his files
        for i in range(ix):
            sd = sd + math.pow(times[i] - mean, 2)
        sd = math.sqrt(sd / (ix))

        #output test logs
        mean_str = "Povprecen cas cakanja klientov preko vseh zahtevanih datotek: " + str(mean)
        num_clients_str = "Stevilo odjemalcev: " + str(ix)
        input_size_str = "Stevilo podatkov v datoteki: " + str(iix)
        num_files_str = "Stevilo razlicnih datotek: " + str(num_files)
        sd_str = "Standardna deviacija preko vseh zahtevanih datotek na klienta: " + str(sd)
        error_str = "Prislo do napake: " + str(err)

        print("---------------------------------------------------------")
        print(input_size_str)
        print(mean_str)
        print(num_clients_str)
        print(num_files_str)
        print(sd_str)
        print(error_str)
        print("-----------------------------------------------------------")

        test_file = open("../testi/Test_" + str(iix) + "_" + str(ix) + "_" + str(num_files) + ".txt", "w+")
        test_file.write(input_size_str+'\n')
        test_file.write(mean_str+'\n')
        test_file.write(num_clients_str+'\n')
        test_file.write(num_files_str+'\n')
        test_file.write(sd_str+'\n')
        test_file.write(error_str+'\n')
