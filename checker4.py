#!/usr/bin/python3

'''SOSP23-Paper21: '''
'''Checker4: F_start --> S_(G_H|P_H) --> F_end'''

import os
import configparser
import json
from utils import *

g_record_file = 'checker4.log'

put_apis = {'of_parse_handle':'of_node_put',
            'of_get_parent':'of_node_put',
            'of_get_child_by_name':'of_node_put',
            'of_find_compatible_node':'of_node_put',
            'of_find_matching_node':'of_node_put',
            'of_find_node_by_name':'of_node_put',
            'of_find_node_by_path':'of_node_put',
            'of_find_node_by_phandle':'of_node_put',
            'of_find_node_by_type':'of_node_put',
            'ip_dev_find':'dev_put',
            'afs_alloc_read':'afs_put_read',
            'perf_cpu_map__new':'perf_cpu_map__put',
            'setup_find_cpu_node':'of_node_put',
            'gfs2_holder_init':'gfs2_holder_uninit',
            'tipc_node_find':'tipc_node_put',
            'sockfd_lookup':'sockfd_put',
            'fc_rport_lookup':'kref_put',            
            'lookup_bdev':'bdput',
            '__tcp_ulp_find_autoload':'module_put',
            '__ipv4_neigh_lookup':'neigh_release',
            'class_find_device':'put_device',
            'mpol_shared_policy_lookup':'mpol_cond_put',
            'usb_anchor_urb':'usb_put_urb',
            'tomoyo_mount_acl':'path_put'           
            }


def checker4_get(func_str, apis, file_name, g_logger):
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
                    #print('%s %s %s'%('+'*10, file_name, '+'*10))
                    #print('\tMeet API: %s - %s'%(api, src))
                    #print('\tParent: %s'%(cur_node.parent[0].dot_src))
                    line_num = 0
                    if cur_node.parent[0].dot_src.find('assignment')!=-1:
                        return_var = ''
                        cp = cur_node.parent[0]
                        assign_line_num = cp.line
                        for nb in cp.nb:
                            #print('\tNB: %s'%(nb.dot_src))
                            if nb.dot_src.find('IDENTIFIER')!=-1:
                                return_var = nb.dot_src.split(',')[1].strip()
                                #print('\tReturn: %s'%(return_var))
                                break
                        
                        if return_var!='':                            
                            root_node = cp
                            while root_node.type!=AST_NODE_TYPE_METHOD:
                                root_node = root_node.parent[0]
                            #print('%s'%t_node.dot_src)
                            
                            node_set = [root_node]
                            has_put = 0
                            has_assign = 0
                            has_return = 0
                            assign_node = ''
                            return_node = ''
                            while len(node_set)!=0:
                                t = node_set.pop()
                                
                                for nb in t.nb:
                                    node_set.append(nb)
                                    
                                if t.line>assign_line_num:
                                    if t.dot_src.find('%s'%(put_apis[api]))!=-1:
                                        #print('\tPUT! %s'%(t.dot_src))
                                        has_put = 1
                                        #exit(-1)
                                    if t.dot_src.find('assignment')!=-1:
                                        if t.dot_src.find('= %s;'%(return_var))!=-1:
                                            has_assign = 1
                                            assign_node = t
                                    if t.dot_src.find('return %s'%(return_var))!=-1:
                                        has_return = 1
                                        return_node = t
                            if has_put==0:                            
                                if has_assign==1:
                                    #print('%s %s %s'%('+'*10, file_name, '+'*10))
                                    #print('\tMeet Assignment: %s'%(assign_node.dot_src))
                                    #exit(-1)
                                    continue
                                    
                                if has_return==1:
                                    #print('%s %s %s'%('+'*10, file_name, '+'*10))
                                    #print('\tMeet Return: %s'%(return_node.dot_src))
                                    #exit(-1)                                    
                                    continue
                            
                                print('%s %s %s'%('+'*10, file_name, '+'*10))
                                g_logger.write(file_name+'\n')
                                print('\tMeet No-PUT-Paired API: %s - %s'%(api, src))
                                g_logger.write('\tMeet No-PUT-Paired API: %s - %s\n'%(api, src))
                                g_logger.flush()


def checker4_put(func_str, apis, file_name, g_logger):
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
                    from_arg = src.split(',')[1].split('(')[1].strip()
                    if from_arg!='NULL':
                        print('%s %s %s'%('+'*10, file_name, '+'*10))
                        root_node = cur_node
                        while root_node.type!=AST_NODE_TYPE_METHOD:
                            root_node = root_node.parent[0]
                        
                        node_set = [root_node]
                        has_get = 0
                        while len(node_set)!=0:
                            t = node_set.pop()
                            
                            for nb in t.nb:
                                node_set.append(nb)
                                
                            if t.line==cur_node.line-1:
                            
                                if t.dot_src.find('of_node_get')!=-1:
                                    has_get = 1
                                    
                        if has_get==0:
                            print('%s %s %s'%('+'*10, file_name, '+'*10))
                            g_logger.write(file_name+'\n')
                            print('\tMeet No-GET-Paired API: %s - %s'%(api, src))
                            g_logger.write('\tMeet No-GET-Paired API: %s - %s\n'%(api, src))
                            g_logger.flush()    
                                    
                        
                        
def run_checker():

    g_logger = open(g_record_file, 'w')

    config = configparser.ConfigParser()
    config.read('checkers.ini', encoding='utf-8')

    #secs = config.sections()
    #print(secs)
    apis_get = ''
    apis_put = ''
    ast_kernel_functions_file = config.get('global', 'ast_kernel_functions')

    if config.has_section('hidden_get'):
        #print('yes') 
        apis_get = config.get('hidden_get', 'apis')[1:-1].split(',')         
    else:
        print('no section *hidden_get* for checker4')
        return -1

    if config.has_section('hidden_put'):
        #print('yes') 
        apis_put = config.get('hidden_put', 'apis')[1:-1].split(',')         
    else:
        print('no section *hidden_put* for checker4') 
        return -1        


    i = 0
    
    with open(ast_kernel_functions_file) as f:
        while True:
            l = f.readline()
            if l=='': break
            
            l = l.strip()
            if l=='': continue
            dot_file = l.split(' ')[0].split(':')[1]  
            #dot_file = '/data1/linux-ast/0/+data1+struck-linux+arch+arm+mach-imx+cpu-imx31.c+outdir/70-ast.dot'
            #print('Process --- %s'%dot_file)
            with open(dot_file) as df:
                #checker4_get(df.read(), apis_get, l, g_logger)
                checker4_put(df.read(), apis_put, l, g_logger)
            #break
            i+=1
            if i%10000==0:
                print(i)
            #if i>10:  break

    g_logger.close()
if __name__ == '__main__':

    run_checker()


