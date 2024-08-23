import os
import time
from time import strftime, gmtime
import sys
from collections import deque
import logging
import string
import random

cache = deque()

if len(sys.argv) >= 2:
        size_in_mb = int(sys.argv[1])
else:
        size_in_mb = 10

if len(sys.argv) >= 3:
      sleepTime = int(sys.argv[2])
else:
      sleepTime = 60

if len(sys.argv) >= 4:
      capacity = int(sys.argv[3])
else:
      capacity = sys.maxsize

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='file_util.log')
logger = logging.getLogger()

while True:
    start = time.time()
    formatted_time = strftime("%Y_%m_%d_%H__%M__%S", gmtime())
    
    file_path = "./dummy_files/" + formatted_time + ".txt"
	
    if len(cache) >= capacity:
	    removed_item = cache.popleft()
    else:
         removed_item = None
    
    if removed_item is  not None:
        os.remove(removed_item)
        logger.info("Removed" + removed_item)

    with open(file_path, 'w') as file:
        file.write(''.join(random.choices(string.ascii_letters + string.digits, k=size_in_mb * 1024 * 1024)))
        cache.append(file_path)

    logger.info("Written file at " + formatted_time)
    logger.info("")

    end = time.time()

    elapsed = end - start
    
    if elapsed > sleepTime:
          s = 0
    else:
          s = sleepTime - elapsed

    time.sleep(s)