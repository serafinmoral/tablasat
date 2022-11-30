# -*- coding: utf-8 -*-
"""
Created on 31 Enero 2022

@author: Serafin
"""
from statistics import variance
from utils import *


class varpot:

        def __init__(self, Qin=20, partirin=True): #EDM

            self.tabla = dict()
            self.unit = set()
            self.contradict = False
            self.Q = Qin #EDM
            self.partir=partirin #EEDM          

        def anula(self):
            self.tabla = dict()
            self.unit = set()
            self.contradict = True

        def insertaru(self,v):
            self.reduce(v, inplace=True)
            self.unit.add(v)

        def getvars(self):
            res = set(map(abs,self.unit))
            for v in self.tabla:
                if self.tabla[v]:
                    res.add(v)

            return res


        def trivial(self):
            if self.unit:
                return False
            if self.tabla:
                for v in self.tabla:
                    if self.tabla[v]:
                        return False
            return True

        def checkdetermin(self):
            values = dict()
            for v in  self.tabla.keys():
                values[v] = 0.0
            i=0
            j=0
            for v in self.tabla.keys():
                j+=1
                determ=False
                lista = self.tabla[v]
                print("Variable ", v)
                for p in lista:
                    d = p.checkdetermi(v)

                    if d:
                        determ = True

                        print("determinista " , p.listavar)
                        q = p.minimizadep(v , seg = set())
                        print("minimo " , q.listavar)
                        l = len(q.listavar)
                        for w in q.listavar:
                            if not w ==v:
                                values[w] += 1.0/(2**(l-2))
                if determ:
                    i+=1
            # for v in self.tabla.keys():
            #     print(v, values[v])
            print(i,j)
            return max(values, key=values.get)





        def insertar(self,p):
            print("inserto alternativo !")
            if len(p.listavar) ==1:
                if p.contradict():
                    self.anula()
                    return
                if not p.trivial():
                    u = valord(p)
                    self.insertaru(u)
                    return
                else:
                    return 
            if self.unit:
                varsu = set(map(abs,self.unit))
                if varsu.intersection(set(p.listavar)):
                    varr = filter(lambda x: abs(x) in p.listavar, self.unit)
                    
                    p = p.reduce(varr,inplace=False)
                    self.insertar(p)
                    return 
            for v in p.listavar:
                if v in self.tabla:
                    self.tabla[v].append(p)
                else:
                    self.tabla[v] = [p]

        def reduce(self,v,inplace=True):
            new = set()
            res = self if inplace else  self.copia()
            if v in self.unit:
                res.unit.discard(v)
            elif -v in self.unit:
                res.anula()
            elif v in self.tabla:
                lista = res.get(v)
                res.borrarv(v)
                for p in lista:
                    q = p.reduce([v],inplace = False)
                    new.update(q.calculaunit())
                    res.insertar(q)
            elif -v in self.tabla:
                lista = res.get(-v)
                res.borrarv(-v)
                for p in lista:
                    q = p.reduce([v],inplace = False)
                    new.update(q.calculaunit())
                    res.insertar(q)

            for x in new:
                # print("nueva unidad " , x)
                res.reduce(x, inplace=True)
            return res


        def copia(self):
            res = varpot()
            res.unit = self.unit.copy()
            res.contradict = self.contradict
            for x in self.tabla.keys():
                res.tabla[x] = self.tabla[x].copy()
            return res




        def createfrompot(self,pot):
            self.contradict = self.contradict
            self.unit = pot.unit.copy()
            for p in pot.listap:
                self.insertar(p)


        

        def createfromlista(self,l):
            for p in l:
                self.insertar(p)


        def borrarpot(self,p):
            if len(p.listavar) == 1:
                v = p.listavar[0]
                if not p.tabla[0]:
                    self.unit.discard(-v)
                elif not p.tabla[1]:
                    self.unit.discard(v)
                return 
            for v in p.listavar:
                if v in self.tabla:
                    try:
                        self.tabla[v].remove(p)
                    except ValueError:
                        pass # or scream: thing not in some_list!self.tabla[v].remove(p)

        def borrarv(self,v):
            self.unit.discard(v)
            self.unit.discard(-v)
            if v in self.tabla:
                for p in self.tabla[v].copy():
                    self.borrarpot(p)
                del self.tabla[v]

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
            r = filter (lambda x: abs(x) not in proh, self.unit)
            h = filter ( lambda x: abs(x) not in proh, self.tabla.keys()  )
            if not h and r:
                x = self.unit.pop()
                self.unit.add(x)
                return abs(x)
            else:
                mav = max(h,key = lambda x: len(self.tabla.get(x)))
                return mav


        def borrafacil(self,vars,M=20,ver = False):
            orden = []
            listan = []
            listaq = []
            e = True
            nuevas = []
            antiguas = []
            while vars and not self.contradict:
                
                if self.tabla:
                    var = self.siguientep(vars)
                    lista = self.get(var)
                else:
                    var = vars.pop()
                    lista = []
                
                


                ordenaycombinaincluidas(lista,self)
                if ver:
                    print("var", var, "quedan ", len(vars))


                vars.discard(var)
                (exac,nuevas,antiguas) = self.marginalizae(var,M)
                if not exac:
                    print("borrado no exacto " )
                    e = False
                    return (e,orden,nuevas,antiguas)
                else:

                    orden.append(var)
                    listan.append(nuevas)
                    listaq.append(antiguas)
                
                    ordenaycombinaincluidas(nuevas,self)


            return(e,orden,nuevas,antiguas)


        
        def combina(self,rela, inplace=True):
            res = self if inplace else  self.copia()
            for u in rela.unit:
                res.insertaru(u)
            for v in rela.tabla:
                for p in rela.tabla[v]:
                    if min(p.listavar) ==v:
                        res.insertar(p)

            return res


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

        def marginalizaset2(self,vars,M = 30, Q=20, ver = True, inplace = True, pre = False, orden = []):
            if not pre:
                vars.intersection_update(self.getvars())
            
            if inplace:
                if not pre:
                    orden = []
                listan = []
                listaq = []
                nuevas = []
                if pre:
                    nvars = [x for x in orden if x in vars]
                    nvars.reverse()
                    vars = nvars
                e = True
                i = 0
                while vars and not self.contradict:
                    if pre:
                        var = vars.pop()
                    else:
                        var = self.siguientep(vars)
                    

                    
                    tama = tam(self.tabla.get(var))
                    lista = self.get(var)
                    
                    if not pre:
                        pos = vars.copy()
                        dif = 0
                        while pos and dif <=2:

                            met = calculamethod(lista,var)
                            if met == 1:
                                break
                            else:
                                if not pre:
                                    pos.discard(var)
                                
                                if pos:
                                    var = self.siguientep(pos)
                                    lista =self.get(var)
                                    dif = tam(self.tabla.get(var))- tama

                        if met==2:
                            var = self.siguientep(vars)
                            lista = self.get(var)


                    u.ordenaycombinaincluidas(lista,self, borrar = True, inter=False)
                    if ver:
                        print("var", var, "quedan ", len(vars))

                    if not pre:
                        vars.discard(var)
                    (exac,nuevas,antiguas) = self.marginaliza(var,M,Q)
                    if not exac:
                        print("borrado no exacto " )
                        e = i
                        return(e,orden,nuevas,listaq)
                    else:
                        i += 1
                    if not pre:
                        orden.append(var)
                    listan.append(nuevas)
                    listaq.append(antiguas)
                    if not self.contradict:
                        u.ordenaycombinaincluidas(nuevas,self, borrar=True)

                e = i
                return(e,orden,nuevas,listaq)
            else:
                res = self.copia()
                res.marginalizaset(vars,M , Q, ver , inplace = True)

                return res


        def marginalizaset(self,vars,M = 30, Q=20, ver = True, inplace = True, pre = False, orden = []):
            if not pre:
                vars.intersection_update(self.getvars())
            
            if inplace:
                if not pre:
                    orden = []
                listan = []
                listaq = []
                nuevas = []
                if pre:
                    nvars = [x for x in orden if x in vars]
                    nvars.reverse()
                    vars = nvars
                e = True
                while vars and not self.contradict:
                    if pre:
                        var = vars.pop()
                    else:
                        var = self.siguientep(vars)
                    

                    
                    tama = tam(self.tabla.get(var))
                    lista = self.get(var)
                    
                    if not pre:
                        pos = vars.copy()
                        dif = 0
                        while pos and dif <=2:

                            met = calculamethod(lista,var)
                            if met == 1:
                                break
                            else:
                                if not pre:
                                    pos.discard(var)
                                
                                if pos:
                                    var = self.siguientep(pos)
                                    lista =self.get(var)
                                    dif = tam(self.tabla.get(var))- tama

                        if met==2:
                            var = self.siguientep(vars)
                            lista = self.get(var)


                    u.ordenaycombinaincluidas(lista,self, borrar = True, inter=False)
                    if ver:
                        print("var", var, "quedan ", len(vars))

                    if not pre:
                        vars.discard(var)
                    (exac,nuevas,antiguas) = self.marginaliza(var,M,Q)
                    if not exac:
                        print("borrado no exacto " )
                        e = False
                    if not pre:
                        orden.append(var)
                    listan.append(nuevas)
                    listaq.append(antiguas)
                    if not self.contradict:
                        u.ordenaycombinaincluidas(nuevas,self, borrar=True)


                return(e,orden,nuevas,listaq)
            else:
                res = self.copia()
                res.marginalizaset(vars,M , Q, ver , inplace = True)

                return res


        
        def extraelista(self):
            lista = []
            for v in self.tabla:
                for p in self.tabla[v]:
                    if min(p.listavar) == v:
                        lista.append(p)
            return lista

        def atabla(self):
            res = nodoTabla([])
            for v in self.unit:
                res.combina(potdev(v), inplace=True)
            for v in self.tabla:
                for p in self.tabla[v]:
                    if min(p.listavar) == v:
                        res.combina(p, inplace=True)
            return res

        def mejoralocal(self,M=25,Q=20,N=2):

            
            listap = self.extraelista()        

            for p in listap:                
                    old = np.sum(p.tabla)
                    vars = set(p.listavar)
                    nvars = vars.copy()
                    tvars = set(p.listavar)
                    lista = []
                    for i in range(N):
                        for v in nvars:
                            for q in self.tabla[v]:
                                if not q in lista:
                                    lista.append(q)
                                    qv = set(q.listavar)
                                    tvars.update(qv)
                            nvars = tvars-vars
                            vars = tvars.copy()
                    

                    r = varpot()
                    r.createfromlista(lista)
                    
                    r.marginalizaset(tvars-set(p.listavar),M,self.Q, ver=False) #EDM
                    nl = r.extraelista()
                    lk = nodoTabla([])
                    for q in nl:
                        lk.combina(q,inplace=True)
                    
                    
                    ns = np.sum(lk.tabla)

                    if (ns < old):
                        # print("mejora", ns, old,len(p.listavar), len(lk.listavar)) #EDM
                        self.borrarpot(p)
                        self.insertar(lk)

                    



        def siguientep(self,pos):

            if self.unit:
                varu = set(map(abs,self.unit))
                if varu.intersection(pos):
                    x = varu.pop()
                
                    return x

            miv = min(pos,key = lambda x: len(self.tabla.get(x)) if self.tabla.get(x) else 0)
            mav = max(pos,key = lambda x: len(self.tabla.get(x)) if self.tabla.get(x) else 0)

            # print(miv,mav,len(self.tabla.get(miv)),len(self.tabla.get(mav)))

            if not self.tabla.get(miv) or  len(self.tabla.get(miv)) == 1:
                # print("un solo potencial !!!!!!!!!!!!!!!!")
                return (miv)
            miv = min(pos,key = lambda x: tam(self.tabla.get(x)) if self.tabla.get(x) else 0)
            mav = max(pos,key = lambda x: tam(self.tabla.get(x)) if self.tabla.get(x) else 0)
            # print (miv,mav,tam(self.tabla.get(miv)),tam(self.tabla.get(mav)))
            return miv

        def get(self,i, deep=True):
            if deep:
                return self.tabla.get(i,[]).copy()
            else:
                return self.tabla.get(i,[])




                    
                

