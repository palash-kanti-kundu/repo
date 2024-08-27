import os
import time
from time import strftime, localtime
import sys
from collections import deque
import logging
import numpy as np
import math

cache = deque()


words = np.array([
    "business - services - products - software - research - comments - national - internet - shipping - reserved - security - american - computer - download - pictures - personal - location - children - students - shopping - previous - property - customer - december - training - advanced - category - register - november - features - industry - provided - required - articles - feedback - complete - standard - programs - language - password - question - building - february - analysis - possible - problems - interest - learning - delivery - original - includes - messages - provides - specific - director - planning - database - official - district - calendar - resource - document - material - together - function - economic - projects - included - received - archives - magazine - policies - position - listings - wireless - purchase - response - practice - hardware - designed - discount - remember - increase - european - activity - although - contents - regional - supplies - exchange - continue - benefits - anything - mortgage - solution - addition - clothing - military - decision - division - university - management - technology - government - department - categories - conditions - experience - activities - additional - washington - california - discussion - collection - conference - individual - everything - production - commercial - newsletter - registered - protection - employment - commission - electronic - particular - facilities - statistics - investment - industrial - associated - foundation - population - navigation - operations - understand - connection - properties - assessment - especially - considered - enterprise - processing - resolution - components - assistance - disclaimer - membership - background - trademarks - television - interested - throughout - associates"
])

if len(sys.argv) >= 2:
        size_in_mb = int(sys.argv[1])
else:
        size_in_mb = 1

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

logger.info("File Size: " + str(size_in_mb) + " MB")
logger.info("sleepTime: " + str(sleepTime) + " Seconds")
logger.info("capacity: " + str(capacity) + " files")

while True:
    start = time.time()
    formatted_time = strftime("%Y_%m_%d-%H_%M_%S",  localtime())
    
    file_path = "dummy_files/" + formatted_time + ".txt"
    logger.info("Cache size now " + str(len(cache)))	
    if len(cache) >= capacity:
	    removed_item = cache.popleft()
    else:
         removed_item = None
    
    if removed_item is  not None:
      try:
            os.remove(removed_item)
            logger.info("Removed " + removed_item)
      except:
        logger.info("Error deleting file: " + removed_item)

    st = ' - '.join(np.random.choice(words, math.ceil(int(size_in_mb * 1024 * 1024 / 6400))))
    
    with open(file_path, 'w') as file:
       file.write(st)
       cache.append(file_path)

    end = time.time()
    elapsed = end - start
    logger.info("Took " + str(elapsed) + " seconds")
    logger.info("")
    
    if elapsed > sleepTime:
          s = 1
    else:
          s = int(sleepTime - elapsed)

    time.sleep(s)