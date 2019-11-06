
import sqlite3
import matplotlib.pyplot as plt

def function_a(alpha,beta,gamma):
    return alpha+2*beta+gamma
    
def function_b(alpha,beta,gamma):
    return alpha-2*beta - 2*gamma

def function_c(alpha,beta,gamma):
    return alpha-3*gamma/beta

def database_intialize():
    connection = sqlite3.connect('mockup-experiment.db')
    c = connection.cursor()
    c.execute("""
        CREATE TABLE fact (
            experiment integer,
            alpha real,
            beta real,
            gamma real,
            a real,
            b real,
            c real
        )
    """)
    c.execute("""
        CREATE TABLE experiment (
            id integer primary key,
            name text,
            description text,
            variable text,
            initial_alpha real,
            initial_beta real,
            initial_gamma real,
            per_step real,
            step integer
        )
    """)
    connection.commit()
    connection.close()

def prepare_experiment():
    connection = sqlite3.connect('mockup-experiment.db')
    e1 = (1,'change alpha','study to how alpha value affact the output a,b,c','alpha',1,1,1,0.25,10)
    e2 = (2,'varie beta','How beta variable change output a,b,c ','beta',1,1,1,0.25,10)
    e3 = (3,'gamma observe','output a,b,c that create from difference gamma value ','gamma',1,1,1,0.25,10)
    c = connection.cursor()
    sql_insert = ''' 
        INSERT INTO experiment(
            id,name,description,variable,initial_alpha,initial_beta,initial_gamma,per_step,step
        ) VALUES (
            ?,?,?,?,?,?,?,?,?
        ) 
    '''
    c = connection.cursor()
    c.execute(sql_insert, e1)
    c.execute(sql_insert, e2)
    c.execute(sql_insert, e3)
    connection.commit()
    connection.close()

def run_experiment():
    connection = sqlite3.connect('mockup-experiment.db')
    connection.row_factory = sqlite3.Row  
    cursor = connection.cursor()
    cursor.execute("SELECT id,variable,initial_alpha,initial_beta,initial_gamma,per_step,step FROM experiment")
    rows = cursor.fetchall()
    for row in rows:
        v = {
            'alpha': row['initial_alpha'],
            'beta': row['initial_beta'],
            'gamma': row['initial_gamma']
        }
        for i in range(row['step']):
            a = function_a(v['alpha'],v['beta'],v['gamma'])
            b = function_b(v['alpha'],v['beta'],v['gamma'])
            c = function_c(v['alpha'],v['beta'],v['gamma'])
            value = (row['id'],v['alpha'],v['beta'],v['gamma'],a,b,c)
            cursor.execute('INSERT INTO fact(experiment,alpha,beta,gamma,a,b,c) VALUES (?,?,?,?,?,?,?)',value)
            v[row['variable']] = v[row['variable']] + row['per_step']
    connection.commit()
    connection.close()

def plot_experiment():
    connection = sqlite3.connect('mockup-experiment.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM experiment')
    experiment_rows = cursor.fetchall()
    for experiment in experiment_rows:
        cursor.execute('SELECT')
    connection.close()
    connection.close()
# database_intialize()
# prepare_experiment()
# run_experiment()
