import sqlite3
import numpy as np
import matplotlib.pyplot as plt
import os

class SQLiteExperiment(object):
    
    def __init__(self,inputs,outputs,computeFunction = None, path = 'experiment.db',overwrite = False):
        self.__inputs = inputs
        self.__outputs = outputs
        self.__database_path = path
        self.__database_overwrite = overwrite
        self.__connection = None
        self.__computeFunction = computeFunction
        

    def build(self):
        """ create database file """
        if os.path.isfile(self.__database_path):
            if self.__database_overwrite:
                os.remove(self.__database_path)
            else:
                return #don't overwrite database
        fact_f = ','.join([f + ' real' for f in self.__inputs+self.__outputs])
        experiment_f = ',\n'.join(['initial_'+ f + ' real' for f in self.__inputs])
        sql_fact = 'CREATE TABLE fact (experiment integer,{})'.format(fact_f)
        sql_experiment = '''
            CREATE TABLE experiment (
                id integer primary key autoincrement,
                name text,
                description text,
                variable text,
                {},
                per_step real,
                step integer
            )
        '''.format(experiment_f)
        c = self.get_cursor()
        c.execute(sql_fact)
        c.execute(sql_experiment)
        self.commit()

    def add(self,name,variable,initials,per_step,step,description = ''):
        """ add experiment """
        initials_f = ','.join(['initial_'+f for f in self.__inputs])
        place_f = ','.join('?' for f in self.__inputs)
        values = [initials[f] if f in initials else 0 for f in self.__inputs]
        values = tuple([name,description,variable] + values + [per_step,step])
        sql_insert = ''' 
            INSERT INTO experiment(
                name,description,variable,{},per_step,step
            ) VALUES (
                ?,?,?,{},?,?
            )
        '''.format(initials_f,place_f)
        c = self.get_cursor()
        c.execute(sql_insert,values)
        self.commit()
        return c.lastrowid
    
    def compute(self, inputs):
        return dict([(k,0) for k in self.__outputs])


    def run(self,computeFunction = None):
        """ run the experiment """
        c = self.get_cursor()
        c.execute('SELECT * FROM experiment')
        experiment_rows = c.fetchall()
        computeCode = computeFunction
        if computeFunction is None:
            computeCode = self.__computeFunction
        if computeCode is None:
            computeCode = self.compute
        for row in experiment_rows:
            for step in range(row['step']):
                init_pair = [(f,row['initial_'+f] + ( \
                    step*row['per_step'] if f == row['variable'] else 0 \
                )) for f in self.__inputs ] 
                outputs = computeCode(dict(init_pair))
                input_key, input_value = zip(*init_pair)
                output_key, output_value = zip(*list(outputs.items()))
                values = tuple([row['id']] + list(input_value) + list(output_value))
                keys = tuple(list(input_key) + list(output_key))
                key_f = ','.join(keys)
                place_f = ','.join(['?' for k in values])
                sql = 'INSERT INTO fact(experiment,{}) VALUES ({})'
                sql = sql.format(key_f,place_f)
                c.execute(sql,values)
        self.commit()

    def plot(self):
        """ display the port """
        c = self.get_cursor()
        c.execute('SELECT * FROM experiment')
        experiment_rows = c.fetchall()
        fig, axs = plt.subplots(len(experiment_rows))
        trend = lambda a,b: np.poly1d(np.polyfit(a, b, 1))(a)
        input_len = len(self.__inputs)
        output_len = len(self.__outputs)
        for i in range(len(experiment_rows)):
            axs[i].set_title(experiment_rows[i]['name'])
            axs[i].set_xlabel(experiment_rows[i]['description'])
            c.execute('SELECT * FROM fact WHERE experiment = ?', (i+1,))
            fact_rows = list(c.fetchall())
            varie_variable = self.__inputs.index(experiment_rows[i]['variable']) + 1
            x_axis = [f[varie_variable] for f in fact_rows]
            for j in range(input_len):
                y_axis = [f[j + output_len + 1] for f in fact_rows]
                axs[i].scatter(x_axis, y_axis)
                axs[i].plot(x_axis,trend(x_axis, y_axis))
        fig.tight_layout()
        try:
            plt.show()
        except:
            plt.savefig("plot.png")

    def connect(self):
        """ connect database """
        self.__connection = sqlite3.connect(self.__database_path)
        self.__connection.row_factory = sqlite3.Row 
    def commit(self):
        self.__connection.commit()
    def disconnect(self):
        """ disconnect database """
        self.__connection.close()

    def get_cursor(self):
        """ return cursor of database """
        if self.__connection is None:
            self.connect()
        return self.__connection.cursor()

    def __del__(self):
        if not self.__connection is None:
            self.disconnect()

    # TODO feature implement soon (TM)
    # def get():
    #    """ get experiment """
    # def fact():
    #    """ get fact table """
    # def remove()
    #    """ remove experiment """
