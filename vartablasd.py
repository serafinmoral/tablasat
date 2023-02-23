# -*- coding: utf-8 -*-
"""
Created on 31 Enero 2022

@author: Serafin
"""
from secrets import choice
from statistics import variance
from utils import *
from time import *
from random import shuffle
from arboltabla import *


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
            self.orden = []
            self.posvar = dict()
            self.clau = dict()
          
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

        def getvarsd(self,v):
            res  = set()
            l = self.get(v) + self.getd(v)
            for p in l:
                res.update(set(p.getvars()))
         


            return res

        def copia(self):
            res = varpot()
            for v in self.tabla:
                res.tabla[v] = self.tabla[v].copy()
            for v in self.tablad:
                res.tablad[v] = self.tablad[v].copy()

            for v in self.clau:
                res.clau[v] = self.clau[u].copy()
   
            res.orden = self.orden.copy()
            res.posvar = self.posvar.copy()
            
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
            return min([self.posvar[x] for x in p])

        
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
                lista = self.get(var) + self.getd(var)
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



                
                    
        def back2(self, M):
            
            vars = self.getvars()
            pos = list(vars)
            orden = []
            n = len(vars)

            level=len(vars)-1
            config = []
            while level>0:
                oldl = level
                var = self.siguienteb(config,pos)
                print(level,len(config) , var, config)

                self.posvar[var]= level
                pos.remove(var)
                orden.append(var)


                list1 = []
                list2 = []
                listap = self.get(var) + self.getd(var)
                vars = set(map(abs,config))
                print(len(listap))
                lista = []
                for p in listap:
                    
                    if len(set(p.getvars())-vars )<=1:
                        lista.append(p)
                print(len(lista))
                # sleep(1)
                margi = False
                # if len(lista)>1:
                #     print("posible problema")
                for p in lista:
                    t = p.reduce(config)
                    if t.contradict():
                        print("contradiccion ")
                        nueva = p.borra([var], inplace = False)
                        todas = self.insertarb2(nueva)
                        level = max([self.level(x) for x in todas])
                        pos = pos + orden[-(level-oldl)-1:]
                        del orden[-(level-oldl)-1:]
                        del config[-(level-oldl):]
                        print("aprendo ", nueva.getvars())
                        margi = True
                        break   
                        
                    elif not t.tabla[0]:
                        list1.append(p)
                    elif not t.tabla[1]:
                        list2.append(p)
                if margi:
                    continue

                print(len(list1),len(list2))
                # sleep(2)
                

                lcl = self.clau.get(var,[])

                lred = []

                for cl in lcl:
                    vcl = set(map(abs,cl))
                    if len(vcl-vars)<=1:
                        lred.append(cl)

                l1 = []
                l2 = []
                for cl in lred:
                    ncl = cl -{var,-var}
                    if ncl <= set(config):
                        if -var in cl:
                            l1.append(cl)
                        elif var in cl:
                            l2.append(cl)

                print(len(l1),len(l2))

                if not list2 and not list1 and not l1 and not l2:
                    # x = choice([var,-var])
                    x= -var
                    config.append(x)
                    level+=-1
                    continue

                if not list2 and not l2:
                    config.append(var)
                    level+=-1
                    continue
                
                if not list1 and not l1:
                    config.append(-var)
                    level+=-1
                    continue

                if list1 and list2:
                    n1 = min(list1, key = lambda x: len(x.getvars()))

                    n2 = min(list2, key = lambda x: len(set(x.getvars()).union(set(n1.getvars()))))

                    if (len(set(n1.getvars()).union(set(n2.getvars()))))<= M:
                        nueva = n1.combina(n2, inplace = False)
                        nueva.borra([var], inplace=True)
                        print("aprendo ", nueva.getvars(), 2**(len(nueva.getvars())), np.sum(nueva.tabla))
                        
                        if n1 in self.getd(var):
                            if n2 in self.getd(var):
                                if len(n2.getvars()) < len(n1.getvars()): 
                                    self.eliminar(n1)
                                else:
                                    self.eliminar(n2)
                            else:
                                self.eliminar(n2)
                        elif n2 in self.getd(var):
                            self.eliminar(n1)
                        todas = self.insertarb2(nueva)
                        level = max([self.level(x) for x in todas])
                        del config[-(level-oldl):]
                        pos = pos + orden[-(level-oldl)-1:]
                        del orden[-(level-oldl)-1:]
                    else:
                        cl = set(filter(lambda x: abs(x) in n1.getvars() or abs(x) in n2.getvars(),config))
                        todas = self.insertarclau(cl) 
                        print(cl)
                        print(todas)
                        level = max([self.level(x) for x in todas])
                        print(level)
                        del config[-(level-oldl):]
                        pos = pos + orden[-(level-oldl)-1:]
                        del orden[-(level-oldl)-1:]
                    continue

                if list1 and l2:
                    n1 = min(list1, key = lambda x: len(x.getvars()))
                    cl2 = l2[0]
                    if n1 in self.getd(var):

                        self.eliminarc(cl2)
                    cl = set(filter(lambda x: abs(x) in n1.getvars() or x in cl2,config))
                    todas = self.insertarclau(cl) 
                    level = max([self.level(x) for x in todas])
                    del config[-(level-oldl):]
                    pos = pos + orden[-(level-oldl)-1:]
                    del orden[-(level-oldl)-1:]
                    continue

                if list2 and l1:
                    cl1 = l1[0]
                    n2 = min(list2, key = lambda x: len(x.getvars()))
                    if n2 in self.getd(var):
                            self.eliminarc(cl1)


                    cl = set(filter(lambda x: abs(x) in n2.getvars() or x in cl1,config))
                    todas = self.insertarclau(cl) 
                    level = max([self.level(x) for x in todas])
                    del config[-(level-oldl):]
                    pos = pos + orden[-(level-oldl)-1:]
                    del orden[-(level-oldl)-1:]
                    continue

                if l1 and l2:
                    cl1 = min(l1, key = lambda x: len(x))
                    cl2 = min(l2,key = lambda x: len(x.union(cl1)))
                    cl = cl1.union(cl2) - {var, -var}
                    # if len(cl1)<=len(cl2):
                    #     self.eliminarc(cl2)
                    # else:
                    #     self.eliminarc(cl1)
                    todas = self.insertarclau(cl) 
                    level = max([self.level(x) for x in todas])
                    del config[-(level-oldl):]
                    pos = pos + orden[-(level-oldl)-1:]
                    del orden[-(level-oldl)-1:]
                    continue
    

                        



                
                    
                
                
        
            

            

         

           

            
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
            
            lista = res.get(abs(v))+res.getd(abs(v))
            for p in lista:
                res.eliminar(p)
            for p in lista:
                q = p.reduce({v})
               
                res.insertarb2(q)

             
            return res
            
            
 
        def simplifica(self,p):
            if p.trivial():
                return nodoTabla([])
            
            if p.contradict():
                res = nodoTabla([])
                res.anula()
                return res

            res = p.copia()

            svar = set(p.getvars())
            
            # for v in p.getvars():
            #     if v in self.tablad:
            #         for q in self.tablad[v]:
            #             if set(q.getvars())<= svar:
            #                 h = q.combina(p,inplace=False)
            #                 h.borra([v], inplace=True)
            #                 return self.simplifica(h)
                            

            lista = []
            for v in p.getvars():
                if v in self.tabla:
                    for q in self.tabla[v]:
                        if q not in lista:
                            lista.append(q)

            for v in p.getvars():
                if v in self.tablad:
                    for q in self.tablad[v]:
                        if q not in lista:
                            lista.append(q)
               
            for q in lista:
                if set(q.getvars())<= svar:
                    res.combina(q, inplace = True)
                    
            return res

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



                        
        def insertarb2(self,p, Q = 10):
            if p.contradict():
                self.anula()
                return []
            

            if p.trivial():
                return []
            
            lp = p.getvars()
            n = len(lp)

            svar = set(lp)

            for v in lp:
                if v in self.tablad:
                    for q in self.tablad[v]:
                        lq = q.getvars()
                        if len(lq) <= n and set(lq)<= svar:
                            h = q.combina(p)
                            h = h.borra([v])
                            return self.insertarb2(h)
            lista = []
            lista2 = []
            for v in lp:
                if v in self.tabla: 
                    for q in self.tabla[v]:
                        lq = q.getvars()
                        if len(lq)==n and q not in lista:
                            lista.append(q)
                        elif len(lq)<n and q not in lista2:
                            lista2.append(q)


            for q in lista:
                sq = set(q.getvars())
                if  sq<=svar:
                    p = p.combina(q)
                    self.eliminar(q)

            if len(lp)<=Q:
                for q in lista2:
                    sq = set(q.getvars())
                    if sq<= svar:
                        p = p.combina(q)


                for v in lp:
                    if p.checkdetermi(v):
                        var = v
                        t = p.minimizadep(v, seg = set())
                        # print("nuevo determinismo ", len(p.getvars()), len(t.getvars()))
                        if len(t.getvars())< len(lp):
                            l1 = self.insertarb2(t)
                            q = p.borra([var])
                            l2 = self.insertarb2(q)
                            return l1 + l2
                        else:
                            
                            res = [lp]
                            lista = []
                            for v in lp:
                                if v in self.tablad:
                                    for q in self.tablad[v]:
                                        lq = q.getvars()
                                        if len(lq) >n and q not in lista:
                                            lista.append(q)
                                if v in self.tabla: 
                                    for q in self.tabla[v]:

                                        if len(q.getvars()) >n and q not in lista:
                                            lista.append(q)
                            ins = []
                            for q in lista:
                                    sq = set(q.getvars())
                                    if svar <= sq:
                                        
                                        self.eliminar(q)
                                        h = q.combina(p)
                                        h = h.borra([var])
                                        ins.append(h)

                            for h in ins:
                                res = res + self.insertarb2(h)


                            if var in self.tablad:
                                    self.tablad[var].append(p)
                            else:
                                    self.tablad[var] = [p]

                            for v in lp:
                                    if not v == var:
                                        if v in self.tabla:
                                            self.tabla[v].append(p)
                                        else:
                                            self.tabla[v] = [p]
                        return res
            



            res= [p.getvars()]
            for v in lp:
                if v in self.tabla:
                    self.tabla[v].append(p)
                else:
                    self.tabla[v] = [p] 

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

        def insertar(self,p, small = [], vc = -1):
            # print("inserto ", p.getvars())

     

            
           

            if not small:
                small = self


            if p.contradict():
                self.anula()
                return []
            

            if p.trivial():
                return []

            svar = set(p.getvars())
            
            
            
            for v in p.getvars():
                if v in self.tablad:
                    for q in self.tablad[v]:
                        if set(q.getvars())<= svar:
                            if len(q.getvars()) == len(svar):
                                if p.implicadopor(q):
                                    return []
                            h = q.combina(p,inplace=False)
                            h.borra([v], inplace=True)
                            return self.insertar(h, small)
                            

            lista = []
            for v in p.getvars():
                if v in self.tabla:
                    for q in self.tabla[v]:
                        if q not in lista:
                            lista.append(q)

            
               
            for q in lista:
                if set(q.getvars())<= svar:
                    if len(q.getvars()) == len(svar):
                        if p.implicadopor(q):
                            return []
                    p.combina(q, inplace = True)
                    
                 

            
            dets = []
            for v in p.getvars():
                if p.checkdetermi(v):
                    t = p.minimizadep(v, seg = set())
                    # print("nuevo determinismo ", len(p.getvars()), len(t.getvars()))
                    if len(t.getvars())< len(p.getvars()):
                        t = small.simplifica(t)
                        l1 = self.insertar(t,small)
                        q = p.borra([v],inplace = False)
                        q = small.simplifica(q)
                        l2 = self.insertar(q,small)
                        return l1 + l2
                        
                
                    dets.append(v)
    

            


            

            lista = []


            for v in p.getvars():
                if v in self.tablad:
                    for q in self.tablad[v]:
                        if q not in lista:
                            lista.append(q)
                if v in self.tabla:
                    for q in self.tabla[v]:
                        if q not in lista:
                            lista.append(q)
            incl = False
            ins = []
            nd = []
            for q in lista:
                if svar <= set(q.getvars()):
                    r = q.combina(p,inplace = False)
                    if dets:
                        # print("obrrao ",vard, q.getvars())
                        r.borra([dets[0]],inplace = True)
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
                            return []
            for q in ins:
                nd = nd + self.insertar(q, small)
             
                        
            if dets:
                
                nd.append(p)


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
                # if len(p.getvars())<=4:
                #     print("Nueva pequeña ", len(p.getvars()))
                #     nd.append(p)
                for v in svar:
                    if v in self.tabla:
                            self.tabla[v].append(p)
                    else:
                            self.tabla[v] = [p]


                    
            return nd


        def insertard(self,p):
            # print("inserto ", p.getvars())
           
            if p.contradict():
                self.anula()
                return []
            

            if p.trivial():
                return []

            svar = set(p.getvars())
            
            
            
            for v in p.getvars():
                if v in self.tablad:
                    for q in self.tablad[v]:
                        if set(q.getvars())<= svar:
                            h = q.combina(p,inplace=False)
                            h.borra([v], inplace=True)
                            return self.insertard(h)
                                 
            det = False
            for v in p.getvars():
                if p.checkdetermi(v):
                    t = p.minimizadep(v, seg = set())
                    # print("nuevo determinismo ", len(p.getvars()), len(t.getvars()))
                    if len(t.getvars())< len(p.getvars()):
                        l1 = self.insertard(t)
                        q = p.borra([v],inplace = False)
                        l2 = self.insertard(q)
                        return l1+l2                        
                
                    det = True
                    var = v

                    break

            if det:
    
                lista = []

                tec = []
                for v in p.getvars():
                    if v in self.tablad:
                        for q in self.tablad[v]:
                            if q not in lista:
                                lista.append(q)
                    if v in self.tabla:
                        for q in self.tabla[v]:
                            if q not in lista:
                                lista.append(q)
                ins = []
                for q in lista:
                    if svar <= set(q.getvars()):
                        self.eliminar(q)
                        h = p.combina(q, inplace = False)
                        h.borra([var], inplace = True)
                        ins.append(h)
                
                for h in ins:
                    self.insertar(h)

                for v in svar-{var}:
                    if v in self.tabla:
                            self.tabla[v].append(p)
                    else:
                            self.tabla[v] = [p]

                if var in self.tablad:
                    self.tablad[var].append(p)
                else:
                    self.tablad[var] = [p]
                
                tec.append(p)
                
                return tec

            else:
                for v in svar:
                    if v in self.tabla:
                            self.tabla[v].append(p)
                    else:
                            self.tabla[v] = [p]


                    
            return []



        def eliminarc(self,cl):
            lvar = map(abs,cl)
            for v in lvar:
                    self.clau[v].remove(cl)
                





        def eliminar(self,p):
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
                        mat += 2**len(set(p.getvars()).union(q.getvars())) - 2**(len(q.getvars()))
                if v in self.tabla:
                    for q in self.tabla[v]:
                        if len(set(p.getvars()).union(q.getvars()))> mat:
                            mat += 2**len(set(p.getvars()).union(q.getvars())) - 2**(len(q.getvars()))
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

            return (mat + 2**(len(sset)))

                    
                        
        
  
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

            posc= pos.copy()

            for x in pos:
                x1 = len(self.tabla.get(x)) if self.tabla.get(x) else 0
                x2 = len(self.tablad.get(x)) if self.tablad.get(x) else 0
                if x1+x2 <= 1:
                    return x


            miv = min(posc,key = lambda x: self.tad(x))
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


        def mini(self,vorig,small, Q, trabajo, gorden=[], verb=True, M=15, H=40):
            
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


        def minid(self,Q, nue = False):
            
            vorig  = self.getvars()
            orden = []
            
            posvar = dict()
            trabajo = self.copia()


            while vorig and not self.contradict: 
                var = trabajo.siguientep(vorig)
                orden.append(var)
                posvar[var] = len(orden)-1


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
                
                       

                vorig.discard(var)


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
                
                if nue:
                    for p in nuevas:
                        self.insertarb2(p)


                self.orden = orden
                self.posvar = posvar

                # for p in nuevas:
                #     self.insertar(p)
                   

                
            return 



        def borraf(self,Q):
            
            vorig  = self.getvars()
            trabajo = self
            res = varpot()
            
            while vorig and not self.contradict: 
                var = trabajo.siguientep(vorig)
                print("var ", var, len(vorig),  trabajo.tad(var))

                list1 = trabajo.get(var)
                list2 = trabajo.getd(var)

                if trabajo.tad(var)>Q:
                    return res
                res.orden.append(var)
                


                for p in list1:
                    trabajo.eliminar(p)
                for p in list2:
                    trabajo.eliminar(p)

                n = len(list1) + len(list2)

                combinaincluidas(list1, K=0)
                eliminaincluidas(list1,list2)
                
                
                       

                vorig.discard(var)

                if not list2:
                    for p in list1:
                        if p.checkdetermi(var):
                            list1.remove(p)
                            list2.add(p)
                            print("nuevo")
                            sleep(30)
                            break

                if list2:
                    print("determinista")
                    pivote = min(list2, key = lambda x: len(x.getvars()))
                    res.insertarb2(pivote)
                    if n<=1:
                        h = pivote.borra([var], inplace = False)
                        trabajo.insertarb2(h)
                        
                            
                    
                    else:
                        for p in list1:
                                

                                pivote = min(list2, key=lambda x: len(set(p.getvars()).union(set(x.getvars()))))
                                if len(set(p.getvars()).union(set(pivote.getvars())))<= Q:
                                    h = pivote.combina(p)
                                    h = h.borra([var])
                                    trabajo.insertarb2(h)
                                else:
                                    print("error en limite")
                                    sleep(100)
                                
                                        


                        list2.sort(key = lambda x :  len(x.getvars()) )

                        while len(list2) > 1:
                                p = list2.pop()
                                pivote =  min(list2, key=lambda x: len(set(p.getvars()).union(set(x.getvars()))))
                                
                                if len(set(p.getvars()).union(set(pivote.getvars())))<= Q:
                                    h = pivote.combina(p)
                                    h = h.borra([var])
                                    trabajo.insertarb2(h)
                                

                                else:
                                    print("problema en limite")
                                    sleep(100)

                elif list1:
                    h = nodoTabla([])        

                    while list1:
                        r = list1.pop()
                        h = h.combina(r)
                    h = h.borra([var])
                    trabajo.insertarb2(h)





            return res
        
        def borra(self,Q=10):
            
            vorig  = self.getvars()
            trabajo = self.copia()
            compil = []
            orden = []


         


            
            
            while vorig and not self.contradict: 
                var = trabajo.siguientep(vorig)
                print("var ", var, len(vorig),  trabajo.tad(var))

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
                        if isinstance(h,arbol):
                            h.poda(Q)
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

                                if isinstance(h,arbol):
                                    if h.trivial():
                                        print("trivial")
                                    print("tam ", h.size())
                                    h.poda(Q)
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
                                if isinstance(h,arbol):
                                    print("tam ", h.size())
                                    h.poda(Q)

                                    print("tam ", h.size())
                                trabajo.insertarb2(h)
                                

                            

                elif list1:
                    h = nodoTabla([])        
                    combinaincluidas(list1, K=1)

                    if len(list1)==1:
                        h = list1[0]
                        h = h.borra([var])
                        trabajo.insertarb2(h)

                    else:
                        nt = len(list1)
                        for i in range(nt):
                            for j in range(i+1,nt):
                                h1 = list1[i]
                                h2 = list1[j]
                                h = h1.combina(h2)
                                h = h.borra([var])
                                if isinstance(h,arbol):
                                    print("tam ", h.size())
                                    h.poda(Q)

                                    print("tam ", h.size())
                                trabajo.insertarb2(h)


                    







        def siguienteb(self,config, pos):

            return max(pos, key = lambda x: self.tamb(x,config))

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