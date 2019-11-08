
import sqlite3
import matplotlib.pyplot as plt
import numpy as np

def function_a(alpha,beta,gamma):
    return -alpha-2*beta-2*gamma+6
    
def function_b(alpha,beta,gamma):
    return alpha-2*beta+gamma

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
    fig, axs = plt.subplots(len(experiment_rows))
    trend = lambda a,b: np.poly1d(np.polyfit(a, b, 1))(a)
    colors = ['#f00000','#00f000','#0000f0']
    markers = ['o','*','x']
    for i in range(len(experiment_rows)):
        axs[i].set_title(experiment_rows[i]['name'])
        axs[i].set_xlabel(experiment_rows[i]['description'])
        cursor.execute('SELECT * FROM fact WHERE experiment = ?', (i+1,))
        fact_rows = list(cursor.fetchall())
        varie_variable = ['alpha','beta','gamma'].index(experiment_rows[i]['variable']) + 1
        x_axis = [f[varie_variable] for f in fact_rows]
        for j in range(3):
            y_axis = [f[j+4] for f in fact_rows]
            axs[i].scatter(x_axis, y_axis, color=colors[j], marker=markers[j])
            axs[i].plot(x_axis,trend(x_axis, y_axis), c=colors[j], ls ='--')
    fig.tight_layout()
    try:
        plt.show()
    except:
        plt.savefig("plot.png")


    connection.commit()
    connection.close()
#database_intialize()
#prepare_experiment()
#run_experiment()
plot_experiment()