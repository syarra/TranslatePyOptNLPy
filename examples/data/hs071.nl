g3 0 1 0	# problem hs071
 4 2 1 0 1	# vars, constraints, objectives, ranges, eqns
 2 1	# nonlinear constraints, objectives
 0 0	# network constraints: nonlinear, linear
 4 4 4	# nonlinear vars in constraints, objectives, both
 0 0 0 1	# linear network variables; functions; arith, flags
 0 0 0 0 0	# discrete variables: binary, integer, nonlinear (b,c,o)
 8 4	# nonzeros in Jacobian, gradients
 0 0	# max name lengths: constraints, variables
 0 0 0 0 0	# common exprs: b,c,o,c1,o1
C0	#inequality
o2	#*
o2	#*
o2	#*
v0	#x1
v1	#x2
v2	#x3
v3	#x4
C1	#equality
o54	#sumlist
4
o5	#^
v0	#x1
n2
o5	#^
v1	#x2
n2
o5	#^
v2	#x3
n2
o5	#^
v3	#x4
n2
O0 0	#obj
o2	#*
o2	#*
v0	#x1
v3	#x4
o54	#sumlist
3
v0	#x1
v1	#x2
v2	#x3
x4	# initial guess
0 1
1 5
2 5
3 1
r	#2 ranges (rhs's)
2 25
4 40
b	#4 bounds (on variables)
0 1 5
0 1 5
0 1 5
0 1 5
k3	#intermediate Jacobian column lengths
2
4
6
J0 4
0 0
1 0
2 0
3 0
J1 4
0 0
1 0
2 0
3 0
G0 4
0 0
1 0
2 1
3 0
