import requests
import random
from time import sleep 

while 1:
    n = random.randint(1011,1019)
    m = random.randint(91,99)
    requests.get(f'http://localhost:5000/request_data?co_2={n}&t_voc={m}')
    sleep(3.0)