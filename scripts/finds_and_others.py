#!/usr/bin/env python3

from subprocess import check_output as bash
import unicodedata

import sys
import re


class TextoEnLineaTitulo(Exception):

    def __init__(self, message="Hay texto en la línea de título"):
        self.message = message

        super().__init__(self.message)

class ErrorParametrosFig(Exception):

    def __init__(self, message="Faltan parámetros en la figura"):
        self.message = message

        super().__init__(self.message)

def my_replace(f_data, i_line, new_text):

    #print("------> ", new_text)

    # Encontrar la posición de la primera comilla doble
    index_firts_quote = f_data[i_line].find('"')

    # Realizar la sustitución
    f_data[i_line]= f_data[i_line][:index_firts_quote + 1] +new_text 
        #f_data[i_start_p][f_data[i_start_p].find('\n', indice_primera_comilla + 1):] 
    

def remove_capital_accents(string):
    # Normalizar y eliminar acentos
    normalized_string = ''.join((c for c in unicodedata.normalize('NFD', string) if unicodedata.category(c) != 'Mn'))

    # Convertir a minúsculas
    final_string = normalized_string.lower()

    return final_string


def grep_file_index(grep_command):
    
    out_grep_command = bash(grep_command, shell=True).decode("utf-8")

    index_list = []
    for line in out_grep_command.splitlines():
        index_list.append(int(line)-1)
    
    return index_list


def find_div_boxes(f_data, i_start_list):
    i_end_list           = [] 
    #i_start_list         = []
    i_start_p_list       = []
    i_end_p_list         = []
    i_start_details_list = []
    i_end_details_list   = []
    i_title_list         = []
    title_details_list        = []
    title_list                = []
    title_lowercase_list      = []
    subtitle_list             = []


    i_end_last_iteration = 0
    for i_start in i_start_list:
        try: 
            assert i_end_last_iteration < i_start, f"{i_end_last_iteration} < {i_start} The previous box ends after the begining of the next one"

            i_end           = i_start 
            i_start_p       = []
            i_end_p         = []
            i_start_details = 0
            i_end_details   = 0
            i_title         = 0
            
            title_details   = None
            subtitle        = None
            title           = None
            title_lowercase = None
            subtitle        = None
                    
            found = False
            while not found:

                if "<details><summary>" in f_data[i_end]:
                    i_start_details = i_end
                elif "</details>"       in f_data[i_end]:
                    i_end_details   = i_end
                elif "<p"               in f_data[i_end]:
                    i_start_p.append(i_end)
                elif "</p></div>"       in f_data[i_end]:
                    i_end_p.append(i_end)
                    found = True
                elif "</p>"             in f_data[i_end]:
                    i_end_p.append(i_end)
                elif "<b>"              in f_data[i_end] and i_title == 0:
                    i_title         = i_end
                elif "</div>"           in f_data[i_end]:
                    found = True
                
                i_end += 1
            i_end -= 1       

            i_end_last_iteration = i_end
            ########################
            ######## TITLE 

            #line_title   = f_data[i_title]
            
            # Esta expresión es para borrar los espacios       
            # title_no_clean_aux = e.sub(r'"(.*?)"', 
            #                     lambda x: x.group(0).replace(' ', ''), line_title)
            

            #title_no_clean = re.search(r'"([^"]*)"', line_title).group(1)
            #title = re.sub(r'<.*?>', '', title_no_clean.split(':')[0]).strip()   #  +'\\n",\n'

            #print(f_data[i_title])
            #print(i_title)
            title = re.search(r'<b>(.*?)</b>', f_data[i_title]).group(1).replace(":","").rstrip().lstrip()
            # .rstrip() elimina los espacios al final
            # .lstrip() elimina los espacios al principio
            title_lowercase = remove_capital_accents(title).strip()
            
            ########################
            ######## SUB-TITLE 

            if "<i>" in f_data[i_title]:
                #subtitle = re.search(r'<i>(.*?)</i>', f_data[i_title]).group(1).replace("(","").replace(")","").rstrip().lstrip()
                subtitle = re.search(r'<i>(.*?)</i>', f_data[i_title]).group(1).rstrip().lstrip().rstrip(")").lstrip("(")
                if f_data[i_title].split('</i>')[1].replace(" ","") != '\\n",\n':
                    raise TextoEnLineaTitulo()
            else:
                if f_data[i_title].split('</b>')[1].replace(" ","").replace(":","") != '\\n",\n':
                    raise TextoEnLineaTitulo()
            

            
            ########################
            ######## #prints y asserts

            #assert i_start_p       <= i_end_p, f"Problems findins <p>, {i_start_p} and </p> {i_end_p}"
            #assert i_start_details <= i_end_details, f"Problems findins <details>, {i_start_p} and </details> {i_end_p}"
            
            #print(i_start,             {f_data[i_start]})
            
            if len(i_start_p)> 0:
                for k in range(len(i_start_p)):
                    assert i_start <= i_start_p[k] < i_end, f"{i_start} <= {i_start_p[k]} < {i_end}:  i_start <= i_start_p < i_end"
                    #if i_start < i_start_p:
                        #print(i_start_p,   {f_data[i_start_p]})
            
            #print(i_title,  title, title_lowercase, subtitle)
            
            if i_start_details > 0:
                assert i_start < i_start_details <= i_end, f"{i_start} < {i_start_details} <= {i_end}: i_start < i_start_details <= i_end"

                ###### Title details:
                try:
                    title_details = re.search(r'<i>(.*?)</i>', f_data[i_start_details]).group(1)

                except Exception as error :
                    print(f"\033[91m======\033[0m") 
                    print(f"\033[91m    ",{f_data[i_start]},"\033[0m")
                    print(f"\033[91m    ",{f_data[i_start+1]}," \033[0m")
                    print(f"\033[91m    ",{f_data[i_start+2]}," \033[0m")
                    print(f"\033[91m    ",{f_data[i_start+3]}," \033[0m")
                    print("")
                    print(f"\033[91m Error encontrando un details {i_start_details}. No tiene título\033[0m")
                    print(f"\033[91m    ",error," \033[0m")
                    print(f"\033[91m======\033[0m") 
                    raise

                #print(i_start_details, {f_data[i_start_details]})
                #print("")
                #print(i_start_details, {f_data[i_start_details]} , title_details)

            if i_end_details > 0:
                
                assert i_start < i_start_details < i_end_details <= i_end, f"{i_start} < {i_start_details} < {i_end_details} <= {i_end}:  i_start < i_start_details < i_end_details <= i_end"
                
                #print(i_end_details,   {f_data[i_end_details]})
            
            if len(i_end_p)> 0:
                for k in range(len(i_end_p)):
                    assert i_start <= i_start_p[k] < i_end_p[k] <= i_end, f"{i_start} <= {i_start_p[k]} < {i_end_p} <= {i_end}:  i_start <= i_start_p < i_end_p <= i_end"
                
                #if i_end > i_end_p:
                    #print(i_end_p,   {f_data[i_end_p]})

            #print("")
            #print(i_end,               {f_data[i_end]})
            #print("===============================================================")
            
            if not title == None:

                i_end_list.append(i_end) 
                #i_start_list.append(i_start) 
                i_start_p_list.append(i_start_p) 
                i_end_p_list.append(i_end_p) 
                i_start_details_list.append(i_start_details) 
                i_end_details_list.append(i_end_details) 
                i_title_list.append(i_title) 
                title_details_list.append(title_details) 
                title_list.append(title) 
                title_lowercase_list.append(title_lowercase) 
                subtitle_list.append(subtitle)
        

        except Exception as error :
            print(f"\033[91m======\033[0m") 
            print(f"\033[91m Error encontrando un cuadro: linea {i_start}\033[0m")
            print(f"\033[91m    ",{f_data[i_start]},"\033[0m")
            print(f"\033[91m    ",{f_data[i_start+1]}," \033[0m")
            print(f"\033[91m    ",{f_data[i_start+2]}," \033[0m")
            print(f"\033[91m    ",{f_data[i_start+3]}," \033[0m")
            print("")
            print(f"\033[91m    ",error," \033[0m")
            print(f"\033[91m======\033[0m") 
            raise
 

    
    index_list_list = [i_start_list, 
                       i_end_list,
                       i_start_p_list, 
                       i_end_p_list, 
                       i_start_details_list, 
                       i_end_details_list, 
                       i_title_list]

    titles_list_list = [title_details_list, title_list, title_lowercase_list, subtitle_list]
        
    return index_list_list, titles_list_list










def find_figures(f_data, i_start_list):
    i_end_list      = [] 
    i_start_list_clean    = []
    i_label_a_list  = []
    i_img_list      = []
    i_caption_list  = []

    path_fig_list    = []
    align_fig_list   = []
    width_fig_list   = []
    caption_fig_list = []
    label_fig_list   = []
    number_ref  = False


    i_end_last_iteration = 0
    for i_start in i_start_list:

        try:
            assert i_end_last_iteration < i_start, f"{i_end_last_iteration} < {i_start} The previous figure ends after the begining of the next one"

            i_end     = i_start 
            i_label_a = 0
            i_img     = 0
            i_caption = 0
            
            path_fig    = None
            align_fig   = None
            width_fig   = None
            caption_fig = None
            label_fig   = None
            
                    
            found = False
            while not found:

                if "<a id"           in f_data[i_end]:
                    i_label_a   = i_end
                    label_fig = f_data[i_label_a].split('>')[0].split('=')[1].replace("\'",'')

                elif "<img"        in f_data[i_end]:
                    i_img     = i_end
                
                elif "<center>"    in f_data[i_end] and  "</center>"    in f_data[i_end]:
                    i_caption = i_end
                    caption_fig = re.search(r'<center>(.*?)</center>', f_data[i_caption]).group(1)
                
                elif "</figure>"   in f_data[i_end]:
                    found = True
                
                i_end += 1
            i_end -= 1       

            i_end_last_iteration = i_end

            ########################
            ######## Path, align, scale

            line_img   = f_data[i_img]
            
            line_img_split = line_img.split(' ')

            for i in range(len(line_img_split)):
                if 'src='      in line_img_split[i]:
                    path_fig   = line_img_split[i].split('=')[1].replace('\\"','').replace("\\'",'').replace('/>','').replace('\\n",\n','').replace(',\n','')
                elif 'align='  in line_img_split[i]:
                    align_fig  = line_img_split[i].split('=')[1].replace('\\"','').replace("\\'",'').replace('/>','').replace('\\n",\n','').replace(',\n','')
                elif 'width='  in line_img_split[i]:
                    width_fig  = line_img_split[i].split('=')[1].replace('\\"','').replace("\'",'').replace('/>','').replace('\\n",\n','').replace(',\n','')
                elif 'alt=' in line_img_split[i] and i_caption > 0:
                    number_ref = True
                    caption_fig = line_img_split[i].split('=')[1].replace('\\"','').replace("\'",'').replace('/>','').replace('\\n",\n','').replace(',\n','').replace("--"," ")
                    if caption_fig == "":
                        caption_fig = re.search(r'<center>(.*?)</center>', f_data[i_caption]).group(1)


            if i_caption > 0 and not 'alt=' in line_img:
                caption_fig = re.search(r'<center>(.*?)</center>', f_data[i_caption]).group(1)

            ########################
            ######## #prints y asserts
        
            if i_label_a > 0:
                assert i_start <= i_label_a < i_end, f"{i_start} <= {i_label_a} < {i_end}"

            if i_caption > 0:
                assert i_start < i_caption <= i_end, f"{i_start} < {i_caption} <= {i_end}"

            if path_fig == None or align_fig == None or width_fig == None:
                raise ErrorParametrosFig()
            else:
                i_end_list.append(i_end) 
                i_start_list_clean.append(i_start) 
                i_label_a_list.append(i_label_a)
                i_img_list.append(i_img)
                i_caption_list.append(i_caption)

                path_fig_list.append(path_fig)
                align_fig_list.append(align_fig)
                width_fig_list.append(width_fig)
                caption_fig_list.append(caption_fig)
                label_fig_list.append(label_fig)
    
        except Exception as error:
            print(f"\033[91m======\033[0m") 
            print(f"\033[91m Error encontrando un cuadro: linea {i_start}\033[0m")
            print(f"\033[91m    ",{f_data[i_start]},"\033[0m")
            print(f"\033[91m    ",{f_data[i_start+1]}," \033[0m")
            print(f"\033[91m    ",{f_data[i_start+2]}," \033[0m")
            print(f"\033[91m    ",{f_data[i_start+3]}," \033[0m")
            print(f"\033[91m    ",{f_data[i_start+4]}," \033[0m")
            print("")
            print(f"\033[91m    ",error," \033[0m")
            print(f"\033[91m======\033[0m") 
            raise


    index_list_list = [i_start_list_clean, 
                       i_end_list,
                       i_label_a_list, 
                       i_img_list, 
                       i_caption_list]

    datos_list_list = [path_fig_list, align_fig_list, width_fig_list, caption_fig_list, label_fig_list]
        
    return index_list_list, datos_list_list, number_ref


def find_cell(f_data, i_pattern):

    i_start_cell    = i_pattern
    i_end_content      = i_pattern
    i_start_content = 0

    found = False
    while not found:         
                    
        if f_data[i_start_cell] == '   "source": [\n' and i_start_content == 0:
            i_start_content = i_start_cell + 1
        elif '   "cell_type":' in f_data[i_start_cell]:
            found = True

        i_start_cell -= 1
    i_pattern += 1

    

    found = False
    while not found:
        if f_data[i_end_content] == '   "source": [\n' and i_start_content == 0:
            i_start_content = i_end_content + 1
        
        elif f_data[i_end_content] == '   ]\n':
            found = True
        
        i_end_content += 1
    i_end_content -= 2

    content = []
    for i in range(i_start_content, i_end_content+1):
        content.append(f_data[i])

    full_cell = []
    for i in range(i_start_cell,i_end_content+3):
        full_cell.append(f_data[i])

    return i_start_cell, i_start_content, i_end_content, content, full_cell