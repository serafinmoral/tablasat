# -*- coding: utf-8 -*-
"""
Created on 31 Enero 2022

@author: Serafin
"""
from secrets import choice
from statistics import variance
from utils import *
from time import *
from random import shuffle,choices
from arboltabla import *

def update(value,dvar,dvard,total):
    for x in total:
        value[x] = 0.0
        lista1 = dvar.get(x,[])
        lista2 = dvard.get(x,[])
        if lista2:
            pivote = min(lista2,key = lambda y: len(y))
            for p in lista1:
                value[x] += 2**(len(pivote.union(p))-1) - 2**(len(p))
            
            for p in lista2:
                if not p == pivote:
                    value[x] += 2**(len((pivote.union((p))))-1) - 2**(len(p))
        else:
            t = set()
            for p in lista1:
                value[x] -= - 2**(len(p))
                t.update(p)
            value[x] += 2**(len(t)-1)

def updateclus(x,dvar,dvard):
    res = set()
    lista1 = dvar.get(x,[])
    lista2 = dvard.get(x,[])
    nue = []

    if lista2:
            pivote = min(lista2,key = lambda y: len(y))
            res.update(pivote)
            for p in lista1:
                nue.append(p.union(pivote) -{x})
                res.update(p)

            for p in lista2:
                if not p == pivote:
                    nue.append(p.union(pivote) -{x})
                    res.update(p)

    else:
            
            for p in lista1:
                res.update(p)
                
            nue.append(res)
    for v in res:
            dvar[v] = list(filter(lambda z: x not in z, dvar.get(v,[]) ))
            dvard[v] = list(filter(lambda z: x not in z, dvard.get(v,[]) ))

    res.discard(x)
    
   
    for p in nue:
        for v in p:
            if v in dvar:
                dvar[v].append(p)
            else:
                dvar[v] = [p]

    return res

def groupp(l,Q=30):
    if not l:
        return
    ln = l.copy()
    t = min(ln,key = lambda x: len(x.getvars()))   
    l.remove(t) 
    ln.remove(t)
    while ln:
        h = min(ln,key = lambda x: len(set(x.getvars()).union(set(t.getvars()))))
        if len(set(h.getvars()).union(set(t.getvars()))) <= Q:
            t = t.combina(h)
            ln.remove(h)
            l.remove(h)
        else:
            l.append(t)
            t = min(ln,key = lambda x: len(t.getvars()))   
            ln.remove(t)
            l.remove(t)
    l.append(t)
    


def ordena(l,Q):

    lc = l.copy()
    l.clear()

    while lc:
        q = min(lc, key = lambda x: len(x.getvars()))
        lc.remove(q)
        l.append(q)
        lista = set(q.getvars())
        while lc:
            q = min(lc, key = lambda x: len(lista.union(set(x.getvars()))))
            if len(lista.union(set(q.getvars())))<=Q:
                lc.remove(q)
                l.append(q)
                lista.update(set(q.getvars()))
            else:
                break

class varpot:

        def __init__(self): #EDM

            self.tabla = dict()
            self.tablad = dict()
            self.contradict = False
            self.tablam = dict()
            self.orden = []
            self.posvar = dict()
            self.clau = dict()
            self.prob = dict()
            self.w = 1
            
            
          
        def anula(self):
            self.tabla = dict()
            self.tablad = dict()
            self.contradict = True
            self.small = dict()
            self.clau = dict()

 

        def getvars(self):
            res = set()
            for v in self.tabla:
                if self.tabla[v]:
                    res.add(v)
            for v in self.tablad:
                if self.tablad[v]:
                    res.add(v)


            return res
        

        def computefromBayes(self,tables,evid):
            self.w  = 1
            tar = []
            for p in tables:
                q = p.reduce(evid)
                tar.append(q)
            for x in evid:
                p = tableunit(x)
                self.insertar(p)
            for p in tar:
                self.insertbay(p)
               
                q = nodoTabla(p.listavar)
                q.tabla = p.tabla > 0
                if not q.trivial():
                    self.insertar(q)

        def insertbay(self,p):
            if not p.getvars():
                print("sin variables ")
                self.w = self.w*p.tabla
                print(self.w)
                # sleep(3)
            for v in p.getvars():
                if v in self.prob:
                    self.prob[v].append(p)
                else:
                    self.prob[v] = [p]

            
            
        def removebay(self,p):    
            for v in p.getvars():
                self.prob[v].remove(p)
               

        def getpot(self,Q=5):
            res = []
            for v in self.tabla:
                for p in self.tabla[v]:
                    if len(p.getvars())>= Q and not p in res:
                        res.append(p)
            for v in self.tablad:
                for p in self.tablad[v]:
                    if len(p.getvars())>= Q and not p in res:
                        res.append(p)

                return res
            
        def getpotd(self):
            lista = []
            for v in self.tablad:
                for p in self.tablad[v]:
                    if not p in lista:
                        lista.append(p)
            return lista

        def getpotl(self,l):
            res = []
            for v in l:
                if v in self.tabla:
                    for p in self.tabla[v]:
                        if not p in res:
                            res.append(p)
            for v in l:
                if v in self.tablad:
                    for p in self.tablad[v]:
                        if not p in res:
                           res.append(p) 
            return res
        

        def getvarsd(self,v):
            res  = set()
            l = self.get(v) + self.getd(v)
            for p in l:
                res.update(set(p.getvars()))
         


            return res

        def copia(self):
            res = varpot()
            if self.contradict:
                res.contradict = True
                return 
            for v in self.tabla:
                res.tabla[v] = self.tabla[v].copy()
            for v in self.tablad:
                res.tablad[v] = self.tablad[v].copy()
            for v in self.tablam:
                res.tablam[v] = self.tablam[v].copy()

            for v in self.clau:
                res.clau[v] = self.clau[u].copy()

            for v in self.prob:
                res.prob[v] = self.prob[v].copy()

   
            res.orden = self.orden.copy()
            res.posvar = self.posvar.copy()

            res.w = self.w
            
            
            return res

        def calculab(self):
            res = varpot()
            trabajo = self.copia()
            res.orden = self.orden.copy()
            res.posvar = self.posvar.copy()
            for v in self.orden:
                lista1 = trabajo.get(v)
                lista2 = trabajo.getd(v)
                res.tabla[v] = lista1
                res.tablad[v] = lista2
                for p in lista1+lista2:
                    trabajo.eliminar(p)
                    for w in p.getvars():
                        if w in res.tablat:
                            res.tablat[w].append(p)
                        else:
                            res.tablat[w] = [p]
            return res 

        def level(self,p):
            print(self.posvar)
            print(p.listavar)
            return min([self.posvar[x] for x in p.getvars()])

        
        def levelc(self,cl):
            return min([self.posvar[abs(x)] for x in cl])
        
        def back(self):
            
            vars = self.orden.copy()
            level=len(vars)-1
            config = []
            while level>0:
                oldl = level
                print(level,len(config) , level+len(config), config)
                var = self.orden[level]
                list1 = []
                list2 = []
                lista = self.get(var) + self.getd(var) + self.getm(var)
                margi = False
                for p in lista:
                    t = p.reduce(config)
                    if t.contradict():
                        nueva = p.borra([var])
                        self.insertarb(nueva)
                        level = self.level(nueva)
                        del config[-(level-oldl):]
                        margi = True
                        break   
                    elif not t.tabla[0]:
                        list1.append(p)
                    elif not t.tabla[1]:
                        list2.append(p)
                if margi:
                    continue
                
                if not list2:
                    config.append(var)
                    level+=-1
                    continue
                if not list1:
                    config.append(-var)
                    level+=-1
                    continue

                n1 = min(list1, key = lambda x: len(x.getvars()))

                n2 = min(list2, key = lambda x: len(set(x.getvars()).union(set(n1.getvars()))))

                nueva = n1.combina(n2, inplace = False)
                nueva.borra([var], inplace=True)
                self.insertarb(nueva)
                level = self.level(nueva)
                del config[-(level-oldl):]


        def belong(self,p):
            h = p.getvars()
            if not h:
                return False
            v = h[0]
            if v in self.tabla and p in self.tabla[v]:
                return True
            if v in self.tablad and p in self.tablad[v]:
                return True
            return False

                
                    
        def back2(self, Q=15):
            
            vars = self.getvars()
            pos = list(vars)
            orden = []
            n = len(vars)

            level=len(vars)-1
            config = []
            while level>0:
                oldl = level
                (var,apren) = self.siguienteb(config,pos)
                print(level,len(config) , var, config)

                self.posvar[abs(var)]= level
                pos.remove(abs(var))
                orden.append(abs(var))

                if apren:
                        sets= []
                        for nueva in apren:
                            print("aprendo ", nueva.getvars())
                            sets = sets+self.insertback(nueva)
                        if self.contradict:
                            break
                        for h in sets:
                            level = max(level,self.level(h))
                        pos = pos + orden[-(level-oldl)-1:]
                        del orden[-(level-oldl)-1:]
                        del config[-(level-oldl):]
                        
                else:
                    config.append(var)
                    level+=-1
                  


                

                        



                
                    
                
                
        
            

            

         

           

            
            return config 

        def compruebasol(self,config):
            vars = self.getvars()
            for v in vars:
                lista = self.get(v) + self.getd(v)
                for p in lista:
                    h = p.reduce(config,inplace = False)
                    if not h.trivial():
                        print ("error " ,p.getvars())
            

        def trivial(self):
        
            if self.tabla:
                for v in self.tabla:
                    if self.tabla[v]:
                        return False
            if self.tablad:
                for v in self.tablad:
                    if self.tablad[v]:
                        return False
            return True

        def reduce(self,v):
            res = self.copia()
         
            res.orden.remove(abs(v))
            
            lista = res.get(abs(v))+res.getd(abs(v))
            for p in lista:
                res.eliminar(p)
            for p in lista:
                q = p.reduce({v})
               
                res.insertar(q)

             
            return res
            
             
 
        def simplifica(self,p):
            

            res = p

            svar = set(p.getvars())

            n = len(svar)
                            

            lista = []
            lista2 = []

            for v in p.getvars():
                if v in self.tabla:
                    for q in self.tabla[v]:
                        if len(q.getvars()) <n and not q in lista:
                            lista.append(q)
                            if set(q.getvars())<= svar:
                                res = res.combina(q)
                                self.eliminar(q)

            for v in p.getvars():
                if v in self.tablad:
                    for q in self.tablad[v]:
                        if len(q.getvars()) <n and not q in lista and not q in lista2:
                            lista2.append(q)
                            


            

            
               
            for q in lista2:
                if set(q.getvars())<= svar:
                    res = res.combina(q)
                    
            return res

        def simplify(self,p):
            if self.contradict:
                return
            if p.contradict():
                self.anula()
                return []
            

            if p.trivial():
                return []
            
            lp = p.getvars()
            n = len(lp)

            svar = set(lp)
            lista = []
            for v in lp:
                if v in self.tabla: 
                    for q in self.tabla[v]:
                        lq = q.getvars()
                        if len(lq)>=n and q not in lista:
                            lista.append(q)
                if v in self.tablad: 
                    for q in self.tablad[v]:
                        lq = q.getvars()
                        if len(lq)>=n and q not in lista:
                            lista.append(q)
                        

            for q in lista:
                sq = set(q.getvars())
                if  svar<= sq:
                    # print("intento combinar")
                    nq = q.combina(p)
                    # print(nq.tabla.sum(),q.tabla.sum())
                    if not nq.implicadopor(q):
                        if self.belong(q):
                            self.eliminar(q)
                        print("mejoro existen",nq.tabla.sum(),q.tabla.sum(), 2**(len(nq.getvars())))
                        self.insertar(nq)

        def simplificat(self,p):
            if p.trivial():
                return (nodoTabla([]), [])
            
            if p.contradict():
                res = nodoTabla([])
                res.anula()
                return (res, [])

            res = p.copia()

            svar = set(p.getvars())
            
            # ol = sorted(p.getvars(),key = lambda x : self.posvar[x])

            ol = p.getvars()
    
            for v in ol:
                if v in self.tablad:
                    for q in sorted(self.tablad[v], key = lambda x: len(x.getvars())):
                        if set(q.getvars())<= svar:
                            h = q.combina(p,inplace=False)
                            h.borra([v], inplace=True)
                            (h1,l1) = self.simplificat(h)
                            l1.append(q)
                            return (h1,l1)
                      
            res = p.copia()

            lista = []
            for v in p.getvars():
                if v in self.tabla:
                    for q in self.tabla[v]:
                        if q not in lista:
                            lista.append(q)

           
               
            for q in lista:
                if set(q.getvars())<= svar:
                    res.combina(q, inplace = True)
                    
            return (res, [])

        def insertarb(self,p):
            if p.contradict():
                self.anula()
                return []
            

            if p.trivial():
                return []

            i = self.level(p)
            var = self.orden[i]
            svar = set(p.getvars())

            for v in p.getvars():
                if v in self.tablad and not v==var:
                    for q in self.tablad[v]:
                        if set(q.getvars())<= svar:
                            h = q.combina(p,inplace=False)
                            h.borra([v], inplace=True)
                            self.insertarb(h)

            if p.checkdetermi(var):
                    t = p.minimizadep(var, seg = set())
                    # print("nuevo determinismo ", len(p.getvars()), len(t.getvars()))
                    if len(t.getvars())< len(p.getvars()):
                        self.insertarb(t)
                        q = p.borra([var],inplace = False)
                        self.insertarb(q)
                    else:
                        if var in self.tablad:
                            self.tablad[var].append(p)
                        else:
                            self.tablad[var] = [p]

                        for v in p.getvars():
                            if v in self.tablat:
                                self.tablat[v].append(p)
                            else:
                                self.tablat[v] = [p]

                    lista = self.tablat.get(var,[])
                    listn = self.get(var) + self.getd(var)
                    for q in lista:
                        if not q in listn:
                            if svar <= set(q.getvars()):
                                self.eliminarb(q)
                                h = q.combina(p, inplace = False)
                                h.borrar([var], inplace=True)
                                self.insertarb(h)
            else:
                if var in self.tabla:
                    self.tabla[var].append(p)
                else:
                    self.tabla[var] = [p]

                for v in p.getvars():
                    if v in self.tablat:
                        self.tablat[v].append(p)
                    else:
                        self.tablat[v] = [p]   



        def getXor(self):
            lista = self.getpotd()
            res = []
            for p in lista:
                h = p.checkxor()
                if h:
                    res.append(h)
                    # if p.tabla.sum()==2**(len(p.getvars())-1):
                    #     self.eliminar(p)

            return res



        def insertarclau(self,cl):

            if len(cl) <= 10:
                vars = list(map(abs,cl))
                p = nodoTabla(vars)
                p.introduceclaun(cl)
                return self.insertarb2(p)
            
            if not cl:
                self.anula()
                return ([])


         
            svar = set(map(abs,cl))
            lcl = list(cl)
            


            for v in svar:
                if v in self.tablad:
                    for q in self.tablad[v]:
                        if set(q.getvars())<= svar:
                            if q.getvalue(lcl):
                                ncl = cl-{v,-v}
                                return self.insertarclau(ncl)

                if v in self.clau:
                    for d in self.clau[v]:
                        if d <= cl:
                            return []
                        if v in cl:
                            ncl = d-{v}
                            ncl.add(-v)
                            if ncl <= cl:
                                ncl = cl.discard(v)
                                return self.insertarclau(ncl)
                        if -v in cl:
                            ncl = d-{-v}
                            ncl.add(v)
                            if ncl <= cl:
                                ncl = cl.discard(-v)
                                return self.insertarclau(ncl)




            lista = []

        
            for v in svar:
                        if v in self.tablad:
                            for q in self.tablad[v]:
                                if q not in lista:
                                    lista.append(q)
                        if v in self.tabla: 
                            for q in self.tabla[v]:
                                if q not in lista:
                                    lista.append(q)
                
            for q in lista:
                if svar <= set(q.getvars()):
                    q.introduceclaun(cl)    
    
            ins = []  

            res = [map(abs,cl)]                
            for v in svar:
                if v in self.clau:
                    for d in self.clau[v]:
                        if v == min(svar) and cl <= d:
                            self.eliminarc(d)
                        if v in d:
                            ncl = d-{v}
                            ncl.add(-v)
                            if cl <= ncl:
                                ncl.discard(-v)
                                ins.append(ncl)
                                self.eliminarc(d)

                        if -v in d:
                            ncl = d-{-v}
                            ncl.add(v)
                            if cl <= ncl:
                                ncl.discard(v)
                                ins.append(ncl)
                                self.eliminarc(d)
                    
            for d in ins:
                res = res + self.insertarclau(d)

            for v in svar:
                if v in self.clau:
                    self.clau[v].append(cl)
                else:
                    self.clau[v] = [cl]


            return res



                            


                        
                        
                            
            
                            


        def eliminarb(self,p):
            i = self.level(p)
            var = self.orden[i]
            if p in self.get(var):
                self.tabla[var].remove(p)
            if p in self.getd(var):
                self.tablad[var].remove(p)

            for v in p.getvars():
                self.tablat[v].remove(p)

        def checkequal(self,p):
            svar = set(p.getvars())
            n = len(svar)
            lista = []
            for v in p.getvars():
                if v in self.tablad:
                    for q in self.tablad[v]:
                        if len(q.getvars())==n and not q in lista:
                            lista.append(q)
                            
                if v in self.tabla:
                    for q in self.tabla[v]:
                        if len(q.getvars())==n  and not q in lista:
                            lista.append(q)
                            
            for q in lista:
                    if set(q.getvars()) == svar:
                        if p.implicadopor(q):
                            return None
                        else:
                            self.eliminar(q)
                            return p.combina(q)
            return p
        
        def checkequalv(self,svar):
            
            n = len(svar)
            lista = []
            for v in svar:
                if v in self.tablad:
                    for q in self.tablad[v]:
                        if len(q.getvars())==n and not q in lista:
                            lista.append(q)
                            
                if v in self.tabla:
                    for q in self.tabla[v]:
                        if len(q.getvars())==n  and not q in lista:
                            lista.append(q)
                            
            for q in lista:
                    if set(q.getvars()) == svar:
                        return set()
                    
            return svar
        
        def recomputeorder(self):
            orden = []
            total = set()
            lista = self.getpotl(self.getvars())
            dvar = dict()
            dvard = dict()

            for p in lista:
                con = set(p.listavar)
                total.update(con)
                for v in con:
                    if p in self.tablad.get(v,set()):
                        if v in dvard:
                            dvard[v].append(con)
                        else:
                            dvard[v] = [con]
                    else:
                        if v in dvar:
                            dvar[v].append(con)
                        else:
                            dvar[v] = [con]
                        
            n = len(total)
    
            i= 0
  
            value = dict()
            
            update(value,dvar,dvard,total)

            
            i = 0
            while total:
                nnode = min(value, key = value.get )
                orden.append(nnode)
                res = updateclus(nnode,dvar,dvard)
                update(value,dvar,dvard,res)
                
                
                del value[nnode]
                del dvar[nnode]
                total.discard(nnode)
            
            self.orden = orden      

        def recomputeorderb(self,var):
            
            orden = []
            total = set()
            lista = self.getpotl(self.getvars())
            dvar = dict()
            dvard = dict()
            last = set()

            for p in lista:
                con = set(p.listavar)
                total.update(con)
                for v in con:
                    if p in self.tablad.get(v,set()):
                        if v in dvard:
                            dvard[v].append(con)
                        else:
                            dvard[v] = [con]
                    else:
                        if v in dvar:
                            dvar[v].append(con)
                        else:
                            dvar[v] = [con]

            lista = self.getpotl([vars])
            for p in lista:
                last.update(p.getvars())
                        
            
            n = len(total)
    
            i= 0
  
            value = dict()
            
            total = total-last

            update(value,dvar,dvard,total)

            
            i = 0
            while total:
                nnode = min(value, key = value.get )
                orden.append(nnode)
                res = updateclus(nnode,dvar,dvard)
                update(value,dvar,dvard,res)
                
                
                del value[nnode]
                del dvar[nnode]
                total.discard(nnode)
            total = last
            update(value,dvar,dvard,total)
            while total:
                nnode = min(value, key = value.get )
                orden.append(nnode)
                res = updateclus(nnode,dvar,dvard)
                update(value,dvar,dvard,res)
                
                
                del value[nnode]
                del dvar[nnode]
                total.discard(nnode)

            
            self.orden = orden                             
                      
        def sim(self,p,K=0):
            svar = set(p.getvars())
            orvar = sorted(p.getvars(),key = lambda x: self.orden.index(x))
            n = len(svar)
            for v in orvar:
                if v in self.tablad:
                    for q in self.tablad[v]:
                        if len(q.getvars())<n and  set(q.getvars()) <= svar:
                            p = p.combina(q)
                            p = p.borra([v])
                            p = self.checkequal(p)
                            if not p:
                                return []
                            return self.sim(p)
                            
            if K>0:
                for v in orvar:
                    if v in self.tablad:
                        for q in self.tablad[v]:
                            if len(q.getvars())<n+K and   len(svar - set(q.getvars()))<=K:
                                sse= self.simv(svar.union(set(q.getvars()))     - {v})
                                if len(sse)<n:
                                    # print("reduccion 1 paso")
                                    # sleep(1)
                                    p = p.combina(q)
                                    p = p.borra([v])
                                    p = self.checkequal(p)
                                    if not p:
                                        return p
                                    return self.sim(p)


                                    
            
            return p
        
        def simv(self,svar):
                
            svar = self.checkequalv(svar)
            if not svar:
                return svar
            orvar = sorted(svar,key = lambda x: self.orden.index(x))
            n = len(svar)
            for v in orvar:
                if v in self.tablad:
                    for q in self.tablad[v]:
                        if len(q.getvars())<n and  set(q.getvars()) <= svar:
                            nvar = svar - {v}
                            nvar = self.checkequalv(nvar)
                            if not nvar:
                                return nvar
                            return self.simv(nvar)
                            
                                
            
            return svar

        def insertmix(self,p, Q=25):
            
            
            svar = set(p.getvars())
            orvar = sorted(p.getvars(),key = lambda x: self.orden.index(x))
            n = len(svar)
            for v in orvar:
                if v in self.tablad:
                    for q in self.tablad[v]:
                        if len(q.getvars())<n and  set(q.getvars()) <= svar:
                            p = p.simplifyd(q,v)
                            
            svar = set(p.getvars())
            n = len(svar)
            if n<=Q:
                h = p.toTable()
                return self.insertar(h)
            
            for v in svar:
                if v in self.tablam:
                            self.tablam[v].append(p)
                else:
                            self.tablam[v] = [p]

            return []


        def insertars(self,p):
            
               
        

            for v in p.getvars():
                if v in self.tabla:
                            self.tabla[v].append(p)
                else:
                            self.tabla[v] = [p]


                

        def insertar(self,p, s=True):

            # print("entro insertar", p.listavar)
     
            if self.contradict:
                return []
            
           

            svar = set(p.getvars())
            
            n = len(svar)


            
            

            if p.trivial():
                return []
            
            if isinstance(p,mix):
                return self.insertmix(p)
            op = p
            p = self.checkequal(p)
            if not p:
                return []
            if s and op==p:
                p = self.simplifica(p)
            p = self.sim(p)
            if not p:
                return []
               
            svar = set(p.getvars())


            n = len(svar)




            
            if p.contradict():
                self.anula()
                return []

            
            
            
                 

            
            dets = []
            for v in p.getvars():
                
                if p.checkdetermi(v):
                    t = p.minimizadep(v, seg = set())
                    if len(t.getvars())< len(p.getvars()):
                        l1 = self.insertar(t)
                        q = p.borra([v],inplace = False)
                        l2 = self.insertar(q)
                        return l1 + l2
                        
                
                    dets.append(v)
    

            


            

            lista = []


            for v in p.getvars():
                if v in self.tablad:
                    for q in self.tablad[v]:
                        if len(q.getvars())>= n and q not in lista:
                            lista.append(q)
                if v in self.tabla:
                    for q in self.tabla[v]:
                        if  len(q.getvars())>= n and q not in lista:
                            lista.append(q)
            incl = False
            ins = []
            nd = []
            for q in lista:
                if svar <= set(q.getvars()):
                    r = q.combina(p)
                    if dets:
                        # print("obrrao ",vard, q.getvars())
                        var = min(dets,key = lambda x: self.orden.index(x) )
                        r.borra([var],inplace = True)
                        # print("añado ", vard, r.getvars())
                        self.eliminar(q)
                        ins.append(r)
                        test = False
                    else:
                        incl= True
                        test = True
                    if test:
                        if not r.implicadopor(q):
                            self.eliminar(q)
                            ins.append(r)
                        elif len(q.getvars())==len(p.getvars()):
                            print("Caso imposible")
                            return []
            for q in ins:
                nd = nd + self.insertar(q)
             
                        
            if dets:
                
                nd.append(p)
                lista = []
                for v in p.getvars():
                    if v in self.tablam:
                        for q in self.tablam[v]:
                            if len(q.getvars())>= n and q not in lista:
                                lista.append(q)
                for q in lista:
                    self.eliminar(q)
                    h= q.simplifyd(p, min(dets,key = lambda x: self.orden.index(x) ))
                    self.insertar(h)



                for v in p.getvars():
                    if not v in dets:
                        if v in self.tabla:
                            self.tabla[v].append(p)
                        else:
                            self.tabla[v] = [p]
                    else:
                        if v in self.tablad:
                            self.tablad[v].append(p)
                        else:
                            self.tablad[v] = [p]
            elif not incl:
                

                for v in svar:
                    if v in self.tabla:
                            self.tabla[v].append(p)
                    else:
                            self.tabla[v] = [p]

            
            
       
            return nd


                

        def insertback(self,p):

            # print("entro insertar", p.listavar)
     
            if self.contradict:
                return []
            
           

            svar = set(p.getvars())
            
            n = len(svar)


            
            

            if p.trivial():
                return []
            
            if isinstance(p,mix):
                return self.insertmix(p)
            op = p
            p = self.checkequal(p)
            if not p:
                return []
            if op==p:
                p = self.simplifica(p)
            p = self.sim(p)
            if not p:
                return []
               
            svar = set(p.getvars())


            n = len(svar)




            
            if p.contradict():
                self.anula()
                return []

            
            
            
                 

            
            dets = []
            for v in p.getvars():
                
                if p.checkdetermi(v):
                    t = p.minimizadep(v, seg = set())
                    # print("nuevo determinismo ", len(p.getvars()), len(t.getvars()))
                    if len(t.getvars())< len(p.getvars()):
                        l1 = self.insertback(t)
                        q = p.borra([v],inplace = False)
                        l2 = self.insertback(q)
                        return l1 + l2
                        
                
                    dets.append(v)
    

            


            

            lista = []


            for v in p.getvars():
                if v in self.tablad:
                    for q in self.tablad[v]:
                        if len(q.getvars())>= n and q not in lista:
                            lista.append(q)
                if v in self.tabla:
                    for q in self.tabla[v]:
                        if  len(q.getvars())>= n and q not in lista:
                            lista.append(q)
            incl = False
            ins = []
            nd = [p.getvars()]
            for q in lista:
                if svar <= set(q.getvars()):
                    r = q.combina(p)
                    if dets:
                        # print("obrrao ",vard, q.getvars())
                        var = min(dets,key = lambda x: self.orden.index(x) )
                        r.borra([var],inplace = True)
                        # print("añado ", vard, r.getvars())
                        self.eliminar(q)
                        ins.append(r)
                        test = False
                    else:
                        incl= True
                        test = True
                    if test:
                        if not r.implicadopor(q):
                            self.eliminar(q)
                            ins.append(r)
                        elif len(q.getvars())==len(p.getvars()):
                            print("Caso imposible")
                            return []
            for q in ins:
                nd = nd + self.insertar(q)
             
                        
            if dets:
                
                lista = []
                for v in p.getvars():
                    if v in self.tablam:
                        for q in self.tablam[v]:
                            if len(q.getvars())>= n and q not in lista:
                                lista.append(q)
                for q in lista:
                    self.eliminar(q)
                    h= q.simplifyd(p, min(dets,key = lambda x: self.orden.index(x) ))
                    self.insertar(h)



                for v in p.getvars():
                    if not v in dets:
                        if v in self.tabla:
                            self.tabla[v].append(p)
                        else:
                            self.tabla[v] = [p]
                    else:
                        if v in self.tablad:
                            self.tablad[v].append(p)
                        else:
                            self.tablad[v] = [p]
            else:
                

                for v in svar:
                    if v in self.tabla:
                            self.tabla[v].append(p)
                    else:
                            self.tabla[v] = [p]

            
            
            # print("salgo insertar", p.listavar)
       
            return nd




 
        def eliminarc(self,cl):
            lvar = map(abs,cl)
            for v in lvar:
                    self.clau[v].remove(cl)
                





        def eliminar(self,p):
            if isinstance(p,mix):
                for v in p.getvars():
                    self.tablam[v].remove(p)
                return
            for v in p.getvars():
                if v in self.tabla and p in self.tabla[v]:
                    self.tabla[v].remove(p)
                else:
                    self.tablad[v].remove(p)

        






        

        def createfromlista(self,l):
            for p in l:
                self.insertar(p)


 
        def siguiente(self):

            if self.unit:
                x = self.unit.pop()
                self.unit.add(x)
                return abs(x)
            miv = min(self.tabla,key = lambda x: len(self.tabla.get(x)))
            mav = max(self.tabla,key = lambda x: len(self.tabla.get(x)))

            # print(miv,mav,len(self.tabla.get(miv)),len(self.tabla.get(mav)))

            if len(self.tabla.get(miv)) == 1:
                return (miv)
                


            miv = min(self.tabla,key = lambda x: tam(self.tabla.get(x)))
            mav = max(self.tabla,key = lambda x: tam(self.tabla.get(x)))
            # print (miv,mav,tam(self.tabla.get(miv)),tam(self.tabla.get(mav)))
            return miv



        def getmax(self, proh = set()):
            pos = set(self.getvars())-proh

            bue = dict()

            for x in pos:
                bue[x] = 0.0
            
            for v in self.getvars():
                if v in self.tablad:
                    for p in self.tablad[v]:
                        n = len(p.getvars())
                        for y in p.getvars():
                            bue[y] += 1/n

                
            return  max(bue,key = bue.get )
                


     



        def marginaliza(self,var,M = 30, Q=20):
            lista = []
            
            if self.contradict:
                    print("contradiction ")

                    return (True,lista,[])
            if var in  self.unit:
                    self.unit.discard(var)
                    return (True,lista,[u.potdev(var)])
            elif -var in self.unit:
                    self.unit.discard(-var) 

                    return (True,lista,[u.potdev(-var)])

               
            
            

            (exact,lista,listaconvar) = u.marginaliza(self.get(var).copy(),var,self.partir,M,Q) #EEDM

            
            if exact and lista and not lista[0].getvars():
                if lista[0].contradict():
                    print ("contradict")
                    self.anula()    
                    return(True,lista,listaconvar)
            for p in lista:
                if p.contradict():
                    print ("contradict")

                    self.anula()
                else:
                    # print(p.getvars())
                    self.insertar(p)     

            self.borrarv(var)

                        
            return (exact,lista,listaconvar)


        def marginalizae(self,var,M = 20):
            lista = []
            
            if self.contradict:

                    return (True,lista,[])
            if var in  self.unit:
                    self.unit.discard(var)
                    return (True,lista,[u.potdev(var)])
            elif -var in self.unit:
                    self.unit.discard(-var) 

                    return (True,lista,[u.potdev(-var)])

               

           

            (exact,lista,listaconvar,unit) = u.marginalizas(self.get(var).copy(),var,self.partir,M) #EEDM
            if 0 in unit:
                self.anula()
                return (True,lista,listaconvar)
            
            if exact and lista and not lista[0].getvars():
                if lista[0].contradict():
                    self.anula()    
                    return(True,lista,listaconvar)
            if exact:
                for p in lista:
                    self.insertar(p)     

                self.borrarv(var)

                        
            return (exact,lista,listaconvar)

        def progresa(self):
            for v in self.orden:
                if v in self.tablad:
                    ins = []
                    bor = []
                 
                    for p in self.tablad[v]:
                        if v in self.tabla:
                            for q in self.tabla[v]:
                                dif = set(p.getvars())-set(q.getvars())
                                if len(dif)==1:
                                    z = dif.pop()
                                    if self.varpos[v] < self.varpos[z]:
                                        bor.append(q)
                                        r = p.combina(q,inplace = False)
                                        r.borra([v], inplace = True)
                                        ins.append(r)
                        
                    for p in bor:
                        self.eliminar(p)
                    
                    
                    for q in ins:
                        self.insertar(q)

        def esta(self,p):
            if not p.getvars():
                if p.trivial():
                    return False
                if p.contradict() and self.contradict:
                    return True
                else:
                    return False
            v = p.getvars()[0]
            if v in self.tabla and p in self.tabla[v]:
                return True
            if v in self.tablad and p in self.tablad[v]:
                return True
            return False

        def estad(self,p):
            if not p.getvars():
                if p.trivial():
                    return False
                if p.contradict() and self.contradict:
                    return True
                else:
                    return False
            
            for v in p.getvars():

                if  p in self.tablad.get(v,[]):
                    
                    return True
            return False

        def pos(self,p):
            return min([self.posvar[x] for x in p.getvars()])
  
 
        def marginalizaset(self,vars, Q = 4, M=15, verb = False):

            small = varpot()
            small = self.copia()
            nde = True
            porins = []
            i=0
            solved = False
            sol = varpot()

            remo = set()

            HT = 40
    
            while not solved and Q<3:
                orden = []
                clusters = []
                posvar  = dict()
                solved = True
                trabajo = self.copia()
        
                HT+=1
                
            
                vorig = vars.copy()
                

                if nde:
                    Q+=1
                else:
                    Q+=1
                if (Q>31):
                    Q= 29

                print("Q = ",Q)
                pd = 0
                pnd = 0
                ex = 0
                nex = 0
                cset = set()

                porins= []

                elimi = True

                while vorig and not trabajo.contradict:
                   
                    var = trabajo.siguientepref(vorig,small)
                    lset = cset.union(self.getvarsd(var))
                    clusters.append(lset-cset)
                    cset = lset
                    
                    
                    
                    if verb:
                        print("var", var, "quedan ", len(vorig))
                    

                    list1 = trabajo.get(var)
                    list2 = trabajo.getd(var)

                    x1 = trabajo.tadref(var,small,vorig)
                    x2 = trabajo.tad(var)

                    if verb:
                        print(x1,x2)
                        print(len(list1), len(list2))


                   
                    orden.append(var)
                    posvar[var] = len(orden)-1
                        
                        
                    if min(x1,x2)> Q:
                        if verb:
                            print("No exacto")
                            elimi = False
                        if solved:
                            rem = len(vorig)
                            first = var
                            clus = trabajo.getvarsd(var)
                        solved = False
                        nex += 1
                    else:
                        ex +=1
                    


                

                    

                    # for p in list1:
                    #     print("lista 1", p.getvars())
                    # for p in list2:
                    #     print("lista 2", p.getvars())    
                  

                    for p in list1:
                        # print(p.getvars())
                        trabajo.eliminar(p)
                    for p in list2:
                        # print(p.getvars())

                        trabajo.eliminar(p)
                    n = len(list1) + len(list2)
                    nd = []
                    traba = []
                    nuevas = []
                    if  x1 < x2:
                        if verb:
                            print("incluir ")
                        lists = small.tablad.get(var,[])
                        lists2 = list(filter(lambda x: set(x.getvars()) <= set(vorig), lists))
                        if lists2:
                            if verb:
                                print("heredo determinismo", len(list1))
                           
                            p = min(lists2, key = lambda x: len(x.getvars()))
                            list2.append(p)
                            # if solved:
                            #     print("inserto p ", p.getvars())
                            #     self.insertar(p, vc = var)
                                # sleep(3)
                               
                        



                    vorig.discard(var)

                    if list2:
                        det = True
                        if Q>=7 and elimi:
                            hr = list2[0]
                            sol.insertar(hr)
                            sol.orden.append(var)
                        
                        if verb:
                            print("determinista")
                        pd+=1
                        pivote = min(list2, key = lambda x: len(x.getvars()))
                        if n<=1:
                            h = pivote.borra([var], inplace = False)
                            (h,l1) = trabajo.simplificat(h)
                            (h,l1) = small.simplificat(h)
                            nd = nd + trabajo.insertar(h,small)
                            nuevas.append(h)
                            for r in l1:
                                nd = nd + trabajo.insertar(h,small)
                                # if solved:
                                #     self.insertar(r)
                    
                        else:
                            for p in list1:
                                

                                pivote = min(list2, key=lambda x: len(set(p.getvars()).union(set(x.getvars()))))
                                if len(set(p.getvars()).union(set(pivote.getvars())))<= Q:
                                    h = pivote.combina(p, inplace = False)
                                    h.borra([var], inplace =True)
                                    (h,l1) = trabajo.simplificat(h)
                                    (h,l1) = small.simplificat(h)
                                    nd = nd + trabajo.insertar(h,small)
                                    nuevas.append(h)
                                    for r in l1:
                                        nd = nd + trabajo.insertar(r,small)
                                        # if solved:
                                        #     self.insertar(r)



                                else:
                                    traba.append(p)
                            while len(list2) > 1:
                                list2.sort(key = lambda x :  len(x.getvars()) )
                                p = list2.pop()
                                pivote =  min(list2, key=lambda x: len(set(p.getvars()).union(set(x.getvars()))))
                                
                                if len(set(p.getvars()).union(set(pivote.getvars())))<= Q:
                                    h = pivote.combina(p, inplace = False)
                                    h.borra([var], inplace =True)
                                    (h,l1) = trabajo.simplificat(h)
                                    (h,l1) = small.simplificat(h)
                                    nd = nd+  trabajo.insertar(h,small)
                                    nuevas.append(h)
                                    for r in l1:
                                        nd = nd + trabajo.insertar(r,small)
                                        # if solved:
                                        #     self.insertar(r)


                                else:
                                    traba.append(p)
                                    solved = False
                            
                            if traba:
                    

                                for p in traba:
                                    
                                    h = p.borra([var], inplace=False)
                                    (h,l1) = trabajo.simplificat(h)
                                    (h,l1) = small.simplificat(h)
                                    # print(len(h.getvars()),len(l1))
                                    # sleep(1)
                                    nd = nd+  trabajo.insertar(h,small)
                                    nuevas.append(h)
                                    for r in l1:
                                        nd = nd + trabajo.insertar(r,small)
                                        # if solved:
                                        #     self.insertar(r)

                        

                        


                    else:
                        if verb:
                            print("no determinista")
                        # if elimi:
                        #     orden.append(var)
                        #     posvar[var] = len(orden)-1
                        elimi = False
                        pnd+=1
                        h = nodoTabla([])
                        ordena(list1,Q)
                        if list1:
                            for q in list1:
                                # r = q.descomponev(var)
                                # if len(r) == 2:
                                #     q = r[0]
                                #     qn = r[1]
                                
                                #     trabajo.insertar(qn)
                                if len(set(h.getvars()).union(set(q.getvars())))<= Q or not h.getvars():
                                    h.combina(q,inplace=True)
                                else:
                                    h.borra([var],inplace=True)

                                    nd = nd+  trabajo.insertar(h,small)
                                    nuevas.append(h)
                                    h = nodoTabla([])
                                    h.combina(q,inplace=True)

                            h.borra([var], inplace=True)
                            # print(len(h.getvars()))
                            (h,l1) = trabajo.simplificat(h)
                            (h,l1) = small.simplificat(h)
                            # print(len(h.getvars()),len(l1))
                            # sleep(1)
                            nd = nd+  trabajo.insertar(h, small)
                            nuevas.append(h)
                            for r in l1:
                                nd = nd + trabajo.insertar(r,small)
                                # if solved:
                                #     self.insertar(r)

                    for p in nd:
                        porins = porins + small.insertar(p)
                        if len(p.getvars())<=2:
                            self.insertar(p)
        

                    for p in nuevas:
                        if not p in nd and len(p.getvars())<=M:
                            porins = porins +small.insertar(p, small)


                if porins:
                    nde=True
                else:
                    nde=False
                    

                    

                self.orden = orden
                self.posvar = posvar
                small.orden = orden
                small.posvar = posvar
                rorden = []
                for l in clusters:
                    rorden = list(l)  + rorden

              





                print("Q = ", Q, "quedan ", rem)

                print("e = ", ex," ne = ", nex)


                print("d = ", pd," nd = ", pnd)
                    
                if (Q>5):
                    sleep(3)
                i+=1

                trabajo = self.copia()
                vorig = vars.copy()


                self.mini(vorig,small, min(Q,10), trabajo,  verb=verb, H=HT)

               

                # trabajo = self.copia()
                # vorig = vars.copy()


                # self.mini(vorig,small, min(Q,10), trabajo, gorden = rorden, H=HT,verb = verb)



            traba = small.calculab()
              
            config = traba.back()    

            print("resuelto ", config)


            solved = False


            Q = 32


















    

            while not solved:
                orden = []
                clusters = []
                posvar  = dict()
                solved = True
                trabajo = self.copia()
                

                # for v in vars:
                #     if v in small.tablad and small.tablad[v]:
                #         for p in small.tablad[v]:
                #             if len(p.getvars())<=20:
                #                 trabajo.insertar(p)

                # for v in vars:
                #     if not v in trabajo.tablad or not trabajo.tablad[v]:
                #         if v in small.tablad and small.tablad[v]:
                #             p = min(small.tablad[v], key = lambda x: len(x.getvars()))
                #             trabajo.insertar(p)
            
                vorig = vars.copy()
                Q+= 0.5 

                # if nde:
                #     Q+=-1
                # else:
                #     Q+=1
                # if (Q>31):
                #     Q= 29

                print("Q = ",Q)
                nde = False
               

                while vorig and not trabajo.contradict:
            
                    if len(vorig)>Q:
                        var = trabajo.siguientep(vorig)
                    else:
                        var = choice(list(vorig))
                    print("var", var, "quedan ", len(vorig))
                    orden.append(var)
                    posvar[var] = len(orden)-1

                    if trabajo.tad(var)> Q:
                        print("No exacto", trabajo.tad(var))
                    

                    vorig.discard(var)

                    list1 = trabajo.get(var)
                    list2 = trabajo.getd(var)

                    # for p in list1:
                    #     print("lista 1", p.getvars())
                    # for p in list2:
                    #     print("lista 2", p.getvars())    

                    for p in list1:
                        # print(p.getvars())
                        trabajo.eliminar(p)
                    for p in list2:
                        # print(p.getvars())

                        trabajo.eliminar(p)

                    if not list2 and len(list1)>3:
                            lists = small.tablad.get(var,[])
                            lists2 = list(filter(lambda x: set(x.getvars()) <= set(vorig), lists))
                            if lists2:
                                print("heredo determinismo", len(list1))
                                p = min(lists2, key = lambda x: len(x.getvars()))
                                list2.append(p)
                            


                    n = len(list1) + len(list2)
                    nd = []
                    traba = []
                    nuevas = []
                    if list2:
                        det = True
                        print("determinista")
                        pivote = min(list2, key = lambda x: len(x.getvars()))
                        if n<=1:
                            h = pivote.borra([var], inplace = False)
                            h = small.simplifica(h)
                            nd = nd + trabajo.insertar(h,small)
                            nuevas.append(h)
                    
                        else:
                            for p in list1:
                                

                                pivote = min(list2, key=lambda x: len(set(p.getvars()).union(set(x.getvars()))))
                                if len(set(p.getvars()).union(set(pivote.getvars())))<= Q:
                                    h = pivote.combina(p, inplace = False)
                                    h.borra([var], inplace =True)
                                    h = small.simplifica(h)
                                    nd = nd + trabajo.insertar(h,small)
                                    nuevas.append(h)


                                else:
                                    solved = False
                                    traba.append(p)
                            while len(list2) > 1:
                                list2.sort(key = lambda x :  len(x.getvars()) )
                                p = list2.pop()
                                pivote =  min(list2, key=lambda x: len(set(p.getvars()).union(set(x.getvars()))))
                                
                                if len(set(p.getvars()).union(set(pivote.getvars())))<= Q:
                                    h = pivote.combina(p, inplace = False)
                                    h.borra([var], inplace =True)
                                    h = small.simplifica(h)
                                    nd = nd+  trabajo.insertar(h,small)
                                    nuevas.append(h)

                                else:
                                    traba.append(p)
                                    solved = False
                            
                            if traba:
                        

                                for p in traba:
                                    h = p.borra([var], inplace=False)
                                    h = small.simplifica(h)
                                    nd = nd+  trabajo.insertar(h,small)
                                    nuevas.append(h)
                        

                            


                    else:
                        print("no determinista")

                        h = nodoTabla([])
                        ordena(list1,Q)
                        if list1:
                            for q in list1:
                                # r = q.descomponev(var)
                                # if len(r) == 2:
                                #     q = r[0]
                                #     qn = r[1]
                                
                                #     trabajo.insertar(qn)
                                if len(set(h.getvars()).union(set(q.getvars())))<= Q or not h.getvars():
                                    h.combina(q,inplace=True)
                                else:
                                    h.borra([var],inplace=True)

                                    nd = nd+  trabajo.insertar(h,small)
                                    nuevas.append(h)
                                    h = nodoTabla([])
                                    h.combina(q,inplace=True)
                                    solved = False

                            h.borra([var], inplace=True)
                            h = small.simplifica(h)
                            nd = nd+  trabajo.insertar(h, small)
                            nuevas.append(h)
                    h = []
                    for p in nd:
                        h = h + small.insertar(p)
                    if h:
                        nde = True

                    for p in nuevas:
                        if not p in nd and len(p.getvars())<=M:
                            small.insertar(p, small)

                    

                self.orden = orden
                self.posvar = posvar
                small.orden = orden
                small.posvar = posvar
                # small.progresa()
        
                    



                

                    
                

                
            
        


        
        def extraelista(self):
            lista = []
            for v in self.tabla:
                for p in self.tabla[v]:
                    if min(p.getvars()) == v:
                        lista.append(p)
            return lista

    
        def tadm(self,v):
            mat = 0
            if v in self.tablad and self.tablad[v]:
                # print(self.tablad[v])
                p = min (self.tablad[v], key = lambda x: len(x.getvars()))
                for q in self.tablad[v]:
                    if not q==p:
                        mat += 2**(len(set(p.getvars()).union(q.getvars()))-1) - 2**(len(q.getvars()))
                if v in self.tabla:
                    for q in self.tabla[v]:
                            mat += 2**(len(set(p.getvars()).union(q.getvars()))-1) - 2**(len(q.getvars()))
                return mat

            sset = set()
            if v in self.tabla:
                for q in self.tabla[v]:
                    sset.update(set(q.getvars()))
                    mat += - 2**(len(q.getvars()))
            if v in self.tablad:
                for q in self.tablad[v]:
                    sset.update(set(q.getvars()))
                    mat += - 2**(len(q.getvars()))

            return (mat + 2**(len(sset)-2))

                    
                        
        
  
        def tadref(self,v, small, rest):
            mat = 0
            lista = self.getd(v)
            
            lista2 = list(filter(lambda x: set(x.getvars()) <=rest, small.tablad.get(v,[])))

            if lista2:
                p = min(lista2, key = lambda x: len(x.getvars()))
                lista.append(p)
            if lista:
                # print(self.tablad[v])
                p = min (lista, key = lambda x: len(x.getvars()))
                for q in lista:
                    if len(set(p.getvars()).union(q.getvars()))> mat:
                        mat = len(set(p.getvars()).union(q.getvars()))
                if v in self.tabla:
                    for q in self.tabla[v]:
                        if len(set(p.getvars()).union(q.getvars()))> mat:
                            mat = len(set(p.getvars()).union(q.getvars()))

                return mat

            sset = set()
            if v in self.tabla:
                for q in self.tabla[v]:
                    sset.update(set(q.getvars()))
            if v in self.tablad:
                for q in self.tablad[v]:
                    sset.update(set(q.getvars()))
            return (len(sset))

                    
                       
  
        def tad(self,v):
            mat = 0
            if v in self.tablad and self.tablad[v]:
                # print(self.tablad[v])
                p = min (self.tablad[v], key = lambda x: len(x.getvars()))
                for q in self.tablad[v]:
                    if len(set(p.getvars()).union(q.getvars()))> mat:
                        mat = len(set(p.getvars()).union(q.getvars()))
                if v in self.tabla:
                    for q in self.tabla[v]:
                        if len(set(p.getvars()).union(q.getvars()))> mat:
                            mat = len(set(p.getvars()).union(q.getvars()))
                return mat

            sset = set()
            if v in self.tabla:
                for q in self.tabla[v]:
                    sset.update(set(q.getvars()))
            if v in self.tablad:
                for q in self.tablad[v]:
                    sset.update(set(q.getvars()))

            return (len(sset))

                    
                        

 
        def siguientep(self,pos):

            posc= pos

            det = []
            for x in pos:
                x1 = len(self.tabla.get(x)) if self.tabla.get(x) else 0
                x2 = len(self.tablad.get(x)) if self.tablad.get(x) else 0
                if x1+x2 <= 1:
                    return x
                # if x2>0:
                #     det.append(x)
                
            # if det:
            
                
            #     return min(det, key = lambda x: self.tadm(x))

            # else:

            miv = min(posc,key = lambda x: self.tadm(x))
            return miv
            posc.discard(miv)

            if not posc:
                return miv
            miv2 = min(posc,key = lambda x: self.tad(x))

            return choice([miv,miv2])

            # print(miv,mav,len(self.tabla.get(miv)),len(self.tabla.get(mav)))

        def siguientepref(self,pos,small):

            for x in pos:
                x1 = len(self.tabla.get(x)) if self.tabla.get(x) else 0
                x2 = len(self.tablad.get(x)) if self.tablad.get(x) else 0
                if x1+x2 <= 1:
                    return x

            miv = min(pos,key = lambda x: min(self.tadref(x,small,pos), self.tad(x)))
            return miv   

        def get(self,i, deep=True):
            if deep:
                return self.tabla.get(i,[]).copy()
            else:
                return self.tabla.get(i,[])

        def getd(self,i, deep=True):
            if deep:
                return self.tablad.get(i,[]).copy()
            else:
                return self.tablad.get(i,[])
            
        def getm(self,i, deep=True):
            if deep:
                return self.tablam.get(i,[]).copy()
            else:
                return self.tablam.get(i,[])


        def mini(self,vorig,small, Q, trabajo, gorden=[], verb=True, M=3, H=40):
            
            clusters = []
            posvar  = dict()
            solved = True
            
            orden = []
            horden = gorden.copy()
            horden.reverse()
            cset = set()
            pd = 0
            pnd = 0

            while vorig and not trabajo.contradict:
                
                if len(vorig)>H:
                    QV = Q
                else:
                    QV = 31

                if gorden:
                    var = horden.pop()
                else:
                    var = trabajo.siguientepref(vorig,small)
                lset = cset.union(self.getvarsd(var))
                clusters.append(lset-cset)
                cset = lset
                
                if verb:
                    print("var", var, "quedan ", len(vorig))
                orden.append(var)
                posvar[var] = len(orden)-1

                list1 = trabajo.get(var)
                list2 = trabajo.getd(var)

                x1 = trabajo.tadref(var,small,vorig)
                x2 = trabajo.tad(var)

                if verb:
                    print(x1,x2)
                    print(len(list1), len(list2))

                
                


            

                

                for p in list1:
                    trabajo.eliminar(p)
                for p in list2:
                    trabajo.eliminar(p)

                n = len(list1) + len(list2)
                nd = []
                traba = []
                nuevas = []
                if  x1 < x2:
                    if verb:
                        print("incluir ")
                    lists = small.tablad.get(var,[])
                    lists2 = list(filter(lambda x: set(x.getvars()) <= set(vorig), lists))
                    if lists2:
                        if verb:
                            print("heredo determinismo", len(list1))
                        
                        p = min(lists2, key = lambda x: len(x.getvars()))
                        list2.append(p)
                       

                vorig.discard(var)

                if list2:
                    det = True
                    if verb:
                        print("determinista")
                    pd+=1
                    pivote = min(list2, key = lambda x: len(x.getvars()))
                    if n<=1:
                        h = pivote.borra([var], inplace = False)
                        (h,l1) = trabajo.simplificat(h)
                        (h,l1) = small.simplificat(h)
                        nd = nd + trabajo.insertar(h,small)
                        nuevas.append(h)
                        for r in l1:
                            nd = nd + trabajo.insertar(h,small)
                          
                
                    else:
                        for p in list1:
                            

                            pivote = min(list2, key=lambda x: len(set(p.getvars()).union(set(x.getvars()))))
                            if len(set(p.getvars()).union(set(pivote.getvars())))<= QV:
                                h = pivote.combina(p, inplace = False)
                                h.borra([var], inplace =True)
                                (h,l1) = trabajo.simplificat(h)
                                (h,l1) = small.simplificat(h)
                                nd = nd + trabajo.insertar(h,small)
                                nuevas.append(h)
                                for r in l1:
                                    nd = nd + trabajo.insertar(r,small)
                                    



                            else:
                                traba.append(p)
                        while len(list2) > 1:
                            list2.sort(key = lambda x :  len(x.getvars()) )
                            p = list2.pop()
                            pivote =  min(list2, key=lambda x: len(set(p.getvars()).union(set(x.getvars()))))
                            
                            if len(set(p.getvars()).union(set(pivote.getvars())))<= QV:
                                h = pivote.combina(p, inplace = False)
                                h.borra([var], inplace =True)
                                (h,l1) = trabajo.simplificat(h)
                                (h,l1) = small.simplificat(h)
                                nd = nd+  trabajo.insertar(h,small)
                                nuevas.append(h)
                                for r in l1:
                                    nd = nd + trabajo.insertar(r,small)


                            else:
                                traba.append(p)
                                solved = False
                        
                        if traba:
                

                            for p in traba:
                                
                                h = p.borra([var], inplace=False)
                                (h,l1) = trabajo.simplificat(h)
                                (h,l1) = small.simplificat(h)
                                # print(len(h.getvars()),len(l1))
                                # sleep(1)
                                nd = nd+  trabajo.insertar(h,small)
                                nuevas.append(h)
                                for r in l1:
                                    nd = nd + trabajo.insertar(r,small)
                                    # if solved:
                                    #     self.insertar(r)

                    

                    


                else:
                    if verb:
                        print("no determinista")
                    pnd+=1
                    h = nodoTabla([])
                    ordena(list1,QV)
                    if list1:
                        for q in list1:
                        
                            if len(set(h.getvars()).union(set(q.getvars())))<= QV or not h.getvars():
                                h.combina(q,inplace=True)
                            else:
                                h.borra([var],inplace=True)

                                nd = nd+  trabajo.insertar(h,small)
                                nuevas.append(h)
                                h = nodoTabla([])
                                h.combina(q,inplace=True)

                        h.borra([var], inplace=True)
                        (h,l1) = trabajo.simplificat(h)
                        (h,l1) = small.simplificat(h)
                        nd = nd+  trabajo.insertar(h, small)
                        nuevas.append(h)
                        for r in l1:
                            nd = nd + trabajo.insertar(r,small)
                           

                for p in nd:
                    small.insertar(p)
                    if len(p.getvars())<=2:
                        self.insertar(p)


                for p in nuevas:
                    if not p in nd and len(p.getvars())<=M:
                        small.insertar(p, small)
            return (solved,orden)


        def minid2(self,orden,rever,Q):
            
            for o in (orden,rever):
                vorig = o.copy()
                vorig.reverse()
                trabajo = self.copia()


            



            
                while vorig and not self.contradict: 
                    var = vorig.pop()

                    print(var, len(vorig))


                    


                    list1 = trabajo.get(var)
                    list2 = trabajo.getd(var)


                    for p in list1:
                        trabajo.eliminar(p)
                    for p in list2:
                        trabajo.eliminar(p)



                    n = len(list1) + len(list2)
                    nd = []
                    traba = []
                    nuevas = []
                    
                        



                    if list2:
                    
                        pivote = min(list2, key = lambda x: len(x.getvars()))
                        if n<=1:
                            h = pivote.borra([var], inplace = False)
                            nd = nd + trabajo.insertard(h)
                            nuevas.append(h)
                        
                            
                    
                        else:
                            for p in list1:
                                

                                pivote = min(list2, key=lambda x: len(set(p.getvars()).union(set(x.getvars()))))
                                if len(set(p.getvars()).union(set(pivote.getvars())))<= Q:
                                    h = pivote.combina(p, inplace = False)
                                    h.borra([var], inplace =True)
                                    nd = nd + trabajo.insertar(h)
                                    nuevas.append(h)
                                
                                        



                                else:
                                    traba.append(p)
                            list2.sort(key = lambda x :  len(x.getvars()) )

                            while len(list2) > 1:
                                p = list2.pop()
                                pivote =  min(list2, key=lambda x: len(set(p.getvars()).union(set(x.getvars()))))
                                if len(set(p.getvars()).union(set(pivote.getvars())))<= Q:
                                    h = pivote.combina(p, inplace = False)
                                    h.borra([var], inplace =True)
                                    nd = nd+  trabajo.insertar(h)
                                    nuevas.append(h)
                                

                                else:
                                    traba.append(p)
                            
                            
                            
                            if traba:
                    

                                for p in traba:
                                    
                                    h = p.borra([var], inplace=False)
                                
                                    nd = nd+  trabajo.insertard(h)
                                    nuevas.append(h)
                                

                        

                        


                    else:
                        
                        h = nodoTabla([])
                        combinaincluidas(list1,K=1)
                        if list1:
                            for q in list1:
                            
                                if len(set(h.getvars()).union(set(q.getvars())))<= Q or not h.getvars():
                                    h.combina(q,inplace=True)
                                else:
                                    h.borra([var],inplace=True)

                                    nd = nd+  trabajo.insertard(h)
                                    nuevas.append(h)
                                    h = nodoTabla([])
                                    h.combina(q,inplace=True)

                            h.borra([var], inplace=True)
                            nd = nd+  trabajo.insertar(h)
                            nuevas.append(h)
                            
                            
                    
                    for p in nd:
                            self.insertarb2(p)
                    
                    
                    for p in nuevas:
                            self.insertarb2(p)


           

                
            return 


        def minid(self,Q, ins = True, nue = True):
            
            vorig  = self.orden.copy()

            vorig.reverse()
            orden = []
            
            posvar = dict()
            trabajo = self.copia()

            print("en orden directo")



            while vorig and not self.contradict: 
                # var = trabajo.siguientep(vorig)
                var = vorig.pop()
                orden.append(var)
                posvar[var] = len(orden)-1

                # print(var,len(vorig))


                list1 = trabajo.get(var)
                list2 = trabajo.getd(var)


                for p in list1:
                    trabajo.eliminar(p)
                for p in list2:
                    trabajo.eliminar(p)



                n = len(list1) + len(list2)
                nd = []
                traba = []
                nuevas = []
                
                       
                # vorig.discard(var)


                if list2:
                   
                    pivote = min(list2, key = lambda x: len(x.getvars()))
                    if n<=1:
                        h = pivote.borra([var], inplace = False)
                        nd = nd + trabajo.insertar(h)
                        if trabajo.contradict:
                            return 
                        nuevas.append(h)
                      
                          
                
                    else:
                        for p in list1:
                            

                            pivote = min(list2, key=lambda x: len(set(p.getvars()).union(set(x.getvars()))))
                            if len(set(p.getvars()).union(set(pivote.getvars())))<= Q:
                                h = pivote.combina(p, inplace = False)
                                h.borra([var], inplace =True)
                                nd = nd + trabajo.insertar(h)
                                if trabajo.contradict:
                                    return
                                nuevas.append(h)
                               
                                    



                            else:
                                traba.append(p)
                        list2.sort(key = lambda x :  len(x.getvars()) )

                        while len(list2) > 1:
                            p = list2.pop()
                            pivote =  min(list2, key=lambda x: len(set(p.getvars()).union(set(x.getvars()))))
                            if len(set(p.getvars()).union(set(pivote.getvars())))<= Q:
                                h = pivote.combina(p, inplace = False)
                                h.borra([var], inplace =True)
                                nd = nd+  trabajo.insertar(h)
                                if trabajo.contradict:
                                    return
                                nuevas.append(h)
                              

                            else:
                                traba.append(p)
                                # if len(list2) == 1:
                                #     traba.append(list2[0])

                    
                        
                        
                        
                        if traba:
                

                            for p in traba:
                                
                                h = p.borra([var], inplace=False)
                                if trabajo.contradict:
                                    return
                               
                                nd = nd+  trabajo.insertar(h)
                                nuevas.append(h)
                            

                    

                    


                elif list1:
                    
                    h = nodoTabla([])
                    combinaincluidas(list1,K=1)

                
                    for q in list1:
                            if len(set(h.getvars()).union(set(q.getvars())))<= Q or not h.getvars():
                                h = h.combina(q)
                            else:
                                h.borra([var],inplace=True)

                                nd = nd+  trabajo.insertar(h)
                                if trabajo.contradict:
                                    return 
                                nuevas.append(h)
                                h = nodoTabla([])
                                h.combina(q,inplace=True)

                    h.borra([var], inplace=True)
                    nd = nd+  trabajo.insertar(h)
                    nuevas.append(h)
                    
                           
                if ins:
                    for p in nd:
                        if len(p.getvars())<=15:
                            print("nuevo determinismo" , p.getvars())
                            self.insertar(p)
                
                if nue:
                    i=1
                    for p in nuevas:
                        # print("intento ", p.getvars())
                        if len(p.getvars()) <= 5:
                            self.insertar(p)
                        else:
                            self.simplify(p)

                        # print("salgo")
                        if self.contradict:
                            # print("salgo con contradict")
                            return 


           

                
            return 
        

        def simplifyp(self,t):
            lista = self.getpotl(self.getvars())
            for p in lista:
                cand = []
                n = len(p.getvars())
                svar = set(p.getvars())
                op = p.tabla.sum()
                for v in p.getvars():
                    if v in   t.tabla:
                        for q in t.tabla[v]:
                            if len(q.getvars())<= n and set(q.getvars()) <= svar:
                                p.combina(q,inplace=True)
                    if v in t.tablad:
                        for q in t.tablad[v]:
                            if len(q.getvars())<= n and set(q.getvars()) <= svar:
                                p.combina(q,inplace=True)

                np = p.tabla.sum()
                print(op,np,n)





        def localimprove(self,Q=25):
            lista = self.getpot(Q=Q)
            print(len(lista))
            sleep(3)
            i=0
            for p in lista:
                i+=1
                print(i)
                if not self.belong(p):
                    continue
                work = self.copia()

                vorig = set(work.getvars()) - set(p.getvars())
                while vorig and not self.contradict: 
                    var = work.siguientep(vorig)
                    vorig.discard(var)
                    list1 = work.get(var)
                    list2 = work.getd(var)
                    h = nodoTabla([])
                    for q in list1:
                        if len(set(h.getvars()).union(set(q.getvars())))<=25:
                            h = h.combina(q)
                        else:
                            r = q.borra([var])
                            work.insertar(r)
                        work.eliminar(q)
                    for q in list2:
                        if len(set(h.getvars()).union(set(q.getvars())))<=25:
                            h = h.combina(q)
                        else:
                            r = q.borra([var])
                            work.insertar(r)
                        work.eliminar(q)
                    if not h.trivial():
                        h = h.borra([var])
                        work.insertar(h)

                listf = work.getpot(0)
                h = nodoTabla([])
                for q in listf:
                        h = h.combina(q)

                print(p.tabla.sum(),h.tabla.sum(),2**(len(p.getvars())))
                sleep(1)
                

                if not h.implicadopor(p):
                    print("mejora")
                    # sleep(4)

                    self.eliminar(p)
                    self.insertar(h)


        def checkincluded(self):
            lista = self.getpotl(self.getvars())        
            lista.sort(key = lambda x : - len(x.getvars()) )

    
            i=0
            while i <len(lista)-1:
        
                j = i+1
                while j < len(lista):
                    # print("lista, i, j", len(lista), i, j)
                    if set(lista[j].getvars()) <= set(lista[i].getvars()):
                        p = lista[i]
                        q = lista[j]
                        self.eliminar(q)
                        self.eliminar(p)
                        t = p.combina(q)
                        self.insertar(t)
                        print("algo no va bien")
                        sleep(1)
                        
                        lista[i] = t
                        
                        lista.remove(q)
                        
                    else:
                        j+=1
                
                i+=1
            
        def minentr(self):
            ent = dict()
            pos = dict()
            neg = dict()
            lista = self.getvars()
            lp = self.getpotl(lista)
            for v in lista:
                pos[v] = 1
                neg[v] = 1 
            for p in lp:
                for v in p.getvars():
                    (x0,x1) = p.cuenta(v)
                    
                    pos[v] *= x0
                    neg[v] *= x1
                    s = pos[v] + neg[v]
                    pos[v] = pos[v]/s
                    neg[v] = neg[v]/s

            

            for v in lista:
                x0=pos[v]
                x1 = neg[v]
                if x0==0 or x1 == 0:
                    ent[v] = 0
                else:
                    
                    ent[v] = -x0*math.log(x0) -x1*math.log(x1)  
                print(ent[v])

            return min(ent, key = ent.get)


    

                    
        def borrac(self,Q, conf=[]):
            print(conf)

            # self.recomputeorder()
            print("ntro en borraf")
            self.borraf(Q=Q)
            print("salgo de  borraf")

            # self.extrac(Q=15)
            # self.minid(Q=10)

            if self.contradict:
                return 

            lvars = self.getvars()
            if not lvars:
                return
            print(len(lvars))
            count = dict()
            for x in lvars:
                count[x] = 0

            lpot = self.getpotl(lvars)

            for p in lpot:
                # x = p.tabla.sum()
                # n = len(p.getvars())
                # y = 1-x/2**(n)
                for z in p.getvars():
                    if p in self.tablad.get(z,[]):
                        count[z]+= 3
                    else:
                        count[z]+= 1
                        

            var = max(count,key=count.get)

            # var = self.minentr()



            print(var)
            conf.append(-var)
            n1 = self.reduce(-var)
            n1.borrac(Q=Q, conf=conf)
            conf.pop()
            conf.append(var)

            n2 = self.reduce(var)
            n2.borrac(Q=Q, conf=conf)
            conf.pop()

            


        def compile(self,Q):
            
            vorig  = self.getvars()
            trabajo = self
            res = varpot()
            res.orden =self.orden.copy()
            this = []
            
            while vorig and not trabajo.contradict: 
                var = trabajo.siguientep(vorig)
                # var = trabajo.orden[0]
                i = self.orden.index(var)
                print("var ", var, i, len(vorig),  trabajo.tad(var))
                this.append(var)

                


                list1 = trabajo.get(var)
                list2 = trabajo.getd(var)

                print(len(list1),len(list2))

                for p in list1:
                            trabajo.eliminar(p)
                for p in list2:
                            trabajo.eliminar(p)  
                
                    
                

                               
                            



                         

                vorig.discard(var)
                del self.orden[i]

               


                n = len(list1) + len(list2)

                # combinaincluidas(list1, K=0)
                # eliminaincluidas(list1,list2)
                
                list1.sort(key = lambda x :  len(x.getvars()) )

                       


                if not list2 and n>2:
                    for p in list1:
                        if p.checkdetermi(var):
                            list1.remove(p)
                            list2.append(p)
                            print("nuevo")
                            break
                for p in list1:
                    if n ==1:
                        break
                    l = p.descomponev(var)
                    if len(l)>1:
                        print(len(p.getvars()),len(l[0].getvars()), len(l[1].getvars()))
                        trabajo.insertar(l[1])
                        list1.remove(p)
                        if not l[0].trivial():
                            list1.append(l[0])
                        # sleep(5)


                if list2:
                    print("determinista")
                    pivote = min(list2, key = lambda x: len(x.getvars()))
                    svar = set(pivote.getvars())
                    res.insertars(pivote)
                    if n<=1:
                        h = pivote.borra([var], inplace = False)
                        trabajo.insertar(h)
                        
                        
                            
                    
                    else:
                        for p in list1:
                                
                                if len(svar.union(set(p.getvars())))<=Q:
                                    h = pivote.combina(p)
                                    h = h.borra([var])
                                    # print("inserto " ,h.getvars())
                                    trabajo.insertar(h)
                                # print("salgo de insertar")
                                else:
                                    h = p.borra([var])
                                    trabajo.insertar(h)
                                    res.insertar(p)
                                    print("no exacto")


                                
                                if trabajo.contradict:
                                    break
                                
                                
                                        


                        list2.remove(pivote)

                        for p in list2:
                                
                                if len(svar.union(set(p.getvars())))<=Q:
                                    h = pivote.combina(p)
                                    h = h.borra([var])
                                    # print("inserto " ,h.getvars())
                                    trabajo.insertar(h)
                                # print("salgo de insertar")
                                else:
                                    h = p.borra([var])
                                    trabajo.insertar(h)
                                    res.insertar(p)
                                    print("no exacto")

                                if trabajo.contradict:
                                    break
                                    
                                
                        
                                

                                

                elif list1:
                    h = nodoTabla([])        

                    for r in list1:
                        if not h.getvars() or len(set(h.getvars()).union(set(r.getvars())))<=Q:
                            h = h.combina(r)
                        else:
                            print("no exacto")
                            res.insertar(h)
                            h = h.borra([var])
                            trabajo.insertar(h)
                            if trabajo.contradict:
                                    break
                            h = r.copia()
                            

                    res.insertar(h)
                    h = h.borra([var])
                    # print("inserto " ,h.getvars())
                    trabajo.insertar(h)
                    # print("salgo de insertar")
                    if trabajo.contradict:
                                    break
                    




            if self.contradict:
                print("contradict")
                res.anula()
            
            res.orden = this
            self.orden = res.orden
            self.tabla = res.tabla
            self.tablad = res.tablad
            self.contradict = res.contradict




        def borraf(self,Q, xor = None):
            
            vorig  = self.getvars()
            trabajo = self
            res = varpot()
            res.orden = self.orden.copy()
            msize = 0

            torden = []
            
            while vorig and not trabajo.contradict: 
                if not self.orden:
                    var = trabajo.siguientep(vorig)
                else:
                    var = trabajo.orden[0]
                i = self.orden.index(var)
                # print("var ", var, i, len(vorig),  trabajo.tad(var))
                

                # if trabajo.tad(var)>=Q:
                #     return 

                list1 = trabajo.get(var)
                list2 = trabajo.getd(var)
                list3 = trabajo.getm(var)

                # print(len(list1),len(list2),len(list3))

                for p in list1:
                            trabajo.eliminar(p)
                for p in list2:
                            trabajo.eliminar(p)   
                for p in list3:
                            trabajo.eliminar(p)           
             
                torden.append(var)
                vorig.discard(var)
                del self.orden[i]
                
               


                n = len(list1) + len(list2) + len(list3)

             
                
                list1.sort(key = lambda x :  len(x.getvars()) )

                       


                if n>1:
                    nl = list1.copy()
                    list1 = []
                        
                    for p in nl:
                
                        l = p.descomponev(var)
                        if len(l)>1:
                            # print(len(p.getvars()),len(l[0].getvars()), len(l[1].getvars()))
                            self.insertar(l[1])
                            if not l[0].trivial():
                                list1.append(l[0])
                        else:
                            list1.append(p)
                        # sleep(5)
                if not list2 and len(list1)>1:
                    # print(len(list1))
                    s = nodoTabla([])
                    for p in list1:
                        s = s.combina(p)
                    
                    list1 = [s]
                    
                    # groupp(list1,Q=Q)
                    # print(len(list1) , [len(x.getvars()) for x in list1])
                    # sleep(5)


                if list2:
                    # print("determinista")
                    pivote = min(list2, key = lambda x: len(x.getvars()))
                    res.insertars(pivote)
                    if len(list1) + len(list2) + len(list3)<=1:
                        h = pivote.borra([var], inplace = False)
                        msize = max(msize,len(pivote.getvars()))
                        trabajo.insertar(h)
                        
                        
                            
                    
                    else:
                        for p in list1:
                                

                                pivote = min(list2, key=lambda x: len(set(p.getvars()).union(set(x.getvars()))))
                                if len(set(p.getvars()).union(set(pivote.getvars())))<=Q:
                                    h = pivote.combina(p)
                                    msize = max(msize,len(h.getvars()))

                                    h = h.borra([var])
                                    # print("inserto " ,h.getvars())
                                    
                                    trabajo.insertar(h)
                                else:
                                    h = pivote.resolution(p,var)
                                    trabajo.insertar(h[0])
                                    trabajo.insertar(h[1])

                                    r = p.borra([var])
                                    msize = max(msize,len(h[0].getvars()),len(h[1].getvars()),len(r.getvars()))

                                    trabajo.insertar(r)
                                # print("salgo de insertar")
                                
                                if trabajo.contradict:
                                    break

                        
                        for p in list3:
                                

                                pivote = min(list2, key=lambda x: len(set(p.getvars()).union(set(x.getvars()))))
                                h = pivote.resolution(p,var)
                                trabajo.insertar(h[0])
                                trabajo.insertar(h[1])
                                r = p.borra([var])
                                trabajo.insertar(r)
                                msize = max(msize,len(h[0].getvars()),len(h[1].getvars()),len(r.getvars()))


                                if trabajo.contradict:
                                    break
                                
                                
                                        


                        list2.sort(key = lambda x :  len(x.getvars()) )

                        while len(list2) > 1:
                                p = list2.pop()
                                pivote =  min(list2, key=lambda x: len(set(p.getvars()).union(set(x.getvars()))))
                                if len(set(p.getvars()).union(set(pivote.getvars())))<=Q:
                                    h = pivote.combina(p)
                                    msize = max(msize,len(h.getvars()))
                                    h = h.borra([var])
                                    # print("inserto " ,h.getvars())
                                    
                                    trabajo.insertar(h)
                                else:
                                    h = pivote.resolution(p,var)
                                    trabajo.insertar(h[0])
                                    trabajo.insertar(h[1])
                                    r = p.borra([var])
                                    trabajo.insertar(r)
                                    msize = max(msize,len(h[0].getvars()),len(h[1].getvars()),len(r.getvars()))

                                # print("salgo de insertar")
                                if trabajo.contradict:
                                    break
                        p = list2.pop()
                        r = p.borra([var])
                        trabajo.insertar(r)
                                

                                

                elif list1 or list3:

                    listt = list1 + list3
                    k = len(listt)
                    for i in range(k):
                        r1 = listt[i]
                        for j in range(i+1,k):
                            r2 = listt[j]
                            (res1,res2) = r2.resolution(r1,var)
                            trabajo.insertar(res1)
                            trabajo.insertar(res2)
                            msize = max(msize,len(res1.getvars()),len(res2.getvars()))

                    for p in listt:
                        res.insertars(p)
                        r = p.borra([var])
                        msize = max(msize,len(p.getvars()))


                        trabajo.insertar(r)
                    if trabajo.contradict:
                                    break




            if self.contradict:
                print("contradict")

            print("tamaño máximo", msize)
            sleep(5)
            # else:
            #     orden = self.orden.copy()
            #     self.recomputeorderb(var)
            #     self.minid(Q-1,ins=False)
            #     self.orden = orden

            res.orden = torden
            return (res,msize)
        
        def addproborden(self):
            for v in self.prob:
                if v not in self.orden:
                    self.orden = [v] + self.orden


        def importancesampling(self, N=1000, method = 0, K=10):
            
            borr = self.orden.copy()
            
            listprobb = []
            listlogic = []
            listprob = []
            oldw = self.w
            sumw = dict()
            for x in borr:
                sumw[x] = 0.0
                sumw[-x] = 0.0

            t1 = time()
            listprobb = []
            for v in borr:
                 for p in self.prob.get(v,[]):
                     if not p in listprobb:
                         listprobb.append(p)

            for v in borr:
                ll = self.get(v) + self.getd(v)
                ld = self.getd(v)
                listlogic.append(ll)
                for p in ll:
                    self.eliminar(p)
                lp = self.prob.get(v,[]).copy()

                listprob.append(lp)
                for p in lp:
                    self.removebay(p)

                lpc = lp.copy()
                if ld and method==0:
                    for p in lpc:
                        for q in  ld:
                            print(q.getvars(), p.getvars())
                            if q.getvars() <= p.getvars():
                                print("Reducción")
                                h = p.combinab(q).sumab([v])
                                self.insertbay(h)
                                lp.remove(p)
                                print("quito ")
                                print(p.tabla)
                                print("añado ")
                                print(h)
                                break

                elif ld and (method==1 or method ==2):
                    piv = min(ld, key= lambda x: len(x.getvars()))
                    for p in lpc:
                        print("Reducción")
                        h = p.combinab(piv).borrab([v])
                        self.insertbay(h)
                        lp.remove(p)
                        print("quito ")
                        print(q.tabla)
                        print("añado ")
                        print(h)

                elif method==2 and lp:

                    h = lp.pop()
                
                    
                    lpc = lp.copy()
                    for p in lpc:
                        lp.remove(p)
            
                    for p in lpc:
                        if len(set(h.getvars()).union(set(p.getvars()))) <=K:
                            h = h.combinab(p)
                        else:
                            if h.getvars():
                                q = h.borrab([v])
                                self.insertbay(q)
                                t = h.divideb(q)
                                lp.append(t)
                                h = p
                                # if not q.getvars():
                                #     print(h.tabla)
                                #     print(q.tabla)
                                #     print(t.tabla)
                    if h.getvars():
                         q = h.borrab([v])
                         self.insertbay(q)
                         t = h.divideb(q)
                         lp.append(t)
                        #  if not q.getvars():
                        #      print(h.tabla)
                        #      print(q.tabla)
                        #      print(t.tabla)
                             



                                                    

            ttotal = 0                        
                    
                    
             
            borr.reverse()
            listlogic.reverse()
            listprob.reverse()

            pesos = 0.0
            pesos2 = 0.0
            ceros = 0

           
            
            
            for j in range(N):

                sol = []
                pe = 1.0
                for i in range(len(borr)):
                    
                    var = borr[i]

                    ll = listlogic[i]
                    lp = listprob[i]
                    pos = False
                    neg = False
                    t1 = time()
                    for p in ll:
                        

                        h = p.reduce(sol)
                   
                        # if not len(h.getvars()) == 1:
                        #     print("algo va mal longitud de variables")
                        #     sleep(5)
                        if not h.tabla[0]:
                            pos = True
        
                        if not h.tabla[1]:
                            neg = True
                    # if pos and neg:
                    #     print("peso 0")
                        
                    #     sleep(5)
                    #     break

                    ttotal += (time()-t1)

                    pw = 1.0
                    nw = 1.0
                    for p in lp:
                        h = p.reduce(sol)
                        # if not len(h.getvars()) == 1:
                        #     print("algo va mal longitud de variables prob")
                        #     print(h.getvars())
                        #     print(p.getvars())
                        #     print(var)
                        #     print(446 in self.orden)
                        #     print(446 in sol, -446 in sol)
                        #     print(sol)
                            # sleep(5)
                        nw *= h.tabla[0]
                        pw *= h.tabla[1]
                    # print("pesos= ",method,nw,pw)

                    if pos and not neg:
                        sol.append(var)
                        pe *= pw
                        # 
                        # print("Solo positivo", pe, pw)
                        # sleep(0.02)
                        # if pe == 0:
                        #     print("peso 0 no coherente")
                        #     sleep(50)

                    if neg and not pos:
                        sol.append(-var)
                        pe *= nw
                        # print("Solo negativo", pe, nw)

                      
                    if not neg and not pos:
                        value = choices([-var,var], weights = [nw,pw])
                        pe *= (nw+pw)
                    
                        # print("ambos",pe,nw,pw)
                      
                        sol.append(value[0])

                

                for x in sol:
                    sumw[x] += pe   
                    
                if pe == 0:
                    ceros+=1
                else:
                    pesos += pe
                    pesos2 += pe*pe

                # pc = 1.0
                # opc = 1.0
                # for i in range(len(borr)):
                #     lp = listprob[i]
                #     for p in lp:
                #         pc*= p.getvalue(sol)
                # for p in listprobb:
                #         opc*= p.getvalue(sol)
                # print(oldw,self.w)
                # print(pc*self.w,opc*oldw)
                

                

            print(ttotal)
            print(self.w,pesos)

            pesos = pesos*self.w
            pesos2 = pesos2*self.w*self.w



            me = pesos/N
            va = pesos2/N - me*me

          



            return(ceros,me , va, sumw )

        def importancesampling2(self, N=1000, method = 0, K=10):
            
            borr = self.orden.copy()
            

            listprob = []
            sumw = dict()
            for x in borr:
                sumw[x] = 0.0
                sumw[-x] = 0.0


            for v in borr:
                
                lp = self.prob.get(v,[]).copy()
                listprob.append(lp)
                for p in lp:
                    self.removebay(p)

                

              

                if method==2 and lp:

                    h = lp.pop()
                
                    
                    lpc = lp.copy()
                    for p in lpc:
                        lp.remove(p)
            
                    for p in lpc:
                        if len(set(h.getvars()).union(set(p.getvars()))) <=K:
                            h = h.combinab(p)
                        else:
                            if h.getvars():
                                q = h.borrab([v])
                                self.insertbay(q)
                                t = h.divideb(q)
                                lp.append(t)
                                h = p
                                # if not q.getvars():
                                #     print(h.tabla)
                                #     print(q.tabla)
                                #     print(t.tabla)
                    if h.getvars():
                         q = h.borrab([v])
                         self.insertbay(q)
                         t = h.divideb(q)
                         lp.append(t)
                        #  if not q.getvars():
                        #      print(h.tabla)
                        #      print(q.tabla)
                        #      print(t.tabla)
                             

                    

            borr.reverse()
            listprob.reverse()

            pesos = 0.0
            pesos2 = 0.0
            ceros = 0

           

            
            for j in range(N):
                sol = []
                pe = 1.0
                for i in range(len(borr)):
                    
                    var = borr[i]

                    lp = listprob[i]
                 
                 

                    pw = 1.0
                    nw = 1.0
                    for p in lp:
                        h = p.reduce(sol)
                        # if not len(h.getvars()) == 1:
                        #     print("algo va mal longitud de variables prob")
                        #     print(h.getvars())
                        #     print(p.getvars())
                        #     print(var)
                        #     print(446 in self.orden)
                        #     print(446 in sol, -446 in sol)
                        #     print(sol)
                            # sleep(5)
                        nw *= h.tabla[0]
                        pw *= h.tabla[1]

                  
                      
                    if nw+pw>0:
                        value = choices([-var,var], weights = [nw,pw])
                        sol.append(value[0])

                    else:
                        sol.append(-var)
                    pe *= (nw+pw)
                      

                        
                if math.isnan(pe):
                    pe = 0.0

                # print(pe)                 
                for x in sol:
                    sumw[x] += pe   
                    
                if pe == 0:
                    ceros+=1
                else:
                    pesos += pe
                    pesos2 += pe*pe

            print(self.w,pesos)
            
            pesos = pesos*self.w
            pesos2 = pesos2 * self.w*self.w


            me = pesos/N
            va = pesos2/N - me*me

         


            return(ceros,me , va, sumw )


        def count(self,  Q=1.0E6):
            
        
            borr = self.orden.copy()
            
            listlogic = []
        

            for v in borr:
                ll = self.get(v) + self.getd(v)
    
                listlogic.append(ll)
                for p in ll:
                    self.eliminar(p)
            
                    

            borr.reverse()
            listlogic.reverse()
            level = []
            for v in borr:
                level.append([0,1])
          
            
            sols = [[]]
           

            for i in range(len(borr)):
                print(i, len(sols))
                if len(sols) > Q:
                    break
                

                var = borr[i]
                ins = []
                for sol in sols:

                    ll = listlogic[i]
                    pos = False
                    neg = False
                    for p in ll:
                        
                        h = p.reduce(sol)
                    
                        if not len(h.getvars()) == 1:
                            print("algo va mal longitud de variables")
                            sleep(5)
                        if not h.tabla[0]:
                            pos = True

                        if not h.tabla[1]:
                            neg = True
                        if pos and neg:
                            print("peso 0")

                            
                            sleep(5)
                            level[i] = []
                            
                            break

                    
                    if pos and not neg:
                            sol.append(var)
                        

                    if neg and not pos:
                        sol.append(-var)

                    if not neg and not pos:
                        sol1 = sol.copy()
                        sol.append(var)
                        sol1.append(-var)
                        ins.append(sol1)
                        
                for s in ins:
                    sols.append(s)

                        

            return sols
                                  
                    
                    
              







        def borrae(self,Q):
            
            vorig  = self.getvars()
            trabajo = self.copia()
            res = varpot()
            lres = []
            res.orden = self.orden.copy()
            
            while vorig and not trabajo.contradict: 
                var = trabajo.siguientep(vorig)
                i = self.orden.index(var)
                print("var ", var, i, len(vorig),  trabajo.tad(var))
                


                list1 = trabajo.get(var)
                list2 = trabajo.getd(var)

                print(len(list1),len(list2))

               
                      

                               
                            



                for p in list1:
                            trabajo.eliminar(p)
                for p in list2:
                            trabajo.eliminar(p)            

                res.orden.append(var)
                vorig.discard(var)
                del self.orden[i]
                
               


                n = len(list1) + len(list2)

                # combinaincluidas(list1, K=0)
                # eliminaincluidas(list1,list2)
                
                list1.sort(key = lambda x :  len(x.getvars()) )

                       


                if not list2 and n>2:
                    for p in list1:
                        if p.checkdetermi(var):
                            list1.remove(p)
                            list2.append(p)
                            print("nuevo")
                            break
                # for p in list1:
                #     if n ==1:
                #         break
                #     l = p.descomponev(var)
                #     if len(l)>1:
                #         print(len(p.getvars()),len(l[0].getvars()), len(l[1].getvars()))
                #         trabajo.insertar(l[1])
                #         list1.remove(p)
                #         if not l[0].trivial():
                #             list1.append(l[0])
                        # sleep(5)


                if list2:
                    print("determinista")
                    pivote = min(list2, key = lambda x: len(x.getvars()))
                    res.insertar(pivote)
                    if n<=1:
                        h = pivote.borra([var], inplace = False)
                        trabajo.insertar(h)
                        
                        
                            
                    
                    else:
                        for p in list1:
                                

                                pivote = min(list2, key=lambda x: len(set(p.getvars()).union(set(x.getvars()))))

                                if len(set(p.getvars()).union(set(pivote.getvars()))) <= Q:
                                    h = pivote.combina(p)
                                    h = h.borra([var])
                                    trabajo.insertar(h)
                                    if trabajo.contradict:
                                        res.anula()
                                        break
                                else:
                                    lres.append(p)
                                    h = p.borra([var])
                                    trabajo.insertar(h)


                                
                                
                                        


                        list2.sort(key = lambda x :  len(x.getvars()) )

                        while len(list2) > 1:
                                p = list2.pop()
                                pivote =  min(list2, key=lambda x: len(set(p.getvars()).union(set(x.getvars()))))
                                if len(set(p.getvars()).union(set(pivote.getvars()))) <= Q:
                                    h = pivote.combina(p)
                                    h = h.borra([var])
                                    trabajo.insertar(h)
                                    if trabajo.contradict:
                                        res.anula()
                                        break
                                else:
                                    lres.append(p)
                                    h = p.borra([var])
                                    trabajo.insertar(h)

                                

                                

                elif list1:
                    combinaincluidas(list1,K=1)
                    h = nodoTabla([])        

                    while list1:
                        r = min(list1,key = lambda x: len(set(x.getvars()).union(set(h.getvars()))))
                        if len(set(r.getvars()).union(set(h.getvars())))>Q:
                            break
                        list1.remove(r)
                        h = h.combina(r)
                    res.insertar(h)
                    if var in h.getvars():
                        h = h.borra([var])
                    trabajo.insertar(h)
                    if trabajo.contradict:
                                    res.anula()
                                    break
                    while list1:
                        r = list1.pop()
                        res.insertar(r)
                        h = r.borra([var])
                        trabajo.insertar(h)





            if self.contradict:
                print("contradict")
            return (res,lres)





        def extrac(self,Q):
            
            trabajo = self
            res = varpot()
            res.orden = []
            orden = self.orden.copy()
            
            while orden and not trabajo.contradict: 
                var = orden[0]
                i = self.orden.index(var)
                print("var ", var, i, len(orden),  trabajo.tad(var))
                sor = set(orden)


                list1 = trabajo.get(var)
                list2 = trabajo.getd(var)

                list1 = list(filter(lambda x: set(x.getvars()) <= sor,list1 ))
                list2 = list(filter(lambda x: set(x.getvars()) <= sor,list2 ))

                
                del orden[0]
                
                print(len(list1),len(list2))

                



                
                
                
                       


                ins = []
                bor = []
          


                if list2:
                    print("determinista")
                    
                        
                        
                            
                    
                    for p in list1:
                                
                        l = p.descomponev(var)
                        test = l[0]
                        pivote = min(list2, key=lambda x: len(set(test.getvars()).union(set(x.getvars()))))
                        if len(set(test.getvars()).union(set(pivote.getvars())))<=Q:

                            h = pivote.combina(test)
                            h = h.borra([var])
                            ins.append(h)
                            bor.append(p)
                            print("insertar " , len(h.getvars()), len(p.getvars()) )
                            if len(l)>1:
                                ins.append(l[1])
                        
                                
                                
                                        


                        list2.sort(key = lambda x :  len(x.getvars()) )

                        while len(list2) > 1:
                                p = list2.pop()
                                pivote =  min(list2, key=lambda x: len(set(p.getvars()).union(set(x.getvars()))))
                                if len(set(p.getvars()).union(set(pivote.getvars())))<=Q:
                                    h = pivote.combina(p)
                                    h = h.borra([var])
                                    print("insertar " , len(h.getvars()), len(p.getvars()) )

                                    ins.append(h)
                                    bor.append(p)
                                    
                                
                print("borro e inserto")
                for p in bor:
                    trabajo.eliminar(p)
                for p in ins:
                    trabajo.insertar(p)                

                



            if self.contradict:
                print("contradict")
            return res



        def getmarginalsapr(self,lista,Q=27):
            # print("entro en marginal con  ", len(lista))
            svar = set(self.getvars())
            # print(len(svar))

            if not lista:
                return []

            lt = list(filter(lambda x: svar <= x, lista))

            lh = list(filter(lambda x: not x in lt , lista ))

            res = []
            if lt:
                p = nodoTabla([])
                lp = self.getpotl(svar)
                for q in lp:
                    p.combina(q,inplace=True)

                res.append(p)

            if lh:
                fs = lh[0]
                nuevo = self.copia()
                vtd = svar - fs
                var = self.siguientep(vtd)
                lyes = list(filter(lambda x: var in x,lh))
                lno = list(filter(lambda x: not var in x,lh))
                # print("borro ", var)
                nuevo.borravmini(var,Q)
                # print("termino de borrar")
                res = res + nuevo.getmarginalsapr(lno,Q=Q)
                res = res + self.getmarginalsapr(lyes,Q=Q)



            return res


        def borravmini(self,var,Q):
            trabajo = self
            list1 = trabajo.get(var)
            list2 = trabajo.getd(var)


            for p in list1:
                trabajo.eliminar(p)
            for p in list2:
                trabajo.eliminar(p)



            n = len(list1) + len(list2)
            nd = []
            traba = []
            nuevas = []
            
                    



            if list2:
                
                pivote = min(list2, key = lambda x: len(x.getvars()))
                if n<=1:
                    h = pivote.borra([var], inplace = False)
                    nd = nd + trabajo.insertard(h)
                    nuevas.append(h)
                    
                        
            
                else:
                    for p in list1:
                        

                        pivote = min(list2, key=lambda x: len(set(p.getvars()).union(set(x.getvars()))))
                        if len(set(p.getvars()).union(set(pivote.getvars())))<= Q:
                            h = pivote.combina(p, inplace = False)
                            h.borra([var], inplace =True)
                            nd = nd + trabajo.insertar(h)
                            nuevas.append(h)
                            
                                



                        else:
                            traba.append(p)
                    list2.sort(key = lambda x :  len(x.getvars()) )

                    while len(list2) > 1:
                        p = list2.pop()
                        pivote =  min(list2, key=lambda x: len(set(p.getvars()).union(set(x.getvars()))))
                        if len(set(p.getvars()).union(set(pivote.getvars())))<= Q:
                            h = pivote.combina(p, inplace = False)
                            h.borra([var], inplace =True)
                            nd = nd+  trabajo.insertar(h)
                            nuevas.append(h)
                            

                        else:
                            traba.append(p)
                    
                    
                    
                    if traba:
            

                        for p in traba:
                            
                            h = p.borra([var], inplace=False)
                            
                            nd = nd+  trabajo.insertard(h)
                            nuevas.append(h)
                        

                

                


            else:
                
                h = nodoTabla([])
                combinaincluidas(list1,K=1)
                if list1:
                    while list1:
                        q = min(list1, key = lambda x: len(set(x.getvars()) - set(h.getvars())))

                        list1.remove(q)
                    
                        if len(set(h.getvars()).union(set(q.getvars())))<= Q or not h.getvars():
                            h.combina(q,inplace=True)
                        else:
                            h.borra([var],inplace=True)

                            nd = nd+  trabajo.insertard(h)
                            nuevas.append(h)
                            h = nodoTabla([])
                            h.combina(q,inplace=True)

                    h.borra([var], inplace=True)
                    nd = nd+  trabajo.insertar(h)
                    nuevas.append(h)
                    
              



        
        def borraref(self,ref,Q=10):
            
            vorig  = self.getvars()
            trabajo = self.copia()
            compil = []
            orden = []


         


            
            
            while vorig and not self.contradict: 
                var = trabajo.siguientep(vorig)
                print("var ", var, len(vorig),  trabajo.tad(var))
                ref.borravmini(var,Q=25)

                list1 = trabajo.get(var)
                list2 = trabajo.getd(var)

                print(len(list1),len(list2))
                
                orden.append(var)
                
        


                for p in list1:
                    trabajo.eliminar(p)
                for p in list2:
                    trabajo.eliminar(p)

                n = len(list1) + len(list2)

                combinaincluidas(list1, K=0)
                eliminaincluidas(list1,list2)
                
                
                list2d = ref.getd(var)

                if not list2 and list2d:
                    h = min(list2d, key=lambda x: len(x.getvars()))
                    list2.append(h)
                    print("nuevo determinismo")
                    sleep(3)       

                vorig.discard(var)

                if list2:
                    print("determinista")
                    pivote = min(list2, key = lambda x: len(x.getvars()))
                    compil.append([pivote])
                    if n<=1:
                        h = pivote.borra([var], inplace = False)
                        if isinstance(h,nodoTabla) and len(h.getvars())>Q:
                            t = creadesdetabla(h,Q)
                            h = t

                        h = ref.simplifica(h)
                        if isinstance(h,arbol):
                            h.poda(Q)
                            # h.simpli()
                        trabajo.insertarb2(h)
                        
                            
                    
                    else:
                        for p in list1:
                                

                                pivote = min(list2, key=lambda x: len(set(p.getvars()).union(set(x.getvars()))))
                                
                                if isinstance(p,arbol):
                                    print ("combina arbol p", p.size())
                                if isinstance(pivote,arbol):
                                    print ("combina arbol pivote", pivote.size())
                                h = pivote.combina(p)
                                if isinstance(h,arbol):
                                    print ("resultado ", h.size())
                                h = h.borra([var])

                                if  isinstance(h,nodoTabla) and len(h.getvars())>Q:
                                    t = creadesdetabla(h,Q)
                                    h = t

                                h = ref.simplifica(h)
                                if isinstance(h,arbol):
                                    if h.trivial():
                                        print("trivial")
                                    print("tam ", h.size())
                                    h.poda(Q)
                                    # h.simpli()
                                    if h.trivial():
                                        print("trivial")
                                    print("tam ", h.size())

                                trabajo.insertarb2(h)
                                
                                
                                        


                        list2.sort(key = lambda x :  len(x.getvars()) )
                        

                        while len(list2) > 1:
                                p = list2.pop()
                                pivote =  min(list2, key=lambda x: len(set(p.getvars()).union(set(x.getvars()))))
                                
                                h = pivote.combina(p)
                                h = h.borra([var])
                                if isinstance(h,nodoTabla) and len(h.getvars())>Q:
                                    t = creadesdetabla(h,Q)
                                    h = t
                                h = ref.simplifica(h)
                                if isinstance(h,arbol):
                                    print("tam ", h.size())
                                    h.poda(Q)
                                    # h.simpli()

                                    print("tam ", h.size())
                                trabajo.insertarb2(h)
                                

                            

                elif list1:

                    

                    h = nodoTabla([])   

                    for p in list1:
                        h = h.combina(p)
                    
                    h = h.borra([var])
        

                    if isinstance(h,nodoTabla) and len(h.getvars())>Q:
                            t = creadesdetabla(h,Q)
                            h = t

                    h = ref.simplifica(h)
                    if isinstance(h,arbol):
                              print("tam ", h.size())
                              h.poda(Q)
                    

                              print("tam ", h.size())


                   
                    trabajo.insertarb2(h)


                    







        def siguienteb(self,config, pos):
            
            val = dict()
            vars = set(map(abs,config))
            det = False

            for x in pos:
                val[x] = 0.0

            for v in pos:
                lista = self.get(v) + self.getd(v) + self.getm(v)
                l1 = []
                l2 = []
            

                for p in lista:
                    dif = set(p.getvars()) - vars
                    ldif = dif - {v}
                    h = p.reduce(config)
                    if h.contradict():
                            ap = p.borra(list(dif))
                            print("contra 1")
                            sleep(1)
                            return (v,[ap])
                    if isinstance(h,nodoTabla):
                        h = h.borra(list(set(h.getvars())-{v}))
                    if len(h.getvars()) == 1 and not h.trivial():
                        
                        if isinstance(h,mix):
                            h = h.toTable()
                        if h.tabla[0]:
                            ap = p.borra(list(ldif))
                            print("forzado ", -v)
                            l1.append(ap)
                            svar = -v
                        else:
                            ap = p.borra(list(ldif))
                            l2.append(ap)
                            print("forzado ", v)
                            svar = v
                        det = True
                    elif not det:
                        val[v] += 1/len(p.getvars())
                if l1 and l2:
                    p1 = min(l1,key=lambda x: len(x.getvars()))
                    p2 = min(l2,key=lambda x: len(x.getvars()))
                    ap = p1.combina(p2)
                    ap = ap.borra([v])
                    print("contra 2")
                    sleep(1)
                    return (v,[ap])
                
            if det:    
               print("determinado")
               sleep(0.5)
               return(svar,False)

            print("indeterminado ")
            sleep(0.5)

            return (max(pos, key = lambda x: val[x]),False)                   

                    
                   
                        
                    
               




        def tamb(self,v,config):
            lista = self.get(v) + self.getd(v)

            vars = set(map(abs,config))
            s = 0
            for p in lista:
                dif = set(p.getvars()) - vars
                if len(dif) > 1:
                    s+= 1.0/(len(dif) -1)
                else:
                    h = p.reduce(config)
                    if not h.trivial():
                        s+= 1000
            if s>=1000:
                return s
            lista = self.clau.get(v,[])

            for cl in lista:
                vc = set(map(abs,cl))
                dif = vc-vars
                if len(dif)<=1:
                    return 1000
                else:
                    s+= 1.0/(len(dif)+2)

            return s
        

        def tamc(self,v,config):
            lista = self.get(v) + self.getd(v)

       

            vars = set(map(abs,config))
            s = 0
            for p in lista:
                dif = set(p.getvars()) - vars
                if len(dif) > 1:
                    s+= 1.0/(len(dif) -1)
                else:
                    h = p.reduce(config)
                    if not h.trivial():
                        s+= 1000
            if s>=1000:
                return s
            
            return s
            