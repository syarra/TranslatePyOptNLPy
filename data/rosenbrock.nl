g3 0 1 0	# problem rosenbrock
 2 1 1 1 0	# vars, constraints, objectives, ranges, eqns
 1 1	# nonlinear constraints, objectives
 0 0	# network constraints: nonlinear, linear
 2 2 2	# nonlinear vars in constraints, objectives, both
 0 0 0 1	# linear network variables; functions; arith, flags
 0 0 0 0 0	# discrete variables: binary, integer, nonlinear (b,c,o)
 2 2	# nonzeros in Jacobian, gradients
 0 0	# max name lengths: constraints, variables
 0 0 0 0 2	# common exprs: b,c,o,c1,o1
C0	#constraint1
o2	#*
v0	#x[1]
v1	#x[2]
V2 1 2	#f1
1 10
o2	#*
n-10
o5	#^
v0	#x[1]
n2
V3 1 2	#f2
0 -1
n1
O0 0	#norm
o0	# + 
o5	#^
v2	#f1
n2
o5	#^
v3	#f2
n2
x2	# initial guess
0 -1.2
1 1
r	#1 ranges (rhs's)
0 -2e+05 2e+05
b	#2 bounds (on variables)
3
3
k1	#intermediate Jacobian column lengths
1
J0 2
0 0
1 0
G0 2
0 0
1 0
