import os
import math
from pickle import FALSE
from tablaClausulas  import *
from time import * 
from utils import potdev

def creadesdetabla(t, Q=10):
        # r = t.minimiza(con = nodoTabla([]))
            res = arbol()
            if t.trivial():
                res.value =  nodoTabla([])
                res.var = 0
            elif t.contradict():
                res.value =  nodoTabla([])
                res.var = 0
                res.value.tabla = False
            elif len(t.listavar)<=Q:
                res.value= t
                res.var = 0
            else:

                v = t.minentropia()
                res.var = v
                t0 = t.reduce([-v], inplace = False)
                t1 = t.reduce([v], inplace = False)
               
                l0 = creadesdetabla(t0, Q)
                l1 = creadesdetabla(t1, Q)
                res.hijos[0] = l0
                res.hijos[1] = l1 
            return res

class arbol:
    def __init__(self):
        self.var = 0
        self.value = nodoTabla([])
        self.hijos = [None,None]

    def contradict(self):
        if self.value.contradict():
            return True
        if self.var == 0:
            return False
        if self.hijos[0].contradict() and self.hijos[1].contradict():
            return True
        return False
    
    def copia(self):
        res = arbol()
        res.var = self.var
        res.value = self.value.copia()
        if not res.var == 0:
            res.hijos[0] = self.hijos[0].copia()
            res.hijos[1] = self.hijos[1].copia()
        return res


    
    def getvars(self):
        res = set()
        if self.var ==0:
            return set(self.value.listavar)
        res = set(self.value.listavar)
        res.add(self.var)
        res.update(self.hijos[0].getvars())
        res.update(self.hijos[1].getvars())
        return list(res)
    

    def trivial(self):
        if not self.value.trivial():
            return False
        if self.var == 0:
            return True
        if self.hijos[0].trivial() and self.hijos[1].trivial():
            return True
        return False
        

    def poda(self,Q=20):
        if self.var == 0:
            if len(self.value.listavar)<= Q:
                return
            else:
                h = creadesdetabla(self.value)
                self.value = h.value
                self.var = h.var
                self.hijos = h.hijos
                return
        self.hijos[0].poda(Q)
        self.hijos[1].poda(Q)

        if self.hijos[0].var ==0 and self.hijos[1].var ==0:
            if self.hijos[0].value.contradict() and self.hijos[1].value.contradict():
                self.var = 0
                self.hijos = [None,None]
                self.value.anula()
                return

            if self.hijos[0].value.trivial() and self.hijos[1].value.trivial():
                self.var = 0
                self.hijos = [None,None]
                self.value= nodoTabla([])
                return

            if len(set(self.hikos[0].value.listavar).union(set(self.hikos[1].value.listavar)))<=Q-1:
                v = self.var
                self.var = 0
                self.hijos = [None,None]
                r0 = self.hijos[0].value.suma(potdev(v))
                r1 = self.hijos[1].value.suma(potdev(-v))
                self.value = r0.combina(r1)
                return
        

    def reduce(self,lv):
        if self.var == 0:
            t = self.value.reduce(lv)
            
            res = arbol()
            res.value = t
            return res
        
        v = self.var
        if v in lv:
            return self.hijos[1].reduce(lv)
        if -v in lv:
            return self.hijos[0].reduce(lv)

        res = arbol()
        res.var=v
        res.hijos[0] = self.hijos[0].reduce(lv)
        res.hijos[1] = self.hijos[0].reduce(lv)
        return res

    def combina(self,t, Q= 20,inplace = False):
        res = self if inplace else arbol()
        if isinstance(t,nodoTabla):
            if self.var == 0:
                        value = self.value.combina(t,inplace)
                        if res.value.contradict():
                            res.value.anula()
                            return res
                        else:
                            resq = creadesdetabla(value)
                            
                    
                            res.var = resq.var
                            res.value = resq.value
                            res.hijos = resq.hijos
                        
                            return res



            else:
                res.var = self.var
                res.hijos[0] = self.hijos[0].combina(t.reduce([-self.var]),inplace)
                res.hijos[1] = self.hijos[1].combina(t.reduce([self.var]),inplace)
                return res

        if t.var ==0:
            return self.combina(t.value,inplace)
        if self.var == 0:
            res.var = t.var
            res.hijos[0] = self.combina(t.hijos[0],inplace)
            res.hijos[1] = self.combina(t.hijos[1],inplace)
            return res

        res.var = self.var
        res.hijos[0] = self.hijos[0].combina(t.reduce([-self.var]),inplace)
        res.hijos[1] = self.hijos[1].combina(t.reduce([self.var]),inplace)
        return res
        

    def suma(self,t, Q= 20,inplace = False):
        res = self if inplace else arbol()
        if isinstance(t,nodoTabla):
            if self.var == 0:
                    if len(set(t.listavar).union(set(self.value.listavar)))<=Q:
                        res.value = self.value.suma(t,inplace)
                        if res.value.trivial():
                            res.value = nodoTabla([])
                        return res
                    else:
                        v = self.value.minentropia()
                        res.var = v
                        h0 = arbol()
                        h1 = arbol()
                        h0.value = self.value.reduce([-v])
                        h1.value = self.value.reduce([v])
                        res.hijos[0] = h0.suma(t.reduce([-v]))
                        res.hijos[1] = h1.suma(t.reduce([v]))
                        return res



            else:
                res.var = self.var
                res.hijos[0] = self.hijos[0].suma(t.reduce([-self.var]),inplace)
                res.hijos[1] = self.hijos[1].suma(t.reduce([self.var]),inplace)
                return res

        if t.var ==0:
            return self.suma(t.value,inplace)
        if self.var == 0:
            res.var = t.var
            res.hijos[0] = self.suma(t.hijos[0],inplace)
            res.hijos[1] = self.suma(t.hijos[1],inplace)
            return res

        res.var = self.var
        res.hijos[0] = self.hijos[0].suma(t.reduce([-self.var]),inplace)
        res.hijos[1] = self.hijos[1].suma(t.reduce([self.var]),inplace)
        return res
        
                    
    def borra(self,lv,Q=20, inplace = False):
        res = self if inplace else arbol()
        if self.var ==0:
            nlv = list(set(lv).intersection(set(self.value.listavar)))
            res.value = self.value.borra(nlv)
            if res.value.trivial():
                res.value = nodoTabla([])
            return res
        v = self.var
        if v in lv:
            res = self.hijos[0].suma(self.hijos[1],Q,inplace)
            return res
        else:
            res.var = v
            res.hijos[0] = self.hijos[0].borra(lv,Q,inplace)
            res.hijos[1] = self.hijos[1].borra(lv,Q,inplace)
            return res

    def checkdetermi(self,v):
        
        t0 = self.reduce([v])
        t1 = self.reduce([-v])

        t = t0.combina(t1, Q=20,inplace=False)

        if t.contradict():
            return True
        else:
            return False

    def minimizadep(self,v, seg = set()):
        # print(self.listavar,v, seg)
        vars = set(self.getvars()) - seg
        vars.remove(v)

        if not vars:
            return self
        nv = vars.pop()

        np = self.borra([nv])



        if not np.trivial() and np.checkdetermi(v):
            return np.minimizadep(v, seg.copy())
        else:
            seg.add(nv)
            return self.minimizadep(v,seg)




    def imprime(self, str = ''):

            print (str +"variable ",self.var)
            if self.var==0:
                print(str + "valor " , self.value)
            else:
                print(str +"hijo 1")
                self.hijos[0].imprime(str  + '   ')
                print(str +"hijo 2")
                self.hijos[1].imprime(str  + '   ')     