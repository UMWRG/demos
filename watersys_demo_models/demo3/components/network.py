
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

from watersys import Network


class Demo3Network(Network):
    type = 'network'
    _properties = dict(
        predicted_rainfall={},
        rainfall=10,
    )

    def set_initial_storage(self, storage):
        for node in self.nodes:
            if node.type == 'surface reservoir' and node.type == 'aquifer storage':
                    node.initial_storage = storage[node.name]


