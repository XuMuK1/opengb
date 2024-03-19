import numpy as np

from copy import deepcopy
import random

import openGB.polynomials as polys



class IdealException(Exception):
    def __init__(self,msg):
        self.msg=msg
        
    def __str__(self):
        return "IdealException: " + self.msg
    
class IdealCoefficinentMismatchException(IdealException):
    def __init__(self,msg):
        super(IdealException, self).__init__(msg)
        
    def __str__(self):
        return "IdealCoefficinentMismatchException: " + self.msg
    

class Ideal:
    '''
    Ideals generated by set of polynomials    
    '''
    def __init__(self, polynomials, order, vars):
        '''
        Parameters
        Polynomial[] polynomials -- a sequence of polynomials
        MonomialOrder order -- a monomial order applied to the polynomials
        '''
        self.polynomials = polynomials
        self.order = order
        self.isGB = False
        self.vars = vars

    def sort(self):
        '''
        Sorts all monomials in polynomials
        '''
        for i in np.arange(len(self.polynomials)):
            self.polynomials[i].sort()
            
    def getInTerms(self):
        '''
        Gives a set of initial terms
        
        Returns
        Monomial[] mons
        '''
        return [poly.inTerm() for poly in self.polynomials]

    #a fancy-looking string representation
    def __str__(self):
        return "( "+",\n".join([str(poly) for poly in self.polynomials])+" )"
    
    def getComb(self,polys):
        '''
        Computes a polynomial combination
        
        Input
        Polynomial[] polys -- list of polynomial coefficients
        
        Returns
        Polynomial poly
        '''
        if(len(self.polynomials)==len(polys)):
            polyFinal = sum([polys[i]*self.polynomials[i] for i in np.arange(len(self.polynomials))])
            polyFinal.simplify()
        else:
            raise IdealCoefficinentMismatchException("Wrong number of coffiecients in polynomial combination")
        return polyFinal

    def genSPolys(self,ids):
        '''
        Generates a set of S-polynomials Sij with given sets of pairwise indices

        Input
        ids -- list of tuples (i,j)
        Returns
        Polynomial[] spolys
        '''
        return [self.getSPoly(self.polynomials[i],self.polynomials[j]) for i,j in ids]

    def getSPoly(self, p1, p2):
        '''
        Gives an S-polynomial from two given polynomials

        Returns
        Polynomial spoly
        '''
        in1 = p1.inTerm()
        in2 = p2.inTerm()
        degDiff = in1.deg - in2.deg
        mul1 = -degDiff*(degDiff<=0)
        mul2 = degDiff*(degDiff>=0)
        mon1 = polys.Monomial(deg=mul1, coef=in2.coef, order=self.order, vars=self.vars).toPolynomial()
        mon2 = polys.Monomial(deg=mul2, coef=in1.coef, order=self.order, vars=self.vars).toPolynomial()
        return mon1*p1 - mon2*p2
        

    def existsIntersection(self, p1,p2):
        '''
        Check if there is an intersection in initial terms of p1 and p2

        Returns
        bool result
        '''
        return not np.all(p1.inTerm().deg - p2.inTerm().deg == 0)
    def checkGB(self):
        '''
        Checks if the set of polynomials forms a GB
        '''
        #gen Spolys
        ids = [ (i,j) for i in np.arange(len(self.polynomials)) 
                            for j in np.arange(len(self.polynomials))
                            if (i>j and 
                                self.existsIntersection(self.polynomials[i], self.polynomials[j]))]
        spolysRedResult = np.all([ self.baseReduce(sp).isZero() for sp in self.genSPolys(ids) ])
        return spolysRedResult

    def computeGB(self, debugVerbose=False, minGB=True):
        '''
        Computes a Groebner Basis using Buchberger algorithm

        Input
        bool debugVerbose -- whether to output interim computations
        bool minGB -- whether to output minimal GB
        '''
        #start index
        indices = [ (i,j) for i in np.arange(len(self.polynomials)) 
                            for j in np.arange(len(self.polynomials))
                            if (i>j and 
                                self.existsIntersection(self.polynomials[i], self.polynomials[j]))]
        random.shuffle(indices)#hoping for the best

        while( len(indices)>0 ):
            i,j = indices.pop()
            sPoly=self.getSPoly(self.polynomials[i],self.polynomials[j])
            if(debugVerbose):
                print(f"Reducing S({i},{j})= {sPoly}")
                print("With")
                print(self)
            resid = self.baseReduce(sPoly,debugVerbose=debugVerbose)

            if( not resid.isZero()):
                #append new element to the base
                self.polynomials = self.polynomials + [resid]
                #append new spolys
                indices = indices + [ (i,len(self.polynomials)-1) for i in np.arange(len(self.polynomials)-1) 
                            if (self.existsIntersection(self.polynomials[i], self.polynomials[-1]))]
                random.shuffle(indices)#hoping for the best
        
        if(minGB):
            self.setMinGB()

    def setMinGB(self):
        '''
        Transforms GB into minimial GB
        '''    
        def checkDivisibility(mon1,mon2):
            return np.all(mon1.deg-mon2.deg<=0)#mon1 | mon2
        self.polynomials = [poly for poly in self.polynomials 
                                if np.all([not checkDivisibility(p.inTerm(),poly.inTerm()) 
                                        for p in self.polynomials if not (p-poly).isZero()])]
    
    
    def baseReduce(self, p1, debugVerbose=False):
        '''
        Reduces with self.polynomials as much as possible
        
        Input
        Polynomial p1 -- what to reduce
        bool debugVerbose -- whether to print reduction steps
        
        Returns
        Polynomial poly
        '''
        while(True):
            for poly in self.polynomials:
                p1,suc = self.reduce(p1,poly,debugVerbose=debugVerbose)
                if(suc):
                    break
            else:
                return p1
            
    def getReductionMonomial(self,mon1,in2):
        '''
        Gives a reduction monomial

        Input
        Monomial mon1 -- monomial to reduce
        Monomial in2 -- monomial to reduce with
        MonomialOrder order -- order to pass
        str[] vars -- list of variables to pass
        
        Returns
        Monomial redMon
        '''
        return polys.Monomial(deg=mon1.deg-in2.deg, 
                                     coef=mon1.coef/in2.coef,
                                     order=self.order, vars=self.vars).toPolynomial()
    def reduce(self, p1, p2, debugVerbose=False):
        '''
        Reduces p1 with p2 as much as possible
        
        Input
        Polynomial p1 -- what to reduce
        Polynomial p2 -- reducer
        
        Returns
        Polynomial poly
        '''
        in2 = p2.inTerm()
        p1copy = deepcopy(p1)# just in case
        
        success=False
        firstDiv = np.where([np.all((mon.deg-in2.deg)>=0) for mon in p1copy.monomials])[0]
        while(firstDiv.shape[0]>=1):
            firstDiv = firstDiv[0]
            polyMon = self.getReductionMonomial(p1copy.monomials[firstDiv],in2)

            if(debugVerbose):
                print("RED", p1copy)
            p1copy = p1copy - polyMon*p2
            if(debugVerbose):
                print("RED by", polyMon,",", p2,",", p1copy)

            success=True
            firstDiv = np.where([np.all((mon.deg-in2.deg)>=0) for mon in p1copy.monomials])[0]
            
        return p1copy, success
    
        
            
        
