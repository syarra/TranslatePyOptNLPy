"""
Translation between pyOpt and NLPy

..moduleauthor:: S. Arreckx <sylvain.arreckx@polymtl.ca>
"""

import numpy
from pyOpt import Optimization
from pyOpt_gradient import Gradient
from nlpy.model import NLPModel


"""
Class to translate a pyOpt model into a NLPy model or a NLPy model into
a pyOpt model
"""

class PyOpt_From_NLPModel(Optimization):

    def __init__(self, nlpy_model, **kwargs):
        """
        :parameters:

            :nlpy_model: nonlinear problem from the NLPModel class or
                         from AmplModel class
        """

        if nlpy_model.__module__ == 'nlpy.model.amplpy':
            print 'AMPL model'
            print "AMPL isn't handling complex values"
            print "Choose 'FD' or 'opt_prob.grad_func' for sensitivity"

        # Initialize model.
        Optimization.__init__(self, nlpy_model.name, lambda x:
                                    (self.nlpy_model.obj(x),
                                     self.nlpy_model.cons(x),0),
                                     var_set={}, obj_set={}, con_set={},
                                     use_groups=False, **kwargs)

        self.nlpy_model = nlpy_model

        self.addObj('f')

        # Assigning lower and upper bounds on variables
        for i in range(0,self.nlpy_model.n):

            if i in self.nlpy_model.lowerB:
                self.addVar("x"+ "%d"%(i+1), lower=self.nlpy_model.Lvar[i],
                        upper=numpy.inf, value=self.nlpy_model.x0[i])
            elif i in self.nlpy_model.upperB:
                self.addVar("x"+ "%d"%(i+1), lower=-numpy.inf,
                        upper=self.nlpy_model.Uvar[i], value=self.nlpy_model.x0[i])
            elif i in self.nlpy_model.rangeB:
                self.addVar("x"+ "%d"%(i+1), lower=self.nlpy_model.Lvar[i],
                        upper=self.nlpy_model.Uvar[i], value=self.nlpy_model.x0[i])
            elif i in self.nlpy_model.freeB:
                self.addVar("x"+ "%d"%(i+1), value=self.nlpy_model.x0[i],
                            lower=-numpy.inf, upper=numpy.inf)

        # Assigning lower and upper bounds on constraints
        for i in range(0,nlpy_model.m):

            if i in nlpy_model.lowerC:
                self.addCon("g"+"%d"%(i+1), 'i', lower=nlpy_model.Lcon[i],
                            upper=numpy.inf)
            elif i in nlpy_model.upperC:
                self.addCon("g"+"%d"%(i+1), 'i', lower=-numpy.inf,
                            upper=nlpy_model.Ucon[i])
            elif i in nlpy_model.rangeC:
                self.addCon("g"+"%d"%(i+1), 'i', lower=nlpy_model.Lcon[i],
                            upper=nlpy_model.Ucon[i])
            elif i in nlpy_model.equalC:
                self.addCon("g"+"%d"%(i+1), 'e', equal=nlpy_model.Lcon[i])



    def grad_func(self, x, f, g):

        g_obj = numpy.array([self.nlpy_model.grad(x)])
        g_con = numpy.zeros([self.nlpy_model.m, self.nlpy_model.n])

        for i in range(0,self.nlpy_model.m):
            g_con[i] = self.nlpy_model.igrad(i,x)

        fail = 0
        return g_obj, g_con, fail


class NLPModel_From_PyOpt(NLPModel):

    def __init__(self, pyopt_model, sens_type, **kwargs):
        """
        :parameters:

           :nlp:       nonlinear problem pyOpt
            :sens_type:  sensitivity type
                'FD' : estimation of gradients using finite differences
                'CS' : estimation of gradients using complex step
                grad_func : user provided gradients
        """

        self.pyopt_model = pyopt_model

        # Problem dimensions.
        nbVar = len(pyopt_model._variables)
        nbCons = len(pyopt_model._constraints)

        # Bounds on variables.
        LVar = -numpy.inf * numpy.ones(nbVar)
        UVar = numpy.inf * numpy.ones(nbVar)
        X0 = numpy.zeros(nbVar)

        for i in range(nbVar):
            var = pyopt_model.getVar(i)
            LVar[i] = var.lower
            UVar[i] = var.upper
            X0[i] = var.value

        # Constraints left and right-hand side.
        LCon = -numpy.inf * numpy.ones(nbCons)
        UCon = numpy.inf * numpy.ones(nbCons)

        for j in range(nbCons):
            cons = pyopt_model.getCon(j)
            if cons.type=='i':
                LCon[j] = cons.lower
                UCon[j] = cons.upper
            elif cons.type=='e':
                LCon[j] = cons.equal
                UCon[j] = cons.equal

        # Differentiation method.
        self.sens_type = sens_type
        if sens_type == 'FD':
            self.sens_step = 1e-6
        else:
            self.sens_step = 1e-20

        self.gradient_method = Gradient(pyopt_model, sens_type, '',
                                        self.sens_step)

        # Saved values (private).
        self._last_x = None
        self._last_obj = None
        self._last_grad_obj = None
        self._last_cons = None
        self._last_grad_con = None

        # Initialize model.
        NLPModel.__init__(self, name=pyopt_model.name, n=nbVar, m=nbCons, Lvar=LVar, Uvar=UVar,
                          Lcon=LCon, Ucon=UCon, x0=X0, **kwargs)

    def obj(self, x):
        if self._last_obj is not None and (self._last_x == x).all():
            return self._last_obj
        f, c, fail = self.pyopt_model.obj_fun(x)
        self._last_x = x[:]
        self._last_obj = f
        self._last_cons = c
        self._last_grad_obj = None  # Gradient out of date.
        self._last_grad_con = None # Gradient out of date.
        return f

    def cons(self, x):
        if self._last_cons is not None and (self._last_x == x).all():
            return self._last_cons
        f, c, fail = self.pyopt_model.obj_fun(x)
        self._last_x = x[:]
        self._last_obj = f
        self._last_cons = c
        self._last_grad_obj = None  # Gradient out of date.
        self._last_grad_con = None # Gradient out of date.
        return c

    def grad(self, x):
        if self._last_grad_obj is not None and (self._last_x == x).all():
            return self._last_grad_obj
        f, c, fail = self.pyopt_model.obj_fun(x)
        grad = self.gradient_method.getGrad(x, {}, [f], c)
        self._last_x = x[:]
        self._last_obj = f
        self._last_cons = c
        self._last_grad_obj = grad[0].flatten()
        self._last_grad_con = grad[1]
        return grad[0].flatten()

    def igrad(self, x, i):
        if self._last_grad_con is not None and (self._last_x == x).all():
            return self._last_grad_con[i]
        f, c, fail = self.pyopt_model.obj_fun(x)
        grad = self.gradient_method.getGrad(x, {}, [f], c)
        self._last_x = x[:]
        self._last_obj = f
        self._last_cons = c
        self._last_grad_obj = grad[0].flatten()
        self._last_grad_con = grad[1]
        return grad[1][i]


