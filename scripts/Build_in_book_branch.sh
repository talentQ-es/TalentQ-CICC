rama_origen=$(git rev-parse --abbrev-ref HEAD)
git book_branch respaldo_rama_$rama_origen

git diff --quiet
error=$?
if ! [ $error == 0 ] ; then echo "ERROR. Ejecución abortada. Estás en la rama: " `git rev-parse --abbrev-ref HEAD`;  exit; fi


git checkout book_branch
error=$?
if ! [ $error == 0 ] ; then echo "ERROR: falta hacer un commit. Ejecución abortada. Estás en la rama: " `git rev-parse --abbrev-ref HEAD`; exit
fi

git checkout -B tmp_book_branch book_branch
error=$?
if ! [ $error == 0 ] ; then echo "ERROR: falta hacer un commit. Ejecución abortada. Estás en la rama: " `git rev-parse --abbrev-ref HEAD`; exit
fi

git checkout book_branch
error=$?
if ! [ $error == 0 ] ; then echo "ERROR: falta hacer un commit. Ejecución abortada. Estás en la rama: " `git rev-parse --abbrev-ref HEAD`; exit
fi

git reset --hard $rama_origen
error=$?
if ! [ $error == 0 ] ; then echo "ERROR: falta hacer un commit. Ejecución abortada. Estás en la rama: " `git rev-parse --abbrev-ref HEAD`; exit
fi

git checkout tmp_book_branch -- ../Book/_build

./Notebook_to_myst.sh
error=$?
if ! [ $error == 0 ] ; then echo "ERROR: falta hacer un commit. Ejecución abortada. Estás en la rama: " `git rev-parse --abbrev-ref HEAD`; exit
fi

git add ../

git commit -m "Compilamos book"

#git pull -s recursive -X ours origin book_branch --no-edit
#error=$?
#if ! [ $error == 0 ] ; then echo "ERROR: falta hacer un commit. Ejecución abortada. Estás en la rama: " `git rev-parse --abbrev-ref HEAD`; exit
#fi


#git push origin book_branch
#error=$?
#if ! [ $error == 0 ] ; then echo "ERROR: falta hacer un commit. Ejecución abortada. Estás en la rama: " `git rev-parse --abbrev-ref HEAD`; exit
#fi

git checkout $rama_origen
error=$?
if ! [ $error == 0 ] ; then echo "ERROR: falta hacer un commit. Ejecución abortada. Estás en la rama: " `git rev-parse --abbrev-ref HEAD`; exit
fi
