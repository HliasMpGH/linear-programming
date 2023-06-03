from pyomo.environ import *

# Transporation cost Matrix, i.e. it costs t_cost[i,j] to get
# 1 quantity worth of food to T.K. i from kitchen j
t_cost = [[1.5, 2.4, 2.1, 3.9, 1.3, 3.8, 2.3, 3.4, 2.9, 4.6],
         [3.2, 3.8, 4.3, 4.5, 3.8, 2.4, 4.7, 4.4, 4.9, 4.8],
         [2.9, 2.3, 3.3, 4.1, 2.3, 2, 4.5, 5, 1.8, 4.5],
         [4.4, 3.5, 2, 2.6, 3.5, 5, 4.9, 1, 1.9, 3.5],
         [2.5, 1.7, 4.7, 1.3, 2.5, 2.4, 4.4, 4.3, 2.1, 4.6],
         [4.8, 4.3, 2.6, 3.7, 1.2, 1.4, 3.9, 4.4, 3.2, 4.5],
         [3.5, 2.6, 3.8, 4.2, 4, 4.4, 2.5, 4.7, 3.7, 3.9],
         [2.9, 2.8, 4.6, 2.4, 1.8, 1.2, 1.8, 1.1, 5, 4.6],
         [1, 1.6, 1.3, 2.8, 2.9, 4.8, 4, 4.6, 2.8, 5],
         [1.8, 3, 3.4, 2.9, 3.9, 4.9, 1.7, 1.2, 5, 3.9],
         [2.4, 2.6, 2.9, 4.6, 3.6, 2.9, 4, 2.7, 2.5, 4.4],
         [3.9, 4.9, 4.3, 4.8, 2.1, 4.8, 3.6, 2.4, 3, 3.3],
         [3.3, 3.8, 2.6, 4.3, 1, 4.4, 3.9, 3.2, 1.9, 2.4],
         [4.5, 2.1, 1.9, 2.8, 2, 4.6, 1.5, 1.6, 5, 1.2],
         [4.3, 4.6, 2.4, 4.6, 1.2, 2.1, 5, 3.9, 4.5, 3.1],
         [5, 3, 4.2, 4, 2.3, 1.1, 2.5, 1.5, 4.1, 3.5],
         [2.8, 1, 4.4, 1.4, 3.1, 1.4, 3.5, 4.2, 4.5, 4.6],
         [4.7, 2.2, 3.7, 3.3, 3.2, 2.2, 5, 3.2, 1.7, 2],
         [1.7, 2.3, 4.4, 1.8, 2.9, 4.3, 3.9, 2.5, 2.3, 4.6],
         [4.2, 4.6, 1.1, 1.6, 4.8, 2.5, 3.1, 4.4, 3.3, 2.3],
         [1.9, 3.6, 4.1, 4.6, 4.9, 3.1, 3.3, 4.7, 3.7, 3.3],
         [1.3, 3.1, 2.1, 1.8, 1.8, 1.2, 3.1, 1.8, 1.1, 4.8],
         [2, 4.1, 4.5, 4.7, 1.3, 4.6, 2.1, 4.3, 4.8, 4.1],
         [2.2, 2.7, 2.8, 4.8, 2.4, 1.6, 2.2, 2.5, 3.5, 2.8],
         [5, 3.6, 3, 1.5, 4.2, 4.9, 3.3, 4.7, 2.7, 2.7],
         [2.6, 4.4, 2.8, 3.3, 2.1, 3.3, 2.7, 4.5, 1.6, 3.7],
         [4, 4.7, 2.4, 3.2, 1.8, 2.9, 2, 3, 3, 2.9],
         [5, 2.9, 1.9, 1.6, 2.2, 3, 1.2, 1.1, 2.7, 2.8],
         [1.4, 3.6, 4.1, 2.6, 4.2, 4.7, 4.3, 2.1, 2.1, 1.7],
         [2.4, 3.7, 3.2, 3.3, 4.5, 3.7, 3.1, 1.2, 1.6, 3.7]]

# demand per T.K., where demand[j] is the demand in T.K. j
demand = [567, 689, 432, 582, 312, 304, 668, 595, 697, 712, \
          622, 446, 712, 411, 334, 664, 754, 573, 672, 739, \
          553, 736, 364, 719, 443, 515, 658, 722, 703, 334]

# available space per kitchen, where av_space[i] is the available space in kitchen i
av_space = [3100, 3600, 4500, 5200, 4000, 3200, 3500, 4500, 3300, 5500]

nDestinations = 30
nLocations = 10

model = ConcreteModel(name = "Assignment")

model.i = RangeSet(0, nDestinations) # set of Destinations (T.K.)
model.j = RangeSet(0, nLocations) # set of Locations (kitchens)
    
#model.nI = Param(initialize = nDestinations) # set of Destinations (T.K.)
#model.nJ = Param(initialize = nLocations) # set of Locations (kitchens)
#model.i = RangeSet(model.nI) # set of Destinations (T.K.)
#model.j = RangeSet(model.nJ) # set of Locations (kitchens)

model.d = Var(model.j, within = Binary) # dj, binary variable so that d[i] is 1 if kitchen i opens
model.m = Var(model.i, model.j, within = NonNegativeReals) # mij, where m[i][j] is the quantity that is being transfered to i from j 

print(*model.i)
print(model.d[0])
print(model.m[0][0])

model.obj = Objective(expr = sum(t_cost[i][j]*model.m[i][j] for j in model.j for i in model.i ))

model.constraints = ConstraintList()

opt = SolverFactory("glpk")

#results_obj = opt.solve(model, tee = False)