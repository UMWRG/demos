**    (c) Copyright 2016, University of Manchester
**
**    This file is part of the GAMS Plugin Demo Suite.
**
**    The GAMS Plugin Demo Suite is free software: you can redistribute it and/or modify
**    it under the terms of the 	 as published by
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

*Source: https://www.gams.com/noalib/libhtml/edc2.htm
*------------------------------------------------------------------------


*    Edc2 : Economic Dispatch Calculation of a Total Power of 1,980 MW
*    Using 15 Power Generating Units

*------------------------------------------------------------------------
*Reference: Neculai Andrei, Nonlinear Optimization Applications Using the
*GAMS Technology, Springer Optimization and Its Applications, Model
*Edc2/ (6.7) in chapter /Applications in Electrical Engineering /, 2013
*-----------------------------------------------------------------------

$Ontext
Economic load dispatch for 15 generator systems with transmission losses
modeled using B-matrix formulation (Kron).
EDC of a total power of 1980 MW using 15 power generating units.
$Offtext

$ include Edc2.txt


Variables P(i) optimal generation level of i [-]
          obj  minimum cost [USD] ;

Equations  cost  total generation cost
           bal   demand-supply balance ;

* Objective function:
cost.. obj =e= sum(i,a(i)*POWER(p(i),2) +
                     b(i)*P(i) +
                     c(i));

* Constraints:
bal.. sum(i,P(i))-sum((i,j),P(i)*Losscoef(i,j)*P(J)/10000) =e= Load;

* Bounds on variables:
P.lo(i) = low(i);
p.up(i) = upp(i);

p.l(i) = (low(i) + upp(i))/2;

	Model edc2 /all/;

$iftheni x%mode%==xbook
$onecho >bench.opt
  solvers conopt knitro minos snopt
$offecho
edc2.optfile=1;
option nlp=bench;
$endif

Solve edc2 minimizing obj using nlp;
* End edc2











