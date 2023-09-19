#!/usr/bin/python3

'''SOSP23-Paper21: '''
'''Checker1: F_start --> S_G_E --> B_error --> F_end'''

import os
import configparser
import json
from utils import *




g_record_file = 'checker1.log'

put_apis = {'pm_runtime_get_sync':'pm_runtime_put',
            'kobject_init_and_add':'kobject_put'}


def checker1(func_str, apis, file_name, g_logger):
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
                
                    return_var = src.split(',')[1].split('=')[0].strip()
                    closest_nb = ''
                    closest_line_delta = 1000
                    for nb in cur_node.parent[0].nb:
                        if nb.line>cur_node.line:                            
                            if nb.dot_src.find('if')!=-1 and nb.dot_src.find(return_var)!=-1:                                
                                #print(nb.dot_src)                                
                                '''we should not add ')' as there may be other condition'''
                                if nb.dot_src.find('if (%s)'%(return_var))!=-1 \
                                    or nb.dot_src.find('if (unlikely(%s))'%(return_var))!=-1 \
                                    or nb.dot_src.find('if (%s &lt; 0'%(return_var))!=-1 \
                                    or nb.dot_src.find('if (unlikely(%s &lt; 0'%(return_var))!=-1 \
                                    or nb.dot_src.find('if (%s == -E'%(return_var))!=-1: #some specific error
                                    
                                    if (nb.line-cur_node.line) < closest_line_delta:
                                        #print('Meet Close IF: %s'%(nb.dot_src))
                                        closest_nb = nb
                                        closest_line_delta = nb.line-cur_node.line
                                    
                    #print('NB: %s'%nb.dot_src)                    
                    if closest_nb=='': 
                        continue
                    
                    nb = closest_nb
                    
                    has_put = 0
                    has_return = 0
                    has_goto = 0
                    goto_target = ''
                    block_src = nb.dot_src+'\n'
                    for nnb in nb.nb:
                        if nnb.dot_src.find('BLOCK')!=-1:
                            for target_nb in nnb.nb:                                                
                                block_src+='\t'+target_nb.dot_src+'\n'
                                #print('\t%s'%(target_nb.dot_src))
                                if target_nb.dot_src.find('put')!=-1:
                                    has_put=1
                                    #break
                                if target_nb.dot_src.find('return')!=-1:
                                    has_return=1    
                                if target_nb.dot_src.find('goto')!=-1:
                                    has_goto=1
                                    goto_target=target_nb.dot_src.split(',')[-1].split(';')[0].split(' ')[1].strip()
                                    #print(target_nb.dot_src)
                                    #print('GOTO: %s'%(goto_target))                                    
                                    
                    if has_put==0 and has_return==1:
                        print(file_name)
                        g_logger.write(file_name+'\n')                                                                              
                        print('LINE: %d SRC: %s'%(cur_node.line, src))
                        g_logger.write(src+'\n')                    
                        print(block_src)
                        g_logger.write(block_src+'\n')
                        g_logger.flush()
                        
                    if has_put==0 and has_goto==1:
                        for n in ast_f.node_set.keys():                             
                            if ast_f.node_set[n].type==AST_NODE_TYPE_JUMP_TARGET:
                                node_jt = ast_f.node_set[n]
                                cur_jt = node_jt.dot_src.split(',')[1].split(')')[0].strip()
                                if cur_jt==goto_target:
                                    #print("Meet JUMP_TARGET: %s"%(node_jt.dot_src))
                                    has_goto_put = 0
                                    for nb in node_jt.parent[0].nb:
                                        if nb.line>node_jt.line:
                                            if nb.dot_src.find(put_apis[api])!=-1:
                                                has_goto_put = 1
                                                break
                                            
                                            tb = nb.nb
                                            while len(tb)>0:
                                                node = tb.pop()                                                
                                                if len(node.nb)!=0:
                                                    for nnb in node.nb:
                                                        if len(nnb.nb)>0:
                                                            tb.append(nnb)
                                                        if nnb.dot_src.find(put_apis[api])!=-1:
                                                            #print('Find PUT: %s'%(nnb.dot_src))
                                                            has_goto_put = 1
                                                            break
                                                    if has_goto_put==1:
                                                        break
                                    
                                    if has_goto_put==0:
                                        print(file_name)
                                        g_logger.write(file_name+'\n')                                                                              
                                        print('LINE: %d SRC: %s'%(cur_node.line, src))
                                        g_logger.write(src+'\n')                    
                                        print(block_src)
                                        g_logger.write(block_src+'\n')
                                        g_logger.flush()
                                    
                                    
                        

def run_checker():

    g_logger = open(g_record_file, 'w')

    config = configparser.ConfigParser()
    config.read('checkers.ini', encoding='utf-8')

    #secs = config.sections()
    #print(secs)
    apis = ''
    ast_kernel_functions_file = config.get('global', 'ast_kernel_functions')

    if config.has_section('return_error'):
        #print('yes')
        apis = config.get('return_error', 'apis')[1:-1].split(',')         
    else:
        print('no section *return_error* for checker1')

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
            #print('Process --- %s'%dot_file)
            with open(dot_file) as df:
                checker1(df.read(), apis, l, g_logger)
            #break
            i+=1
            if i%10000==0:
                print(i)
            #if i>10:  break

    g_logger.close()
if __name__ == '__main__':

    run_checker()


