
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

from pynsim import Network

class CostMinimsationNetwork(Network):
    type = 'network'
    _properties = dict(
        predicted_rainfall={},
        rainfall=10,
    )

    def set_initial_storage(self, storage):
        for node in  self.nodes:
            if node.type == 'surface reservoir':
                    node.initial_storage=storage[node.name]


