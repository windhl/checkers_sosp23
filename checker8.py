#!/usr/bin/python3

'''SOSP23-Paper21: '''
'''Checker8: F_start --> S_P(p0) --> S_D(p0) --> F_end'''

import os
import configparser
import json
from utils import *

g_record_file = 'checker8.log'




def checker8(func_str, apis, file_name, g_logger):
    
    ast_f = build_ast_from_str(func_str)
    if ast_f=='': return

    bug_lines = []
    for api in apis:
        api = api.strip()
        
        for n in ast_f.node_set.keys():            
            cur_node = ast_f.node_set[n]
            src = cur_node.dot_src
            
            if cur_node.type == AST_NODE_TYPE_REAL_METHOD:
            
                if src.find(api)!=-1:                    
                    pointer = src.split(',')[1].split(')')[0].split('(')[1]                    
                    if pointer.find('-&gt')!=-1:
                        continue
                    
                    has_return = 0
                    for nb in cur_node.parent[0].nb:
                        #print(nb.dot_src)
                        if nb.line>cur_node.line:
                            if nb.dot_src.find('return')!=-1:
                                #print('Find Return!!!!')
                                has_return = 1
                                break
                    if has_return == 1:
                        continue
                    
                    #print(file_name)
                    #print('Find: %s'%(src))
                    #print('Pointer: %s'%(pointer))
                    
                    root_node = cur_node
                    while root_node.type!=AST_NODE_TYPE_METHOD:
                        root_node = root_node.parent[0]
                    
                    node_set = [root_node]                        
                    
                    goto_nodes = []
                    while len(node_set)!=0:
                        t = node_set.pop()
                        
                        for nb in t.nb:
                            node_set.append(nb)
                            
                        if t.line>cur_node.line and (not (t.line in bug_lines)):
                        
                            if t.dot_src.find('%s-&gt'%(pointer))!=-1:
                                print('%s %s %s'%('+'*10, file_name, '+'*10))
                                g_logger.write('%s %s %s\n'%('+'*10, file_name, '+'*10))
                                print('Find Bug: %s'%(t.dot_src))
                                g_logger.write('Find Bug: %s\n'%(t.dot_src))
                                g_logger.flush()
                                bug_lines.append(t.line)
                                
    
def run_checker():

    g_logger = open(g_record_file, 'w')

    config = configparser.ConfigParser()
    config.read('checkers.ini', encoding='utf-8')

    #secs = config.sections()
    #print(secs)
    
    apis   = ''
    ast_kernel_functions_file = config.get('global', 'ast_kernel_functions')

    if config.has_section('future_put'):
        #print('yes') 
        apis   = config.get('future_put', 'apis')[1:-1].split(',')        
    else:
        print('no section *future_put* for checker8')
        return -1

   
    i = 0    
    

    with open(ast_kernel_functions_file) as f:
        while True:
            l = f.readline()
            if l=='': break
            
            l = l.strip()
            if l=='': continue
            dot_file = l.split(' ')[0].split(':')[1]  
            #dot_file = '/data1/linux-ast/0/+data1+struck-linux+arch+powerpc+platforms+powernv+opal.c+outdir/45-ast.dot'
            #print('Process --- %s'%dot_file)
            
            with open(dot_file) as df:                
                file_str = df.read()
                checker8(file_str, apis, l, g_logger)
                
            #break
            i+=1
            if i%10000==0:
                print(i)
            
            #if i>50000: break


            

    g_logger.close()
if __name__ == '__main__':

    run_checker()


