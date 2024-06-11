#!/usr/bin/env python3

import numpy as np
import re

from finds_and_others import grep_file_index
from finds_and_others import my_replace


def number_cells(i_pattern_code_list, i_start_all_cells):

    num_cells_pattern_code = []
    num_cell = 0

    for i_pattern_code in i_pattern_code_list:
        found = False
        while not found:
            if i_pattern_code > i_start_all_cells[-1]:
                num_cells_pattern_code.append(len(i_start_all_cells)-1)
                found = True
            elif i_pattern_code < i_start_all_cells[num_cell]:
                num_cells_pattern_code.append(num_cell-1)
                found = True
            num_cell +=1
        num_cell -=1

    return num_cells_pattern_code


def create_mask(f_data, num_cells_pattern, i_pattern_list):

    masks_list = []
    mask = np.zeros([len(num_cells_pattern)], dtype = bool)
    mask[0] = 1
    first_pattern = re.search(r'\'\'\'(.*?)\'\'\'', f_data[i_pattern_list[0]]).group(1)
    for i in range(1,len(num_cells_pattern)):
        pattern = re.search(r'\'\'\'(.*?)\'\'\'', f_data[i_pattern_list[i]]).group(1)
        if num_cells_pattern[i] == num_cells_pattern[i-1]+1 and first_pattern != pattern:
            mask[i] = 1
        else:
            masks_list.append(mask)
            mask = np.zeros([len(num_cells_pattern)], dtype = bool)
            mask[i] = 1
            first_pattern = re.search(r'\'\'\'(.*?)\'\'\'', f_data[i_pattern_list[i]]).group(1)
    masks_list.append(mask)
    return masks_list


def delete_cell(f_data, i_start_cell, i_end_cell):
    for i in range(i_start_cell,i_end_cell+3):
                f_data[i] = ''


def build_admonition_box(i, f_data, index_list_list, titles_list_list, Class):

    i_start         = index_list_list[0][i]  
    i_end           = index_list_list[1][i]  
    i_start_p       = index_list_list[2][i]  
    i_end_p         = index_list_list[3][i]
    i_start_details = index_list_list[4][i]
    i_end_details   = index_list_list[5][i]
    i_title         = index_list_list[6][i]
       
    title_details   = titles_list_list[0][i]
    title           = titles_list_list[1][i]
    #title_lowercase = titles_list_list[2][i]
    subtitle        = titles_list_list[3][i]
    
    #for i in range(i_end-i_start+1):
    #    print({f_data[i_start+i]})
    #print("")

    ############################################################################
    ###### Empezamos a sustituir por el final

    ### </div>    
    if f_data[i_end + 1] == "   ]\n":
        my_replace(f_data, i_end, '::::::'+'\\n"\n' )
    else:
        my_replace(f_data, i_end, '::::::'+'\\n",\n' )

    ### </p>
    if len(i_end_p) > 0:
        for j in range(len(i_end_p)):
            if i_end > i_end_p[j]:
                my_replace(f_data, i_end_p[j], ''+'\\n",\n' )

    ### </details>
    if i_end_details > 0:
        if i_end > i_end_details:
            my_replace(f_data, i_end_details, ':::'+'\\n",\n')

    ### <detail>
    if i_start_details > 0:
        my_replace(f_data, i_start_details, ':::{dropdown} '+ title_details+'\\n",\n')

    #### TITLE 
    my_replace(f_data, i_title,''+'\\n",\n')
    
    ### <p style=...>
    if len(i_start_p) > 0:
        for j in range(len(i_start_p)):
            if i_start < i_start_p[j]:
                my_replace(f_data, i_start_p[j], ''+'\\n",\n')

    #### <div class...> o <div class...><p style...>
    if subtitle == None:
        my_replace(f_data, i_start, '::::::{admonition} '+ title+'\\n",\n' + '    ":class: '+Class+'\\n",\n')
    else:
        my_replace(f_data, i_start, '::::::{admonition} '+ title + ' (' + subtitle + ') '+'\\n",\n' + '    ":class: '+Class+'\\n",\n')

    #print("")
    #for i in range(i_end-i_start+1):
    #    print({f_data[i_start+i]})
    #print("")


def build_card_box(i, f_data, index_list_list, titles_list_list):
    i_start         = index_list_list[0][i]  
    i_end           = index_list_list[1][i]  
    i_start_p       = index_list_list[2][i]  
    i_end_p         = index_list_list[3][i]
    i_start_details = index_list_list[4][i]
    i_end_details   = index_list_list[5][i]
    i_title         = index_list_list[6][i]
       
    title_details   = titles_list_list[0][i]
    title           = titles_list_list[1][i]
    #title_lowercase = titles_list_list[2][i]
    subtitle        = titles_list_list[3][i]
    
    #for i in range(i_end-i_start+1):
    #    print({f_data[i_start+i]})
    #print("")

    ############################################################################
    ###### Empezamos a sustituir por el final

    ##################################
    ######## </div> o </p></div>

    ### </div>    
    if f_data[i_end + 1] == "   ]\n":
        my_replace(f_data, i_end, '::::::'+'\\n"\n' )
    else:
        my_replace(f_data, i_end, '::::::'+'\\n",\n' )


    if len(i_end_p) > 0:
        ##############################
        ######## </p>
        for j in range(len(i_end_p)):
            if i_end > i_end_p[j]: 
                my_replace(f_data, i_end_p[j], ''+'\\n",\n' )


    if i_end_details > 0:
        ##############################
        ######## </details>
        if i_end > i_end_details:
            my_replace(f_data, i_end_details, ':::'+'\\n",\n')

    if i_start_details > 0:
        ##############################
        ######## <detail>
        my_replace(f_data, i_start_details, ':::{dropdown} '+ title_details+'\\n",\n')

    if title != "":
        my_replace(f_data, i_title, '^^^\\n",\n')
    else:
        my_replace(f_data, i_title, '\\n",\n')
    
    if len(i_start_p) > 0:
        ##############################
        ######## <p style=...>
        for j in range(len(i_start_p)):
            if i_start < i_start_p[j]:
                my_replace(f_data, i_start_p[j], ''+'\\n",\n')

    ##############################
    ######## TITLE and <div class...> o <div class...><p style...>
    
    if title != "":
        if subtitle == None:
            my_replace(f_data, i_start, '::::::{card} \\n",\n'+'    "<b>'+title+'</b>: '+' \\n",\n')
        else:
            my_replace(f_data, i_start, '::::::{card} \\n",\n'+'    "<b>'+title+'</b>: </i>'+ subtitle + '</i> '+'\\n",\n')
    else:
        my_replace(f_data, i_start, '::::::{card} \\n",\n')

    #print("")
    #for i in range(i_end-i_start+1):
    #    print({f_data[i_start+i]})
    #print("")

def build_figure(i, f_data, index_fig_list_list, datos_list_list):

    i_start   = index_fig_list_list[0][i]
    i_end     = index_fig_list_list[1][i]
    i_label_a = index_fig_list_list[2][i]
    i_img     = index_fig_list_list[3][i]
    i_caption = index_fig_list_list[4][i]

    path_fig    = datos_list_list[0][i]
    align_fig   = datos_list_list[1][i]
    width_fig   = datos_list_list[2][i]
    caption_fig = datos_list_list[3][i]
    label_fig   = datos_list_list[4][i]
        
    ############################################################################
    ###### Empezamos a sustituir por el final


    if f_data[i_end + 1] == "   ]\n":
        my_replace(f_data, i_end, '::::'+'\\n"\n' )
    else:
        my_replace(f_data, i_end, '::::'+'\\n",\n' )
    

    if i_caption != 0 and caption_fig != None:
        my_replace(f_data, i_caption, caption_fig +'\\n",\n')
    
    my_replace(f_data, i_img, 
               ':width: ' + width_fig + '\\n",\n' + 
               '    ":align: ' + align_fig + '\\n",\n')
        
    if i_label_a != 0 and label_fig != None:
        my_replace(f_data, i_label_a, ':name: ' + label_fig +'\\n",\n')

    my_replace(f_data, i_start, '::::{figure} '+ path_fig +'\\n",\n' )



def build_tabset(f_data, i_start_next_cell, name_code_list ,content_list):

    def build_tab_item(f_data, i_start_next_cell, name_code, content):
        f_data[i_start_next_cell] = \
            '    "```\\n",\n' + \
            '    "::::\\n",\n' + \
            f_data[i_start_next_cell]
        
        for line in reversed(content):
            f_data[i_start_next_cell] = line + f_data[i_start_next_cell]
        
        f_data[i_start_next_cell] = \
            '    "::::{tab-item} '+name_code+'\\n",\n' + \
            '    "```python\\n",\n' + \
            f_data[i_start_next_cell]
    

    f_data[i_start_next_cell] = '    ":::::\\n"\n' + '   ]\n' + '  },\n' + f_data[i_start_next_cell] 

    for i in reversed(range(len(name_code_list))):
        content   = content_list[i]
        name_code = name_code_list[i]
        
        #print({content[-1]}, {content[-1][:-2]+'\\n",\n'})
        content[-1] = content[-1][:-2]+'\\n",\n'

        build_tab_item(f_data, i_start_next_cell, name_code, content)
    
    f_data[i_start_next_cell] = \
        '  {\n' + \
        '   "cell_type": "markdown",\n' + \
        '   "metadata": {},\n' + \
        '   "source": [\n' + \
        '    ":::::{tab-set}\\n",\n' + f_data[i_start_next_cell]
    


def build_code_block(f_data, i_start_cell, i_start_all_cells, content, language):

    f_data[i_start_cell] = \
        '  {\n' + \
        '   "cell_type": "markdown",\n' + \
        '   "metadata": {},\n' + \
        '   "source": [\n' + \
        '    "```{code-block} '+language+'\\n",\n'
    
    content[-1] = content[-1][:-2]+'\\n",\n'

    for line in content:
        f_data[i_start_cell] = f_data[i_start_cell] + line
    
    if i_start_cell >= i_start_all_cells[-1]:
        f_data[i_start_cell] =  f_data[i_start_cell] + '    "```\\n"\n' + '   ]\n' + '  }\n'
    else:
        f_data[i_start_cell] =  f_data[i_start_cell] + '    "```\\n"\n' + '   ]\n' + '  },\n'


def bluid_references(f_data, pattern_ref, file_name, out_ref, i_start_all_cells):
    
    if pattern_ref == 'bib_' :
        pattern_ref_grep = '\](#'+pattern_ref
        command_i_pattern_ref = 'grep -n "'+pattern_ref_grep+'" '+ file_name + ' |  cut -d":" -f1 '
        i_pattern_ref_list = grep_file_index(command_i_pattern_ref)
        
        # Sustituimos las referencias de la forma    [[...]](#bib_...)  por  {cite}`bib_...` o {numref}`sec_...`
        # Tenemos que tener cuidado con el doble [[ ]] y con que lo que aparezca ahi dentro no importa
        for i_pattern_ref in i_pattern_ref_list:
            f_data[i_pattern_ref] = re.sub(r'\[\[(\d+)\]\]\(#'+pattern_ref+r'(\w+)\)', out_ref+r'`'+pattern_ref+r'\2`', f_data[i_pattern_ref])
            #f_data[i_pattern_ref] = re.sub(r'\[(\d+)\]\(#'+pattern_ref+r'(\w+)\)', out_ref+r'`'+pattern_ref+r'\2`', f_data[i_pattern_ref])
            #f_data[i_pattern_ref] = re.sub(r'\[([^\]]+)\]\(#'+pattern_ref+r'(\w+)\)', out_ref+r'`\1 <'+pattern_ref+r'\2>`', f_data[i_pattern_ref])

    elif pattern_ref == 'sec_':
        pattern_ref_grep = '#'+pattern_ref
        command_i_pattern_ref = 'grep -n "'+pattern_ref_grep+'" '+ file_name + ' |  cut -d":" -f1 '
        i_pattern_ref_list = grep_file_index(command_i_pattern_ref)

        for i_pattern_ref in i_pattern_ref_list:
            # Sustituimos las referencias del estilo      [...](path#sec_...) por {ref}`sec_...` o {numref}`sec_...`
            #f_data[i_pattern_ref] = re.sub(r'\[([^\]]+)\]\([^)]*#'+pattern_ref+r'(\w+)\)', out_ref+r'`'+pattern_ref+r'\2`', f_data[i_pattern_ref])
            f_data[i_pattern_ref] = re.sub(r'\[([^\]]+)\]\([^)]*#'+pattern_ref+r'([^\)]+)\)', out_ref+r'`'+pattern_ref+r'\2`', f_data[i_pattern_ref])


    elif pattern_ref == 'ec_':
        # Eliminamos las referencias con <a id='ec_... 
        pattern_a_grep = '<a id=\''+pattern_ref
        command_i_pattern_a = 'grep -n "'+pattern_a_grep+'" '+ file_name + ' |  cut -d":" -f1 '
        i_pattern_a_list = grep_file_index(command_i_pattern_a)
        for i_pattern_a in i_pattern_a_list:
            f_data[i_pattern_a] = re.sub(r'<a id=\'ec_[^>]+></a>', '', f_data[i_pattern_a])

        # Añadimos las ecuaciones con \begin{...} \label{...} e un bloque ```{math}
        
        command_i_begin_label = 'grep -n "begin{" ' + file_name + ' | grep "label{" |  cut -d":" -f1 ' 
        i_begin_label_list = grep_file_index(command_i_begin_label)

        for i_begin_label in i_begin_label_list:
            number_begin = 1
            i_end = i_begin_label + 1 
            while number_begin > 0:
                if "begin{" in f_data[i_end]:
                    number_begin +=1
                    
                if "end{" in f_data[i_end]:
                    number_begin -=1
               
                i_end += 1
            i_end -= 1

            label = f_data[i_begin_label].split('label{')[1].split('}')[0]
        
            f_data[i_begin_label] = '    "```{math}\\n",\n' + \
                                    '    ":label: ' + label +' \\n",\n' + \
                                    f_data[i_begin_label].split('}')[0] + '} \\n",\n'
            

            end = f_data[i_end].split('}')[0] 
            end_part_2 = f_data[i_end].split('}')[1]
            
            f_data[i_end] = end + '} \\n",\n' + \
                            '    "```' + end_part_2

        pattern_ref_grep = '#'+pattern_ref
        command_i_pattern_ref = 'grep -n "'+pattern_ref_grep+'" '+ file_name + ' |  cut -d":" -f1 '
        i_pattern_ref_list = grep_file_index(command_i_pattern_ref)

        for i_pattern_ref in i_pattern_ref_list:

            # Sustituimos las referencias del estilo      [...](#ec_...) por {eq}`Ec. %s <eq_...>` 
            f_data[i_pattern_ref] = re.sub(r'\[([^\]]+)\]\([^)]*#'+pattern_ref+r'([^\)]+)\)', 'Ec. ' + out_ref+r'`'+pattern_ref+r'\2`', f_data[i_pattern_ref])
            #f_data[i_pattern_ref] = re.sub(r'\[([^\]]+)\]\([^)]*#'+pattern_ref+r'([^\)]+)\)', out_ref+r'`'+pattern_ref+r'\2`', f_data[i_pattern_ref])
            #{numref}`sec. %s <sec_Code_Blocks_y_Ecuaciones>`

            #regex_pattern = r'\[([^\]]+)\]\(#' + pattern_ref + r'([^\)]+)\)'

    elif pattern_ref == 'fig_':
        pattern_ref_grep = '\](#'+pattern_ref
        command_i_pattern_ref = 'grep -n "'+pattern_ref_grep+'" '+ file_name + ' |  cut -d":" -f1 '
        i_pattern_ref_list = grep_file_index(command_i_pattern_ref)

        if out_ref == True:
            out_ref = '{numref}'
            for i_pattern_ref in i_pattern_ref_list:
                # Sustituimos las referencias de la forma    [...](#fig_...)  por  {ref}`sec_...` o {numref}`sec_...`
                #f_data[i_pattern_ref] = re.sub(r'\[([^\]]+)\]\(#'+pattern_ref+r'(\w+)\)', out_ref+r'`'+pattern_ref+r'\2`', f_data[i_pattern_ref])
                f_data[i_pattern_ref] = re.sub(r'\[([^\]]+)\]\(#'+pattern_ref+r'([^\)]+)\)', out_ref+r'`'+pattern_ref+r'\2`', f_data[i_pattern_ref])
                
        else:
            out_ref = '{ref}'
            for i_pattern_ref in i_pattern_ref_list:
                # Sustituimos las referencias de la forma    [...](#fig_...)  por  {ref}`sec_...` o {numref}`sec_...`
                #f_data[i_pattern_ref] = re.sub(r'\[([^\]]+)\]\(#'+pattern_ref+r'(\w+)\)', out_ref+r'`\1 <'+pattern_ref+r'\2>`', f_data[i_pattern_ref])
                f_data[i_pattern_ref] = re.sub(r'\[([^\]]+)\]\(#'+pattern_ref+r'([^\)]+)\)', out_ref+r'`\1 <'+pattern_ref+r'\2>`', f_data[i_pattern_ref])

                



