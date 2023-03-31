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
from DeterministicDeletion import *
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
        con = set(p.listavar)
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
        # info.contradict = False
        # info.solved = False
        

        test()

        prob.inicial.solved = False         
        print("entro en main")  #EDM

        prob.inicia0() 

        if Previo: #EDM
            prob.previo()       
        

       


        
        (prob.orden,prob.clusters,prob.borr,prob.posvar,prob.child,prob.parent) = triangulap(prob.pinicial.listap) 

        # prob.cuclusters()
       
        # (order,clusters,iorder,posvar,child,parent) = triangulap(back.getpotl(back.getvars()))
           

        # prob.rela.mejoralocal()           
        # if Mejora:  #EDM
        #     prob.rela.mejoralocal()      #EDM  
            
        prob.inicia1() 

        back = prob.rela.copia()

        (orden,prob.clusters,prob.borr,prob.posvar,prob.child,prob.parent) = triangulap(back.getpotl(back.getvars())) 


        h = back.getXor()
        back.orden = orden

        xorp = xor(h)
       
        # print(xorp.compiled) 
        # print(xorp.order)
        ls = xorp.getTables()


        back.minid(30)


        for p in h:
           
            back.insertar(p)





        back.orden = orden

       
        # back.orden = order
       


        # for i in [3,3,4,4,5,3,5,3,3,6,3,7,3,4,5]:
        #     print("i = ",i)
        #     back.minid(i)

        # back.recomputeorder()
        # orden = back.orden.copy()

        # back = prob.rela.copia()

        # back.orden = orden

        for i in [3,3,4,4,5,3,5,3,3,6,3,7,3,4,5]:
            print("i = ",i)
            back.minid(i)



        for i in [6,3,7,3,7,3,8,3,9,3,10,3,3,4,3,4,3,4,11,12,13,14,15,14,13,12,11,10,9,8,7,6,5,4,3]:
            print("i = ",i)
            back.minid(i)
        




       
        # back.localimprove()

        back.borraf(Q=5)


        print("termino borraf")

        nuevo = back.copia()

        print("termino copia")





        # listpot = nuevo.getpotl(nuevo.getvars())

        # print(len(listpot))

        
        # listac = getclusters(listpot)

        # print(len(listac))

        

        
        
        # sleep(4)

        # npot = nuevo.getmarginalsapr(listac,Q=5)


        # nuevo = varpot()
        # for p in npot:
        #     print(2**len(p.getvars()), p.tabla.sum() )
        #     nuevo.insertarb2(p)
       

        for i in range(10,25):
            print("i=",i)
            nuevo.borraf(Q=i)
           

        # listat = []
        # (res,lista) = nuevo.borrae(Q=25)
        # for p in lista:
        #     print(len(p.getvars()),p.getvars())
        #     sleep(1)
        # listat = listat + lista
        # while listat:
        #     p = listat[0]
        #     del listat[0]
        #     print(len(p.getvars()),p.getvars())
        #     res.insertar(p)
        #     (res,lista) = res.borrae(Q=25)
        #     for p in lista:
        #         print(len(p.getvars()),p.getvars())
        #     sleep(10)
        #     listat = listat + lista


        
         


            # listpot = nuevo.getpotl(nuevo.getvars())

            # print(len(listpot))
            # listac = getclusters(listpot)

            # print(len(listac))
            # npot = nuevo.getmarginalsapr(listac,Q=10)

            # nuevo = varpot()
            # for p in npot:
            #     print(2**len(p.getvars()), p.tabla.sum() )
            #     nuevo.insertarb2(p)

            # sleep(20)



        # for i in [3,3,4,4,5,5,3,3,6,7,8,9,10]:
        #     print("i = ",i)
        #     nuevo.minid(i)

        # back.simplifyp(nuevo)

        # nuevo.checkincluded()
      
        t1 = time()

        


        nuevo.borrac(Q=25)

        t2 = time()

        print(t2-t1)

        wait = input("Press Enter to continue.")


        # config = nuevo.back2(30)
        # vars = set(prob.rela.getvars())
        # print(len(vars))
        # vars2 = set(map(abs,config))
        # back.compruebasol(config)
        # print("diferencia" , vars-vars2)
        # print(config)
        


    

        # print("salgo de borrado")

        # if not prob.contradict:
        #     prob.sol = prob.findsol()
        #     prob.compruebaSol()
        #     return True
        # else:
        #     print(" problema contradictorio ")
        #     return False

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


def borradofacil(archivolee, Q=[5,10,15,20,25,30],Mejora=[False], Previo=[True], Partir=[True], archivogenera="salida.csv"):
    try:
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
                # param = linea.split()
                # nombre = param[0]
                # N1 = int(param[1])
                nombre=linea.strip()
                print(nombre)     
                t1 = time()
                (info, nvar, nclaus) = leeArchivoGlobal(nombre)
                t2= time()
                for Qev in Q:
                    for Mej in Mejora:
                        for Pre in Previo:
                            for Part in Partir:
                                    t3 = time()
                                      
                                    prob = problemaTrianFactor(info,Qin=Qev) #EDM   #Último parámetro es Q
                                    # prob = problemaTrianFactor(info,N1,Qev) #EDM   #Último parámetro es Q
                                    t4 = time()
                                    # main(prob)  #EDM 
                                    nv = main2(prob, Pre,Mej) #EDM 
                                    t5 = time()
                                    print("tiempo lectura ",t2-t1)
                                    print("tiempo busqueda ",t5-t4)
                                    print("tiempo TOTAL ",t5-t3+t2-t1)
                                    cadena =   str(nv) +"\n"
                            writer.write(cadena)
        writer.close()
        reader.close()    
    except ValueError:
        print("Error")

def borradocontablas(archivolee, Q=[5,10,15,20,25,30],Mejora=[False], Previo=[True], Partir=[True], archivogenera="salida.csv"):
        # reader=open("D:/satsolver/"+archivolee,"r")
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
                # param = linea.split()
                # nombre = param[0]
                # N1 = int(param[1])
                nombre=linea.strip()
                print(nombre)     
                t1 = time()
                (info, nvar, nclaus) = leeArchivoGlobal(nombre)
                t2= time()
                for Qev in Q:
                    for Mej in Mejora:
                        for Pre in Previo:
                            for Part in Partir:
                                    t3 = time()
                                    cadena= nombre + ";" + str(nvar) + ";" + str(nclaus) + ";" + str(Qev) + ";" + str(Mej) + ";" + str(Pre) + ";" + str(Part) + ";"
                                    prob = problemaTrianFactor(info,Qin=Qev) #EDM   #Último parámetro es Q
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
