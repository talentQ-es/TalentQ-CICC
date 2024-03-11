#!/bin/bash


jupytext $1 --to myst

md_file=$(echo $1 | awk -F"." '{printf $1".md"}')
#echo $md_file

lines=($(grep -n -- "---" $md_file | head -n 3 | tail -n 2 | cut -d':' -f1))

sed -i ''${lines[0]}','${lines[1]}'d' $md_file

START=$(cat $md_file | grep -n -- "math"  | head -n 1 | cut -d':' -f1)
((START += 1))
END=$(cat $md_file | grep -n -- "---" | head -n 2 | tail -n 1| cut -d':' -f1)
((END -= 1))

#echo $START, $END
math=($(sed -n ''$START','$END'p' $md_file | grep -o "'[^']*'" | awk -F"'" '{print $2}' | sed "s/ /\!/g"))

# Crear un nuevo array combinando dos elementos consecutivos

((END += 2))

for ((i = 0; i < ${#math[@]}; i += 2)); do
    if echo "${math[i+1]}" | grep \# > /dev/null
    then
        #echo ${math[i+1]}
        max_numero=$(echo "${math[i+1]}" | grep -o '[0-9]*' | sort -nr | head -n1)
        #echo $max_numero
        texto_a_insertar=$(echo "\newcommand{"${math[i]}"}["$max_numero"]{"${math[i+1]}"}")
    else
        texto_a_insertar=$(echo "\newcommand{"${math[i]}"}{"${math[i+1]}"}")
    fi

    texto_a_insertar=$(echo $texto_a_insertar | sed "s/\!/ /g" | sed 's/\\/\\\\/g')
    sed -i ''$END'i\'"\$$texto_a_insertar\$" $md_file

done
