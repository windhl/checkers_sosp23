#!/usr/bin/python3

'''SOSP23-Paper21: '''
'''Checker9: F_start --> S_G|O --> F_end'''

import os
import configparser
import json
from utils import *

g_record_file = 'checker9.log'




def checker9(func_str, args_apis, global_apis, file_name, g_logger):
    
    ast_f = build_ast_from_str(func_str)
    if ast_f=='': return


    has_arg = 0
    has_global = 0


    arg_var_type = {}    
    global_var_type = {}
    

    for n in ast_f.node_set.keys():
        cur_node = ast_f.node_set[n]
        src = cur_node.dot_src
        if cur_node.type==AST_NODE_TYPE_PARAM:
            struct = src.split(',')[1].split(')')[0].strip()
            
            if struct.find('struct')!=-1 and len(struct.split(' '))>=2:                        
                #print('Find ARG Node: %s'%(struct))            
                struct_type = struct.split(' ')[1]
                
                var         = struct.split(' ')[-1]
                if var[0]=='*':
                    var = var[1:]
                
                if struct_type in args_apis.keys():
                    #print('Target Func: %s'%(src))
                    has_arg = 1                     
                    if not (var in arg_var_type.keys()):
                        arg_var_type[var] = struct_type

        for k in global_apis.keys():
            if src.find(k)!=-1:
                has_global = 1
                global_var_type[k] = k
    

    if has_arg == 1 or has_global==1:
        #print('Begin Analyzing...')
    
        for n in ast_f.node_set.keys():
            cur_node = ast_f.node_set[n]
            src = cur_node.dot_src
            if cur_node.type==AST_NODE_TYPE_OP_ASSIGN:
                if len(src.split('='))!=3:
                    continue
                #print(src)
                right_hand = src.split('=')[2].strip().split(')')[0].strip()
                
                #print('RIGHT-HAND: %s'%(right_hand))
                if (right_hand in arg_var_type.keys()) or (right_hand in global_var_type.keys()):
                    
                    #print('%s %s %s'%('+'*10, file_name, '+'*10))
                    #print('AS: %s'%(cur_node.dot_src))
                    
                    
                    if right_hand in arg_var_type.keys():                    
                        api = args_apis[arg_var_type[right_hand]]
                    
                    if right_hand in global_var_type.keys(): 
                        api = global_apis[global_var_type[right_hand]]
                    
                    root_node = cur_node
                    while root_node.type!=AST_NODE_TYPE_METHOD:
                        root_node = root_node.parent[0]
                    
                    node_set = [root_node]
                    has_get = 0
                    while len(node_set)!=0:
                        t = node_set.pop()
                        
                        for nb in t.nb:
                            node_set.append(nb)
                            
                        if t.line<cur_node.line:
                            if t.dot_src.find(api)!=-1:
                                has_get = 1
                                break
                                
                    
                    if has_get == 0:
                        print('%s %s %s'%('+'*10, file_name, '+'*10))
                        g_logger.write('%s %s %s\n'%('+'*10, file_name, '+'*10))
                        print('Find Bug: %s'%(cur_node.dot_src))
                        g_logger.write('Find Bug: %s\n'%(cur_node.dot_src))
                        g_logger.flush()
            
    
    
    
                                
    
def run_checker():

    g_logger = open(g_record_file, 'w')

    config = configparser.ConfigParser()
    config.read('checkers.ini', encoding='utf-8')

    #secs = config.sections()
    #print(secs)
    
    apis   = ''
    ast_kernel_functions_file = config.get('global', 'ast_kernel_functions')

    if config.has_section('future_escape'):
        #print('yes') 
        apis   = config.get('future_escape', 'apis')[1:-1].split(',')        
    else:
        print('no section *future_escape* for checker9')
        return -1


    args_apis = {}
    
    global_apis = {}

    for api in apis:        
        api = api.strip()
        struct  = api.split(':')[1].strip()
        get_api = api.split(':')[2].strip()
        
        if api[0]=='a':
            
            
            if struct in args_apis.keys():
                print(' Has Already This ARG Key: %s'%(struct))
                exit(-1)
            else:
                print('ARG: %s - %s'%(struct, get_api))
                args_apis[struct]=get_api
        if api[0]=='g':        
            if struct in global_apis.keys():
                print(' Has Already This GLOBAL Key: %s'%(struct))
                exit(-1)
            else:
                print('GLOBAL: %s - %s'%(struct, get_api))
                #global_apis[struct]=get_api
   
    #return 
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
                checker9(file_str, args_apis, global_apis, l, g_logger)
                
            #break
            i+=1
            if i%10000==0:
                print(i)
            
            #if i>50000: break


            

    g_logger.close()
if __name__ == '__main__':

    run_checker()


