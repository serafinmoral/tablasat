# -*- coding: utf-8 -*-
"""
Created on Tue Oct 19 20:13:39 2021

@author: efrai
"""

from operator import index
import time

from numpy import False_
from SimpleClausulas import *
from tablaClausulas import *
from utils import *
import random as ra
from time import *
from vartablasd import *







class problemaTrianFactor:
    def __init__(self,info=None,M=30, Qin=20, Partirin=True): #EDM
         self.M = M
         self.inicial = info
         self.pinicial = PotencialTabla()
         self.rela = varpot() #EDM
         self.orden = []
         self.porden = []
         self.clusters = []
         self.uclusters = []
         self.disa = []
         self.lqueue  = []
         self.ldeter = []
         self.lprev = []
         self.lfloat = []
         self.posvar = dict()
         self.sol = set()
         self.borr = []
         self.child = []
         self.parent = []
         if info:
            self.contradict = info.contradict
         self.evid = set()
         self.toriginalfl = []
         self.Q=Qin  #EDM
         self.Partir=Partirin #EDM

         



    def  cuclusters(self):
        ant = set()
        for i in range (len(self.clusters)):
            nuevo = ant.union(self.clusters[i])
            self.uclusters.append(nuevo)
            ant = nuevo
        self.disa.append(self.clusters[0].copy())
        for i in range (1,len(self.clusters)):
            self.disa.append(self.uclusters[i]-self.uclusters[i-1])
        for i in range (len(self.clusters)):
            print(i,self.disa[i])

        

    def inicia0(self):

            
            self.pinicial.computefromsimple(self.inicial)

    def inicia1(self):
        self.rela.orden = self.orden
        self.rela.posvar = self.posvar
        
        self.inserta(self.pinicial)    





    def previo(self, Q = 2, pre = False):
        print("entro en previo")
        if pre:
            return

        for x in self.pinicial.unit:
            # print("unitaria ", x)
            self.porden.append(abs(x))
            t = potdev(x)
            self.lprev.append(t)
        self.pinicial.unit = set()


        vars = self.pinicial.getvars()

        

        


        total = 0
        for K in range(2,Q+1):
            varb = []
            potb = []
        
            total = 1
            while total >0:
                total = 0
                i=0
                while i < len(self.pinicial.listap):
                    p = self.pinicial.listap[i]
                    if len(p.listavar) <= K:
                        for v in p.listavar:
                                deter = p.checkdetermi(v)
                                if deter:
                                    varb.append(v)
                                    potb.append(p)
                                    self.porden.append(v)
                                    self.lprev.append(p)
                                    print("variable ", v, " determinada ", p.listavar)
                                    print(p.tabla)
                                    self.borrad(v,p)
                                    total += 1
                                    break
                    i+= 1
                print(total)
        if self.pinicial.contradict:
            self.contradict = True
        return (varb,potb)

    def borrad(self,v,p):
        
        bor = []
        tota = set()
        for i in range(len(self.pinicial.listap)):
            q = self.pinicial.listap[i]
            if v in q.listavar:
                # print("var pot", q.listavar)
                if q == p:
                    h = q.borra([v],inplace = False)
                    if h.trivial():
                        bor.append(h)
                    
                else:
                    h = q.combina(p,inplace = False, des= False)
                    h.borra([v], inplace = True)
                    if h.trivial():
                        bor.append(h)
                        # print("trivial 2")
                        # sleep(1)
                    if h.contradict():
                        self.anula()
                        print("contradictorio")
                self.pinicial.listap[i] = h
                
        for q in bor:
            self.pinicial.listap.remove(q)



    def anula(self):

        for i in range(len(self.orden)):
            self.lqueue[i] = []
            self.ldeter[i] = []
        self.contradict = True

           
    def insertaunit(self,x):
       
        pot =  potdev(x)
        self.rela.insertar(pot)

            

    

    def insertacolapot(self,p, check=True):
            # print("inserto ", p.listavar)
            # sleep(0.2)
            if p.contradict():
                self.anula()
                return
            if p.trivial():
                # print("trivial")
                return
            vcl = p.listavar
            vcls = set(vcl)

            if check:
                for v in vcl:
                    pos = self.posvar[v]
                    for z in self.ldeter[pos]:
                        if set(z.listavar) <= vcls:
                            p.combina(z,inplace=True)
                            p.borra([v], inplace=True)
                            self.insertacolapot(p,check = True )
                            print("eliminando " , v)
                            return

            if vcl:
                up = False
                pup = None
                pos = min(map(lambda h: self.posvar[h], vcl))
                var = self.orden[pos]
                # print(var)
                if self.ldeter[pos]:
                    # print("hay determinista")
                    h = self.ldeter[pos][0]
                    # print(h.listavar)
                    if len(vcl)<len(h.listavar):
                        d = p.checkdetermi(var)
                        if d:
                            lista = self.ldeter[pos].copy()
                            p1 = p.minimizadep(var, seg=set())
                            self.ldeter[pos] = [p1]
                            up = True
                            pup = p1

                            h = p.borra([var],inplace=False)
                            self.insertacolapot(h)
                            
                            for q in lista:
                                if set(q.listavar) <= set(p1.listavar):
                                    q.combina(p1, inplace=True)
                                    q.borra([var],inplace=True)
                                    self.insertacolapot(q, check=True)
                                else:
                                    self.lqueue[pos].append(q)
                            return
                        else:
                            if set(h.listavar)<= set(p.listavar):
                                q = p.combina(h,inplace=False)
                                q.borra([var], inplace=True)
                                self.insertacolapot(q, check = True)
                        
                                return
                            else:
                                self.lqueue[pos].append(p)
                    else:
                        if set(p.listavar) <= set(h.listavar):
                            q = p.combina(h,inplace=False)
                            q.borra([var], inplace=True)
                            self.insertacolapot(q, check = True)
                            return
                        else:
                            self.lqueue[pos].append(p)


                else:
                    # print("no hay determinista")
                    lista = self.lqueue[pos].copy()
                    for q in lista:
                        if set(q.listavar)<= vcls or vcls <= set(q.listavar) :
                            p.combina(q,inplace=True)
                            self.lqueue[pos].remove(q) 
                        

                    d = p.checkdetermi(var)
                    if d:
                        print("nuevo determinismo")

                        # print(p.listavar,var)
                        p1 = p.minimizadep(var, seg=set())
                        up = True
                        pup = p1
                        h = p.borra([var],inplace=False)
                        self.insertacolapot(h)
                        self.ldeter[pos] = [p1]
                        lista = self.lqueue[pos].copy()
                        ins = []
                        for q in lista:
                            if set(p1.listavar) <= set(q.listavar):
                                self.lqueue[pos].remove(q)
                                q.combina(p1, inplace=True)
                                q.borra([var],inplace=True)
                                ins.append(q)
                        for q in ins:
                            self.insertacolapot(q,check=True)
                    else:
                        self.lqueue[pos].append(p)

                if up and len(pup.listavar)<=30:
                    print("simplifica arriba ", pup.listavar)
                    vas = set(pup.listavar)
                    i = pos-1
                    while not  vas.intersection(self.disa[i+1]) and i>=0:
                        for z in self.ldeter[i]:
                            if  vas <= set( z.listavar):
                                z.combina(pup, inplace=True)
                                z.borra([var], inplace=True)
                                if z.contradict():
                                    self.anula()

            
                        lista = self.lqueue[i].copy()
                        ins = []
                        for z in lista:
                            if vas <= set( z.listavar):
                                print("minimiando ", z.listavar)
                                self.lqueue[i].remove(z)
                                z.combina(pup, inplace=True)
                                z.borra([var], inplace=True)
                                if z.contradict():
                                    self.anula()
                                else:
                                    ins.append(z)
                        for z in ins:
                            self.insertacolapot(z)

                        i+= -1
                                    
                                    
        
    
            

    def mejorainicial(self):
        res = []
        for p in self.pinicial.listap:
            old = np.sum(p.tabla)
            oldl = len(p.listavar)
            vcl = set(p.listavar)
            if vcl:
                pos = min(map(lambda h: self.posvar[h], vcl))
            else:
                pos = len(self.orden)

            pot = self.lqueue[pos]
            npot = pot.marginalizas( set(pot.getvars()) - vcl)

            for v in npot.unit:
                p.reduce([v],inplace=True)
            for q in npot.listap:
                p.combina(q, inplace=True)
            new = np.sum(p.tabla)
            if new < old:
                print("mejora ", old, new, len(p.listavar))
                res.append(p)
                # sleep(2)            
        return res

    def borraproi(self):
        
        for i in reversed(range(len(self.orden))):
            if self.inicial.contradict:
                break
            print("i= ", i, "var = ", self.orden[i], "cluster ", self.clusters[i])
            pot = self.lqueue[i]

           
            if pot.contradict:
                self.inicial.contradict=True #ojo
                print("contradiccion antes de normalizar ")
                break
            
            for j in self.child[i]:
                print (j)
                dif = self.clusters[i]-self.clusters[j]
                
                potn = pot.marginalizapros(dif,self.M, inplace=False)
                
            
            

                  

                    

                    

                self.lqueue[j].insertaa(potn,self.M)

    def mejoradespues(self):
        for p in self.pinicial.listap:
            old = np.sum(p.tabla)
            pos = min(map(lambda h: self.posvar[h],p.listavar))
            pot = self.lqueue[pos]
            potn = pot.marginalizaset(pot.getvars() - set(p.listavar), Q=self.Q, ver=False, inplace=False) #EDM
            tablan = potn.atabla()
            p.combina(tablan, inplace=True)    
            nu =  np.sum(p.tabla)
            print(nu,old)
            if nu<old:
                print("mejoro", old,nu)
        
    def borrai(self):
        

        for i in reversed(range(len(self.orden))):
            if self.inicial.contradict:
                break
            print("i= ", i, "var = ", self.orden[i], "cluster ", self.clusters[i])
            pot = self.lqueue[i]
            
            if pot.contradict:
                self.inicial.contradict=True #ojo
                print("contradiccion antes de normalizar ")
                break
            
            for j in self.child[i]:
                # print (j)
                dif = self.clusters[i]-self.clusters[j]
                # print(dif)
                # print("entro en copia")
                # potn = self.lqueue[i].copia()
                # print("salgo de copia") 

                
                potn = pot.marginalizaset(dif, Q=self.Q,ver = False,inplace=False) #EDM
                self.lqueue[j].combina(potn)

    

    

    

    

    def crealistatop(self,top):
        lista = self.toriginalfl.copy()
        lista.sort(key = lambda x: top.index(x.listavar.copy().pop()))
        return lista

    def likelihoode(self):
        (ceros,me,va ) = self.likelihoodw(method = 1)
        print(ceros,me,va)

    def likelihoodw(self, N=500, method = 0):
        
        lista = []

        for x in self.toriginalfl:
            lista.append(x.listavar.copy())
        
        toporden = topologico(lista)
        
        self.orden = toporden[::-1]

       

       
        self.lfloat = self.crealistatop(toporden)

        pesos = 0.0
        pesos2 = 0.0
        ceros = 0

        vare = dict()
        for x in self.evid:
            vare[abs(x)] = x

        if method == 1:
            self.calculalogico()
            self.borradin(pre=True)
            # self.findallsol()

        logicalpot = self.lqueue[::-1]
        print(len(logicalpot))
        sleep(3)

        K = len(toporden)
        
        for j in range(N):
            sol = []
            pe = 1.0
            for i in range(K):
                v = toporden[i]
                pot = self.lfloat[i]
                potr = pot.reduce(sol)
                if v in vare:
                    va = vare[v]
                    sol.append(va)
                    if va>0:
                        pe *= potr.tabla[1]
                    else:
                        pe *= potr.tabla[0]
                    if pe == 0:
                        break

                elif method == 0:
                        x = ra.random()
                        p0 = potr.tabla[0]
                        p1 = potr.tabla[1]
                        sum = p0+p1
                        p0 = p0/sum
                        p1 = p1/sum
                        
                        
                        pe*=sum
                        va = v if x>p0 else -v
                        sol.append(va)
                        if pe==0:
                            break
                elif method == 1:
                        lpot = logicalpot[i]
                        lpotr = lpot.reduce(sol)
                        if lpotr.contradict():
                            pe = 0
                            break
                        elif lpotr.trivial():
                            x = ra.random()
                            p0 = potr.tabla[0]
                            p1 = potr.tabla[1]
                            sum = p0+p1
                            p0 = p0/sum
                            p1 = p1/sum
                            
                            
                            pe*=sum
                            va = v if x>p0 else -v
                            sol.append(va)
                            if pe==0:
                                break
                        else:
                            
                            va = v if lpotr.tabla[1] else -v
                            sol.append(va)
                            if va>0:
                                pe *= potr.tabla[1]
                            else:
                                pe *= potr.tabla[0]
                            if pe == 0:
                                break
            if pe == 0:
                ceros+=1
            else:
                print(pe)
                pesos += pe
                pesos2 += pe*pe

        me = pesos/N
        va = pesos2/N - me*me



        return(ceros,me, va/N )





        
    def calculalogico(self):
        self.rela = varpot(self.Q, self.Partir)
        for x in self.evid:
            self.rela.insertaru(x)
        for p in self.toriginalfl:
            q = nodoTabla(p.listavar)
            q.tabla = p.tabla > 0
            if not q.trivial():
                self.rela.insertar(q)



    

    def borradrela(self):
    
        if self.rela.contradict:
                print("contradictorio")
                self.anula()
                return


   
        self.rela.marginalizaset(self.pinicial.getvars()) #EDM
       

            # (self.clusters,self.posvar,self.child,self.parent) = triangulaconorden(self.pinicial,self.orden) 


        
        



        
    def borradin2(self, pre = False):
    
        if self.rela.contradict:
                print("contradictorio")
                self.anula()
                return self.pinicial.getvars()


        if pre:
            (e,orden,nuevas,antiguas)= self.rela.marginalizaset(set(self.orden), Q=self.Q,pre = True, orden = self.orden.copy()) #EDM
        else:
            (e,orden,nuevas,antiguas)= self.rela.marginalizaset2(self.pinicial.getvars(), Q=self.Q,pre = False) #EDM
        self.contradict =  self.rela.contradict
        if not pre:
            self.orden = self.orden +  orden
        
            i=0
        if not self.contradict:
            for x in antiguas:
                # print(i, x) #EDM
                i+=1
                y = nodoTabla([])
                
                self.lqueue.append(y)


            # (self.clusters,self.posvar,self.child,self.parent) = triangulaconorden(self.pinicial,self.orden) 


        
        



        return e      

    def borra12(self,x,l,rela, M= 20):
            print("total ", len(l))
            i = x[0]
            while l:

                p= l.pop()
                sp = p.extraesimple()
                if not sp.trivial():

                    if len(sp.listavar) == 1:
                        var = sp.listavar[0]
                        areducir = rela.get(var)
                        print(" i " , i , "var ", var, "reduccion unitaria ")
                        i +=1
                        sleep(1)
                        rela.borrarv(var)
                        for q in areducir:
                            
                            if q in l:
                                l.remove(q)
                            r = q.combina(sp)
                            r.borra([var],inplace=True)
                            if r.contradict():
                                rela.anula()
                                print("contradiction ")
                                return
                            elif not r.trivial():
                                l.append(r)
                                rela.insertar(r)


                    elif len(sp.listavar) == 2:
                        v1 = sp.listavar[0]
                        v2 = sp.listavar[1]
                        
                        det1 = sp.checkdetermi(v2)
                        if not det1:
                            det2 = sp.checkdetermi(v1)
                        if not det1 and not det2:
                            continue
                        if not det1 and det2:
                            v1,v2 = v2,v1
                        var = v2
                        print(" i " , i, "var ", var, "doble ")
                        sleep(1)
                        i+=1
                        areducir = rela.get(var)
                        rela.borrarv(var)
                        for q in areducir:
                            if q in l:
                                l.remove(q)
                            r = q.combina(sp)
                            r.borra([var],inplace=True)
                            if r.contradict():
                                rela.anula()
                                print("contradiction ")
                                return
                            elif not r.trivial():
                                l.append(r)
                                rela.insertar(r)
                else:
                    print("extraigo trivial ")

            x[0] = i
        


                        
            
    def borradet(self):
        tot = len(self.orden)
        print(tot)
        sleep(0.2)

        for i in range(len(self.orden)):
            if self.inicial.contradict:
                break
            var = self.orden[i]
            print("i= ", i, "var = ", var, "quedan: ", tot-i, "cluster ", self.clusters[i])
            if self.ldeter[i]:
                p = self.ldeter[i][0]
                print("determinista")
                for x in self.lqueue[i]:
                    q = p.combina(x,inplace = False)
                    q.borra([var],inplace=True)
                    self.insertacolapot(q, check=True)
            else:
                t = len(self.lqueue[i])

                print("no determinista ", t)

                p = nodoTabla([])

                for x in self.lqueue[i]:
                    p.combina(x,inplace = True)
                p.borra([var],inplace=True)
                self.insertacolapot(p, check=True)
                
                

       
            # pot.imprime()
            
            
    def borrapro(self):
        print(len(self.orden))
        for i in range(len(self.orden)):
            if self.inicial.contradict:
                break
            var = self.orden[i]
            print("i= ", i, "var = ", self.orden[i], "cluster ", self.clusters[i])
            pot = self.lqueue[i]
       
            # pot.imprime()

            
            
            if pot.contradict:
                self.inicial.contradict=True #ojo
                print("contradiccion antes de normalizar ")
                break
            
            
            potn = pot.marginalizapro(var,self.M)
            
            # potn.imprime()
            pos = self.parent[i]

            poti = self.lqueue[pos]

            

            
            poti.insertaa(potn,self.M)

            


    def inserta(self,pot):
        for x in pot.unit:
                print("inserto unidad")
                self.insertaunit(x)

        for p in pot.listap:
                print("inserto potencial " , p.listavar)
                
                self.rela.insertar(p)
       



    


            


    def findsol(self):
        sol = set()
        for i in reversed(range(len(self.orden))):
            print(i)
            tabla = self.lqueue[i]
            

            
            
            var = self.orden[i]
            print(var) #EDM
            # print(tabla.listavar,tabla.tabla)

            t = tabla.reduce(list(sol))
            # print(t.listavar,t.tabla)

            if len(t.listavar) > 1:
                for x in t.listavar:
                    if not x == var:
                        sol.add(x) 
                t = t.reduce(list(sol))


            

            if t.contradict():
                print("contradiccion buscando solucion" , sol )
                break

            elif t.trivial():
                sol.add(var)
                # print("elijo ", var) #EDM
        
            elif t.tabla[0]:
                sol.add(-var)
                # print(-var) #EDM
            else:
               sol.add(var)
               # print(var)  #EDM

            
            
        self.sol = sol
        return sol




    def findallsol(self):
        soll = [set()]
        for i in reversed(range(len(self.orden))):
            print(i)
            sleep(1)
            tabla = self.lqueue[i]
            

            
            
            var = self.orden[i]
            print(var)
            # print(tabla.listavar,tabla.tabla)
            nsol = []
            for sol in soll:
                t = tabla.reduce(list(sol))
            # print(t.listavar, t.tabla)
                if t.contradict():
                    print("contradiccion buscando solucion" , sol )
                    sol = []
                    break

                elif t.trivial():
                    sol.add(var)
                    sol2 = sol.copy()
                    sol2.add(-var)
                    nsol.append(sol2)
                    print("elijo ", var)
                    print("elijo ", -var)

        
                elif t.tabla[0]:
                    sol.add(-var)
                    print(-var)
                else:
                    sol.add(var)
                    print(var) 
            soll.extend(nsol)
            
        print(len(soll)) 
        sleep(10)
        self.sol = sol
        return soll
    
    def randomsol(self,T=40000):
        sol = []
        i = len(self.orden)-1
        k = 0
        while i >0 and k<T:
            k+=1
            # print(i,k,sol)
            pot = self.lqueue[i].copia()
            
            pot.simplificaunits(sol)
            pot.normaliza(N=1000)

            pots = pot.tosimple()
            
            var = self.orden[i]
            
            if pots.contradict:
                pot = self.lqueue[i].copia()
                cl = pot.extraeclaus(sol,var)
                # print(cl)
                vcl = map(abs,cl)
               
                j = min(map(lambda h: self.posvar[h], vcl))
                self.lqueue[j].insertaclau(cl)
                t = j-i

                i = j

                del sol[-t:]

                if len(cl)<=3:
                     print("buena", cl)
                     self.inicial.insertar(cl)
            else:


                i=i-1
                pots.simplificaunit(var)
                if pots.contradict:
                    sol.append(-var)
                else:
                    sol.append(var)
            
            
        if i<0:
            self.sol = sol
        print(sol)
        return sol

    def compruebaSol(self):
        aux = 0
        print("entro en comprueba solucion")
        for clau in self.inicial.listaclausOriginal:
            print(clau)
            aux = aux + 1
            if len(clau.intersection(self.sol))==0:
                print("Error en cláusula: ", clau)
                return False
        print("Cumple solución satisfactoriamente, Número de cláusulas validadas: ", aux)
        return True
    
    
    
            
    def problemacontradict(self):
        print("contradiccion")
        self.inicial.solved = True
        self.inicial.contradict = True
        
    def anula(self):
        self.inicial.solved = True
        self.inicial.contradict = True
        for pot in self.lpot:
            pot.anula()
        for por in self.lqueue:
            pot.anula()