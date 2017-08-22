# -*- coding: utf-8 -*-

import json
from numpy.random import randint
import numpy as np

class dataGen:
    def __init__(self):
        with open('./conf.json', 'r') as r:
            self.config = json.load(r)
            self.N = self.config['N']['value']
            self.k = self.config['k']['value']
            self.l = self.config['l']['value']
            self.s = self.config['s']['value']
            self.t = self.config['t']['value']
            self.z = self.config['z']['value']

        error = False
        if self.k < self.s:
            print "[Error] invalid paramemter: k < s"
            error = True
        if self.l < self.t:
            print "[Error] invalid paramemter: l < t"
            error = True
        if self.N < self.z:
            print "[Error] invalid paramemter: N < z"
            error = True

        if error:
            exit(0)


    def main(self):
        print 'R is', self.N, 'records,', self.k, 'attributes.'
        print 'S is', self.N, 'records,', self.l, 'attributes.'
        print self.s, 'out of', self.k, 'in R are used for order-oriented join.'
        print self.t, 'out of', self.l, 'in S are used for order-oriented join.'

        ### random attributes
        R = randint(self.N, size=(self.N, self.k-self.s-1))
        S = randint(self.N, size=(self.N, self.l-self.t-1))

        ### order-oriented attributes
        r = self.ooAttributeGen((self.z, self.s))
        s = self.ooAttributeGen((self.z, self.t))
        R = np.array([np.append(x, y) for x, y in zip(R, r)])
        S = np.array([np.append(x, y) for x, y in zip(S, s)])

        ### common attributes
        # equi-join condition
        r = [j for j in range(int(self.N/self.z)+1) for i in range(self.z)][:self.N]
        s = r[:]
        R = np.array([np.append(x, y) for x, y in zip(R, r)])
        S = np.array([np.append(x, y) for x, y in zip(S, s)])

        print R
        print S

        np.savetxt("R.csv", R, fmt="%d", delimiter=",")
        np.savetxt("S.csv", S, fmt="%d", delimiter=",")



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
