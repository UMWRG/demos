$        include water.txt



 Parameter  dist(i,j)  distance between nodes (m);
            dist(links(i,j)) = sqrt( sqr( x(i)-x(j) ) + sqr( y(i)-y(j) ) );
            display dist;
 Scalar
            davg       average diameter (geometric mean)
            rr         ratio of demand to supply;

            davg = sqrt(dmin*dmax);
            rr   = sum(demand_nodes, demand(demand_nodes)) / sum(reservoirs_nodes, supply(reservoirs_nodes));

 Variables  q(i,j)     flow on each arc - signed       (m**3 per sec)
            d(i,j)     pipe diameter for each arc      (m)
            h(i)       pressure at each node           (m)
            s(i)       supply at reservoir nodes       (m**3 per sec)
            pcost_n      annual recurrent pump costs     (mill rp)
            dcost      investment costs for pipes      (mill rp)
            wcost_n      annual recurrent water costs    (mill rp)
            cost       total discounted costs          (mill rp)

 Equations  cont(i)    flow conservation equation at each node
            loss(i,j)  pressure loss on each arc
            peq        pump cost equation
            deq        investment cost equation
            weq        water cost equation
            obj        objective function;

 cont(i)..  sum(links(j,i), q(links)) - sum(links(i,j), q(links)) + s(i)$reservoirs_nodes(i) =e= demand(i);

 loss(links(i,j)).. h(i) - h(j) =e= (hloss*dist(links)*abs(q(links))**(qpow-1)*q(links)/d(links)**dpow) $(qpow <> 2) +
                                  (hloss*dist(links)*abs(q(links))          *q(links)/d(links)**dpow) $(qpow = 2);

 peq..  pcost_n =e= sum(reservoirs_nodes, s(reservoirs_nodes)*pcost(reservoirs_nodes)*(h(reservoirs_nodes)-height(reservoirs_nodes)));
 

 deq..  dcost =e= dprc*sum(links, dist(links)*d(links)**cpow);

 weq..  wcost_n =e= sum(reservoirs_nodes, s(reservoirs_nodes)*wcost(reservoirs_nodes));

 obj..  cost  =e= (pcost_n + wcost_n)/r + dcost;

*
*  bounds
*

 d.lo(links)  = dmin;              
 d.up(links)  = dmax;
 h.lo(reservoirs_nodes) = height(reservoirs_nodes); h.lo(demand_nodes) = height(demand_nodes) + 7.5 + 5.0*demand(demand_nodes);
 s.lo(reservoirs_nodes) = 0;                 s.up(reservoirs_nodes) = supply(reservoirs_nodes);

*
*  initial values
*

 d.l(links)  = davg;
 h.l(i)  = h.lo(i) + 1.0;
 s.l(reservoirs_nodes) = supply(reservoirs_nodes)*rr;

 Model network /all/;
 Solve network using dnlp minimizing cost;
 Display q.l;
 
 execute_unload "water.gdx"
 q,
 d,
 h,
 s,
 loss,
 pcost_n,
 dcost,
 wcost_n,
 cost