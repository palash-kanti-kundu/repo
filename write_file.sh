#!/bin/bash

# Define the file path
FILE_PATH="./dummy"

# Create a 1GB file
dd if=/dev/zero of=$FILE_PATH bs=1M count=1024

# Delete the old file if it exists
if [ -f "$FILE_PATH.old" ]; then
    rm "$FILE_PATH.old"
fi

# Rename the current file to old
mv $FILE_PATH $FILE_PATH.old
