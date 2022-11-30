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


def ordena(l,Q):

    lc = l.copy()
    l.clear()

    while lc:
        q = min(lc, key = lambda x: len(x.listavar))
        lc.remove(q)
        l.append(q)
        lista = set(q.listavar)
        while lc:
            q = min(lc, key = lambda x: len(lista.union(set(x.listavar))))
            if len(lista.union(set(q.listavar)))<=Q:
                lc.remove(q)
                l.append(q)
                lista.update(set(q.listavar))
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
                res.update(set(p.listavar))
         


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
                    for w in p.listavar:
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
                        nueva = p.borra([var], inplace = False)
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

                n1 = min(list1, key = lambda x: len(x.listavar))

                n2 = min(list2, key = lambda x: len(set(x.listavar).union(set(n1.listavar))))

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
                    
                    if len(set(p.listavar)-vars )<=1:
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
                        print("aprendo ", nueva.listavar)
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
                    n1 = min(list1, key = lambda x: len(x.listavar))

                    n2 = min(list2, key = lambda x: len(set(x.listavar).union(set(n1.listavar))))

                    if (len(set(n1.listavar).union(set(n2.listavar))))<= M:
                        nueva = n1.combina(n2, inplace = False)
                        nueva.borra([var], inplace=True)
                        print("aprendo ", nueva.listavar, 2**(len(nueva.listavar)), np.sum(nueva.tabla))
                        
                        if n1 in self.getd(var):
                            if n2 in self.getd(var):
                                if len(n2.listavar) < len(n1.listavar): 
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
                        cl = set(filter(lambda x: abs(x) in n1.listavar or abs(x) in n2.listavar,config))
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
                    n1 = min(list1, key = lambda x: len(x.listavar))
                    cl2 = l2[0]
                    if n1 in self.getd(var):

                        self.eliminarc(cl2)
                    cl = set(filter(lambda x: abs(x) in n1.listavar or x in cl2,config))
                    todas = self.insertarclau(cl) 
                    level = max([self.level(x) for x in todas])
                    del config[-(level-oldl):]
                    pos = pos + orden[-(level-oldl)-1:]
                    del orden[-(level-oldl)-1:]
                    continue

                if list2 and l1:
                    cl1 = l1[0]
                    n2 = min(list2, key = lambda x: len(x.listavar))
                    if n2 in self.getd(var):
                            self.eliminarc(cl1)


                    cl = set(filter(lambda x: abs(x) in n2.listavar or x in cl1,config))
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
                        print ("error " ,p.listavar)
            

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
            print("empiezo a reduce e insertar")
            for p in lista:
                print(v,p.listavar)
                q = p.reduce({v})
                print(q.listavar)
               
                res.insertarb2(q)

            print("termino")
             
            return res
            
            
 
        def simplifica(self,p):
            if p.trivial():
                return nodoTabla([])
            
            if p.contradict():
                res = nodoTabla([])
                res.anula()
                return res

            res = p.copia()

            svar = set(p.listavar)
            
            # for v in p.listavar:
            #     if v in self.tablad:
            #         for q in self.tablad[v]:
            #             if set(q.listavar)<= svar:
            #                 h = q.combina(p,inplace=False)
            #                 h.borra([v], inplace=True)
            #                 return self.simplifica(h)
                            

            lista = []
            for v in p.listavar:
                if v in self.tabla:
                    for q in self.tabla[v]:
                        if q not in lista:
                            lista.append(q)

            for v in p.listavar:
                if v in self.tablad:
                    for q in self.tablad[v]:
                        if q not in lista:
                            lista.append(q)
               
            for q in lista:
                if set(q.listavar)<= svar:
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

            svar = set(p.listavar)
            
            # ol = sorted(p.listavar,key = lambda x : self.posvar[x])

            ol = p.listavar
    
            for v in ol:
                if v in self.tablad:
                    for q in sorted(self.tablad[v], key = lambda x: len(x.listavar)):
                        if set(q.listavar)<= svar:
                            h = q.combina(p,inplace=False)
                            h.borra([v], inplace=True)
                            (h1,l1) = self.simplificat(h)
                            l1.append(q)
                            return (h1,l1)
                      
            res = p.copia()

            lista = []
            for v in p.listavar:
                if v in self.tabla:
                    for q in self.tabla[v]:
                        if q not in lista:
                            lista.append(q)

           
               
            for q in lista:
                if set(q.listavar)<= svar:
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
            svar = set(p.listavar)

            for v in p.listavar:
                if v in self.tablad and not v==var:
                    for q in self.tablad[v]:
                        if set(q.listavar)<= svar:
                            h = q.combina(p,inplace=False)
                            h.borra([v], inplace=True)
                            self.insertarb(h)

            if p.checkdetermi(var):
                    t = p.minimizadep(var, seg = set())
                    # print("nuevo determinismo ", len(p.listavar), len(t.listavar))
                    if len(t.listavar)< len(p.listavar):
                        self.insertarb(t)
                        q = p.borra([var],inplace = False)
                        self.insertarb(q)
                    else:
                        if var in self.tablad:
                            self.tablad[var].append(p)
                        else:
                            self.tablad[var] = [p]

                        for v in p.listavar:
                            if v in self.tablat:
                                self.tablat[v].append(p)
                            else:
                                self.tablat[v] = [p]

                    lista = self.tablat.get(var,[])
                    listn = self.get(var) + self.getd(var)
                    for q in lista:
                        if not q in listn:
                            if svar <= set(q.listavar):
                                self.eliminarb(q)
                                h = q.combina(p, inplace = False)
                                h.borrar([var], inplace=True)
                                self.insertarb(h)
            else:
                if var in self.tabla:
                    self.tabla[var].append(p)
                else:
                    self.tabla[var] = [p]

                for v in p.listavar:
                    if v in self.tablat:
                        self.tablat[v].append(p)
                    else:
                        self.tablat[v] = [p]   



                        
        def insertarb2(self,p):
            if p.contradict():
                self.anula()
                return []
            

            if p.trivial():
                return []

         
            svar = set(p.listavar)

            for v in p.listavar:
                if v in self.tablad:
                    for q in self.tablad[v]:
                        if set(q.listavar)<= svar:
                            h = q.combina(p,inplace=False)
                            h.borra([v], inplace=True)
                            return self.insertarb2(h)
            n = len(p.listavar)
            lista = []
            for v in p.listavar:
                if v in self.tabla: 
                    for q in self.tabla[v]:
                        if q not in lista:
                            lista.append(q)

            le = filter(lambda x: len(x.listavar)==n, lista)

            for q in le:
                if  set(q.listavar)==svar:
                    p.combina(q, inplace=True)
                    self.eliminar(q)

            if len(p.listavar)<=20:
                for v in p.listavar:
                    if p.checkdetermi(v):
                        var = v
                        t = p.minimizadep(v, seg = set())
                        # print("nuevo determinismo ", len(p.listavar), len(t.listavar))
                        if len(t.listavar)< len(p.listavar):
                            l1 = self.insertarb2(t)
                            q = p.borra([var],inplace = False)
                            l2 = self.insertarb2(q)
                            return l1 + l2
                        else:
                            
                            res = [p.listavar]
                            lista = []
                            for v in p.listavar:
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
                                    if svar <= set(q.listavar):
                                        
                                        self.eliminar(q)
                                        h = q.combina(p, inplace = False)
                                        h.borra([var], inplace=True)
                                        ins.append(h)

                            for h in ins:
                                res = res + self.insertarb2(h)


                            if var in self.tablad:
                                    self.tablad[var].append(p)
                            else:
                                    self.tablad[var] = [p]

                            for v in p.listavar:
                                    if not v == var:
                                        if v in self.tabla:
                                            self.tabla[v].append(p)
                                        else:
                                            self.tabla[v] = [p]
                        return res
            
            
            res= [p.listavar]
            for v in p.listavar:
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
                        if set(q.listavar)<= svar:
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
                if svar <= set(q.listavar):
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

            for v in p.listavar:
                self.tablat[v].remove(p)

        def insertar(self,p, small = [], vc = -1):
            # print("inserto ", p.listavar)

     

            
           

            if not small:
                small = self


            if p.contradict():
                self.anula()
                return []
            

            if p.trivial():
                return []

            svar = set(p.listavar)
            
            
            
            for v in p.listavar:
                if v in self.tablad:
                    for q in self.tablad[v]:
                        if set(q.listavar)<= svar:
                            if len(q.listavar) == len(svar):
                                if p.implicadopor(q):
                                    return []
                            h = q.combina(p,inplace=False)
                            h.borra([v], inplace=True)
                            return self.insertar(h, small)
                            

            lista = []
            for v in p.listavar:
                if v in self.tabla:
                    for q in self.tabla[v]:
                        if q not in lista:
                            lista.append(q)

            
               
            for q in lista:
                if set(q.listavar)<= svar:
                    if len(q.listavar) == len(svar):
                        if p.implicadopor(q):
                            return []
                    p.combina(q, inplace = True)
                    
                 

            
            dets = []
            for v in p.listavar:
                if p.checkdetermi(v):
                    t = p.minimizadep(v, seg = set())
                    # print("nuevo determinismo ", len(p.listavar), len(t.listavar))
                    if len(t.listavar)< len(p.listavar):
                        t = small.simplifica(t)
                        l1 = self.insertar(t,small)
                        q = p.borra([v],inplace = False)
                        q = small.simplifica(q)
                        l2 = self.insertar(q,small)
                        return l1 + l2
                        
                
                    dets.append(v)
    

            


            

            lista = []


            for v in p.listavar:
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
                if svar <= set(q.listavar):
                    r = q.combina(p,inplace = False)
                    if dets:
                        # print("obrrao ",vard, q.listavar)
                        r.borra([dets[0]],inplace = True)
                        # print("añado ", vard, r.listavar)
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
                        elif len(q.listavar)==len(p.listavar):
                            return []
            for q in ins:
                nd = nd + self.insertar(q, small)
             
                        
            if dets:
                
                nd.append(p)


                for v in p.listavar:
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
                # if len(p.listavar)<=4:
                #     print("Nueva pequeña ", len(p.listavar))
                #     nd.append(p)
                for v in svar:
                    if v in self.tabla:
                            self.tabla[v].append(p)
                    else:
                            self.tabla[v] = [p]


                    
            return nd


        def insertard(self,p):
            # print("inserto ", p.listavar)
           
            if p.contradict():
                self.anula()
                return []
            

            if p.trivial():
                return []

            svar = set(p.listavar)
            
            
            
            for v in p.listavar:
                if v in self.tablad:
                    for q in self.tablad[v]:
                        if set(q.listavar)<= svar:
                            h = q.combina(p,inplace=False)
                            h.borra([v], inplace=True)
                            return self.insertard(h)
                                 
            det = False
            for v in p.listavar:
                if p.checkdetermi(v):
                    t = p.minimizadep(v, seg = set())
                    # print("nuevo determinismo ", len(p.listavar), len(t.listavar))
                    if len(t.listavar)< len(p.listavar):
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
                for v in p.listavar:
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
                    if svar <= set(q.listavar):
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
            for v in p.listavar:
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
            
            return  max(pos,key = lambda x: len(self.get(x)) + len(self.getd(x)) )
                


     



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

            
            if exact and lista and not lista[0].listavar:
                if lista[0].contradict():
                    print ("contradict")
                    self.anula()    
                    return(True,lista,listaconvar)
            for p in lista:
                if p.contradict():
                    print ("contradict")

                    self.anula()
                else:
                    # print(p.listavar)
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
            
            if exact and lista and not lista[0].listavar:
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
                                dif = set(p.listavar)-set(q.listavar)
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
            if not p.listavar:
                if p.trivial():
                    return False
                if p.contradict() and self.contradict:
                    return True
                else:
                    return False
            v = p.listavar[0]
            if v in self.tabla and p in self.tabla[v]:
                return True
            if v in self.tablad and p in self.tablad[v]:
                return True
            return False

        def estad(self,p):
            if not p.listavar:
                if p.trivial():
                    return False
                if p.contradict() and self.contradict:
                    return True
                else:
                    return False
            
            for v in p.listavar:

                if  p in self.tablad.get(v,[]):
                    
                    return True
            return False

        def pos(self,p):
            return min([self.posvar[x] for x in p.listavar])
  
 
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
                    #     print("lista 1", p.listavar)
                    # for p in list2:
                    #     print("lista 2", p.listavar)    
                  

                    for p in list1:
                        # print(p.listavar)
                        trabajo.eliminar(p)
                    for p in list2:
                        # print(p.listavar)

                        trabajo.eliminar(p)
                    n = len(list1) + len(list2)
                    nd = []
                    traba = []
                    nuevas = []
                    if  x1 < x2:
                        if verb:
                            print("incluir ")
                        lists = small.tablad.get(var,[])
                        lists2 = list(filter(lambda x: set(x.listavar) <= set(vorig), lists))
                        if lists2:
                            if verb:
                                print("heredo determinismo", len(list1))
                           
                            p = min(lists2, key = lambda x: len(x.listavar))
                            list2.append(p)
                            # if solved:
                            #     print("inserto p ", p.listavar)
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
                        pivote = min(list2, key = lambda x: len(x.listavar))
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
                                

                                pivote = min(list2, key=lambda x: len(set(p.listavar).union(set(x.listavar))))
                                if len(set(p.listavar).union(set(pivote.listavar)))<= Q:
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
                                list2.sort(key = lambda x :  len(x.listavar) )
                                p = list2.pop()
                                pivote =  min(list2, key=lambda x: len(set(p.listavar).union(set(x.listavar))))
                                
                                if len(set(p.listavar).union(set(pivote.listavar)))<= Q:
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
                                    # print(len(h.listavar),len(l1))
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
                                if len(set(h.listavar).union(set(q.listavar)))<= Q or not h.listavar:
                                    h.combina(q,inplace=True)
                                else:
                                    h.borra([var],inplace=True)

                                    nd = nd+  trabajo.insertar(h,small)
                                    nuevas.append(h)
                                    h = nodoTabla([])
                                    h.combina(q,inplace=True)

                            h.borra([var], inplace=True)
                            # print(len(h.listavar))
                            (h,l1) = trabajo.simplificat(h)
                            (h,l1) = small.simplificat(h)
                            # print(len(h.listavar),len(l1))
                            # sleep(1)
                            nd = nd+  trabajo.insertar(h, small)
                            nuevas.append(h)
                            for r in l1:
                                nd = nd + trabajo.insertar(r,small)
                                # if solved:
                                #     self.insertar(r)

                    for p in nd:
                        porins = porins + small.insertar(p)
                        if len(p.listavar)<=2:
                            self.insertar(p)
        

                    for p in nuevas:
                        if not p in nd and len(p.listavar)<=M:
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
                #             if len(p.listavar)<=20:
                #                 trabajo.insertar(p)

                # for v in vars:
                #     if not v in trabajo.tablad or not trabajo.tablad[v]:
                #         if v in small.tablad and small.tablad[v]:
                #             p = min(small.tablad[v], key = lambda x: len(x.listavar))
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
                    #     print("lista 1", p.listavar)
                    # for p in list2:
                    #     print("lista 2", p.listavar)    

                    for p in list1:
                        # print(p.listavar)
                        trabajo.eliminar(p)
                    for p in list2:
                        # print(p.listavar)

                        trabajo.eliminar(p)

                    if not list2 and len(list1)>3:
                            lists = small.tablad.get(var,[])
                            lists2 = list(filter(lambda x: set(x.listavar) <= set(vorig), lists))
                            if lists2:
                                print("heredo determinismo", len(list1))
                                p = min(lists2, key = lambda x: len(x.listavar))
                                list2.append(p)
                            


                    n = len(list1) + len(list2)
                    nd = []
                    traba = []
                    nuevas = []
                    if list2:
                        det = True
                        print("determinista")
                        pivote = min(list2, key = lambda x: len(x.listavar))
                        if n<=1:
                            h = pivote.borra([var], inplace = False)
                            h = small.simplifica(h)
                            nd = nd + trabajo.insertar(h,small)
                            nuevas.append(h)
                    
                        else:
                            for p in list1:
                                

                                pivote = min(list2, key=lambda x: len(set(p.listavar).union(set(x.listavar))))
                                if len(set(p.listavar).union(set(pivote.listavar)))<= Q:
                                    h = pivote.combina(p, inplace = False)
                                    h.borra([var], inplace =True)
                                    h = small.simplifica(h)
                                    nd = nd + trabajo.insertar(h,small)
                                    nuevas.append(h)


                                else:
                                    solved = False
                                    traba.append(p)
                            while len(list2) > 1:
                                list2.sort(key = lambda x :  len(x.listavar) )
                                p = list2.pop()
                                pivote =  min(list2, key=lambda x: len(set(p.listavar).union(set(x.listavar))))
                                
                                if len(set(p.listavar).union(set(pivote.listavar)))<= Q:
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
                                if len(set(h.listavar).union(set(q.listavar)))<= Q or not h.listavar:
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
                        if not p in nd and len(p.listavar)<=M:
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
                    if min(p.listavar) == v:
                        lista.append(p)
            return lista

    
        def tadm(self,v):
            mat = 0
            if v in self.tablad and self.tablad[v]:
                # print(self.tablad[v])
                p = min (self.tablad[v], key = lambda x: len(x.listavar))
                for q in self.tablad[v]:
                    if not q==p:
                        mat += 2**len(set(p.listavar).union(q.listavar)) - 2**(len(q.listavar))
                if v in self.tabla:
                    for q in self.tabla[v]:
                        if len(set(p.listavar).union(q.listavar))> mat:
                            mat += 2**len(set(p.listavar).union(q.listavar)) - 2**(len(q.listavar))
                return mat

            sset = set()
            if v in self.tabla:
                for q in self.tabla[v]:
                    sset.update(set(q.listavar))
                    mat += - 2**(len(q.listavar))
            if v in self.tablad:
                for q in self.tablad[v]:
                    sset.update(set(q.listavar))
                    mat += - 2**(len(q.listavar))

            return (mat + 2**(len(sset)))

                    
                        
        
  
        def tadref(self,v, small, rest):
            mat = 0
            lista = self.getd(v)
            
            lista2 = list(filter(lambda x: set(x.listavar) <=rest, small.tablad.get(v,[])))

            if lista2:
                p = min(lista2, key = lambda x: len(x.listavar))
                lista.append(p)
            if lista:
                # print(self.tablad[v])
                p = min (lista, key = lambda x: len(x.listavar))
                for q in lista:
                    if len(set(p.listavar).union(q.listavar))> mat:
                        mat = len(set(p.listavar).union(q.listavar))
                if v in self.tabla:
                    for q in self.tabla[v]:
                        if len(set(p.listavar).union(q.listavar))> mat:
                            mat = len(set(p.listavar).union(q.listavar))

                return mat

            sset = set()
            if v in self.tabla:
                for q in self.tabla[v]:
                    sset.update(set(q.listavar))
            if v in self.tablad:
                for q in self.tablad[v]:
                    sset.update(set(q.listavar))
            return (len(sset))

                    
                       
  
        def tad(self,v):
            mat = 0
            if v in self.tablad and self.tablad[v]:
                # print(self.tablad[v])
                p = min (self.tablad[v], key = lambda x: len(x.listavar))
                for q in self.tablad[v]:
                    if len(set(p.listavar).union(q.listavar))> mat:
                        mat = len(set(p.listavar).union(q.listavar))
                if v in self.tabla:
                    for q in self.tabla[v]:
                        if len(set(p.listavar).union(q.listavar))> mat:
                            mat = len(set(p.listavar).union(q.listavar))
                return mat

            sset = set()
            if v in self.tabla:
                for q in self.tabla[v]:
                    sset.update(set(q.listavar))
            if v in self.tablad:
                for q in self.tablad[v]:
                    sset.update(set(q.listavar))

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
                    lists2 = list(filter(lambda x: set(x.listavar) <= set(vorig), lists))
                    if lists2:
                        if verb:
                            print("heredo determinismo", len(list1))
                        
                        p = min(lists2, key = lambda x: len(x.listavar))
                        list2.append(p)
                       

                vorig.discard(var)

                if list2:
                    det = True
                    if verb:
                        print("determinista")
                    pd+=1
                    pivote = min(list2, key = lambda x: len(x.listavar))
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
                            

                            pivote = min(list2, key=lambda x: len(set(p.listavar).union(set(x.listavar))))
                            if len(set(p.listavar).union(set(pivote.listavar)))<= QV:
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
                            list2.sort(key = lambda x :  len(x.listavar) )
                            p = list2.pop()
                            pivote =  min(list2, key=lambda x: len(set(p.listavar).union(set(x.listavar))))
                            
                            if len(set(p.listavar).union(set(pivote.listavar)))<= QV:
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
                                # print(len(h.listavar),len(l1))
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
                        
                            if len(set(h.listavar).union(set(q.listavar)))<= QV or not h.listavar:
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
                    if len(p.listavar)<=2:
                        self.insertar(p)


                for p in nuevas:
                    if not p in nd and len(p.listavar)<=M:
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
                   
                    pivote = min(list2, key = lambda x: len(x.listavar))
                    if n<=1:
                        h = pivote.borra([var], inplace = False)
                        nd = nd + trabajo.insertard(h)
                        nuevas.append(h)
                      
                          
                
                    else:
                        for p in list1:
                            

                            pivote = min(list2, key=lambda x: len(set(p.listavar).union(set(x.listavar))))
                            if len(set(p.listavar).union(set(pivote.listavar)))<= Q:
                                h = pivote.combina(p, inplace = False)
                                h.borra([var], inplace =True)
                                nd = nd + trabajo.insertar(h)
                                nuevas.append(h)
                               
                                    



                            else:
                                traba.append(p)
                        list2.sort(key = lambda x :  len(x.listavar) )

                        while len(list2) > 1:
                            p = list2.pop()
                            pivote =  min(list2, key=lambda x: len(set(p.listavar).union(set(x.listavar))))
                            if len(set(p.listavar).union(set(pivote.listavar)))<= Q:
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
                    ordena(list1,Q)
                    if list1:
                        for q in list1:
                        
                            if len(set(h.listavar).union(set(q.listavar)))<= Q or not h.listavar:
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
                print("var ", len(vorig),  trabajo.tad(var))

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
                
                
                       

                vorig.discard(var)

                if list2:
                    print("determinista")
                    pivote = min(list2, key = lambda x: len(x.listavar))
                    res.insertarb2(pivote)
                    if n<=1:
                        h = pivote.borra([var], inplace = False)
                        trabajo.insertarb2(h)
                        
                            
                    
                    else:
                        for p in list1:
                                

                                pivote = min(list2, key=lambda x: len(set(p.listavar).union(set(x.listavar))))
                                if len(set(p.listavar).union(set(pivote.listavar)))<= Q:
                                    h = pivote.combina(p, inplace = False)
                                    h.borra([var], inplace =True)
                                    trabajo.insertarb2(h)
                                else:
                                    print("error en limite")
                                    sleep(100)
                                
                                        


                        list2.sort(key = lambda x :  len(x.listavar) )

                        while len(list2) > 1:
                                p = list2.pop()
                                pivote =  min(list2, key=lambda x: len(set(p.listavar).union(set(x.listavar))))
                                
                                if len(set(p.listavar).union(set(pivote.listavar)))<= Q:
                                    h = pivote.combina(p, inplace = False)
                                    h.borra([var], inplace =True)
                                    trabajo.insertarb2(h)
                                

                                else:
                                    print("problema en limite")
                                    sleep(100)

                elif list1:
                    h = nodoTabla([])        

                    while list1:
                        r = list1.pop()
                        h.combina(r, inplace=True)
                    h.borra([var], inplace =True)
                    trabajo.insertarb2(h)





            return res

        def siguienteb(self,config, pos):

            return max(pos, key = lambda x: self.tamb(x,config))

        def tamb(self,v,config):
            lista = self.get(v) + self.getd(v)

            vars = set(map(abs,config))
            s = 0
            for p in lista:
                dif = set(p.listavar) - vars
                if len(dif) > 1:
                    s+= 1.0/(len(dif) -1)
                else:
                    h = p.reduce(config, inplace=False)
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