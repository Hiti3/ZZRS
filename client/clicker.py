import requests
from threading import Thread
from requests_throttler import BaseThrottler
import logging

def _print(response, client_id, file_id, print_data):
    num_elements = response.text.split('\n')[0]
    total_time = response.elapsed.total_seconds()
    print("client: {:d} file: {:d} elements: {:s} time: {:.3f} s".format(client_id, file_id, num_elements, total_time))
    if(print_data != 0):
        print(response.text)
    return

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

c9_username = ""
c9_workspace_name = ""
url = "https://" + c9_workspace_name + "-" + c9_username + ".c9users.io/nalozi"
data_type = "int"
input_size = 10000
num_files = 10
file_list = ["inputs/{:s}_{:d}_{:d}.txt".format(data_type, input_size, i) for i in range(num_files)]
num_clients = 10
wait_for_response = False
request_delay = 5.0

logging.disable(logging.WARNING)
for i in range(num_clients):
    t = Thread(target=sort_file_list, args=(url, file_list, wait_for_response, request_delay, i))
    t.start()
