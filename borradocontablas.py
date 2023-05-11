# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 13:30:14 2019

@author: Nizziho
""" 
import networkx as nx    
from SimpleClausulas import *
from time import *
from utils import *
from xor import *
from vartablasd import *
# from DeterministicDeletion import *
# from arboltablaglobal import *

def test():
    from tablaClausulas import nodoTabla
    from arboltabla import arbol

    h = np.random.rand(2,2,2,2,2,2)
    t = np.random.rand(2,2,2,2,2,2)
    h = h>0.1
    t = t>0.1
    ht = nodoTabla([1,2,3,4,5,6])
    tt = nodoTabla([3,4,5,6,7,8])
    ht.tabla = h
    tt.tabla = t
    ct = ht.combina(tt)
    ha = creadesdetabla(ht,Q=2)
    ta = creadesdetabla(tt,Q=2)
    print(ha.size(),ta.size())
    ca = ta.combina(ha)
    nt = ca.totable()
    print(nt.tabla.sum(),ct.tabla.sum())
    print(nt.equivalente(ct))
    ha.poda(Q=2)
    ta.poda(Q=2)
    print(ha.size(),ta.size())
    ca = ta.combina(ha)
    ca.poda(Q=2)
    nt = ca.totable()
    print(nt.tabla.sum(),ct.tabla.sum())
    print(nt.equivalente(ct))
    sa = ha.suma(ta)
    # sa.poda(Q=2)
    nst = sa.totable()
    st = ht.suma(tt)
    print(nst.tabla.sum(),st.tabla.sum())
    print(st.equivalente(nst))
    

    





    
def triangulap(lista):
    order = []
    clusters = []
    iorder = []
    child = []
    posvar = dict()
    total = set()
    dvar = dict()
    for p in lista:
        if isinstance(p,nodoTabla):
            con = set(p.listavar)
        else:
            con = set(p)
        total.update(con)
        for v in con:
            if v in dvar:
                dvar[v].append(con)
            else:
                dvar[v] = [con]
    n = len(total)
    parent = [-1]*(n+1)
    for i in range(n+1):
        child.append(set())
    i= 0
  
    value = dict()
    totvar = dict()
    for x in dvar:
        totvar[x] = set()
        for h in dvar[x]:
            totvar[x].update(h)
        value[x] = 2**(len(totvar[x])-1) - sum([2**len(y) for y in dvar[x]])  
    i = 0
    while total:
        nnode = min(value, key = value.get )
        order.append(nnode)
        clus = set()
        for x in dvar[nnode]:
            clus.update(x)
        clusters.append(clus)
        posvar[nnode] = i
        i+=1
        clustersin = clus-{nnode}
        for y in clustersin:
            dvar[y] = list(filter( lambda h: nnode not in h  ,dvar[y] ))
            dvar[y].append(clustersin)
            totvar[y] = set()
            for h in dvar[y]:
                totvar[y].update(h)
            value[y] = 2**(len(totvar[y])-1) - sum([2**len(z) for z in dvar[y]])
        del value[nnode]
        del dvar[nnode]
        del totvar[nnode]
        total.discard(nnode)
    clusters.append(set())
    clust = set()
    for i in range(n):
            con = clusters[i]
            oclus = clust.copy()
            clust.update(con)
            iorder = iorder+ list(clust-oclus)
            cons = con - {order[i]}
            if not cons:
                parent[i] = n
                child[n].add(i)
            else:
                pos = min(map(lambda h: posvar[h], cons))
                parent[i] = pos
                child[pos].add(i)
    iorder.reverse()
    return (order,clusters,iorder,posvar,child,parent) 
    
def leeArchivoGlobal(Archivo):
    reader=open(Archivo,"r") 
    cadena = reader.readline()
    while cadena[0]=='c':
        cadena = reader.readline()
    
    cadena.strip()
    listaaux = cadena.split()
    print(listaaux)
    nvar = int(listaaux[2])
    nclaus = int(listaaux[3])
    print(nvar)
    while cadena[0]=='c':
        cadena = reader.readline()

    infor = simpleClausulas()
    for cadena in reader:
        if (cadena[0]!='c'):
            cadena.strip()
            listaux=cadena.split()
            listaux.pop()
            listaux = map(int,listaux)
            clausula= set(listaux)
            nc = set( map(lambda t: -t, clausula))

            infor.listaclausOriginal.append(clausula.copy())
            if not nc.intersection(clausula):
                infor.insertar(clausula, test = False)
            else:
               print("trivial ", clausula)

            if infor.contradict:
                print("contradiccion leyendo")
    
    return infor, nvar, nclaus
   
    
    



    
    

    
def main(prob, Previo=True, Mejora=False): #EDM
    

        nuevo = prob.copia() 

        print("termino copia")






        

        
       
        t1 = time()

       
           

   


        (res,msize) = nuevo.borraf(32)
        res.prob = prob.prob.copy()
        res.addproborden()
     

        sleep(5)

        t2 = time()

        print(t2-t1)



        


def treeWidth(prob):
    (orden,clusters,borr,posvar,child,parent) = triangulap(prob.pinicial)
    sizes = map(len,clusters)
    return(max(sizes))


def computetreewidhts(archivolee):
    archivogenera = "treewidths" + archivolee
    reader=open(archivolee,"r")
    writer=open(archivogenera,"w")
    writer.write("Problema;TreeWidth\n")
    for linea in reader:
            # i=i+1
            linea = linea.rstrip()
            if len(linea)>0:
                cadena = ""
                # param = linea.split()
                # nombre = param[0]
                # N1 = int(param[1])
                nombre=linea.strip()
                print(nombre)     
                (info, nvar, nclaus) = leeArchivoGlobal(nombre)
                
                cadena= nombre 
                prob = DeterministicDeletion(info) #EDM   #Último parámetro es 
                


                
                                    # prob = problemaTrianFactor(info,N1,Qev) #EDM   #Último parámetro es Q
                                    # main(prob)  #EDM 
                prob.inicia0()
                                    
                tw = treeWidth(prob)
                cadena = cadena + ";" + str(tw) + "\n"
                writer.write(cadena)
                                # ttotal += t5-t1

    writer.close()
    reader.close()



def borradocontablas(archivolee, Q=[5,10,15,20,25,30],Mejora=[False], Previo=[True], Partir=[True], archivogenera="salida.csv"):
        reader=open(archivolee,"r")
        writer=open(archivogenera,"w")
        writer.write("Problema;Variable;Claúsulas;Q;MejoraLocal;Previo;PartirVars;TLectura;TBúsqueda;TTotal;SAT\n")
        ttotal = 0
        # i=0
        for linea in reader:
            # i=i+1
            linea = linea.rstrip()
            if len(linea)>0:
                cadena = ""
              
                nombre=linea.strip()
                print(nombre)     
                t1 = time()
                (tablas,evi) = leeficheroUAI(nombre)
                t2= time()
                for Qev in Q:
                    for Mej in Mejora:
                        for Pre in Previo:
                            for Part in Partir:
                                    t3 = time()
                                    cadena= nombre + ";" +  str(Qev) + ";" + str(Mej) + ";" + str(Pre) + ";" + str(Part) + ";"
                                    prob = varpot()
                                    lclu = [p.getvars() for p in tablas] + [[abs(v)] for v in evi]
                                    (orden,prob.clusters,prob.borr,prob.posvar,prob.child,prob.parent) = triangulap(lclu)
                                    print(max([len(x) for x in prob.clusters]))
                                    # sleep(5)

                                    prob.orden = orden
                                    prob.computefromBayes(tablas,evi)
                                    # prob = problemaTrianFactor(info,N1,Qev) #EDM   #Último parámetro es Q
                                    t4 = time()
                                    # main(prob)  #EDM 
                                    bolSAT = main(prob, Pre,Mej) #EDM 
                                    t5 = time()
                                    print("tiempo lectura ",t2-t1)
                                    print("tiempo busqueda ",t5-t4)
                                    print("tiempo TOTAL ",t5-t3+t2-t1)
                                    cadena =  cadena + str(t2-t1) + ";" + str(t5-t4) + ";" + str(t5-t3+t2-t1) + (";SAT" if bolSAT else ";UNSAT") + "\n"
                            writer.write(cadena)
                                # ttotal += t5-t1
                # print(Q)
        # if i>0:
        #     print ("tiempo medio ", ttotal/i)cd cd 
        #     writer.write("tiempo medio " + str(ttotal/i)+"\n")
        writer.close()
        reader.close()    
    
# computetreewidhts("ListaCNF_Experimento.txt")
borradocontablas("entrada",[5],[False],[True],[False],"prueba05.txt")
# borradofacil("entrada",[5,10,15,20,25],[False],[False],[True],"resultado.txt")
