.. highlight:: shell

===============
CINELDI example
===============

To run the CINELDI example do the following:

.. code-block:: console

    $ cd examples/CINELDI
    $ python run.py

This will produce a directory called "results" containing the simulation
results. The directory has the following structure:

.. code-block:: console

    results                                                                         
    ├── monte_carlo                                                                 
    │   ├── B1                                                                      
    │   ├── B2                                                                      
    │   ├── B3                                                                      
    │   ├── B4                                                                      
    │   ├── B5                                                                      
    │   │   └── EV1                                                                 
    │   ├── B6                                                                      
    │   ├── dist_network1                                                           
    │   ├── M1     
    │   ├── M2
    │   ├── M3                              
    │   ├── microgrid1
    │   ├── ps1                             
    │   └── trans_network1
    └── sequence      
        ├── 1          
        │   ├── battery                     
        │   ├── bus                         
        │   ├── circuitbreaker
        │   ├── disconnector 
        │   ├── dist_network1           
        │   ├── distribution_controllers    
        │   ├── ev_parks                    
        │   ├── line                        
        │   ├── microgrid1              
        │   ├── microgrid_controllers
        │   ├── ps1                         
        │   └── trans_network1              
        └── 2                               
            ├── battery
            ├── bus                         
            ├── circuitbreaker
            ├── disconnector 
            ├── dist_network1           
            ├── distribution_controllers    
            ├── ev_parks                    
            ├── line                        
            ├── microgrid1              
            ├── microgrid_controllers
            ├── ps1                         
            └── trans_network1

As you can see, the results are divided into a Monte Carlo
directory and a sequence directory. They contain Monte Carlo
and sequential results respectively. 

Below is an example of how to read and obtain some distribution
metrics for the `ENS` (Energy Not Supplied) index of the power system
(ps1) using `pandas`.

.. code-block:: python

    import os
    import pandas as pd
    
    path = os.path.join(
        "results",
        "monte_carlo",
        "ps1",
        "ENS.csv",
    )
    
    df = pd.read_csv(path, index_col=0)
    
    print(df.describe())
