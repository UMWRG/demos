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

* Source: BASIC OPTIMIZATION MODELS FOR WATER AND ENERGY MANAGEMENT 
* http://www.ce.utexas.edu/prof/mckinney/ce385d/papers/GAMS-Tutorial.pdf

$        include "input.txt";


Sets
all_genratore(i)
all_consumers(i);

all_genratore(i)=generators(i)+fixed_generators(i);
all_consumers(i)=fixed_consumers(i)+consumers(i);

VARIABLES 
power_generation(i),     power generation 
power_consumption(i),     power consumption 
power_flow(i,j),  power flow 
obj;   

EQUATION 
coni(i,j), 
conu0(i), 
conue(i), 
conur(i), 
ben; 
 
* All nodes 
coni(i,j)..         power_flow(i,j) =e= -power_flow(j,i)  ; 
* Junction nodes 
conu0(i)$(junctions(i))..   sum(j$(links(i,j)),power_flow(i,j)) =e=   0     ; 
* Generation nodes 
conue(i)$(all_genratore(i))..   sum(j$(links(i,j)),power_flow(i,j)) =e=   power_generation(i)  ; 
* Consumption nodes 
conur(i)$(all_consumers(i))..   sum(j$(links(i,j)),power_flow(i,j))  =e=  -power_consumption(i)  ;  
ben..           obj =E= 1;  

power_generation.up(generators)=max_genration(generators);

power_generation.lo(generators)=min_genration(generators);

power_generation.fx(fixed_generators)=fixed_genration(fixed_generators);

power_consumption.fx(fixed_consumers)=fixed_consummation(fixed_consumers);
 
power_flow.fx(Fixed_flow)=fixed_power_flow(Fixed_flow)

MODEL VAN /ALL/; 

SOLVE VAN USING NLP MinimaZING obj; 

file res /result_power.txt/ 
put res; 
put " I  Power Flow " /; 
put "             "; 
loop(i, put i.tl:10; );
         put /; loop(i, put i.tl:10;         
		 loop(j, put power_flow.l(i,j):10:1; );         
		 put /;); 
put /; 
put /; 
put " U  Generation " /; 
put "          ";
loop(i, put i.tl:10; ); 
put /; 

put "      "; 
loop(i, put power_generation.l(i):10:1; ); 
put /; put /; 
put " R  Consumption" /; 
put "          "; 
loop(i, put i.tl:10; ); 
put /; put "      "; 
loop(i, put power_consumption.l(i):10:1; ); 
put /;

scalar ms; 
ms=van.Modelstat; 