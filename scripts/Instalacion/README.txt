Aquí se describe como crear un environment de conda con todos los paquetes necesarios para compilar una web a partir de Notebooks (que usen Qiskit, Qibo y Pennylane), usando el script `Notebooks_to_myst.sh` de este repositorio (este usa de fondo, entre otras cosas, JupyterBook).

Lo pasos serían los siguientes:

Primero creamos el environment y accedemos a el:

    conda create -n qiskit_qibo_pennylane
    conda activate qiskit_qibo_pennylane

Ahora instalamos la versión 3.11.7 de python. De esta forma, instalamos tambien el pip en el environment

    conda install python==3.11.7

Ahora instalamos todos los paquetes necesarios usando el archivo `requirements_qqp.txt`.

    pip install -r requirements_qqp.txt

Para que este comando funcione tal y como está escrito, el terminal debe de estar abierto en la carpeta que contenga el archivo `requirements_qqp.txt`. Sino, habría que poner o la ruta completa al archivo o la relativa desde la carpeta donde esté abrierto el terminal.

En este environment se instala Jupyter Notebook 7. Este entorno es más moderno y cambian bastantes cosas respecto al Jupyter Notebook clásico. Sin embargo, el Nobetbook clásico también se instala. Para ejecutarlo solo hace falta correr

    jupyter nbclassic

Si se quiere usar el famoso paquete nbextensions (con cosas como el slideshow, el spellcheck,...) en nbClassic, hay que ejecutar los siguientes comandos:

    ## Activamos las extensiones del nbclassic

    jupyter nbclassic-serverextension enable --py jupyter_contrib_nbextensions --sys-prefix
    jupyter nbclassic-extension install --py jupyter_contrib_nbextensions --sys-prefix

    jupyter nbclassic-serverextension enable --py jupyter_nbextensions_configurator --sys-prefix
    jupyter nbclassic-extension install --py jupyter_nbextensions_configurator --sys-prefix
    jupyter nbclassic-extension enable jupyter_nbextensions_configurator --py --sys-prefix


También se instala la extension `jupyterlab_myst` en Jupyter Notebook 7 y Jupyter Lab. Esta extensión genera problemas con algunas cosas en los Notebooks. Si no se va usar el lenguaje MyST, se recomiendo desactivarla en el gestor de extensiones de Jupyter Notebook 7 y Jupyter Lab.


