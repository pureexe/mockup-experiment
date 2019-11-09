from SQLiteExperiment import SQLiteExperiment
#class MyExperiment(SQLiteExperiment):
#    def __init__(self):
#        inputs = ['alpha','beta','gamma']
#        outputs = ['a','b','c']
#        super().__init__(inputs,outputs,overwrite = True)

compute = lambda v: {
    'a': -v['alpha']-2*v['beta']-2*v['gamma']+6,
    'b': -v['alpha']-2*v['beta']+v['gamma'],
    'c': v['alpha']-3*v['gamma']/v['beta']
}
experiment = SQLiteExperiment(['alpha','beta','gamma'],['a','b','c'],computeFunction=compute,overwrite=True)
experiment.build()
experiment.add('change alpha','alpha',{'alpha':1,'beta':1,'gamma':1},0.25,10,'study to how alpha value affact the output a,b,c')
experiment.add('varie beta','beta',{'alpha':1,'beta':1,'gamma':1},0.25,10,'How beta variable change output a,b,c ')
experiment.add('gamma observe','gamma',{'alpha':1,'beta':1,'gamma':1},0.25,10,'output a,b,c that create from difference gamma value')
experiment.run()
experiment.plot()
