import pyomo.environ as pyo

model = pyo.ConcreteModel()
model.nVars = pyo.Param(initialize=4)
model.N = pyo.RangeSet(model.nVars)
model.x = pyo.Var(model.N, within=pyo.Binary)
model.obj = pyo.Objective(expr=pyo.summation(model.x))
model.cuts = pyo.ConstraintList()
opt = SolverFactory('glpk')
#opt.solve(model) 