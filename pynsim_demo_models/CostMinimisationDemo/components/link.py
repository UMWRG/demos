
#    (c) Copyright 2014, University of Manchester
#
#    This file is part of Pynsim.
#
#    Pynsim is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Pynsim is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Pynsim.  If not, see <http://www.gnu.org/licenses/>.

from pynsim import Link

class RiverSection(Link):
    """
        The only type of link in this model. Water sections have flow 
        parameters and cost
    """
    _properties = dict(
        flow_multiplier=None,
        lower_flow=None,
        upper_flow=None,
        cost=None
    )

    def setup(self, timestep):
        """
            Set my properties for the current timestep by accessing my internal
            data structures (defined in network creation code). Internal
            data are represented by variable names with a '_' at the beginning
        """
        self.flow_multiplier = self._flow_multiplier[timestep]
        self.lower_flow = self._lower_flow[timestep]
        self.upper_flow = self._upper_flow[timestep]
        self.cost=self._cost[timestep]

