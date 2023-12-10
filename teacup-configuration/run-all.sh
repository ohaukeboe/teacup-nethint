#!/bin/bash

for i in `ls configs/*.py`
do
    echo "Running $i"
    cp $i subconfig.py
    time ./run.sh
    mv exp_* $(basename "$i" .py)
done

echo "Done"
