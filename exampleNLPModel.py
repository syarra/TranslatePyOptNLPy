##################################
# Use an NLP model into pyOpt #
##################################
"""
    Use :

    >>>python exampleNLPModel.py

    Represents a NLP as NLPModel Class and convert it to a pyOpt problem.

    Example :

        min     100 (x2 - x1^2)^2 + (1 - x1)^2
       x1,x2

       s.t.  -2000 <= 2 x2 <= 2000
             -1000 <= 3 x1 <= 1000
             -1000 <=   x1
                        x2 <= 1000
"""

import numpy

# Import NLPModel class
from nlpy.model import NLPModel
from TranslatePyOptNLPy import *

# Import a solver from the pyOpt package
from pyOpt import SNOPT

# Define an objective function
def rosenbrock(x):
    return 100. * (x[1] - x[0]**2)**2 + (1. - x[0])**2


# and its gradient
def gradient_rosenbrock(x):
    grad = numpy.zeros(nlp.n)
    grad[0] = -400. * x[0] * (x[1] - x[0]**2) + 2. * x[0] -2.
    grad[1] = 200. * (x[1] - x[0]**2)

    return grad


# Define a constraint
def constraint(x):

    return numpy.array([2.*x[1],3.*x[0]])


# and its gradient 
def gradient_constraint(i,x):

    grad = numpy.zeros(nlp.n)

    if i == 1:
        grad[0] = 0.
        grad[1] = 2.
    elif i == 2:
        grad[0] = 3.
        grad[1] = 0.

    return grad


Infinity = numpy.inf

# Create an instance of an NLPModel
nlp = NLPModel(n=2, m=2, name='Rosenbrock',
        Lvar=numpy.array([-1000,-Infinity]), Uvar=numpy.array([Infinity,1000]),
        Lcon=numpy.array([-2000,-1000]), Ucon=numpy.array([2000,1000]),
        x0 = numpy.array([-1.2, 1]))


# Assign an objective function and its gradient
nlp.obj = rosenbrock
nlp.grad = gradient_rosenbrock

# Assign constraints and its gradients
nlp.cons = constraint
nlp.igrad = gradient_constraint


# Translate this NLPy problem in a pyOpt problem

opt_prob = PyOpt_From_NLPModel(nlp)
print opt_prob

# Call the imported solver SNOPT
snopt = SNOPT()

# Choose sensitivity type for computing gradients with :
#  opt_prob.grad_func : NLPy is computing the gradients through the grad_func
#                       function
#  'FD' : finite difference
#  'CS' : complex step
SensType = opt_prob.grad_func

# Solve the opt_prob problem with SNOPT
snopt(opt_prob, sens_type=SensType)

# Print solution
print opt_prob._solutions[0]


# Change the sensitivity type to finite difference and solve again
SensType = 'FD'
snopt(opt_prob, sens_type=SensType)
print opt_prob._solutions[1]


# Change the sensitivity type to complex step and solve again
SensType = 'CS'
snopt(opt_prob, sens_type=SensType)
print opt_prob._solutions[2]


