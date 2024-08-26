import os
import time
from time import strftime, localtime
import sys
from collections import deque
import logging
import subprocess

cache = deque()

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

while True:
    start = time.time()
    formatted_time = strftime("%Y_%m_%d-%H_%M_%S", localtime())
    
    file_path = "./dummy_files/" + formatted_time + ".bin"
	
    if len(cache) >= capacity:
	    removed_item = cache.popleft()
    else:
         removed_item = None
    
    if removed_item is  not None:
      try:
            os.remove(removed_item)
            logger.info("Removed" + removed_item)
      except:
        logger.info("Error deleting file: " + removed_item)

    bash_command = "dd if=/dev/urandom of=" + file_path + " bs=1M count=" + str(size_in_mb) + ";sync"
    process = subprocess.Popen(bash_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Get the output and error (if any)
    stdout, stderr = process.communicate()

    logger.info("Written file at " + formatted_time)

    end = time.time()
    elapsed = end - start
    logger.info("Took " + str(elapsed) + " seconds")
    logger.info("")
    
    if elapsed > sleepTime:
          s = 0
    else:
          s = sleepTime - elapsed

    time.sleep(s)