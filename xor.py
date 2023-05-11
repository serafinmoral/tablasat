import numpy as np
from tablaClausulas import *
import itertools as iter


class xor:

    
    def __init__(self, lista):
        
        self.initial = lista
        self.order = []
        self.compiled = []
        self.contra = False
    
    def addlist(self,l):
        self.initial = self.initial + l

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
    
    def getTablevar(self,var):
        tvar = set()
        for p in self.initial:
            tvar.update(p[0])
        svar = set(var)
        dvar = tvar-svar
        equ = self.initial.copy()

        for v in dvar:
            bor = []
            ins = []
            found = False
            for p in equ:
                if v in p[0] and not found:
                    found  = True
                    r = p
                    bor.append(p)
                elif v in p[0] and found:
                    t = p
                    inter = r[0].intersection(t[0])
                    ns = r[0].union(t[0])- inter
                    
                    nv = r[1]^t[1]
                    bor.append(t)
                    if not ns and nv:
                        self.anula()
                    if ns:
                        ins.append((ns,nv))
            for r in bor:
                equ.remove(r)
            for r in ins:
                equ.append(r)

        res = nodoTabla([])
        for t in equ:
            vars = list(t[0])
            vars.sort()
            h = nodoTabla(vars)
            ba = [(0,1)]*len(vars)
            ind = iter.product(*ba)
            for x in ind:
                s = sum(x)
                if not s%2 == t[1]:
                    h.tabla[x] = False

            res = res.combina(h)

        return res


        



    def compile(self):
        
        total = set()
        self.compiled = []
        this = []
        print(self.order)
        
        while self.initial:
            t = min(self.initial, key = lambda x: min(x[0], key = lambda y: self.order.index(y)))
            print(t)
            self.initial.remove(t)
            var = min(t[0], key = lambda y: self.order.index(y))
            total.update(t[0])
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
        while listr:
            pos = len(listr)

            var = listr.pop()
            r = self.compiled[pos-1]

            for i in range(pos-1):
                t = self.compiled[i]
                if var in t[0]:
                    inter = r[0].intersection(t[0])
                    ns = t[0].union(r[0])- inter
                    nv = r[1]^t[1]
                    self.compiled[i] = (ns,nv)

        print(total-set(this))
        print(len(total),len(this))





                        



        