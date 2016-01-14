**    (c) Copyright 2014, University of Manchester
**
**    Authors: Majed Khadem, Silvia Padula, Khaled Mohamed, Stephen Knox and Julien Jarou
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

$TITLE    TrivialExample.gms

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
Q(i,j) flow in each link in each period [1e6 m^3 mon^-1]
delivery (i) water delivered to demand node i in each period [1e6 m^3 mon^-1]
Z objective function [-]
;

POSITIVE VARIABLES
Q
;

EQUATIONS
MassBalance_junction(i)
MassBalance_urban(i)
MassBalance_agricultural(i)
MinFlow(i,j)
MaxFlow(i,j)
Objective
;

* Objective function

Objective ..
    Z =E= SUM((i,j)$links(i,j), Q(i,j) * cost(i,j))
;

* Mass balance constraints for all the non-storage nodes

MassBalance_junction(junction) ..
    inflow(junction) +
    SUM(j$links(j,junction), Q(j,junction) * flow_multiplier(j,junction)) -
    SUM(j$links(junction,j), Q(junction,j)) -
    consumption_coefficient(junction) * 
    delivery(junction)
    =E= 0;

MassBalance_urban(urban) ..
    SUM(j$links(j,urban), Q(j,urban) * flow_multiplier(j,urban)) -
    SUM(j$links(urban,j), Q(urban,j)) -
    consumption_coefficient(urban) * 
    delivery(urban)
    =E= 0;

MassBalance_agricultural(agricultural) ..
    SUM(j$links(j,agricultural), Q(j,agricultural) * flow_multiplier(j,agricultural)) -
    SUM(j$links(agricultural,j), Q(agricultural,j)) -
    consumption_coefficient(agricultural) * 
    delivery(agricultural)
    =E= 0;

* Lower and upper bound of possible flow in links

MinFlow(i,j)$links(i,j) ..
    Q(i,j) =G= min_flow(i,j);

MaxFlow(i,j)$links(i,j) ..
    Q(i,j) =L= max_flow(i,j);

** ----------------------------------------------------------------------
**  Model declaration and solve statements
** ----------------------------------------------------------------------

MODEL TrivialExample /ALL/;

SOLVE TrivialExample USING LP MINIMIZING Z;

*Generating results output

execute_unload "Results.gdx" ,
    Q,
    MassBalance_junction,
    MassBalance_urban,
    MassBalance_agricultural,
    MinFlow,
    MaxFlow,
    Z;
