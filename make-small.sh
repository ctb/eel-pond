#! /bin/bash

if [ -d orig ]; then
    echo 'orig already exists; exiting'
    exit -1
fi

mkdir orig

mv petMar_lamp3.fasta orig
head -20000 orig/petMar_lamp3.fasta > petMar_lamp3.fasta

