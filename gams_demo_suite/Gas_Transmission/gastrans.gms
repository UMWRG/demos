*Source:  https://www.gams.com/modlib/libhtml/gastrans.htm

*------------------------------------------------------------------------


*    gastrans.gms : Gas Transmission Problem - Belgium

*------------------------------------------------------------------------

*The problem of distributing gas through a network of pipelines is formulated as
*a cost minimization subject to nonlinear flow-pressure relations, material
*balances, and pressure bounds. The Belgian gas network is used as an example.

*First, we model a straight-forward NLP formulation that can be solved fine
*by todays NLP solvers.
*Afterwards, the 3-stage approach by Wolf & Smeers is implemented (line 160ff).

*de Wolf, D, and Smeers, Y, The Gas Transmission Problem Solved by
*and Extension of the Simplex Algorithm. Management Science 46, 11
*(2000), 1454-1465.

*------------------------------------------------------------------------
*Reference:

* de Wolf, D, and Smeers, Y, The Gas Transmission Problem Solved by
*    and Extension of the Simplex Algorithm. Management Science 46, 11
*    (2000), 1454-1465. 

*------------------------------------------------------------------------
*Small Model of Type: NLP
*------------------------------------------------------------------------

$title Gas Transmission Problem - Belgium (GASTRANS,SEQ=217)
$ontext
The problem of distributing gas through a network of pipelines is formulated as
a cost minimization subject to nonlinear flow-pressure relations, material
balances, and pressure bounds. The Belgian gas network is used as an example.

First, we model a straight-forward NLP formulation that can be solved fine 
by todays NLP solvers.
Afterwards, the 3-stage approach by Wolf & Smeers is implemented (line 160ff).

de Wolf, D, and Smeers, Y, The Gas Transmission Problem Solved by
and Extension of the Simplex Algorithm. Management Science 46, 11
(2000), 1454-1465.

$offtext
$eolcom //

$ 	include "hydra_input.txt"

parameter lam(link_name,i,j)    lambda constant (page 1464)
          c2(link_name,i,j)     pipe constant (page 1463)
          arep(link_name,i,j,*) Arc Report;

Sets 
 as(link_name) active arcs
 ap(link_name) passive arcs
 aij(link_name,i,i) arc description
;

aij(link_name,i,j) = L(link_name,i,j);

as(link_name) = sum(aij(link_name,i,j), active(link_name));
ap(link_name) = not as(link_name);

  lam(aij(link_name,i,j)) = 1/sqr(2*log10(3.7*D(aij)/e));
  c2(aij(link_name,i,j)) = 96.074830e-15*power(D(aij),5)/lam(aij)/z/t/L(aij)/den;

  arep(aij,'lam') = lam(aij);
  arep(aij,'c2')  = c2(aij);

option arep:6:3:1; 
display arep ,as,ap;

Variables f(link_name,i,j)   Arc flow (1e6 SCM)
          s(i)       supply - demand (1e6 SCM)
          pi(i)      squared pressure
          sc         supply cost
;

Equations flowbalance(i)    flow conservation
          weymouthp(link_name,i,j)  flow pressure relationship - passive
          weymoutha(link_name,i,j)  flow pressure relationship - active
          defsc             definition of supply cost
;

flowbalance(i).. sum(aij(link_name,i,j), f(aij)) =e= sum(aij(link_name,j,i), f(aij)) + s(i);

weymouthp(aij(ap,i,j)).. signpower(f(aij),2) =e= c2(aij)*(pi(i)-pi(j));

weymoutha(aij(as,i,j))..       - sqr(f(aij)) =g= c2(aij)*(pi(i)-pi(j));

defsc.. sc =e= sum(i, c(i)*s(i));

* supply, demand, pressure, and flow bounds
s.lo(i)  = slo(i);
s.up(i)  = sup(i);
pi.lo(i) = sqr(plo(i));
pi.up(i) = sqr(pup(i));
f.lo(aij(as,i,j)) = 0;

* initialize flow to avoid getting trapped at signpower(0,2)
f.l(aij) = uniform(-1,1);

model gastrans / flowbalance, weymouthp, weymoutha, defsc /;

solve gastrans using nlp min sc;

display f.l;




* to run the Wolf & Smeers approach, remove the following $exit
$exit

Parameter frep Flow Report
          sdp  supply demand and pressure;

frep('NLP',aij,'Flow') = f.l(aij);

sdp('NLP',i,'Supply')   =   s.l(i)$(s.l(i) > 0);
sdp('NLP',i,'Demand')   =  -s.l(i)$(s.l(i) < 0);
sdp('NLP',i,'Pressure') =  sqrt(pi.l(i));
sdp('NLP','','Obj')     =  sc.l;


Parameters flow(link_name,i,j,*)    flow bounds
           pirange(link_name,i,j,*) squared pressure bounds
;

flow(aij(ap,i,j),'min') =  -sqrt(c2(aij)*(pi.up(j)-pi.lo(i)));
flow(aij(ap,i,j),'max') =   sqrt(c2(aij)*(pi.up(i)-pi.lo(j)));

pirange(aij(ap,i,j),'min') = pi.lo(i) - pi.up(j);
pirange(aij(ap,i,j),'max') = pi.up(i) - pi.lo(j);

option flow:3:3:1, pirange:3:3:1;
display flow, pirange;

Equations defh              definition of Smeers obj
          defsig(link_name,i,j)     definition of flow direction
          weymouthp2(link_name,i,j) flow pressure relationship - passive
          flo,fup,pilo,piup
;

Variables sig(link_name,i,j) flow direction (-1 or +1 for passive elements)
          b(link_name,i,j)   flow direction ( 1 = i to j )
          h          Smeers obj
;
Binary Variable b;

weymouthp2(aij(ap,i,j)).. sig(aij)*sqr(f(aij)) =e= c2(aij)*(pi(i)-pi(j));

defh.. h =e= sum(aij(link_name,i,j), abs(f(aij))*sqr(f(aij))/3/c2(aij));

defsig(aij(ap,i,j)).. sig(aij) =e= 2*b(aij)-1;

flo(aij(ap,i,j)).. f(aij) =g= flow(aij,'min')*(1-b(aij));
fup(aij(ap,i,j)).. f(aij) =l= flow(aij,'max')* b(aij);

pilo(aij(ap,i,j)).. pi(i) - pi(j) =G= pirange(aij,'min')*(1-b(aij));
piup(aij(ap,i,j)).. pi(i) - pi(j) =l= pirange(aij,'max')*b(aij);


* drop the previous solution
pi.l(i) = 0;
s.l(i) = 0;
f.l(aij) = uniform(-1,1);

model one   / defh, flowbalance /
      two   / defsc,flowbalance,weymouthp2,weymoutha /
      three / defsc,flowbalance,weymouthp2,weymoutha,defsig,pilo,piup,flo,fup /;

option limrow=0,limcol=0;

solve one using dnlp min h; // provides good initial point

solve two using nlp min sc;

* assignmenst below fix known solution
*b.fx(*aij) =1;
*b.fx(aij('7',i,j)) =0;
*b.fx(aij('8',i,j)) =0;

solve three using minlp min sc;

frep('Smeers',aij,'Flow') = f.l(aij);

sdp('Smeers',i,'Supply')   =   s.l(i)$(s.l(i) > 0);
sdp('Smeers',i,'Demand')   =  -s.l(i)$(s.l(i) < 0);
sdp('Smeers',i,'Pressure') =  sqrt(pi.l(i));
sdp('Smeers','','Obj')     =  sc.l;

option frep:6:4:1;
display frep, sdp;

