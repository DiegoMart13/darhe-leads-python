#!/bin/bash

contador=1

for argumento in "$@"
do
    echo "argumento $contador => $argumento"
    ((contador++))
done