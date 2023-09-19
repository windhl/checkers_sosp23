#!/usr/bin/python3

'''SOSP23-Paper21: '''
'''Checker6: F+_start --> S_G --> F+_end ^ F-_start --> F-_end'''

import os
import configparser
import json
from utils import *

g_record_file = 'checker6.log'

put_apis = {'usb_get_dev':'usb_put_dev',
            'sock_hold':'sock_put',            
            'spi_alloc_master':'spi_master_put'           
            }


def checker6(start_ast, end_ast, get_apis, file_name, g_logger):
    
    for api in get_apis:
        api = api.strip()
        get_lines = []
        for sn in start_ast.node_set.keys():  
            start_cur_node = start_ast.node_set[sn]
            start_src = start_cur_node.dot_src            
            #if cur_node.type==AST_NODE_TYPE_OP_ASSIGN:
            if start_src.find(api)!=-1 and (not (start_cur_node.line in get_lines)):
                #print('Find REMOTE_GET: %s'%(start_src))
                get_lines.append(start_cur_node.line)
                remote_has_put = 0
                for en in end_ast.node_set.keys():
                    end_cur_node = end_ast.node_set[en]
                    end_src = end_cur_node.dot_src
                    if end_src.find(put_apis[api])!=-1:
                        #print('Find REMOTE_PUT: %s'%(end_src))
                        remote_has_put = 1
                        break
                    
                if remote_has_put == 0:
                    print('%s %s %s'%('+'*10, file_name, '+'*10))
                    g_logger.write(file_name+'\n')
                    print('\tMeet Remote-Unpaired API: (%s:%s)%s - %s'%(start_ast.get_name(), end_ast.get_name(), api, start_src))
                    g_logger.write('\tMeet Remote-Unpaired API: (%s:%s)%s - %s\n'%(start_ast.get_name(), end_ast.get_name(), api, start_src))
                    g_logger.flush()
                
                break


def get_start_end_name(func_str, pairs, file_name, g_logger, start_or_end):

    #print('SE: %d'%(start_or_end))
    ast_f = build_ast_from_str(func_str)
    
    if ast_f=='':         
        return ('', -1, '', '', '', '') 

    name = ast_f.get_name()
    start_name = ''
    end_name   = ''
    start_word = ''
    end_word   = ''    
    if start_or_end==0:
        #print("START.....")
        start_name = ''
        start_word = ''
        for k in pairs.keys():
            if name.find(k)!=-1:
                #print('START: %s'%(name))
                start_name = name
                start_word = k
                end_word   = pairs[k]
                break
                
        if start_name!='':
            general_name = start_name.replace(start_word, '')
            
            index = 0
            
            for k in start_name.split('_'):
                if k==start_word:
                    #print(index)
                    break
                index+=1
            #print(general_name)
            
            return (general_name, index, start_word, end_word, ast_f, name)
        else:
            return ('', -1, '', '', '', '')

    if start_or_end==1:
        #print("END.....")
        for k in pairs.keys():
            #print('Find End: %s'%(pairs[k]))
            if name.find(pairs[k])!=-1:
                #print('END: %s'%(name))
                end_name   = name
                start_word = k
                end_word   = pairs[k]
                break
                
        if end_name!='':
            general_name = end_name.replace(end_word, '')
            
            index = 0
            
            for k in end_name.split('_'):
                if k==end_word:
                    #print(index)
                    break
                index+=1
            #print(general_name)
            
            return (general_name, index, start_word, end_word, ast_f, name) 
        else:   
            return ('', -1, '', '', '', '')            
    
    return ('', -1, '', '', '', '')

    
def run_checker():

    g_logger = open(g_record_file, 'w')

    config = configparser.ConfigParser()
    config.read('checkers.ini', encoding='utf-8')

    #secs = config.sections()
    #print(secs)
    name_pairs = ''
    get_apis   = ''
    ast_kernel_functions_file = config.get('global', 'ast_kernel_functions')

    if config.has_section('indirect_api'):
        #print('yes') 
        name_pairs = config.get('indirect_api', 'name_pairs')[1:-1].split(',')
        get_apis   = config.get('indirect_api', 'apis')[1:-1].split(',')        
    else:
        print('no section *indirect_api* for checker6')
        return -1

    pairs = {}
    for np in name_pairs:        
        pairs[np.split(':')[0].strip()]=np.split(':')[1].strip()
        
    
    
    
    i = 0    
    
    g_maps = {}
    g_file = ''
    with open(ast_kernel_functions_file) as f:
        while True:
            l = f.readline()
            if l=='': break
            
            l = l.strip()
            if l=='': continue
            dot_file = l.split(' ')[0].split(':')[1]  
            #dot_file = '/data1/linux-ast/0/+data1+struck-linux+arch+powerpc+platforms+powermac+pfunc_core.c+outdir/54-ast.dot'
            #print('Process --- %s'%dot_file)
            
            with open(dot_file) as df:                
                file_str = df.read()
                #checker5(df.read(), apis, l, g_logger)
                (start_g_name, start_index, start_start_name, start_end_name, start_ast_f, start_api_name) = get_start_end_name(file_str, pairs, l, g_logger, 0)
                (end_g_name, end_index, end_start_name, end_end_name, end_ast_f, end_api_name) = get_start_end_name(file_str, pairs, l, g_logger, 1)
                
                if start_g_name!='':
                    #print('Start: %s'%(start_g_name))
                    if start_g_name in g_maps.keys():
                        g_maps[start_g_name][0] = (start_g_name, start_index, start_start_name, start_end_name, start_ast_f, start_api_name, dot_file)
                    else:
                        g_maps[start_g_name] =[(start_g_name, start_index, start_start_name, start_end_name, start_ast_f, start_api_name,dot_file), \
                                                ('', -1, '', '', '', '', '')]
                                               
                if end_g_name!='':
                    #print('End: %s'%(end_g_name))
                    if end_g_name in g_maps.keys():
                        g_maps[end_g_name][1] = (end_g_name, end_index, end_start_name, end_end_name, end_ast_f, end_api_name,dot_file)
                    else:
                        g_maps[end_g_name] = [('', -1, '', '', '', '', ''), (end_g_name, end_index, end_start_name, end_end_name, end_ast_f, end_api_name, dot_file)]
            #break
            i+=1
            if i%10000==0:
                print(i)
            
            #if i>50000: break

    for k in g_maps.keys():
        #print(k)
        if g_maps[k][0][0]!='' and g_maps[k][1][0]!='':
            #print('%s - %s'%(g_maps[k][0][5], g_maps[k][1][5]))
            g_logger.write('%s - %s\n'%(g_maps[k][0][5], g_maps[k][1][5]))
            
            checker6(g_maps[k][0][4], g_maps[k][1][4], get_apis, g_maps[k][0][6], g_logger)
            

    g_logger.close()
if __name__ == '__main__':

    run_checker()


