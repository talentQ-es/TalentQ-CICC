Notebook_folder=../Notebooks       # Path respecto a la carpeta scripts
Notebook_folder_aux=.\\/Notebooks  # Path respecto a la raiz del repositorio
Destination_folder=../Book         # Path respecto a la carpeta scripts
Destination_folder_aux=..\\/Book   # Path respecto a la carpeta scripts
SKIP=".ipynb_checkpoints|\/No_"

README_TOC=README_TOC.md


print_in_readme_toc(){
    if echo $1 | grep ".ipynb$" >/dev/null 2>&1 ; then
        aux=$(cat $1 | grep "^    \"# " | head -n 1 | awk -F'\"# ' '{printf $2}' | sed 's/\\n\"//')

        path_to_readme=$(echo $1 | sed 's/'$Destination_folder_aux'\/docs/'$Notebook_folder_aux'/g')
        # Eliminamos la " del final y hacemos echo
        echo "$2["${aux%?}"]("$path_to_readme")**"

    elif echo $1 | grep ".md$" >/dev/null 2>&1 ; then
        aux=$(cat $1 | egrep "^# " | head -n 1 | awk -F"# " '{printf $2}')

        path_to_readme=$(echo $1 | sed 's/'$Destination_folder_aux'\/docs/'$Notebook_folder_aux'/g')
        echo "$2["$aux"]("$path_to_readme")**"

    elif echo $1 | egrep ".txt$" >/dev/null 2>&1; then
        path_to_readme=$(echo $3 | sed 's/'$Destination_folder_aux'\/docs/'$Notebook_folder_aux'/g')
        name=$(cat $1)
        echo "$2["$name"]("$path_to_readme")**"

    fi
}




part_folders_orig=$(find $Notebook_folder -mindepth 1 -maxdepth 1 -type d -not -path '*/.*' | grep /Part_ |  sort)

#cat $Notebook_folder/index.md | egrep "^# " | head -n 1 > $README_TOC
echo "## Índice" > $README_TOC

for i in $part_folders_orig; do
    echo >> $README_TOC

    caption_part_txt=$(find $i -mindepth 1 -maxdepth 1 -not -path '*/.*' | grep ".txt")

    print_in_readme_toc $caption_part_txt "- **" $i >> $README_TOC


    path_chapters=$(find $i -mindepth 1 -maxdepth 1 -not -path '*/.*' | grep /Chapter_  | sort)
    for j in $path_chapters; do
        if [ -d $j ]; then

            sections=$(find $j -mindepth 1 -maxdepth 1 -not -path '*/.*' | egrep ".ipynb$|.md$" | grep /Section_ | sort )
            for k in $sections; do
                aux=$(echo $k | sed 's/'$Destination_folder_aux'\///g')

                print_in_readme_toc $k "        - **" >> $README_TOC
            done
        else
            
            if echo $j | egrep ".ipynb|.md"  2>&1 > /dev/null ; then
     	       echo >> $README_TOC
     	       print_in_readme_toc $j "    - **" >> $README_TOC
            fi
        fi
    done

done


mkdir -p old_READMEs

fecha_actual=$(date +"%d%m%Y-%H:%M:%S")

mv ../README.md ../README_$fecha_actual.md 2>/dev/null
mv ../README_$fecha_actual.md old_READMEs 2>/dev/null

cat README_head.md README_TOC.md README_tail.md > ../README.md 2>/dev/null
