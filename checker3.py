#!/usr/bin/python3

'''SOSP23-Paper21: '''
'''Checker3: F_start --> M_SL --> S_break --> F_end'''

import os
import configparser
import json
from utils import *

g_record_file = 'checker3.log'

def checker3(func_str, apis, file_name, g_logger):
    ast_f = build_ast_from_str(func_str)
    if ast_f=='': return
    
    for api in apis:
        api = api.strip()
        for n in ast_f.node_set.keys():            
            cur_node = ast_f.node_set[n]
            src = cur_node.dot_src
            
            if cur_node.type == AST_NODE_TYPE_REAL_METHOD:
                if src.find(',')==-1 or src.find('(')==-1:
                    continue
                func_name = src.split(',')[0].split('(')[1].strip()
                
                if func_name==api:
                    second_arg = src.split(',')[-1]
                    second_arg = second_arg[:second_arg.rfind(')')-1].strip()
                    #print(second_arg)
                    for nb in cur_node.parent[0].nb:
                        if nb.type==AST_NODE_TYPE_BLOCK:
                            if nb.line==cur_node.line: # find the for_each block
                                #print(cur_node.dot_src)                                
                                break_node = ''
                                done_break = []
                                tb = [nb]              # find the break
                                while len(tb)!=0:
                                    node = tb.pop()
                                    
                                    for nnb in node.nb:
                                        if len(nnb.nb)>1:
                                            tb.append(nnb)
                                        
                                        #ugly
                                        if nnb.dot_src.find('break')!=-1:                                        
                                            
                                            switch_or_loop_break = 0
                                            np = nnb.parent
                                            while True:                                                
                                                if len(np)>0:                                                    
                                                    if np[0].line == cur_node.line:
                                                        break
                                                    if np[0].dot_src.find('switch')!=-1 or np[0].dot_src.find('for (')!=-1:
                                                        switch_or_loop_break = 1
                                                        break
                                                np = np[0].parent
                                                
                                            if switch_or_loop_break==0 and break_node!=nnb:
                                                break_node = nnb
                                                break
                                            
                                    if break_node != '' and (not break_node in done_break):
                                        has_put = 0
                                        for b_nb in break_node.parent[0].nb:
                                            if b_nb.dot_src.find('of_node_put')!=-1:
                                                has_put = 1
                                                break
                                            
                                            if b_nb.dot_src.find('= %s'%(second_arg))!=-1:
                                                #print(b_nb.dot_src)
                                                has_put = 1
                                                break

                                        
                                        if has_put==0:
                                            print(file_name)
                                            g_logger.write(file_name+'\n')                                                                              
                                            print('SmartLoop: %s Break: %s'%(cur_node.dot_src, break_node.dot_src))
                                            g_logger.write('SmartLoop: %s Break: %s'%(cur_node.dot_src, break_node.dot_src))
                                            g_logger.flush()
                                    
                                        done_break.append(break_node)

def run_checker():

    g_logger = open(g_record_file, 'w')

    config = configparser.ConfigParser()
    config.read('checkers.ini', encoding='utf-8')

    #secs = config.sections()
    #print(secs)
    apis = ''
    ast_kernel_functions_file = config.get('global', 'ast_kernel_functions')

    if config.has_section('smart_loop'):
        #print('yes')
        apis = config.get('smart_loop', 'apis')[1:-1].split(',')         
    else:
        print('no section *smart_loop* for checker3')

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
            #dot_file = '/data1/linux-ast/0/+data1+struck-linux+arch+mips+pci+pci-rt3883.c+outdir/16-ast.dot'
            #print('Process --- %s'%dot_file)
            with open(dot_file) as df:
                checker3(df.read(), apis, l, g_logger)
            #break
            i+=1
            if i%10000==0:
                print(i)
            #if i>10:  break

    g_logger.close()
if __name__ == '__main__':

    run_checker()


