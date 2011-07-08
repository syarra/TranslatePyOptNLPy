g3 3 1 0	# problem diet1
 9 7 1 1 0	# vars, constraints, objectives, ranges, eqns
 0 0	# nonlinear constraints, objectives
 0 0	# network constraints: nonlinear, linear
 0 0 0	# nonlinear vars in constraints, objectives, both
 0 0 0 1	# linear network variables; functions; arith, flags
 0 9 0 0 0	# discrete variables: binary, integer, nonlinear (b,c,o)
 58 9	# nonzeros in Jacobian, gradients
 0 0	# max name lengths: constraints, variables
 0 0 0 0 0	# common exprs: b,c,o,c1,o1
C0	#Diet['Cal']
n0
C1	#Diet['Carbo']
n0
C2	#Diet['Protein']
n0
C3	#Diet['VitA']
n0
C4	#Diet['VitC']
n0
C5	#Diet['Calc']
n0
C6	#Diet['Iron']
n0
O0 0	#Total_Cost
n0
r	#7 ranges (rhs's)
2 2000
0 350 375
2 55
2 100
2 100
2 100
2 100
b	#9 bounds (on variables)
0 0 11
0 0 10
0 0 8
0 0 9
0 0 8
0 0 14
0 0 13
0 0 31
0 0 18
k8	#intermediate Jacobian column lengths
7
14
21
27
34
39
45
51
J0 9
0 510
1 370
2 500
3 370
4 400
5 220
6 345
7 110
8 80
J1 9
0 34
1 35
2 42
3 38
4 42
5 26
6 27
7 12
8 20
J2 9
0 28
1 24
2 25
3 14
4 31
5 3
6 15
7 9
8 1
J3 8
0 15
1 15
2 6
3 2
4 8
6 4
7 10
8 2
J4 7
0 6
1 10
2 2
4 15
5 15
7 4
8 120
J5 8
0 30
1 20
2 25
3 15
4 15
6 20
7 30
8 2
J6 8
0 20
1 20
2 20
3 10
4 8
5 2
6 15
8 2
G0 9
0 1.84
1 2.19
2 1.84
3 1.44
4 2.29
5 0.77
6 1.29
7 0.6
8 0.72
