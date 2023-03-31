import numpy as np
from tablaClausulas import *
import itertools as iter


class xor:

    
    def __init__(self, lista):
        
        self.initial = lista
        self.order = []
        self.compiled = []
        self.contra = False
    
    def anula(self):
        self.initial = []
        self.order = []
        self.compiled = [(set(),1)]
        self.contra = True

    def getTables(self):
        res = []
        for t in self.compiled:
            vars = list(t[0])
            vars.sort()
            h = nodoTabla(vars)
            ba = [(0,1)]*len(vars)
            ind = iter.product(*ba)
            for x in ind:
                s = sum(x)
                if not s%2 == t[1]:
                    h.tabla[x] = False

            res.append(h)
        return res


    def deletion(self):
        
        self.compiled = []
        this = []
        
        while self.initial:
            t = min(self.initial, key = lambda x: min(x[0], key = lambda y: self.order.index(y)))
            self.initial.remove(t)
            var = min(t[0], key = lambda y: self.order.index(y))
            print(var)
            this.append(var)
            self.compiled.append(t)
            bor = []
            ins = []
            for r in self.initial:
                if var in r[0]:
                    inter = r[0].intersection(t[0])
                    ns = r[0].union(t[0])- inter
                    print(ns)
                    nv = r[1]^t[1]
                    bor.append(r)
                    if not ns and nv:
                        self.anula()
                    if ns:
                        ins.append((ns,nv))
            for r in bor:
                self.initial.remove(r)
            for r in ins:
                self.initial.append(r)

        listr = this.copy()
        pos = len(listr)
        while listr:
            var = listr.pop()
            for i in range(pos-1):
                t = self.compiled[i]
                r = self.compiled[pos-1]
                inter = r[0].intersection(t[0])
                ns = t[0].union(r[0])- inter
                nv = r[1]^t[1]
                if len(ns)<=len(t[0])+30:
                    self.compiled[i] = (ns,nv)




                        



        