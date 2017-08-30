# -*- coding: utf-8 -*-

import json
from numpy.random import randint
import numpy as np
from random import sample

class dataGen:
    def __init__(self):

        ### Load configuration file
        with open('./conf.json', 'r') as r:
            config = json.load(r)
            self.attrs = {}
            self.attrs['R'] = config['k']['value']
            self.attrs['S'] = config['l']['value']
            self.oos = {}
            self.oos['R'] = config['s']['value']
            self.oos['S'] = config['t']['value']
            self.vocab = config['vocab']['value']
            self.primary = config['primary']['value']
            self.z = self.vocab**(max(self.oos.values()))
            self.N = self.z*self.primary

        ### Validation of the configuration
        error = False
        if self.attrs['R'] <= self.oos['R']:
            print "[Error] invalid paramemter: k < s"
            error = True
        if self.attrs['S'] <= self.oos['S']:
            print "[Error] invalid paramemter: l < t"
            error = True
        if self.N < self.z:
            print "[Error] invalid paramemter: N < z"
            error = True
        if error:
            exit(0)


    def main(self):
        ### random attributes
        R = randint(self.N, size=(self.N, self.attrs['R']-self.oos['R']-1))
        S = randint(self.N, size=(self.N, self.attrs['S']-self.oos['S']-1))

        ### order-oriented attributes
        r = self.ooAttributeGen((self.z, self.oos['R']))
        s = self.ooAttributeGen((self.z, self.oos['S']))
        R = np.array([np.append(x, y) for x, y in zip(R, r)])
        S = np.array([np.append(x, y) for x, y in zip(S, s)])

        ### common attributes
        # equi-join condition
        r = [j for j in range(int(self.N/self.z)+1) for i in range(self.z)][:self.N]
        s = r[:]
        R = np.array([np.append(x, y) for x, y in zip(R, r)])
        S = np.array([np.append(x, y) for x, y in zip(S, s)])

        ### expected join result
        E = np.array([np.append(x, y) for x, y in zip(R, S)])

        ### Save them into CSV files
        np.savetxt("./generated/R.csv", R, fmt="%d", delimiter=",")
        np.savetxt("./generated/S.csv", S, fmt="%d", delimiter=",")
        np.savetxt("./generated/E.csv", E, fmt="%d", delimiter=",")

        ### Generate Schema
        self.generateCreateTableStatement('R', self.attrs['R'])
        self.generateCreateTableStatement('S', self.attrs['S'])
        self.generateCreateTableStatement('E', (self.attrs['R'], self.attrs['S']))


    def generateCreateTableStatement(self, target, num_of_attrs):
        q = 'drop table if exists %s;' % target 
        q += 'create table %s (' % target
        if target == 'E':
            q += ', '.join(['r%d int' % i for i in range(num_of_attrs[0])])
            q += ', '
            q += ', '.join(['s%d int' % i for i in range(num_of_attrs[1])])
        else:
            q += ', '.join(['%s%d int' % (target, i) for i in range(num_of_attrs)])
        q += ');'
        with open('./generated/%s.sql' % target, 'w') as w:
            w.write(q)


    def ooAttributeGen(self, size):
        ret = []

        if size[1] == 1:
            for i in range(self.primary):
                ret.extend(sorted(sample(range(1, self.N*10), self.z)))
        else:
            for i in range(self.primary):
                ret.extend(self.recursiveOOAttributeGen(0, size[1]-1))

        return ret[:self.N]


    def recursiveOOAttributeGen(self, depth, goal):
        cand = [[s] for s in sorted(sample(range(1, self.N*10), self.vocab))]
        if depth == goal:
            return cand

        ret = []
        for i in range(self.vocab):
            tmp = self.recursiveOOAttributeGen(depth+1, goal)
            for t in tmp:
                con = cand[i][:]
                con.extend(t)
                ret.append(con)

        return ret


if __name__ == "__main__":
    dataGen().main()
