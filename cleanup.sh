#!/bin/bash
# Kamaraj Engine - Nightly Wash (Nohup Version)

# 1. Kill the background Python engine safely
sudo pkill -f "python3 execution_api.py"
sleep 2

# 2. Delete all leftover NsJail temp folders
rm -rf /home/ubuntu/kamaraj-portal1/temp_submissions/*
rm -rf /tmp/*

# 3. Drop Linux System Caches (Frees up RAM)
sync
echo 3 > /proc/sys/vm/drop_caches

# 4. Restart the engine in the background
cd /home/ubuntu/kamaraj-portal1
nohup sudo python3 execution_api.py > engine.log 2>&1 &

echo "System washed at $(date)" >> /home/ubuntu/kamaraj-portal1/wash.logss