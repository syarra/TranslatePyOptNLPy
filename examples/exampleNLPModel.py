"""Use of an NLP.py model into pyOpt
    Use :

    >>>python exampleNLPModel.py

    Represents a NLP.py model as NLPModel Class and convert it to a pyOpt problem.

    Example :

        min     100 (x2 - x1^2)^2 + (1 - x1)^2
       x1,x2

       s.t.  -2000 <= 2 x2 <= 2000
             -1000 <= 3 x1 <= 1000
             -1000 <=   x1
                        x2 <= 1000
"""

import numpy as np

# Import NLPModel class
from nlp.model.nlpmodel import NLPModel
from translatePyoptNLPy import *

# Import a solver from the pyOpt package
from pyOpt import SNOPT
from pyOpt import ALGENCAN

# Create an instance of an NLPModel
class example(NLPModel):
    def __init__(self):

        NLPModel.__init__(self, 2, m=2, name='Rosenbrock', x0 = np.array([-1.2, 1]),
                 Lvar=np.array([-1000, -np.inf]), Uvar=np.array([np.inf, 1000]),
                 Lcon=np.array([-2000, -1000]), Ucon=np.array([2000, 1000]))

    def obj(self, x):
        """Define an objective function.
        fx = 100. * (x[1] - x[0]**2)**2 + (1. - x[0])**2
        return fx

    def grad(self, x):
        """Define the gradient of the objective function."""
        grad = np.zeros(self.n) 
        grad[0] = -400. * x[0] * (x[1] - x[0]**2) + 2. * x[0] -2.
        grad[1] = 200. * (x[1] - x[0]**2)
        return grad

    def cons(self, x):
        """Define a constraint."""
        cons = np.zeros(self.m)
        cons[0] = 2. * x[1]
        cons[1] = 3. * x[0]
        return cons

    def jac(self, x):
        """Define the Jacobian of the constraints."""
        jac = np.zeros([self.m, self.n])
        jac[0][0] = 0.
        jac[0][1] = 2.
        jac[1][0] = 3.
        jac[1][1] = 0.

        return jac


# Translate this NLPy problem in a pyOpt problem
nlp = example()
opt_prob = PyOpt_From_NLPModel(nlp)
print opt_prob

# Instantiate Optimizer (ALGENCAN) & Solve Problem
algencan = ALGENCAN()
algencan.setOption('iprint', 0)
algencan(opt_prob)
print opt_prob.solution(0)


# Call the imported solver SNOPT
snopt = SNOPT()

# Choose sensitivity type for computing gradients with :
#  opt_prob.grad_func : NLP.py is computing the gradients through the grad_func
#                       function
#  'FD' : finite difference
#  'CS' : complex step
SensType = opt_prob.grad_func

# Solve the opt_prob problem with SNOPT
snopt(opt_prob, sens_type=SensType)

# Print solution
print opt_prob.solution(1)

