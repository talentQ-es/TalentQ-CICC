#!/usr/bin/env python3

from subprocess import check_output as bash

import sys
import re
import numpy as np

from finds_and_others import grep_file_index
from finds_and_others import my_replace

from finds_and_others import find_div_boxes
from finds_and_others import find_figures
from finds_and_others import find_cell

from build_functions import build_admonition_box
from build_functions import build_card_box
from build_functions import build_figure
from build_functions import build_tabset
from build_functions import create_mask
from build_functions import number_cells
from build_functions import delete_cell
from build_functions import bluid_references

from build_functions import build_code_block

# Obtenemos el nombre del archivo del primer algumento de la llamada
file_name = sys.argv[1:][0]
print("===========================")
print("Input File  = ", file_name)

# Verificamos que haya tantos <div como </div
command_start_div = 'grep "<div " ' + file_name + " | wc | awk '{print $1}'"
command_end_div = 'grep "</div" ' + file_name + " | wc | awk '{print $1}'"

num_start_div = int(bash(command_start_div, shell=True).decode("utf-8"))
num_end_div = int(bash(command_end_div, shell=True).decode("utf-8"))

if num_start_div != num_end_div:
    print(f"\033[91m======\033[0m")
    print("")
    print(bash('egrep -n "<div |</div" ' + file_name, shell = True).decode("utf-8"))
    print(f"\033[91m{num_start_div} == {num_end_div}. No hay tantos <div como </div.\033[0m")
    print(f"\033[91mArchivo: {file_name}\033[0m")
    print(f"\033[91m======\033[0m")
    assert num_start_div == num_end_div

# Sacamalos el numero de linea del inicio de todos los cuadros con "<div class=.... alert alert-block alert...>"
command_i_start_alert_list   = 'grep -n "<div class=" '+file_name+' | grep "alert alert-block alert" |  cut -d":" -f1'
i_start_alert_list = grep_file_index(command_i_start_alert_list)


# Leemos el archivo linea a linea y modificamos los cuadros
with open(file_name, 'r') as f:
    #f_data = f.read()
    ##print(f_data[20])

    f_data=[]
    for line in f:
        ##print(line)
        f_data.append(line)

############################################################################
# Usando el número de linea donde empiezan los cuadros, sacamos todas las lineas
# importantes de los cuadros
index_list_list, titles_list_list = find_div_boxes(f_data, i_start_alert_list)

############################################################################
# Comenzamos a sustituir los cuadros (empezando por el final)
for i in reversed(range(len(index_list_list[0]))):
    title_lowercase = titles_list_list[2][i]        

    if 'definicion' in title_lowercase or title_lowercase == '':
        build_card_box(i, f_data, index_list_list, titles_list_list)

    elif 'teorema' in title_lowercase:
        build_card_box(i, f_data, index_list_list, titles_list_list)

    elif 'lema' in title_lowercase:
        build_card_box(i, f_data, index_list_list, titles_list_list)
    
    elif 'corolario' in title_lowercase:
        build_card_box(i, f_data, index_list_list, titles_list_list)

    elif 'postulado' in title_lowercase:
        build_card_box(i, f_data, index_list_list, titles_list_list)

    elif 'axioma' in title_lowercase:
        build_card_box(i, f_data, index_list_list, titles_list_list)

    elif 'nota' in title_lowercase:
        build_admonition_box(i, f_data, index_list_list, titles_list_list, Class = "note")

    elif 'ejercicio' in title_lowercase:
        build_admonition_box(i, f_data, index_list_list, titles_list_list, Class = "tip")
    
    elif 'calculo' in title_lowercase:
        build_admonition_box(i, f_data, index_list_list, titles_list_list, Class = "tip")

    elif 'ejemplo' in title_lowercase:
        build_admonition_box(i, f_data, index_list_list, titles_list_list, Class = "tip")
    
    elif 'resumen' in title_lowercase:
        build_admonition_box(i, f_data, index_list_list, titles_list_list, Class = "attention")
    else:
        print(f"\033[91m======\033[0m")
        print(f"\033[91m    ",{f_data[index_list_list[0][i]]},"\033[0m")
        print(f"\033[91m    ",{f_data[index_list_list[0][i]+1]}," \033[0m")
        print(f"\033[91m    ",{f_data[index_list_list[0][i]+2]}," \033[0m")
        print(f"\033[91m    ",{f_data[index_list_list[0][i]+3]}," \033[0m")
        #print(f"\033[91m    tipo de cuadro no reconocido: {title_lowercase}, linea {index_list_list[0][i]}  \033[0m")
        raise TypeError(f"\033[91m    tipo de cuadro no reconocido: {title_lowercase}, linea {index_list_list[0][i]}  \n======\033[0m")
        
################################################################################
## Inicio de todas las celdas

command_i_start_all_cells = 'grep -n "   \\"cell_type\\":" '+ file_name + ' |  cut -d":" -f1 '
i_start_all_cells = grep_file_index(command_i_start_all_cells)

############################################################################
# Sacamalos el numero de linea del inicio de las <figure>
command_i_start_figure_list = 'grep -n "<figure>" ' + file_name + ' |  cut -d":" -f1'
i_start_figure_list = grep_file_index(command_i_start_figure_list)

# Usando el número de linea donde empiezan las figuras, sacamos todas las lineas importantes          
if len(i_start_figure_list) > 0:
    index_fig_list_list, datos_list_list, number_ref_fig = find_figures(f_data, i_start_figure_list)

    ############################################################################
    # Comenzamos a sustituir las figuras (empezando por el final)
    for i in reversed(range(len(index_fig_list_list[0]))):
        build_figure(i, f_data, index_fig_list_list, datos_list_list)



    # Añadimos el tiempo de lectura y la fecha en la primera linea. 
    # Para ello, primero cogemos la fecha del texto, eliminando la línea
    command_i_date = 'grep -n "Notebook_Date" ' + file_name + ' |  cut -d":" -f1 | head -n 1'
    i_date = grep_file_index(command_i_date)

    command_i_first_line = 'grep -n "\\"source\\": \\[" ' + file_name + ' |  cut -d":" -f1 | head -n 1'
    i_first_line = grep_file_index(command_i_first_line)


    from datetime import datetime

    if len(i_date) > 0 :
        i_date = i_date[0]
        try: 
            Notebook_Date = f_data[i_date].split(':')[-1].split('\\n')[0].replace(" ","")
            Date_raw = datetime.strptime(Notebook_Date, "%Y/%m/%d")
            Date_formated = Date_raw.strftime("%b %d, %Y")

            f_data[i_date] = '    "\\n",\n'

            my_replace(f_data, i_first_line[0], 'source": [\n'+
                                            #'    "> {sub-ref}`today` | {sub-ref}`wordcount-words` words | {sub-ref}`wordcount-minutes` min read\\n",\n'
                                            '    "> ' + Date_formated + ' | {sub-ref}`wordcount-minutes` min read\\n",\n'
                                            '    "\\n",\n'    )
        except:

            print(f"\033[91m======\033[0m") 
            print(f"\033[91mFormato erroneo en la fecha. Debe de ser:\033[0m")
            print(f"\033[91m<a id='Notebook_Date'></a> Created: yyyy/mm/dd\033[0m")
            print(f"\033[91m======\033[0m") 
    else:
        my_replace(f_data, i_first_line[0], 'source": [\n'+
                                            #'    "> {sub-ref}`today` | {sub-ref}`wordcount-words` words | {sub-ref}`wordcount-minutes` min read\\n",\n'
                                            '    "> {sub-ref}`today` | {sub-ref}`wordcount-minutes` min read\\n",\n'
                                            '    "\\n",\n'    )

    ################################################################################
    ## Arreglamos las referencias a las figuras
    ##   [...](#fig_...)  --->  {ref}`sec_...` o {numref}`sec_...`

    bluid_references(f_data, 'fig_', file_name, number_ref_fig, i_start_all_cells)



################################################################################
## Buscamos las celdas de código con nuestro patron _code_cell'''
pattern_code = '_code_cell\'\'\''
command_i_pattern_code = 'grep -n "'+pattern_code+'" '+ file_name + ' |  cut -d":" -f1 '
i_pattern_code_list = grep_file_index(command_i_pattern_code)

if len(i_pattern_code_list) > 0: 
    # Vemos a que celdas corresponden 
    num_cells_pattern_code = number_cells(i_pattern_code_list, i_start_all_cells)

    # Sacamos unas mascaras que nos dan las celdas CONSECUTIVAS
    masks_list = create_mask(f_data, num_cells_pattern_code, i_pattern_code_list)




    # Usamos las mascaras y i_pattern_code_list para sacar los datos de las celdas
    for mask in masks_list:
        i_start_cell_list    = []
        i_start_content_list = []
        i_end_content_list   = []
        
        name_code_list  = []
        content_list    = []
        full_cell_list  = []

        k = 0
        for i_pattern_code in np.array(i_pattern_code_list)[mask]:
            i_start_cell, i_start_content, i_end_content, content, full_cell = find_cell(f_data, i_pattern_code)

            name_code = re.search(r'\'\'\'(.*?)\'\'\'', f_data[i_pattern_code]).group(1).split('_')[0]
            
            for i in range(len(content)):
                if content[i] == f_data[i_pattern_code]:
                    content[i] ='    "",\n'

            # La primera celda de cada bloque conserva la salida. Lo que hacemos es esconder la entrada con "remove_input"
            if k == 0:
                f_data[i_start_content-2] = f_data[i_start_content-2] + '   "metadata": {\n    "tags": [\n     "remove_input"\n    ]\n   },\n'
                
                # Si una de las celdas del bloque es la última, hay que quitar una coma
                if np.array(i_pattern_code_list)[mask][-1] > i_start_all_cells[-1]:  
                    f_data[i_end_content+2] = '  }\n'
            
            else:
                delete_cell(f_data, i_start_cell, i_end_content)
                #for i in range(i_start_cell,i_end_content+3):
                #    f_data[i] = ''      


            i_start_cell_list.append(i_start_cell)
            i_start_content_list.append(i_start_content)
            i_end_content_list.append(i_end_content)
            name_code_list.append(name_code)
            content_list.append(content)

            k+=1
        
        build_tabset(f_data, i_start_cell_list[0], name_code_list ,content_list)



################################################################################
## Celdas de código no ejecutables: "skip_execution"

pattern_skip_exe = 'skip_execution'
command_i_pattern_skip_exe = 'grep -n "'+pattern_skip_exe+'" '+ file_name + ' |  cut -d":" -f1 '
i_pattern_skip_exe_list = grep_file_index(command_i_pattern_skip_exe)


if len(i_pattern_skip_exe_list) > 0: 
    
    num_cells_pattern_skip_exe = number_cells(i_pattern_skip_exe_list, i_start_all_cells)


    for k in range(len(i_pattern_skip_exe_list)):
        i_start_cell, i_start_content, i_end_content, content, full_cell = find_cell(f_data, i_pattern_skip_exe_list[k])


        delete_cell(f_data, i_start_cell, i_end_content)

        build_code_block(f_data, i_start_cell, i_start_all_cells, content, "python")




################################################################################
## Arreglamos las referencias bibliograficas
##   [[...]](#bib_...)  --->  {cite}`bib_...` o {numref}`sec_...`

bluid_references(f_data, 'bib_', file_name, '{cite}', i_start_all_cells)

################################################################################
## Arreglamos las referencias a secciones
##    [...](path#sec_...) ---> {ref}`sec_...` o {numref}`sec_...`
    
bluid_references(f_data, 'sec_', file_name, '{ref}', i_start_all_cells)

################################################################################
## Arreglamos las referencias a ecuaciones
##    [...](path#sec_...) ---> {ref}`sec_...` o {numref}`sec_...`
    
bluid_references(f_data, 'ec_', file_name, '{eq}', i_start_all_cells)

################################################################################
## Arreglamos las label de las secciones
##  <d id='sec_...'></a>  ---> (sec_...)=

command_i_pattern_a_sec = 'grep -n "<a id="  '+ file_name + ' | grep "sec_" |  cut -d":" -f1 '
i_pattern_a_sec_list = grep_file_index(command_i_pattern_a_sec)

for i_pattern_a_sec in i_pattern_a_sec_list:
    f_data[i_pattern_a_sec] = '    "('+f_data[i_pattern_a_sec].split('\'')[1]+')= \\n",\n'



################################################################################
## Indice

command_i_ToC_pattern = 'grep -n "## Índice" '+ file_name + ' |  cut -d":" -f1 | head -n 1'
i_ToC_pattern = grep_file_index(command_i_ToC_pattern)

if len(i_ToC_pattern) == 1:
    i_start_ToC_cell, i_ToC_start, i_ToC_end, _, _ = find_cell(f_data, i_ToC_pattern[0])

    my_replace(f_data, i_ToC_start, ':::{contents}\\n",\n'+
                                        '    ":local:\\n",\n'
                                        '    ":depth: 1\\n",\n'
                                        '    ":::\\n",\n')
    for i in range(i_ToC_start+1, i_ToC_end):
        my_replace(f_data, i, '",\n')
    my_replace(f_data, i_ToC_end, '"\n')



################################################################################
## Bibliografia

pattern_ref_bib = '## Bibliograf'
command_i_pattern_ref_bib = 'grep -n "'+pattern_ref_bib+'" '+ file_name + ' |  cut -d":" -f1 '
i_pattern_ref_bib = grep_file_index(command_i_pattern_ref_bib)

if len(i_pattern_ref_bib) > 0:
    i_pattern_ref_bib = i_pattern_ref_bib[0]

    i_start_cell, i_start_content, i_end_content, content, full_cell = find_cell(f_data, i_pattern_ref_bib)

    for i in range(i_start_content, i_end_content):
        f_data[i] ='    "",\n'
    f_data[i_end_content] ='    ""\n'

    f_data[i_start_content] = '    "```{bibliography} \\n",\n' + \
                '    ":style: plain\\n",\n' + \
                '    ":filter: docname in docnames\\n",\n' + \
                '    "```",\n'

################################################################################
###### Guardamos los cambios en un nuevo fichero

out_file = file_name[:-6]+'_myst.ipynb'

with open(out_file, 'w') as f_out:
    for k in range(len(f_data)):
        f_out.write(f_data[k])



################################################################################
###### Eliminamos los </br>

clean_br_command = "sed -i'' -e 's/<br>//g' " + out_file
bash(clean_br_command, shell=True).decode("utf-8")

'''
################################################################################
### Creamos un nuevo fichero {out_file}_clean con las tres celdas de título

number_head = str(int(bash('grep -n "^  }," Firts_cells.ipynb |  cut -d":" -f1 | head -n 3 | tail -n 1' , 
                                shell=True).decode("utf-8")))

bash('head -n ' +number_head+' Firts_cells.ipynb ' +' > ' + out_file + '_clean' , 
     shell=True).decode("utf-8")

################################################################################
### Sacamos la linea de titulo en el archivo {out_file} y sustituimos el título 
### en el archivo {out_file}_clean
### Recordemos que hasta aquí {out_file}_clean solo tiene las tres celdas de título

Title_jupyter = str(bash('grep -n "# " '+ file_name +' |  cut -d":" -f2 | head -n 1 ', 
                     shell=True).decode("utf-8")).split('"')[1]

i_Title_jupyter_new_file = int(bash('grep -n "# " '+ out_file + '_clean' + ' |  cut -d":" -f1 | head -n 1', 
                                shell=True).decode("utf-8"))-1

# Leemos el archivo nuevo
with open(out_file + '_clean', 'r') as f:
    #f_data = f.read()
    ##print(f_data[20])

    f_data=[]
    for line in f:
        ##print(line)
        f_data.append(line)
    
    # Reemplazamos el título
    my_replace(f_data, i_Title_jupyter_new_file , Title_jupyter +'\\n"\n')

# Pisamos el archivo _clean con la nueva versión con el titulo 
with open(out_file + '_clean', 'w') as f_out:
    for k in range(len(f_data)):
        f_out.write(f_data[k])

################################################################################
### Concatenamos al archivo _clean el texto completo con los cuadros nuevos sin 
### las dos primeras celdas primera celda
number = str(int(bash('grep -n "^  }," ' + out_file + ' |  cut -d":" -f1 | head -n 2 | tail -n 1', shell= True).decode("utf-8")) + 1)
bash('tail -n +' + number + ' ' + out_file  +' >> ' + out_file + '_clean', shell=True).decode("utf-8")

### Renombramos para quitar el _clean
bash('mv ' +  out_file + '_clean ' + out_file, shell=True).decode("utf-8")

'''






################################################################################
### Atacamos los <deatail> sueltos (los que no estaban en un cuadro)
# Tenemos que hacerlo despues de haber reemplazado los cuadros, por eso lo 
# hacemos sobre el archivo de salida

command_i_start_details_list = 'grep -n "<details><summary>" '+out_file + ' |  cut -d":" -f1'
command_i_end_details_list   = 'grep -n "</details>" '+ out_file + ' |  cut -d":" -f1'

i_start_details_list = grep_file_index(command_i_start_details_list)
i_end_details_list = grep_file_index(command_i_end_details_list)


################################################################################
# Leemos el archivo linea a linea y modificamos los cuadros
with open(out_file, 'r') as f:
    #f_data = f.read()
    ##print(f_data[20])

    f_data=[]
    for line in f:
        ##print(line)
        f_data.append(line)
    

    for i in i_start_details_list:
        try:
            title_details = re.search(r'<i>(.*?)</i>', f_data[i]).group(1)
            my_replace(f_data, i, '::::::::::{dropdown} '+title_details+'\\n",\n')

        except Exception as error :
            print(f"\033[91m======\033[0m") 
            print(f"\033[91m Error encontrando un details {i}. No tiene título\033[0m")
            print(f"\033[91m    ",{f_data[i]},"\033[0m")
            print(f"\033[91m    ",{f_data[i+1]}," \033[0m")
            print(f"\033[91m    ",{f_data[i+2]}," \033[0m")
            print(f"\033[91m    ",{f_data[i+3]}," \033[0m")
            print("")
            print(f"\033[91m    ",error," \033[0m")
            print(f"\033[91m======\033[0m") 


    
    
    
    for i in i_end_details_list:
        
        if f_data[i+1] == "   ]\n":
            my_replace(f_data, i, '::::::::::'+'\\n"\n')
        else:
            my_replace(f_data, i, '::::::::::'+'\\n",\n')
    

with open(out_file, 'w') as f_out:
    for k in range(len(f_data)):
        f_out.write(f_data[k])

    
print("Output file = ", out_file)
print("===========================")