#!/usr/bin/python3

'''SOSP23-Paper21: '''
'''Checker2: F_start --> S_G_NULL --> S_D_NULL --> F_end'''

import os
import configparser
import json
from utils import *

g_record_file = 'checker2.log'

def checker2(func_str, apis, file_name, g_logger):
    ast_f = build_ast_from_str(func_str)
    if ast_f=='': return
    
    for api in apis:
        api = api.strip()
        for n in ast_f.node_set.keys():            
            cur_node = ast_f.node_set[n]
            src = cur_node.dot_src
            if src.find(api)!=-1:
                
                if src.find('assignment')!=-1:
                
                    func_name = src.split(',')[1].split('=')[1].split('(')[0].strip()
                    if func_name!=api:
                        #print("Meet SubStr: %s (%d) - %s (%d)"%(func_name, len(func_name), api, len(api)))
                        continue
                    #else:
                    #    print('+'*10+file_name+'+'*10)
                    #    print("Meet NULL-RET API: %s"%(api))
                        #continue
                    return_var = src.split(',')[1].split('=')[0].strip()
                    closest_nb = ''
                    closest_line_delta = 1000
                    for nb in cur_node.parent[0].nb:
                        if nb.line>cur_node.line:                            
                            if nb.dot_src.find('%s-&gt;'%(return_var))!=-1:                                
                                #print(nb.dot_src)                                
                                if (nb.line-cur_node.line) < closest_line_delta:
                                    #print('Meet Close IF: %s'%(nb.dot_src))
                                    closest_nb = nb
                                    closest_line_delta = nb.line-cur_node.line
                    
                    
                    #print('CUR: %s'%(cur_node.dot_src))
                    #print('NB: %s DIS: %d'%(closest_nb.dot_src, ))
                    
                    if closest_nb=='': 
                        continue
                    
                    if closest_nb.line-cur_node.line<=1:
                        print(file_name)
                        g_logger.write(file_name+'\n')                                                                              
                        print('SRC: %s NPD: %s'%(cur_node.dot_src, closest_nb.dot_src))
                        g_logger.write('SRC: %s NPD: %s'%(cur_node.dot_src, closest_nb.dot_src))
                        g_logger.flush()
                    
                    else:
                        has_check = 0
                        for nb in cur_node.parent[0].nb:
                            if nb.line>cur_node.line and nb.line<closest_nb.line:
                                if nb.dot_src.find('if (%s)'%(return_var))!=-1 or nb.dot_src.find('if (!%s)'%(return_var))!=-1:
                                    has_check = 1
                                    break
                                    
                        if has_check==0:
                            print(file_name)
                            g_logger.write(file_name+'\n')                                                                              
                            print('SRC: %s NPD: %s'%(cur_node.dot_src, closest_nb.dot_src))
                            g_logger.write('SRC: %s NPD: %s'%(cur_node.dot_src, closest_nb.dot_src))
                            g_logger.flush()
                                    
                    
                    
                                    
                                    
                        

def run_checker():

    g_logger = open(g_record_file, 'w')

    config = configparser.ConfigParser()
    config.read('checkers.ini', encoding='utf-8')

    #secs = config.sections()
    #print(secs)
    apis = ''
    ast_kernel_functions_file = config.get('global', 'ast_kernel_functions')

    if config.has_section('return_null'):
        #print('yes')
        apis = config.get('return_null', 'apis')[1:-1].split(',')         
    else:
        print('no section *return_null* for checker2')

    i = 0
    
    with open(ast_kernel_functions_file) as f:
        while True:
            l = f.readline()
            if l=='': break
            
            l = l.strip()
            if l=='': continue
            dot_file = l.split(' ')[0].split(':')[1]
            #dot_file = '/data1/linux-ast/4/+data1+struck-linux+drivers+w1+masters+omap_hdq.c+outdir/16-ast.dot'
            #dot_file = '/data1/linux-ast/1/+data1+struck-linux+arch+x86+kernel+cpu+mce+amd.c+outdir/136-ast.dot'
            #dot_file = '/data1/linux-ast/3/+data1+struck-linux+drivers+gpu+drm+amd+amdgpu+amdgpu_xgmi.c+outdir/1228-ast.dot'
            #print('Process --- %s'%dot_file)
            with open(dot_file) as df:
                checker2(df.read(), apis, l, g_logger)
            #break
            i+=1
            if i%10000==0:
                print(i)
            #if i>10:  break

    g_logger.close()
if __name__ == '__main__':

    run_checker()


