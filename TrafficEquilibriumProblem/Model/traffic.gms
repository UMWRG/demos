*Source https://www.gams.com/modlib/libhtml/traffic.htm

$title Traffic Equilibrium Problem (TRAFFIC,SEQ=169)
$Ontext
  Three different models are used to compute traffic equilibria. These are
  a mixed complementarity formulation and a primal and dual formulation
  using NLPs.


Ferris, M C, Meeraus, A, and Rutherford, T F, Computing Wardropian
Equilibria in a Complementarity Framework. Optimization Methods and
Software 10 (1999), 669-685.

$Offtext


$include input.txt



PARAMETER ITEMTODISP(i,trip_index);


parameter ca(i,j), cb(i,j), ck(i,j);

ca(i,j)=a(i,j);
cb(i,j)=b(i,j);
ck(i,j)=c(i,j);

parameter c1111;
c1111=card(i);
parameter d1111;
d1111=card(trip_index);

alias(i,j,k,n);

variables  
t(i,j)    time to get from node i to node j
v(i,j)    time to traverse arc form i to j
y(i,j,k)  flow to k along arc i-j
x(i,j)    aggregate flow on arc i-j
objpnlp   objective for nlp formulation
objdnlp   objective for nlp formulation

positive variable y;

equations  balance(i,j)     material balance
           vdef(i,j)        arc travel time definition
           rational(i,j,k)  cost minimization condition
           xdef(i,j)        aggregate flow definition
           defpnlp          defines objective for primal nlp formulation
           defdnlp          defines objective for dual nlp formulation;


balance(i,k)$(not sameas(i,k))..  sum(links(i,j), y(links,k)) =e= sum(links(j,i), y(links,k)) + trip(i,k);

rational(links(i,j),k)$(not sameas(i,k))..   v(links) + t(j,k) =g= t(i,k);

vdef(links)..  v(links) =e= ca(links) + cb(links)*power(x(links)/ck(links),4);

xdef(links)..  x(links) =e= sum(k, y(links,k));

defpnlp..  objpnlp =e= sum(links, ca(links)*x(links) + cb(links)*power(x(links)/ck(links),5)*ck(links)/5);

defdnlp..  objdnlp =e= sum((i,k), trip(i,k)*t(i,k))
                     - sum(links, (4/5)*(ck(links)/cb(links)**(1/4))*(v(links)-ca(links))**1.25);
*primal nlp formulation 
model pnlp / defpnlp, balance, xdef/
*dual nlp formulation   
dnlp /defdnlp, rational /
*mcp formulation        
mcp  /rational.y, balance.t, xdef, vdef.v /;


*  mirror the values
*trip(i,j) $= trip(j,i);        
*  get it back to original values
trip(i,j)  = trip(i,j)*0.11;   
*  has to match the values in the article
option trip:2; 
display trip;   

*!  identify arcs using flow cost parameter a
*links(i,j) = ca(i,j);              
display links;
$stitle Bound Definitions and Solutions

t.fx(i,i)      = 0;
v.lo(links)        = ca(links);
y.fx(links(i,j),i) = 0;

option domlim=1000000;
pnlp.workfactor=3;

parameter rep(i,k,*) summary report;

mcp.OPTFILE = 1; 
solve mcp  using mcp;                    rep(i,j,'mcp   ') =  t.l(i,j);
*solve pnlp using nlp minimizing objpnlp; rep(i,j,'primal') =  balance.m(i,j);
*solve dnlp using nlp maximizing objdnlp; rep(i,j,'dual  ') =  t.l(i,j);

display rep;