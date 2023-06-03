from pyomo.environ import *

model = ConcreteModel(name = "Assignment")
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

# demand per T.K., where demand[k] is the demand in T.K. k
demand = [567, 689, 432, 582, 312, 304, 668, 595, 697, 712, \
          622, 446, 712, 411, 334, 664, 754, 573, 672, 739, \
          553, 736, 364, 719, 443, 515, 658, 722, 703, 334]

# fixed cost, where f_cost[k] is the needed cost to open kitchen k 
f_cost = [300000, 530000, 410000, 395000, 400000, 350000, 285000, 310000, 420000, 480000]

# available space per kitchen, where av_space[k] is the available space in kitchen k
av_space = [3100, 3600, 4500, 5200, 4000, 3200, 3500, 4500, 3300, 5500]

nLocations = 10
nDestinations = 30


model.locations = range(0, nLocations) # set of Locations (kitchens)
model.destinations = range(0, nDestinations) # set of Destinations (T.K.)
    
#model.nI = Param(initialize = nDestinations) # set of Destinations (T.K.)
#model.nJ = Param(initialize = nLocations) # set of Locations (kitchens)
#model.i = RangeSet(model.nI) # set of Destinations (T.K.)
#model.j = RangeSet(model.nJ) # set of Locations (kitchens)

model.d = Var(model.locations, within = Binary) # dj, binary variable so that d[j] is 1 if kitchen j opens
model.m = Var(model.destinations, model.locations, within = NonNegativeIntegers) # mij, where m[i,j] is the quantity that is being transfered to i from j 

#                                                        variable cost                                                     fixed cost
model.obj = Objective(expr = sum(t_cost[i][j] * model.m[i,j] for i in model.destinations for j in model.locations) + sum(model.d[j] * f_cost[j] for j in model.locations), sense = minimize)


model.x = Var(model.locations, within = NonNegativeIntegers) # xj, where x[j] is the quantity that kitchen j produces
model.z = Var(model.destinations, model.locations, within = Binary) # yij, binary variable so that y[i,j] is 1 if TK i is being served from kitchen j

''' 
    ------------------------------------------------
    QA: the mathematical model described in a)
    ------------------------------------------------
'''

model.constraints = ConstraintList()

# define x[k] as the total quantity kitchen k produces
for j in model.locations :
    model.constraints.add(model.x[j] == sum(model.m[i,j] for i in model.destinations))

# each k kitchen can only produce up to av_space[k] of goods
for j in model.locations :
    model.constraints.add(model.x[j] <= av_space[j] * model.d[j])

# each TK has to be served by one and only kitchen
for i in model.destinations:
    model.constraints.add(sum(model.z[i,j] for j in model.locations) == 1)

# each k TK has to receive exaclty demand[k] worth of goods 
for i in model.destinations :
    for j in model.locations :
        model.constraints.add(model.m[i,j] == demand[i] * model.z[i,j])
'''
# each k TK has to receive exaclty demand[k] worth of goods 
for i in model.destinations:
    model.constraints.add(sum(model.m[i,j] for j in model.locations) == demand[i])
'''
''' 
    ------------------------------------------------
    QB: the constraint additions needed in order 
    to implement the model described in b)
    ------------------------------------------------
'''

# kitchen 10 & 2 (9 & 1 in the model) have to open if kitchen 1 does
model.constraints.add(model.d[0] <= model.d[1])
model.constraints.add(model.d[0] <= model.d[9])
# note : if kitchen 1 does *not* open, the other kitchens are not limited about if they work or not 

# if kitchen 6 opens, kitchen 7 has to remain closed
model.constraints.add(model.d[5] + model.d[6] <= 1)

# kitchens 4, 7, 8 & 9 cant open all together
model.constraints.add(model.d[3] + model.d[6] +model.d[7] + model.d[8] <= 3)

opt = SolverFactory("glpk")

results_obj = opt.solve(model, tee = False)

print("------------------------------------------------")
print("\t\tResults")
print("------------------------------------------------\n")
print("FastVegan has to open kitchens in Location(s):", end = " ")
for j in model.locations :
    if value(model.d[j]) == 1 :
        print(j + 1, end = ",")
print("\r")

for j in model.locations :
    if value(model.d[j]) == 1 :
        print(j + 1,"will serve",value(model.x[j]),"portions")
print("\n")

for i in model.destinations :
    print("TK #",i + 1,"is going to eat from Location:", end = " ")
    for j in model.locations :
        if value(model.z[i,j]) == 1 :
            print(j+1)
            break
    print("\r")

print("------------------------------------------------")
print("Total cost of Franchise:",value(model.obj))
print("------------------------------------------------\n")
