*******************************************************************************
*Water Capacity Expansion Model
*******************************************************************************

*option mip=coincbc;
option mip=cplex;
Option domlim=100;
Option Limcol=100;
Option Limrow=1500;
option optcr = 0.1 ;

$        include "ebsd.txt";

Alias(i,aa)

set da fantasma /y0*y10/

Parameter CV(da) "counter variable for construction period" ;
          CV(da) = ord(da)-1 ;

Parameter Time(t) "yearly vector" ;
          Time(t) = ord(t)-1 ;

Parameter FCCs(optSou) "capital costs for future optional sources" ;
          FCCs(optSou)=sum(da$(CV(da)<=(CPs-1)),(capitalS(optSou)/CPs)*power(1+Int_rate,CPs-CV(da))) ;

Parameter FCCl(i,j) "capital costs for future  oprtional links" ;
          FCCl(i,j)=sum(da$(CV(da)<=(CPl-1)),(capitalL(i,j)/CPl)*power(1+Int_rate,CPl-CV(da))) ;

		  

*VARIABLES
*******************************************************************************

Variable
         z "annualised capital and operating cost of sources&links" ;

Binary variables
         AS(t,i) "Activation for optional source during period t"
         AL(t,i,j) "Activitation of link optilnal during period t"

                                                      ;
Positive variables
         Q(t,i,j) "Flow from node i to j during year t"
         S(t,i) "Supply from source i during year t"            ;

Equations

totcost  "annualised capital and operating cost of existing and optional sources and links"
EqMassBal(t,i) "Mass balance constraint for demand nodes"
UpCapS(t,i) "Upper capacity for sources"
UpCapacityL(t,i,j) "Upper capacity constraint for optional links"
ContinuityS(t,i) "Continuity contraint for optional sources"
ContinuityL(t,i,j) "Continuity contraint for links"
eq(t,i,aa,junct)
;
totcost..
         z=e=  sum((t),(  sum(optSou,(((FCCs(optSou)/power(1+Dr,Time(t)))*(AS(t,optSou)-AS(t-1,optSou)))
                               +(((fixedS(optSou)*AS(t,optSou))+((varS(optSou)*S(t,optsou)*3.65)))/power(1+Dr,Time(t)))))

                           +sum(exDO,((fixedS(exDO)+(varS(exDO)*S(t,exDO)*3.65))/power(1+Dr,Time(t))))
                           +sum((i,j)$(connect(i,j)and (not exlink(i,j) and not loc(i,j))),
                                      (    ((FCCl(i,j)/power(1+Dr,Time(t)))*(AL(t,i,j)-AL(t-1,i,j)))
                                            +((((fixedL(i,j)$lft(i,j))*AL(t,i,j))+((fixedL(i,j)$lft(i,j))*Q(t,i,j)*3.65))/power(1+Dr,Time(t))) )   )
                           +sum((i,j)$connect(i,j),((fixedL(i,j)+varL(i,j)*Q(t,i,j)*3.65))/power(1+Dr,Time(t)))
                          )
                     );

EqMassBal(t,i)..
         sum(j$connect(j,i),Q(t,j,i))+S(t,i)$(exDO(i) or optSou(i)) =e= sum(j$connect(i,j),Q(t,i,j)) +  demand(i,t)$dem(i);


UpCapS(t,i)..
         S(t,i)=l= maxcapS(i)$(exDO(i))+(maxcapS(i)*AS(t,i))$optSou(i);

UpCapacityL(t,i,j)$(connect(i,j))..
         Q(t,i,j) =l= (maxcapL(i,j)*AL(t,i,j))$(not exlink(i,j)and not loc(i,j))+ maxcapL(i,j)$(exlink(i,j) or loc(i,j));

ContinuityS(t,i)$((ord(t)<card(t)) and optSou(i)or exDO(i)) .. AS(t+1,i) =g= AS(t,i) ;
ContinuityL(t,i,j)$((ord(t)<card(t)$(connect(i,j)))and not exlink(i,j)and not loc(i,j)).. AL(t+1,i,j) =g= AL(t,i,j) ;
eq(t,i,aa,junct)$(connect(i,junct) and connect(junct,aa)).. AL(t,i,junct)=e=AL(t,junct,aa) ;


Model Water /All/ ;
Solve Water using mip minimizing z;
display S.l, Q.l, AS.l, AL.l,Z.l;

**************plotting output**********************************************************************************************************************************************************************************************************************************************************************

*Unload results to GDX file
execute_unload "Results.gdx" S,Q, AL, AS, Z

