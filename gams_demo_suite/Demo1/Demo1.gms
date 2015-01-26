**    (c) Copyright 2014, University of Manchester
**
**    This file is part of the GAMS Plugin Demo Suite.
**
**    The GAMS Plugin Demo Suite is free software: you can redistribute it and/or modify
**    it under the terms of the GNU General Public License as published by
**    the Free Software Foundation, either version 3 of the License, or
**    (at your option) any later version.
**
**    The GAMS Plugin Demo Suite is distributed in the hope that it will be useful,
**    but WITHOUT ANY WARRANTY; without even the implied warranty of
**    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
**    GNU General Public License for more details.
**
**    You should have received a copy of the GNU General Public License
**    along with the GAMS Plugin Demo Suite.  If not, see <http://www.gnu.org/licenses/>.
**

$TITLE    Demo1.gms

* version: no time-step

 option limrow=10000;
 option limcol=10000;

** ----------------------------------------------------------------------
**  Loading Data: sets, parameters and tables
** ----------------------------------------------------------------------

$        include "dataset.txt";

** ----------------------------------------------------------------------
**  Model variables and equations
** ----------------------------------------------------------------------

VARIABLES
Q(i,j) flow in each link in each period
delivery (i) water delivered to demand node i in each period
Z objective function
;

POSITIVE VARIABLES
Q
;

EQUATIONS
MassBalance_nonstorage(non_storage_nodes)
MinFlow(i,j)
MaxFlow(i,j)
DemandDelivery(demand_nodes)
Objective
;

* Objective function

Objective ..
    Z =E= SUM((i,j)$links(i,j), Q(i,j) * link_scalar_data(i,j, 'cost'))
;

*Calculating water delivery for each demand node at each time step

DemandDelivery(demand_nodes)..
         delivery(demand_nodes) =E= SUM(j$links(j,demand_nodes), link_scalar_data(j,demand_nodes, "flow_multiplier")
         *Q(j,demand_nodes));

* Mass balance constrait for non-storage nodes

MassBalance_nonstorage(non_storage_nodes) ..
    junction_scalar_data(non_storage_nodes, 'inflow')+
    SUM(j$links(j,non_storage_nodes), Q(j,non_storage_nodes)* link_scalar_data(j,non_storage_nodes, 'flow_multiplier'))
    - SUM(j$links(non_storage_nodes,j), Q(non_storage_nodes,j))
    - demand_scalar_data(non_storage_nodes, 'consumption_coefficient')$demand_nodes(non_storage_nodes) * delivery(non_storage_nodes)
    =E= 0;

* Lower and upper bound of possible flow in links

MinFlow(i,j)$links(i,j) ..
    Q(i,j) =G= link_scalar_data(i,j, 'min_flow');

MaxFlow(i,j)$links(i,j) ..
    Q(i,j) =L= link_scalar_data(i,j, 'max_flow');

** ----------------------------------------------------------------------
**  Model declaration and solve statements
** ----------------------------------------------------------------------

MODEL Demo1 /ALL/;

SOLVE Demo1 USING LP MINIMIZING Z;

*Generating results output

execute_unload "Results.gdx" ,
    Q,
    MassBalance_nonstorage,
    MinFlow,
    MaxFlow,
    Z
    link_scalar_data;
