Notebook_folder=../Notebooks
Destination_folder=../Book
SKIP=".ipynb_checkpoints|\/No_"



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
    echo "- caption: " `cat $caption_part_txt`
    echo "  chapters:"
    path_chapters=$(find $i -mindepth 1 -maxdepth 1 -not -path '*/.*' | grep /Chapter_  | sort)
    for j in $path_chapters; do
        if [ -d $j ]; then
            echo "    sections:"
            sections=$(find $j -mindepth 1 -maxdepth 1 -not -path '*/.*' | egrep "_myst.ipynb$|_myst.md$" | grep /Section_ | sort | sed 's/..\/Book\///g')
            for k in $sections; do
                echo "    - file: " $k
            done
        else
            if echo $j | egrep "_myst.ipynb|_myst.md" 2>&1 > /dev/null ; then
                echo "  - file: " $j | sed 's/..\/Book\///g'
            fi

        fi
    done

    echo
done >> $Destination_folder/_toc.yml

jb build --all $Destination_folder
