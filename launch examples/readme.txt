Launch configurations
=====================

The files in this folder are for use in the Eclipse environment. 
There are two types of files: 
(1) run/debug configurations - these are for running Python programs in a configured environment
(2) external tool configurations - these for running arbitrary program
While Python programs can be run by (2), they can be debugged only if they run as (1).

The files are as follows (the number after the name indicates the type):
- riaps ctrl (1): Start the riaps controller app
- riaps dbase start (2) : Start the redis database server
- riaps dbase stop (2) : Stop the redis database server
- riaps depll (1) : Run the deployment language parser (that translates .depl files) 
  on the DistributedEstimator's sample.depl file
- riaps deplo (1) : Run the deployment manager (deplo)
- riaps disco (1) : Run the discovery service (disco)
- riaps lang (1) : Run the riaps modeling language parser (that translates 
  .riaps files) on the DistributedEstimator's sample.riaps file
- riaps run Aggregator (1) : Run the Aggregator actor of the DistributedEstimator test app
- riaps run DAverager (1) : Run the Averager actor of the DistributedAverager test app
- riaps run Estimator (1) : Run the Estimator actor of the DistributedEstimator test app 
- rpyc_registry (2) : Run the registry process (used by the riaps controller and deplo manager)

Type (1) launchers can be started from Eclipse run or debug menus, while type (2) 
launchers must be started as an 'external tool' from Eclipse. 

     