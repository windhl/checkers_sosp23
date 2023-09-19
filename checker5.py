#!/usr/bin/python3

'''SOSP23-Paper21: '''
'''Checker5: F_start --> S_G-->S_P|B_error --> F_end'''

import os
import configparser
import json
from utils import *

g_record_file = 'checker5.log'

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


def checker5(func_str, apis, file_name, g_logger):
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
                            put_line    = 100000
                            return_line = 100000
                            goto_line   = 100000
                            put_node = ''
                            return_node = ''
                            goto_node = ''
                            goto_target = ''
                            while len(node_set)!=0:
                                t = node_set.pop()
                                
                                for nb in t.nb:
                                    node_set.append(nb)
                                
                                
                                if t.line>assign_line_num:
                                    if t.dot_src.find('%s'%(put_apis[api]))!=-1:
                                        #print('\tPUT! %s'%(t.dot_src))
                                        if put_line>t.line:
                                            put_line = t.line
                                            put_node = t
                                            #print('PUTLINE: %d'%put_line)                                    
                                    if t.type==AST_NODE_TYPE_CONTROL and t.dot_src.find('if')!=-1 and \
                                    t.dot_src.find('(!%s)'%return_var)==-1 and t.dot_src.find('%s == NULL'%return_var)==-1:
                                        t_node_set = [t]
                                        while len(t_node_set)!=0:
                                            t_node = t_node_set.pop()
                                            for nb in t_node.nb:
                                                t_node_set.append(nb)
                                            if t_node.dot_src.find('return')!=-1:
                                                    #print('+'*20+file_name+'+'*20)
                                                    #print('CONTROL: %s'%(t.dot_src))
                                                    #print('\t R: %s'%(t_node.dot_src))
                                                    if return_line>t_node.line:
                                                        return_line = t_node.line
                                                        return_node = t_node
                                                        #print('RETLINE: %d'%return_line)
                                            if t_node.dot_src.find('goto')!=-1:
                                                if goto_line>t_node.line:
                                                    goto_line = t_node.line
                                                    goto_node = t_node
                                                    goto_target = t_node.dot_src.split(',')[1].split(' ')[1][:-1]
                                                    #print('GOTO: %s'%goto_target)
                                                    
                                                    
                            #print('PUT: %d RETURN: %d'%(put_line, return_line))        
                            if put_line!=100000 and return_line!=100000 and put_line>return_line:
                                print('%s %s %s'%('+'*10, file_name, '+'*10))
                                g_logger.write(file_name+'\n')
                                print('\tMeet Error-Unpaired API (RETURN): %s - %s'%(api, return_node.dot_src))
                                g_logger.write('\tMeet Error-Unpaired API (RETURN): %s - %s\n'%(api, return_node.dot_src))
                                g_logger.flush()
                                
                            if put_line!=100000 and goto_line!=100000 and put_line>goto_line:
                            
                                root_node = goto_node
                                goto_put = 0
                                jump_target_line = 100000
                                while root_node.type!=AST_NODE_TYPE_METHOD:
                                    root_node = root_node.parent[0]
                            
                                node_set = [root_node]
                                while len(node_set)!=0:
                                
                                    t = node_set.pop()
                                
                                    for nb in t.nb:
                                        node_set.append(nb)
                                    
                                    if t.line>goto_line:
                                        if t.type==AST_NODE_TYPE_JUMP_TARGET:
                                            jump_target = t.dot_src.split(',')[1].split(')')[0].strip()
                                            #print('JT: %s'%(jump_target))
                                            if jump_target==goto_target:
                                                jump_target_line = t.line
                                                #print('Find JT: %s %d'%(t.dot_src, t.line))
                                    
                                node_set = [root_node]
                                while len(node_set)!=0:
                                
                                    t = node_set.pop()
                                
                                    for nb in t.nb:
                                        node_set.append(nb)    
                                    if t.line>=jump_target_line:
                                        #print('After JT: %s'%(t.dot_src))
                                        if t.dot_src.find('%s'%(put_apis[api]))!=-1:
                                            goto_put = 1
                                            #print('goto has put: %s'%(t.dot_src))
                                            #exit(-1)
                            
                                if goto_put==0:
                                    print('%s %s %s'%('+'*10, file_name, '+'*10))
                                    g_logger.write(file_name+'\n')
                                    print('\tMeet Error-Unpaired API (GOTO): %s - %s'%(api, goto_node.dot_src))
                                    g_logger.write('\tMeet Error-Unpaired API (GOTO): %s - %s\n'%(api, goto_node.dot_src))
                                    g_logger.flush()
                                    



                        
def run_checker():

    g_logger = open(g_record_file, 'w')

    config = configparser.ConfigParser()
    config.read('checkers.ini', encoding='utf-8')

    #secs = config.sections()
    #print(secs)
    apis = ''
    ast_kernel_functions_file = config.get('global', 'ast_kernel_functions')

    if config.has_section('get_api'):
        #print('yes') 
        apis = config.get('get_api', 'apis')[1:-1].split(',')         
    else:
        print('no section *get_api* for checker5')
        return -1

    
    i = 0
    
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
                checker5(df.read(), apis, l, g_logger)
            #break
            i+=1
            if i%10000==0:
                print(i)
            #if i>10:  break

    g_logger.close()
if __name__ == '__main__':

    run_checker()


