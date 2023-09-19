#!/usr/bin/python3

'''Add stuffs for checkers'''

if True:
    AST_NODE_TYPE_NULL                      = 0x0
    AST_NODE_TYPE_METHOD                    = 0x1
    AST_NODE_TYPE_PARAM                     = 0x2
    AST_NODE_TYPE_BLOCK                     = 0x3
    AST_NODE_TYPE_LOCAL                     = 0x4
    AST_NODE_TYPE_IDENT                     = 0x5
    AST_NODE_TYPE_FIELD_IDENT               = 0x6
    AST_NODE_TYPE_CONTROL                   = 0x7
    AST_NODE_TYPE_LITERAL                   = 0x8
    AST_NODE_TYPE_JUMP_TARGET               = 0x9
    AST_NODE_TYPE_RETURN                    = 0xa
    AST_NODE_TYPE_METHOD_RETURN             = 0xb
                    
    AST_NODE_TYPE_UNKNOWN                   = 0xc


    AST_NODE_TYPE_OP_ASSIGN                 = 0x100
    AST_NODE_TYPE_OP_ADROF                  = 0x101
    AST_NODE_TYPE_OP_FIELDACCESS            = 0x102
    AST_NODE_TYPE_OP_INDFIELDACCESS         = 0x103
    AST_NODE_TYPE_OP_LOGICALNOT             = 0x104
    AST_NODE_TYPE_OP_LOGICALAND             = 0x105
    AST_NODE_TYPE_OP_LOGICALOR              = 0x106
    AST_NODE_TYPE_OP_INDINDEXACCESS         = 0x107
    AST_NODE_TYPE_OP_EQUAL                  = 0x108
    AST_NODE_TYPE_OP_NOTEQUAL               = 0x109
    AST_NODE_TYPE_OP_ARRAYINIT              = 0x10a
    AST_NODE_TYPE_OP_SUBTRACT               = 0x10b
    AST_NODE_TYPE_OP_LESSTHAN               = 0x10c
    AST_NODE_TYPE_OP_SIZEOF                 = 0x10d
    AST_NODE_TYPE_OP_IND                    = 0x10e
    AST_NODE_TYPE_OP_NOT                    = 0x10f
    AST_NODE_TYPE_OP_AND                    = 0x110
    AST_NODE_TYPE_OP_GREATERTHAN            = 0x111
    AST_NODE_TYPE_OP_GREATEREQTHAN          = 0x112
    AST_NODE_TYPE_OP_COND                   = 0x113
    AST_NODE_TYPE_OP_MINUS                  = 0x114
    AST_NODE_TYPE_OP_MULTI                  = 0x115
    AST_NODE_TYPE_OP_ASSGMINUS              = 0x116
    AST_NODE_TYPE_OP_ASSGOR                 = 0x117
    AST_NODE_TYPE_OP_POSTDEC                = 0x118
    AST_NODE_TYPE_OP_POSTINC                = 0x119
    AST_NODE_TYPE_OP_ARITHSHIFTR            = 0x11a
    AST_NODE_TYPE_OP_CAST                   = 0x11b

    AST_NODE_TYPE_REAL_METHOD               = 0x1000

def get_type(type_str):
    if type_str == 'METHOD':                #1
        return AST_NODE_TYPE_METHOD
    elif type_str == 'PARAM':               #2
        return AST_NODE_TYPE_PARAM
    elif type_str == 'BLOCK':               #3
        return AST_NODE_TYPE_BLOCK
    elif type_str == 'LOCAL':               #4
        return AST_NODE_TYPE_LOCAL
    elif type_str == 'IDENTIFIER':          #5
        return AST_NODE_TYPE_IDENT
    elif type_str == 'FIELD_IDENTIFIER':    #6
        return AST_NODE_TYPE_FIELD_IDENT    
    elif type_str == 'CONTROL_STRUCTURE':   #7
        return AST_NODE_TYPE_CONTROL        
    elif type_str == 'LITERAL':             #8
        return AST_NODE_TYPE_LITERAL 
    elif type_str == 'JUMP_TARGET':         #9
        return AST_NODE_TYPE_JUMP_TARGET    
    elif type_str == 'RETURN':              #A
        return AST_NODE_TYPE_RETURN        
    elif type_str == 'METHOD_RETURN':       #B
        return AST_NODE_TYPE_METHOD_RETURN
    elif type_str == 'UNKNOWN':             #C
        return AST_NODE_TYPE_UNKNOWN        
    elif type_str == '&lt;operator&gt;.assignment':
        return AST_NODE_TYPE_OP_ASSIGN        
    elif type_str == '&lt;operator&gt;.addressOf':
        return AST_NODE_TYPE_OP_ADROF
    elif type_str == '&lt;operator&gt;.fieldAccess':
        return AST_NODE_TYPE_OP_FIELDACCESS 
    elif type_str == '&lt;operator&gt;.indirectFieldAccess':
        return AST_NODE_TYPE_OP_INDFIELDACCESS  
    elif type_str == '&lt;operator&gt;.logicalNot':
        return AST_NODE_TYPE_OP_LOGICALNOT
    elif type_str == '&lt;operator&gt;.logicalAnd':
        return AST_NODE_TYPE_OP_LOGICALAND        
    elif type_str == '&lt;operator&gt;.logicalOr':
        return AST_NODE_TYPE_OP_LOGICALOR        
    elif type_str == '&lt;operator&gt;.indirectIndexAccess':
        return AST_NODE_TYPE_OP_INDINDEXACCESS
    elif type_str == '&lt;operator&gt;.equals':
        return AST_NODE_TYPE_OP_EQUAL
    elif type_str == '&lt;operator&gt;.notEquals':
        return AST_NODE_TYPE_OP_NOTEQUAL
    elif type_str == '&lt;operator&gt;.arrayInitializer':
        return AST_NODE_TYPE_OP_ARRAYINIT
    elif type_str == '&lt;operator&gt;.subtraction':
        return AST_NODE_TYPE_OP_SUBTRACT
    elif type_str == '&lt;operator&gt;.lessThan':
        return AST_NODE_TYPE_OP_LESSTHAN
    elif type_str == '&lt;operator&gt;.sizeOf':
        return AST_NODE_TYPE_OP_SIZEOF 
    elif type_str == '&lt;operator&gt;.indirection':
        return AST_NODE_TYPE_OP_IND 
    elif type_str == '&lt;operator&gt;.not':
        return AST_NODE_TYPE_OP_NOT
    elif type_str == '&lt;operator&gt;.and':
        return AST_NODE_TYPE_OP_AND
    elif type_str == '&lt;operator&gt;.greaterThan':
        return AST_NODE_TYPE_OP_GREATERTHAN
    elif type_str == '&lt;operator&gt;.greaterEqualsThan':
        return AST_NODE_TYPE_OP_GREATEREQTHAN  
    elif type_str == '&lt;operator&gt;.conditional':
        return AST_NODE_TYPE_OP_COND
    elif type_str == '&lt;operator&gt;.minus':
        return AST_NODE_TYPE_OP_MINUS
    elif type_str == '&lt;operator&gt;.multiplication':
        return AST_NODE_TYPE_OP_MULTI
    elif type_str == '&lt;operator&gt;.assignmentMinus':
        return AST_NODE_TYPE_OP_ASSGMINUS
    elif type_str == '&lt;operators&gt;.assignmentOr':
        return AST_NODE_TYPE_OP_ASSGOR
    elif type_str == '&lt;operator&gt;.postDecrement':
        return AST_NODE_TYPE_OP_POSTDEC
    elif type_str == '&lt;operator&gt;.postIncrement':
        return AST_NODE_TYPE_OP_POSTINC
    elif type_str == '&lt;operator&gt;.arithmeticShiftRight':
        return AST_NODE_TYPE_OP_ARITHSHIFTR
    elif type_str == '&lt;operator&gt;.cast':
        return AST_NODE_TYPE_OP_CAST
    else:
        return AST_NODE_TYPE_REAL_METHOD


def get_type_str(t):
    if t == AST_NODE_TYPE_METHOD:                #1
        return 'METHOD'
    elif t == AST_NODE_TYPE_PARAM:               #2
        return 'PARAM'
    elif t == AST_NODE_TYPE_BLOCK:               #3
        return 'BLOCK'
    elif t == AST_NODE_TYPE_LOCAL:               #4
        return 'LOCAL'
    elif t == AST_NODE_TYPE_IDENT:          #5
        return 'IDENTIFIER'
    elif t == AST_NODE_TYPE_FIELD_IDENT:    #6
        return 'FIELD_IDENTIFIER'    
    elif t == AST_NODE_TYPE_CONTROL:   #7
        return 'CONTROL_STRUCTURE'        
    elif t == AST_NODE_TYPE_LITERAL:             #8
        return 'LITERAL' 
    elif t == AST_NODE_TYPE_JUMP_TARGET:         #9
        return 'JUMP_TARGET'    
    elif t == AST_NODE_TYPE_RETURN:              #A
        return 'RETURN'        
    elif t == AST_NODE_TYPE_METHOD_RETURN:       #B
        return 'METHOD_RETURN'
    elif t == AST_NODE_TYPE_UNKNOWN:             #C
        return  'UNKNOWN'        
    elif t == AST_NODE_TYPE_OP_ASSIGN:
        return '.assignment'        
    elif t == AST_NODE_TYPE_OP_ADROF:
        return '.addressOf'
    elif t == AST_NODE_TYPE_OP_FIELDACCESS:
        return '.fieldAccess' 
    elif t == AST_NODE_TYPE_OP_INDFIELDACCESS:
        return '.indirectFieldAccess'  
    elif t == AST_NODE_TYPE_OP_LOGICALNOT:
        return '.logicalNot'
    elif t == AST_NODE_TYPE_OP_LOGICALAND:
        return '.logicalAnd'        
    elif t == AST_NODE_TYPE_OP_LOGICALOR:
        return '.logicalOr'        
    elif t == AST_NODE_TYPE_OP_INDINDEXACCESS:
        return '.indirectIndexAccess'
    elif t == AST_NODE_TYPE_OP_EQUAL:
        return '.equals'
    elif t == AST_NODE_TYPE_OP_NOTEQUAL:
        return '.notEquals'
    elif t == AST_NODE_TYPE_OP_ARRAYINIT:
        return '.arrayInitializer'
    elif t == AST_NODE_TYPE_OP_SUBTRACT:
        return '.subtraction'
    elif t == AST_NODE_TYPE_OP_LESSTHAN:
        return '.lessThan'
    elif t == AST_NODE_TYPE_OP_SIZEOF:
        return '.sizeOf' 
    elif t == AST_NODE_TYPE_OP_IND:
        return '.indirection' 
    elif t == AST_NODE_TYPE_OP_NOT:
        return '.not'
    elif t == AST_NODE_TYPE_OP_AND:
        return '.and'
    elif t == AST_NODE_TYPE_OP_GREATERTHAN:
        return '.greaterThan'
    elif t == AST_NODE_TYPE_OP_GREATEREQTHAN:
        return '.greaterEqualsThan'  
    elif t == AST_NODE_TYPE_OP_COND:
        return '.conditional'
    elif t == AST_NODE_TYPE_OP_MINUS:
        return '.minus'
    elif t == AST_NODE_TYPE_OP_MULTI:
        return '.multiplication'
    elif t == AST_NODE_TYPE_OP_ASSGMINUS:
        return '.assignmentMinus'
    elif t == AST_NODE_TYPE_OP_ASSGOR:
        return '.assignmentOr'
    elif t == AST_NODE_TYPE_OP_POSTDEC:
        return '.postDecrement'
    elif t == AST_NODE_TYPE_OP_POSTINC:
        return '.postIncrement'
    elif t == AST_NODE_TYPE_OP_ARITHSHIFTR:
        return '.arithmeticShiftRight'
    elif t == AST_NODE_TYPE_OP_CAST:
        return '.cast'
    else:
        return 'real_method'

class AST_Node:
    num     = -1
    type    = AST_NODE_TYPE_NULL
    type_str= ''
    src     = ''
    dot_src = ''
    line    = -1
    
    def __init__(self, mytype=AST_NODE_TYPE_NULL):
        self.type = mytype
        self.nb = []
        self.parent = []
        self.var_str = ''

class AST_Graph:
    name = 'unknown'
    
    
    def __init__(self, name):
        self.name = name
        self.node_set = {}
        self.edge_set = {}

    def set_name(self, name):
        self.name = name
    def get_name(self):
        return self.name


def build_ast_from_str(strs):
    ast_g = ''
        
    is_end = False
    last_line = -1
    
    for l in strs.split('\n'):             
        if l=='': break    
        #print(l)
        if is_end==True: 
            print('NOT ONE {, ERROR!!!')
            exit(-1)
        if l.find('label = <>')!=-1:
            continue
        if l[:7]=='digraph': #graph
            m = l.split(' ')[1][1:-1].strip()
            ast_g = AST_Graph(l[l.find('\"')+1:l.rfind('\"')])
            #print 'GRAPH: %s'%(ast_g.get_name())
        elif l.find('->')==-1 and l[0]!='}': # node                     
            is_macro_wrapper_function = 0
            if l.find('SUB')==-1: # ANY real-method should have LINE-NUMBER!
                if l.find('BLOCK')!=-1 or l.find('label')!=-1 or l.find('IDENTIFIER')!=-1:
                    is_macro_wrapper_function=1
                else:
                    print(l)
                    print('No Line Number?')
                    exit(-1)
                #return ''
            
            node = AST_Node()
            node.num = int(l.split(' ')[0][1:-1])                
            attributes      = l.split('<')[1][1:-1].strip()
            
            if is_macro_wrapper_function==1:
                node.line   = 0
            else:
                node.line   = int(l.split('>')[1].split('<')[0].strip())
                
            last_line       = node.line
            node.type_str   = attributes.split(',')[0].strip()                
            node.type       = get_type(node.type_str)
            
            if node.type == AST_NODE_TYPE_IDENT:
                node.var_str = attributes.split(',')[1].strip() 
                
            node.dot_src    = l                
            ast_g.node_set[node.num] = node
        elif l[0]=='}':
            is_end=True
            #print 'Done'
        elif l.find('->')!=-1:
            
            start = int(l.split('->')[0].strip()[1:-1])
            end   = int(l.split('->')[1].strip()[1:-1])
            
            if not ( start in ast_g.node_set.keys()):
                print('Start Node not in Graph!')
                exit(-1)
            if not ( end in ast_g.node_set.keys()):
                print('End Node not in Graph!')
                exit(-1)
            ast_g.edge_set[(start, end)] = (ast_g.node_set[start], ast_g.node_set[end])
            ast_g.node_set[start].nb.append(ast_g.node_set[end])
            ast_g.node_set[end].parent.append(ast_g.node_set[start])
           
        else:
            print(l)
            print('ERROR!')
            exit(-1)
    return ast_g 