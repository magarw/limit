#!/bin/bash
for i in {1..50}
do
  echo "Running $i iteration"
  python add_verified.py
done
