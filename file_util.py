import os
import time
from time import strftime, localtime
import sys
from collections import deque
import logging
import argparse
import subprocess

cache = deque()


parser = argparse.ArgumentParser(description="Process some command-line arguments.")
    
# Adding arguments
parser.add_argument('-s', default=1024, type=int, help='File Size in MB')
parser.add_argument('-f', default=60, type=int, help='Frequency of the script run')
parser.add_argument('-k', default = 5, type=int, help='How many files to keep')
parser.add_argument('-d', default = "dummy_files/", type=str, help='Directory to keep generated files')

# Parsing arguments
args = parser.parse_args()

size_in_mb = args.s
sleepTime = args.f
capacity = args.k
dirName = args.d

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='file_util.log')
logger = logging.getLogger()

logger.info("File Size: " + str(size_in_mb) + " MB")
logger.info("sleepTime: " + str(sleepTime) + " Seconds")
logger.info("capacity: " + str(capacity) + " files")
logger.info("Directory: " + str(dirName))

while True:
    start = time.time()
    formatted_time = strftime("%Y_%m_%d-%H_%M_%S",  localtime())
    
    file_path = dirName + formatted_time + ".txt"
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

    subprocess.call(["./a.out", file_path])
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