Notebook_folder=../Notebooks       # Path respecto a la carpeta scripts
Notebook_folder_aux=.\\/Notebooks  # Path respecto a la raiz del repositorio
Destination_folder=../Book         # Path respecto a la carpeta scripts
Destination_folder_aux=..\\/Book   # Path respecto a la carpeta scripts
SKIP=".ipynb_checkpoints|\/No_"

README_TOC=README_TOC.md


#files_myst=$(find $Notebook_folder -name "*.ipynb" | egrep -v $SKIP | grep "_myst.ipynb")

#for i in $files_myst; do rsync -R $i $destination_folder | grep -v "skipping directory ."; done



###########

rm -r $Destination_folder/docs_old #2>&1 > /dev/null
mv $Destination_folder/docs $Destination_folder/docs_old #2>&1 > /dev/null

rsync -r $Notebook_folder/* $Destination_folder/docs

files=$(find $Destination_folder/docs -name "*.ipynb" | egrep -v $SKIP | grep -v "_myst.ipynb" )

for i in $files; do
    python Notebook_to_myst.py $i
    error=$?
    if ! [ $error == 0 ] ; then
        exit
    fi
done

part_folders=$(find $Destination_folder/docs -mindepth 1 -maxdepth 1 -type d -not -path '*/.*' | grep /Part_ |  sort)

echo "format: jb-book" > $Destination_folder/_toc.yml
echo "root: docs/index" >> $Destination_folder/_toc.yml
echo "parts:" >> $Destination_folder/_toc.yml


for i in $part_folders; do

    caption_part_txt=$(find $i -mindepth 1 -maxdepth 1 -not -path '*/.*' | grep ".txt")
    if [ -z "$caption_part_txt" ]; then
        echo
        echo $i ":  No exite txt con la caption"
        exit
    fi
    echo "- caption: " `cat $caption_part_txt` >> $Destination_folder/_toc.yml

    echo "  chapters:" >> $Destination_folder/_toc.yml
    path_chapters=$(find $i -mindepth 1 -maxdepth 1 -not -path '*/.*' | grep /Chapter_  | sort)
    for j in $path_chapters; do
        if [ -d $j ]; then
            echo "    sections:" >> $Destination_folder/_toc.yml
            sections=$(find $j -mindepth 1 -maxdepth 1 -not -path '*/.*' | egrep "_myst.ipynb$|_myst.md$" | grep /Section_ | sort )
            for k in $sections; do
                aux=$(echo $k | sed 's/'$Destination_folder_aux'\///g')
                echo "    - file: " $aux >> $Destination_folder/_toc.yml

            done
        else
            if echo $j | egrep "_myst.ipynb|_myst.md" 2>&1 > /dev/null ; then
     	       echo "  - file: " $j | sed 's/'$Destination_folder_aux'\///g' >> $Destination_folder/_toc.yml
            fi
        fi
    done

done 




jb build --all $Destination_folder

./make_README.sh
