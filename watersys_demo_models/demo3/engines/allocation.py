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
from PyModel import PyomModel

class PyomoAllocation(Engine):

    name   = """A pyomo-based engine which allocates water throughout a whole
    network in a single time-step."""
    target = None

    def run(self):
        """
            Need to do some stuff here
        """
        print "==== Timestep ===="
        print "==== %s ===="%self.target.current_timestep
        for n in self.target.nodes:
            if n.type == 'agricultural' or n.type == 'urban':
                print n.target_demand

        print "======== calling Pyomo =============="
        pp =PyomModel(self.target)
        result =pp.run()

        print result
