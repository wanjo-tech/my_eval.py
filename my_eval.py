# great eval tool by wanjo 2022-05-10

from mypy import tryx,s2o,sys_import

def fwd(c,m,param_a): return tryx(lambda:getattr(sys_import(c).api(param_a),m)(*param_a),lambda ex:{'errmsg':str(ex)})

def my_eval(s,g={},l={},debug=False):
    if type(s) is bytes: s = s.decode()
    s = f'{s}'.strip()
    if len(s)<1: return None
    a = s2o(s)
    if debug: print(f'===In: {a or s}')
    flg_right = False
    call_id = None
    call_param = None
    call_style = None
    #if type(a) is list: # list-come-list-go
    if s[0]=='[':
        call_style = 1
        len_a = len(a)
        a0i = tryx(lambda:int(a[0]),False)
        if len_a>1 and type(a0i) is int:
            call_entry = a[1]
            call_param = tryx(lambda:a[2:],False)
            call_id = a[0]
            flg_right = True
        elif len_a>0:
            call_entry = a[0]
            call_param = tryx(lambda:a[1:],False)
            flg_right = True

    elif s[0]=='(' or s[0]=='/': # pyql ;)
        s=s.replace('__builtins__','') # safenet...
        if s[0]=='/': s = s[1:]
        return str(tryx(lambda:eval(s,g,l),True))

    #elif type(a) is dict: # dict-come-dict-go, NOTES please try not to...
    elif s[0]=='{':
        call_style = 2
        call_entry = a.get('entry',None)
        call_param = a.get('param',[])
        call_id = a.get('id',None)
        flg_right = True

    elif a is None: # quick console mode sep by comma (not good for special case...)
        call_style = 3
        #a = s.split('\t')
        s=s.replace('\t','')
        a = s.split(',') # not good for some quote case!
        len_a = len(a)
        a0i = tryx(lambda:int(a[0]),False)
        if len_a>1 and type(a0i) is int:
            call_style = 1 # rollback to list-mode
            call_entry = a[1]
            call_param = tryx(lambda:a[2:],False)
            call_id = a0i or a[0]
            flg_right = True
        elif len_a>0:
            call_entry = a[0]
            call_param = tryx(lambda:a[1:],False)
            flg_right = True

    if flg_right:
        a = call_entry.split('.')
        if len(a)<2:
            rt = {'errmsg':'wrong entry {}'.format(call_entry)}
        else:
            rt = fwd('api{}'.format(a[0]),a[1],call_param)
    else:
        rt = {'errmsg':'TODO'}

    if debug:print(f'===Out <{type(rt).__name__}>',len(rt) if type(rt) in [bytes,str,dict,list,tuple] else rt)

    if call_style==1: # list mode
        if call_id is None:
            return [rt] # 
        else:
            return [call_id,rt]
    elif call_style in [2,3]: # dict mode
        return rt
    else:
        return None

if __name__ == '__main__':
  from mypy import sys,now
  for line in sys.stdin: print(my_eval(line,{"__builtins__":{
    'now':now(),'help':'nothing to help u unless u read the source codes'
  }}))

