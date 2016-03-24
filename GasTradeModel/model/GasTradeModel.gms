**  (c) Copyright 2016, University of Manchester
**
**  This file is part of the GAMS Plugin Demo Suite.
**
**  The GAMS Plugin Demo Suite is free software: you can redistribute it and/or modify
**  it under the terms of the GNU General Public License as published by
**  the Free Software Foundation, either version 3 of the License, or
**  (at your option) any later version.
**
**  The Pyomo Plugin Demo Suite is distributed in the hope that it will be useful,
**  but WITHOUT ANY WARRANTY; without even the implied warranty of
**  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
**  GNU General Public License for more details.
**
**  You should have received a copy of the GNU General Public License
**  along with the Pyomo Plugin Demo Suite.  If not, see <http://www.gnu.org/licenses/>.

* The Gas Trade Model (GTM) models interrelated gas markets.
* Prices may be free to move as to equilibrate supplies and
* demand. Disequilibria can be introduced with controls over
* prices and/or quantities traded.

** orginal source: https://www.gams.com/modlib/libhtml/gtm.htm
* Manne, A S, and Beltramo, M A, GTM: An International Gas Trade Model , 
* International Energy Program Report. Stanford University, 1984.

$TITLE GasTradeModel.gms

$        include "input.txt";

$Eject
Sets 
demand_(i)
supply_(i)
;

demand_(i)=demand(i)+ supply_demand(i);
supply_(i) =supply(i)+ supply_demand(i);

Sets
ij(i,j)  feasible links;
;
display demand_;
display supply_;
 Parameters  supa(i)  supply_ constant a
             supb(i)  supply_ constant b
             supc(i)  supply_ capacity
             dema(i)  demand_ constant a
             demb(i)  demand_ constant b ;

  supc(supply_)  =  Limit(supply_);
  supb(supply_)  =  ((ref_P1(supply_)-ref_P2(supply_))/(1/(supc(supply_)-ref_Q1(supply_))-1/(supc(supply_)-ref_Q2(supply_))))
             $(supc(supply_) ne 55555);
  supa(supply_)  =  ref_p1(supply_) - supb(supply_)/(supc(supply_)-ref_q1(supply_));
*                                     we rely on supa(i) evaluating to exactly zero in some cases
  supa(supply_)  =  round(supa(supply_),4);
  supc(supply_)$(supc(supply_) eq 55555) = 100;
* sdat(i,"sup-a") = supa(i); sdat(i,"sup-b") = supb(i); display sdat;

  demb(demand_) = 1/elas(demand_) + 1;
  dema(demand_) = ref_p(demand_)/demb(demand_)/ref_q(demand_)**(demb(demand_)-1);
* ddat(demand_,"dem-a") = dema(demand_); ddat(demand_,"dem-b") = demb(demand_); display ddat;


 Sets  check1(i,j)  supply_ links with zero cost and non-zero capacity
       check2(i,j)  supply_ links with nonzero cost but zero capacity ;

  check1(supply_,demand_) = yes$(utc(supply_,demand_) eq 0 and pc(supply_,demand_) ne 0);
  check2(supply_,demand_) = yes$(utc(supply_,demand_) ne 0 and pc(supply_,demand_) eq 0);

  ij(supply_,demand_) = yes$pc(supply_,demand_);

  Display check1, check2;

Variables  

benefit consumers benefits minus cost[-]
;

Positive Variables 
shipment_of_natural_gas(i,j) shipment of natural gas [-]
regional_supply(i) regional supply(-) [-]
regional_demand(j) regional demand (-) [-]
;
 Equations sb(i)    supply_ balance          (-)
           db(i)    demand_ balance          (-)
           bdef     benefit definition ;

 sb(supply_)..   sum(demand_$ij(supply_,demand_), shipment_of_natural_gas(supply_,demand_)) =l= regional_supply(supply_) ;

 db(demand_)..   sum(supply_$ij(supply_,demand_), shipment_of_natural_gas(supply_,demand_)) =g= regional_demand(demand_) ;

 bdef..    benefit =e= sum(demand_, dema(demand_)*regional_demand(demand_)**demb(demand_)) - sum(supply_, supa(supply_)*regional_supply(supply_) - supb(supply_)*log((supc(supply_)-regional_supply(supply_))/supc(supply_)))
                     - sum((supply_,demand_)$ij(supply_,demand_), utc(supply_,demand_)*shipment_of_natural_gas(supply_,demand_));

 shipment_of_natural_gas.up(supply_,demand_) = pc(supply_,demand_); regional_demand.lo(demand_) = .2; 
 regional_demand.fx(regions_with_fixed_demand) = ref_q(regions_with_fixed_demand); 
 regional_supply.up(supply_) = 0.99*supc(supply_);

 Model gtm gas transport model / all /;  solve gtm maximizing benefit using nlp;

$Eject

Parameter report1(i,*) supply_ summary report
           report2(i,*) demand_ summary report ;

report1(supply_,"supply_") = regional_supply.l(supply_); report1(supply_,"capacity") = regional_supply.up(supply_); report1(supply_,"price") = sb.m(supply_);
report2(demand_,"demand_") = regional_demand.l(demand_); report2(demand_,"price") = -db.m(demand_);
Display report1, report2, shipment_of_natural_gas.l;

*Unload results to GDX file
execute_unload "Results.gdx" shipment_of_natural_gas,regional_demand, regional_supply, benefit
