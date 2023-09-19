#!/usr/bin/python3

'''SOSP23-Paper21: '''
'''Checker7: F_start --> S_G --> S_free --> F_end'''

import os
import configparser
import json
from utils import *

g_record_file = 'checker7.log'




def checker7(func_str, apis, file_name, g_logger):
    
    ast_f = build_ast_from_str(func_str)
    if ast_f=='': return
    
    
    bug_lines = []
    
    for api in apis:
        api = api.strip()
        
        api_count = 0
        for n in ast_f.node_set.keys(): 
            cur_node = ast_f.node_set[n]
            src = cur_node.dot_src
            
            if cur_node.type == AST_NODE_TYPE_REAL_METHOD:
                if src.find(api)!=-1:
                    api_count+=1
        
        if api_count>1:
            return
            
        for n in ast_f.node_set.keys():            
            cur_node = ast_f.node_set[n]
            src = cur_node.dot_src
            
            if cur_node.type == AST_NODE_TYPE_REAL_METHOD:
            
                if src.find(api)!=-1:
                    #print(file_name)
                    #print('Find: %s'%(src))
                    para_var = src.split(',')[1].split('(')[1]
                    
                    if para_var[:5]=='&amp;':
                        target_var = para_var[5:].split('-')[0].strip()
                        
                        root_node = cur_node
                        while root_node.type!=AST_NODE_TYPE_METHOD:
                            root_node = root_node.parent[0]
                        
                        node_set = [root_node]
                        
                        has_goto = 0
                        goto_nodes = []
                        while len(node_set)!=0:
                            t = node_set.pop()
                            
                            for nb in t.nb:
                                node_set.append(nb)
                                
                            if t.line>cur_node.line:
                            
                                if t.dot_src.find('goto')!=-1:
                                    #print('Find GOTO %s'%(t.dot_src))
                                    goto_nodes.append(t)
                                    has_goto = 1
                                
                        if has_goto == 1:
                            goto_info = {}
                            for gn in goto_nodes:
                                goto_target = gn.dot_src.split(',')[1].split(' ')[1][:-1].strip()
                                goto_info[goto_target] = [gn.line, -1]
                                
                            node_set = [root_node]
                            while len(node_set)!=0:
                                t = node_set.pop()
                                
                                for nb in t.nb:
                                    node_set.append(nb)
                                    
                                if t.line>cur_node.line:
                                
                                    if t.type==AST_NODE_TYPE_JUMP_TARGET:
                                        #print(t.dot_src)
                                        
                                        
                                        target = t.dot_src.split(',')[1].split(')')[0].strip()                                        
                                        
                                        
                                        if target in goto_info.keys():
                                            goto_info[target][1]=t.line
                                            #print('%s : %d'%(target, t.line))
                                        else:
                                            #print('No Such Goto:%s'%(t.dot_src))
                                            pass
                                
                                            
                            node_set = [root_node]
                            while len(node_set)!=0:
                                t = node_set.pop()
                                
                                for nb in t.nb:
                                    node_set.append(nb)
                                    
                                if t.line>cur_node.line and (not (t.line in bug_lines)):
                                
                                    if t.type==AST_NODE_TYPE_REAL_METHOD and t.dot_src.find('kfree(%s)'%(target_var))!=-1:
                                        #print(file_name)
                                        #print('Find KFree: %s'%(t.dot_src))
                                        min_kfree_goto = 100000
                                        kfree_goto_line = 0
                                        for gk in goto_info.keys():
                                            #print(goto_info[gk][1])
                                            if goto_info[gk][1]<t.line and (t.line-goto_info[gk][1])<min_kfree_goto:
                                                min_kfree_goto = t.line-goto_info[gk][1]
                                                kfree_goto_line = goto_info[gk][0]
                                                #print('Find Min GOTO: %s %d'%(gk, kfree_goto_line))
                                        
                                        if kfree_goto_line!=0:
                                            if kfree_goto_line>cur_node.line:
                                                print('%s %s %s'%('+'*10, file_name, '+'*10))
                                                g_logger.write('%s %s %s\n'%('+'*10, file_name, '+'*10))
                                                print('Find Bug: %s'%(t.dot_src))
                                                g_logger.write('Find Bug: %s\n'%(t.dot_src))
                                                g_logger.flush()
                                                bug_lines.append(t.line)
                            
                            #exit(-1)
                        
                    #exit(-1)


    
def run_checker():

    g_logger = open(g_record_file, 'w')

    config = configparser.ConfigParser()
    config.read('checkers.ini', encoding='utf-8')

    #secs = config.sections()
    #print(secs)
    
    apis   = ''
    ast_kernel_functions_file = config.get('global', 'ast_kernel_functions')

    if config.has_section('direct_free'):
        #print('yes') 
        apis   = config.get('direct_free', 'apis')[1:-1].split(',')        
    else:
        print('no section *direct_free* for checker7')
        return -1

   
    i = 0    
    

    with open(ast_kernel_functions_file) as f:
        while True:
            l = f.readline()
            if l=='': break
            
            l = l.strip()
            if l=='': continue
            dot_file = l.split(' ')[0].split(':')[1]  
            #dot_file = '/data1/linux-ast/2/+data1+struck-linux+drivers+scsi+fcoe+fcoe_sysfs.c+outdir/52-ast.dot'
            #print('Process --- %s'%dot_file)
            
            with open(dot_file) as df:                
                file_str = df.read()
                checker7(file_str, apis, l, g_logger)
                
            #break
            i+=1
            if i%10000==0:
                print(i)
            
            #if i>50000: break


            

    g_logger.close()
if __name__ == '__main__':

    run_checker()


