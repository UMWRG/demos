#    (c) Copyright 2014, University of Manchester
#
#    This file is part of WaterSys.
#
#    WaterSys is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    WaterSys is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with WaterSys.  If not, see <http://www.gnu.org/licenses/>.

from watersys import Engine

from coopr.pyomo import *
import coopr.environ
from coopr.opt import SolverFactory
from PyModel import OptimisationModel


class PyomoAllocation(Engine):

    name = """A pyomo-based engine which allocates water throughout a whole
    network in a single time-step."""
    target = None
    storage = {}

    def run(self):
        """
            Need to do some stuff here
        """
        print "==== Timestep ===="
        print "==== %s ===="%self.target.current_timestep
        allocation = "==========  Allocation       ============="
        storage = "==========  storage    =============="

        delivery=" ==========  delivery ============="
        for n in self.target.nodes:
            if n.type == 'agricultural' or n.type == 'urban':
                print n.target_demand

        print "======== calling Pyomo =============="
        pp =OptimisationModel(self.target)
        result =pp.run()
        for var in result.active_components(Var):
            if(var=="S"):
                s_var = getattr(result, var)
                for vv in s_var:
                    name= ''.join(map(str,vv))
                    print(name, s_var[vv].value)
                    self.storage[name]=(s_var[vv].value)
                    storage+='\n'+ name+": "+ str(s_var[vv].value)
            elif var=="delivery":
                d_var = getattr(result, var)
                for vv in d_var:
                    name= ''.join(map(str,vv))
                    self.storage[name]=(d_var[vv].value)
                    delivery+='\n'+ name+": "+ str(d_var[vv].value)
            elif var=="X":
                    x_var = getattr(result, var)
                    for xx in x_var:
                        name= "(" + ', '.join(map(str,xx)) + ")"
                        allocation+='\n'+name+": "+str(x_var[xx].value)

        print(allocation)
        print(storage)
        print(delivery)
        print result
