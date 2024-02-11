import numpy as np


class Monomial:
    '''
        A monomial x^deg with deg represented as an integer array
    '''
    def __init__(self, deg, coef, letters = "xyzwtprsuv"):
        '''
        Parameters

        int[] deg -- a sequence of degrees
        float coef -- a coefficient (assumed to be just real for now)
        '''
        self.deg = deg
        self.coef = coef

    #Comparators
    def __eq__(self, other):
        '''
        A comparator x==y
        '''
        pass
    def __lt__(self, other):
        '''
        A comparator x<y
        '''
        pass
    def __le__(self, other):
        '''
        A comparator x<=y
        '''
        pass
    def __gt__(self, other):
        '''
        A comparator x>y
        '''
        pass
    def __ge__(self, other):
        '''
        A comparator x>=y
        '''
        pass

    #Operations
    def __mul__(self,other):
        '''
        * operation, just adding degrees and multiplying coefs
        '''
        pass
    def __add__(self,other):
        '''
        + operation, just adding coefficients if the degrees are the same
        '''
        pass
    def __add__(self,other):
        '''
        - operation, just subtracting coefficients if the degrees are the same
        '''
        pass


    #call as a function
    def __call__(self, x):
        '''
        Computes value at point x

        Parameters
        float[] x -- a batch (...,d) of points
        OR
        float[] x -- a point (d,)
        '''
        pass


    def __str__(self):
        '''
        Gives a string representation
        '''
        pass

    def degree(self):
        '''
        Returns the degree of the polynomial
        '''
        pass



class Polynomial:
    '''
        A monomial x^deg with deg represented as an integer array
    '''
    def __init__(self, monomials, order, letters = "xyzwtprsuv"):
        '''
        Parameters

        Monomial[] -- a sequence of monomials
        MonomialOrder order -- a monomial order
        float coef -- a coefficient (assumed to be just real for now)
        '''
        self.monomials = monomials
        self. order = order
        self.letters = letters

    #Comparator eq
    def __eq__(self, other):
        '''
        A comparator x==y
        '''
        pass
    

    #Operations
    def __mul__(self,other):
        '''
        * operation, just adding degrees and multiplying coefs
        '''
        pass
    def __add__(self,other):
        '''
        + operation, just adding coefficients if the degrees are the same
        '''
        pass
    def __add__(self,other):
        '''
        - operation, just subtracting coefficients if the degrees are the same
        '''
        pass


    #call as a function
    def __call__(self, x):
        '''
        Computes value at point x

        Parameters
        float[] x -- a batch (<shape>,d) of points
        OR
        float[] x -- a point (d,)

        Returns
        float (<shape>) or float
        '''
        pass


    #give a fancy string
    def __str__(self):
        '''
        Gives a string representation
        '''
        pass

    def degree(self):
        '''
        Returns the degree of the polynomial
        '''
        pass

    def sort(self):
        '''
        Sorts the monomials
        '''
        pass
