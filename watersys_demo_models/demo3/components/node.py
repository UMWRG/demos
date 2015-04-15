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

from watersys import Node

class Junction(Node):
    """
        A junction node is simply a connection node and performs no setup. It only
        has an inflow value
    """
    type = 'junction'
    _properties = dict(
        inflow=0,
    )


class WasteWaterTreatmentPlant(Node):
    """
        A junction node is simply a connection node and performs no setup. It only
        has an inflow value
    """
    type = 'waste water treatment plant'
    _properties = dict(
        inflow=0,
    )


class HydropowerPlant(Node):
    """
        A junction node is simply a connection node and performs no setup. It only
        has an inflow value
    """
    type = 'hydropower plant'
    _properties = dict(
        inflow=0,
    )


class DemandNode(Node):
    """
        A demand node is any class with a cost, target demand and inflow.
    """
    type = 'demand'

    _properties = dict(
        cost=0,
        target_demand=0,
        inflow=0,
    )
    
    def setup(self, timestamp):
        """
            set the parameters for this time step by getting the values
            out of private data dictionaries (private data being any variable
            starting with '_')
        """
        self.target_demand = self._demand[timestamp]
        self.cost = self._cost[timestamp]
        self.inflow=0


class AgriculturalNode(DemandNode):
    """
        An agricultural demand node. Has attributes cost, target demand and inflow by virtue
        of being a subclass of DemandNode
    """
    type = 'agricultural'


class UrbanNode(DemandNode):
    """
        An urban demand node.  Has attributes cost, target demand and inflow by virtue
        of being a subclass of DemandNode

    """
    type = "urban"

class SurfaceReservoir(Node):
    """
        Surface reservoir node type. Has an initial storage, inflow, min storage
        and max storage.
    """
    type = 'surface reservoir'

    _properties = dict(
        initial_storage=0,
        inflow = 0,
        min_storage = 0,
        max_storage = 0,
    )

    def setup(self, timestamp):
        """
            Set my properties for the current time step. Get my values
            from internal data (variables which start with '_')
        """
        self.min_storage = self._min_storage[timestamp]
        self.max_storage = self._max_storage[timestamp]
        self.inflow = self._inflow[timestamp]
        #self.initial_storage = self._initial_storage[timestamp]


class AquiferStorage(Node):
    """
        Groundwater reservoir node type. Has an initial storage, inflow, min storage
        and max storage.
    """
    type = 'aquifer storage'

    _properties = dict(
        initial_storage=0,
        inflow = 0,
        min_storage = 0,
        max_storage = 0,
    )

    def setup(self, timestamp):
        """
            Set my properties for the current time step. Get my values
            from internal data (variables which start with '_')
        """
        self.min_storage = self._min_storage[timestamp]
        self.max_storage = self._max_storage[timestamp]
        self.inflow = self._inflow[timestamp]
        #self.initial_storage = self._initial_storage[timestamp]