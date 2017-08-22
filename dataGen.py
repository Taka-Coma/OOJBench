# -*- coding: utf-8 -*-

import json
from numpy.random import randint
import numpy as np

class dataGen:
    def __init__(self):

        ### Load configuration file
        with open('./conf.json', 'r') as r:
            config = json.load(r)
            self.N = config['N']['value']
            self.attrs = {}
            self.attrs['R'] = config['k']['value']
            self.attrs['S'] = config['l']['value']
            self.oos = {}
            self.oos['R'] = config['s']['value']
            self.oos['S'] = config['t']['value']
            self.z = config['z']['value']

        ### Validation of the configuration
        error = False
        if self.attrs['R'] < self.oos['R']:
            print "[Error] invalid paramemter: k < s"
            error = True
        if self.attrs['S'] < self.oos['S']:
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

        ### Save them into CSV files
        np.savetxt("R.csv", R, fmt="%d", delimiter=",")
        np.savetxt("S.csv", S, fmt="%d", delimiter=",")

        ### Generate Schema
        self.generateCreateTableStatement('R')
        self.generateCreateTableStatement('S')


    def generateCreateTableStatement(self, target):
        q = 'create table %s (' % target
        q += ', '.join(['a%d int' % i for i in range(self.attrs[target])])
        q += ');'

        with open('%s.sql' % target, 'w') as w:
            w.write(q)


    def ooAttributeGen(self, size):
        ret = []
        tmp = [sorted(randint(self.N, size=size).tolist(),
            key=lambda y: int(''.join(['%04d' % yy for yy in y])))
            for j in range(int(self.N/self.z)+1)]

        for tt in tmp:
            for t in tt:
                ret.append(t)

        return ret[:self.N]



if __name__ == "__main__":
    dataGen().main()
