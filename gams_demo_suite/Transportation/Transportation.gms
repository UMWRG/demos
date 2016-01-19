**    (c) Copyright 2016, University of Manchester
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


* Source https://optimization.mccormick.northwestern.edu/index.php/Network_flow_problem
* It originally comes from this book:
* R.J. Vanderbei, Linear Programming: Foundations and Extensions. Springer, 2008.  

*This problem finds a least cost shipping schedule that meets
*requirements at markets and supplies at factories.
*There are six cities with demand constraints and three factories with maximum supply constraints. 
*The cost of the transportation is to be minimized given supply and demand constraints.


$ include input.txt

variables
shipment_quantities (i,j) shipment quantities 
Z total transportation costs ; 

equations cost, sup(i), dem(j);
cost..   Z=e= sum((i,j), trans_cost(i,j)*shipment_quantities(i,j) );
sup(i)..   sum(j$city(j), shipment_quantities(i,j) ) =l= capacity(i)$factory(i)    ;
dem(j)..   sum(i$factory(i), shipment_quantities(i,j) ) =g= demand(j)$city(j)    ;

shipment_quantities.lo(i,j) = 0;

model transport /all/;
solve transport using lp minimizing z;