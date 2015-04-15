from components import Junction, WasteWaterTreatmentPlant, HydropowerPlant, UrbanNode, SurfaceReservoir, AgriculturalNode, AquiferStorage, RiverSection, Demo3Network
from engines import PyomoAllocation

from watersys import Simulator, Network


s = Simulator()

timesteps = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

s.set_timesteps(timesteps)

n = Network(name="demo3 network")



initial_storage_matrix = {
    "sr1": {"1": 150, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0},
    "sr2": {"1": 200, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0},
    "sr3": {"1": 600, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0},
    "sr4": {"1": 150, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0},
    "desal1": {"1": 10000, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0},
    "gw1": {"1": 600, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0},
    "gw2": {"1": 600, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0},
}

inflow_matrix = {
    "sr1": {"1": 100, "2": 120, "3": 120, "4": 130, "5": 110, "6": 110, "7": 100, "8": 120, "9": 120},
    "sr2": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0},
    "sr3": {"1": 40, "2": 30, "3": 30, "4": 30, "5": 40, "6": 50, "7": 40, "8": 40, "9": 50},
    "sr4": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0},
    "desal1": {"1": 1000, "2": 1000, "3": 1000, "4": 1000, "5": 1000, "6": 1000, "7": 1000, "8": 1000, "9": 1000},
    "gw1": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0},
    "gw2": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0},
    "ag1": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0},
    "ag2": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0},
    "endpt": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0},
    "urb1": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0},
    "urb2": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0},
    "jn1": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0},
    "jn2": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0},
    "jn3": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0},
    "wwtp1": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0},
    "hp1": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0}
}

min_storage_matrix = {
    "sr1": {"1": 50, "2": 50, "3": 50, "4": 50, "5": 50, "6": 50, "7": 50, "8": 50, "9": 50},
    "sr2": {"1": 20, "2": 20, "3": 20, "4": 20, "5": 20, "6": 20, "7": 20, "8": 20, "9": 20},
    "sr3": {"1": 30, "2": 30, "3": 30, "4": 30, "5": 30, "6": 30, "7": 30, "8": 30, "9": 30},
    "sr4": {"1": 60, "2": 60, "3": 60, "4": 60, "5": 60, "6": 60, "7": 60, "8": 60, "9": 60},
    "desal1": {"1": 10, "2": 10, "3": 10, "4": 10, "5": 10, "6": 10, "7": 10, "8": 10, "9": 10},
    "gw1": {"1": 300, "2": 300, "3": 300, "4": 300, "5": 300, "6": 300, "7": 300, "8": 300, "9": 300},
    "gw2": {"1": 300, "2": 300, "3": 300, "4": 300, "5": 300, "6": 300, "7": 300, "8": 300, "9": 300},
}

max_storage_matrix = {
    "sr1": {"1": 500, "2": 500, "3": 500, "4": 500, "5": 500, "6": 500, "7": 500, "8": 500, "9": 500},
    "sr2": {"1": 200, "2": 200, "3": 200, "4": 200, "5": 200, "6": 200, "7": 200, "8": 200, "9": 200},
    "sr3": {"1": 700, "2": 700, "3": 700, "4": 700, "5": 700, "6": 700, "7": 700, "8": 700, "9": 700},
    "sr4": {"1": 600, "2": 600, "3": 600, "4": 600, "5": 600, "6": 600, "7": 600, "8": 600, "9": 600},
    "desal1": {"1": 100000, "2": 100000, "3": 100000, "4": 100000, "5": 100000, "6": 100000, "7": 100000, "8": 100000, "9": 100000},
    "gw1": {"1": 2000, "2": 2000, "3": 2000, "4": 2000, "5": 2000, "6": 2000, "7": 2000, "8": 2000, "9": 2000},
    "gw2": {"1": 2000, "2": 2000, "3": 2000, "4": 2000, "5": 2000, "6": 2000, "7": 2000, "8": 2000, "9": 2000},
}

cost_matrix = {
    "ag1": {"1": 50, "2": 50, "3": 50, "4": 50, "5": 50, "6": 50, "7": 50, "8": 50, "9": 50},
    "ag2": {"1": 30, "2": 30, "3": 30, "4": 30, "5": 30, "6": 30, "7": 30, "8": 30, "9": 30},
    "endpt": {"1": 1, "2": 1, "3": 1, "4": 1, "5": 1, "6": 1, "7": 1, "8": 1, "9": 1},
    "urb1": {"1": 90, "2": 90, "3": 90, "4": 90, "5": 90, "6": 90, "7": 90, "8": 90, "9": 90},
    "urb2": {"1": 100, "2": 100, "3": 100, "4": 100, "5": 100, "6": 100, "7": 100, "8": 100, "9": 100},
}

demand_matrix = {
    "ag1": {"1": 55, "2": 270, "3": 27, "4": 27, "5": 27, "6": 29, "7": 29, "8": 29, "9": 280},
    "ag2": {"1": 60, "2": 210, "3": 21, "4": 21, "5": 22, "6": 22, "7": 22, "8": 22, "9": 210},
    "endpt": {"1": 15, "2": 160, "3": 14, "4": 15, "5": 15, "6": 15, "7": 14, "8": 15, "9": 160},
    "urb1": {"1": 75, "2": 430, "3": 44, "4": 44, "5": 46, "6": 49, "7": 50, "8": 50, "9": 470},
    "urb2": {"1": 90, "2": 600, "3": 60, "4": 62, "5": 62, "6": 65, "7": 69, "8": 69, "9": 640},
}

flow_mult_matrix = {
    "l1" : {"1":1, "2":1, "3":1, "4":1, "5":1, "6":1, "7":1, "8":1, "9":1},
    "l2" : {"1":1, "2":1, "3":1, "4":1, "5":1, "6":1, "7":1, "8":1, "9":1},
    "l3" : {"1":1, "2":1, "3":1, "4":1, "5":1, "6":1, "7":1, "8":1, "9":1},
    "l4" : {"1":0.95, "2":0.95, "3":0.95, "4":0.95, "5":0.95, "6":0.95, "7":0.95, "8":0.95, "9":0.95},
    "l5" : {"1":1, "2":1, "3":1, "4":1, "5":1, "6":1, "7":1, "8":1, "9":1},
    "l6" : {"1":1, "2":1, "3":1, "4":1, "5":1, "6":1, "7":1, "8":1, "9":1},
    "l7" : {"1":0.95, "2":0.95, "3":0.95, "4":0.95, "5":0.95, "6":0.95, "7":0.95, "8":0.95, "9":0.95},
    "l8" : {"1":1, "2":1, "3":1, "4":1, "5":1, "6":1, "7":1, "8":1, "9":1},
    "l9" : {"1":1, "2":1, "3":1, "4":1, "5":1, "6":1, "7":1, "8":1, "9":1},
    "l10" : {"1":0.9, "2":0.9, "3":0.9, "4":0.9, "5":0.9, "6":0.9, "7":0.9, "8":0.9, "9":0.9},
    "l11" : {"1":0.95, "2":0.95, "3":0.95, "4":0.95, "5":0.95, "6":0.95, "7":0.95, "8":0.95, "9":0.95},
    "l12" : {"1":1, "2":1, "3":1, "4":1, "5":1, "6":1, "7":1, "8":1, "9":1},
    "l13" : {"1":1, "2":1, "3":1, "4":1, "5":1, "6":1, "7":1, "8":1, "9":1},
    "l14" : {"1":1, "2":1, "3":1, "4":1, "5":1, "6":1, "7":1, "8":1, "9":1},
    "l15" : {"1":1, "2":1, "3":1, "4":1, "5":1, "6":1, "7":1, "8":1, "9":1},
    "l16" : {"1":1, "2":1, "3":1, "4":1, "5":1, "6":1, "7":1, "8":1, "9":1},
    "l17" : {"1":1, "2":1, "3":1, "4":1, "5":1, "6":1, "7":1, "8":1, "9":1},
    "l18" : {"1":1, "2":1, "3":1, "4":1, "5":1, "6":1, "7":1, "8":1, "9":1},
    "l19" : {"1":1, "2":1, "3":1, "4":1, "5":1, "6":1, "7":1, "8":1, "9":1},
    "l20" : {"1":1, "2":1, "3":1, "4":1, "5":1, "6":1, "7":1, "8":1, "9":1},
    "l21" : {"1":1, "2":1, "3":1, "4":1, "5":1, "6":1, "7":1, "8":1, "9":1},
    "l22" : {"1":1, "2":1, "3":1, "4":1, "5":1, "6":1, "7":1, "8":1, "9":1},
    "l23" : {"1":1, "2":1, "3":1, "4":1, "5":1, "6":1, "7":1, "8":1, "9":1},
    "l24" : {"1":1, "2":1, "3":1, "4":1, "5":1, "6":1, "7":1, "8":1, "9":1},
    "l25" : {"1":1, "2":1, "3":1, "4":1, "5":1, "6":1, "7":1, "8":1, "9":1},
}

flow_upper_matrix = {
    "l1" : {"1":100, "2":100, "3":100, "4":100, "5":100, "6":100, "7":100, "8":100, "9":100},
    "l2" : {"1":100, "2":100, "3":100, "4":100, "5":100, "6":100, "7":100, "8":100, "9":100},
    "l3" : {"1":100, "2":100, "3":100, "4":100, "5":100, "6":100, "7":100, "8":100, "9":100},
    "l4" : {"1":100, "2":100, "3":100, "4":100, "5":100, "6":100, "7":100, "8":100, "9":100},
    "l5" : {"1":100, "2":100, "3":100, "4":100, "5":100, "6":100, "7":100, "8":100, "9":100},
    "l6" : {"1":100, "2":100, "3":100, "4":100, "5":100, "6":100, "7":100, "8":100, "9":100},
    "l7" : {"1":100, "2":100, "3":100, "4":100, "5":100, "6":100, "7":100, "8":100, "9":100},
    "l8" : {"1":100, "2":100, "3":100, "4":100, "5":100, "6":100, "7":100, "8":100, "9":100},
    "l9" : {"1":100, "2":100, "3":100, "4":100, "5":100, "6":100, "7":100, "8":100, "9":100},
    "l10" : {"1":200, "2":200, "3":200, "4":200, "5":200, "6":200, "7":200, "8":200, "9":200},
    "l11" : {"1":200, "2":200, "3":200, "4":200, "5":200, "6":200, "7":200, "8":200, "9":200},
    "l12" : {"1":100, "2":100, "3":100, "4":100, "5":100, "6":100, "7":100, "8":100, "9":100},
    "l13" : {"1":100, "2":100, "3":100, "4":100, "5":100, "6":100, "7":100, "8":100, "9":100},
    "l14" : {"1":100, "2":100, "3":100, "4":100, "5":100, "6":100, "7":100, "8":100, "9":100},
    "l15" : {"1":100, "2":100, "3":100, "4":100, "5":100, "6":100, "7":100, "8":100, "9":100},
    "l16" : {"1":100, "2":100, "3":100, "4":100, "5":100, "6":100, "7":100, "8":100, "9":100},
    "l17" : {"1":100, "2":100, "3":100, "4":100, "5":100, "6":100, "7":100, "8":100, "9":100},
    "l18" : {"1":350, "2":350, "3":350, "4":350, "5":350, "6":350, "7":350, "8":350, "9":350},
    "l19" : {"1":100, "2":100, "3":100, "4":100, "5":100, "6":100, "7":100, "8":100, "9":100},
    "l20" : {"1":400, "2":400, "3":400, "4":400, "5":400, "6":400, "7":400, "8":400, "9":400},
    "l21" : {"1":400, "2":400, "3":400, "4":400, "5":400, "6":400, "7":400, "8":400, "9":400},
    "l22" : {"1":400, "2":400, "3":400, "4":400, "5":400, "6":400, "7":400, "8":400, "9":400},
    "l23" : {"1":400, "2":400, "3":400, "4":400, "5":400, "6":400, "7":400, "8":400, "9":400},
    "l24" : {"1":400, "2":400, "3":400, "4":400, "5":400, "6":400, "7":400, "8":400, "9":400},
    "l25" : {"1":400, "2":400, "3":400, "4":400, "5":400, "6":400, "7":400, "8":400, "9":400},
}
flow_lower_matrix = {
    "l1" : {"1":10, "2":10, "3":10, "4":10, "5":10, "6":10, "7":10, "8":10, "9":10},
    "l2" : {"1":10, "2":10, "3":10, "4":10, "5":10, "6":10, "7":10, "8":10, "9":10},
    "l3" : {"1":10, "2":10, "3":10, "4":10, "5":10, "6":10, "7":10, "8":10, "9":10},
    "l4" : {"1":0, "2":0, "3":0, "4":0, "5":0, "6":0, "7":0, "8":0, "9":0},
    "l5" : {"1":0, "2":0, "3":0, "4":0, "5":0, "6":0, "7":0, "8":0, "9":0},
    "l6" : {"1":0, "2":0, "3":0, "4":0, "5":0, "6":0, "7":0, "8":0, "9":0},
    "l7" : {"1":0, "2":0, "3":0, "4":0, "5":0, "6":0, "7":0, "8":0, "9":0},
    "l8" : {"1":0, "2":0, "3":0, "4":0, "5":0, "6":0, "7":0, "8":0, "9":0},
    "l9" : {"1":50, "2":50, "3":50, "4":50, "5":50, "6":50, "7":50, "8":50, "9":50},
    "l10" : {"1":0, "2":0, "3":0, "4":0, "5":0, "6":0, "7":0, "8":0, "9":0},
    "l11" : {"1":10, "2":10, "3":10, "4":10, "5":10, "6":10, "7":10, "8":10, "9":10},
    "l12" : {"1":10, "2":10, "3":10, "4":10, "5":10, "6":10, "7":10, "8":10, "9":10},
    "l13" : {"1":0, "2":0, "3":0, "4":0, "5":0, "6":0, "7":0, "8":0, "9":0},
    "l14" : {"1":50, "2":50, "3":50, "4":50, "5":50, "6":50, "7":50, "8":50, "9":50},
    "l15" : {"1":0, "2":0, "3":0, "4":0, "5":0, "6":0, "7":0, "8":0, "9":0},
    "l16" : {"1":0, "2":0, "3":0, "4":0, "5":0, "6":0, "7":0, "8":0, "9":0},
    "l17" : {"1":0, "2":0, "3":0, "4":0, "5":0, "6":0, "7":0, "8":0, "9":0},
    "l18" : {"1":0, "2":0, "3":0, "4":0, "5":0, "6":0, "7":0, "8":0, "9":0},
    "l19" : {"1":10, "2":10, "3":10, "4":10, "5":10, "6":10, "7":10, "8":10, "9":10},
    "l20" : {"1":0, "2":0, "3":0, "4":0, "5":0, "6":0, "7":0, "8":0, "9":0},
    "l21" : {"1":0, "2":0, "3":0, "4":0, "5":0, "6":0, "7":0, "8":0, "9":0},
    "l22" : {"1":0, "2":0, "3":0, "4":0, "5":0, "6":0, "7":0, "8":0, "9":0},
    "l23" : {"1":0, "2":0, "3":0, "4":0, "5":0, "6":0, "7":0, "8":0, "9":0},
    "l24" : {"1":0, "2":0, "3":0, "4":0, "5":0, "6":0, "7":0, "8":0, "9":0},
    "l25" : {"1":0, "2":0, "3":0, "4":0, "5":0, "6":0, "7":0, "8":0, "9":0},
}

# Creating nodes

sr1 = SurfaceReservoir(x=1,  y=2,   name="SR1")
sr1.inflow = inflow_matrix["sr1"]
sr1.min_storage = min_storage_matrix["sr1"]
sr1.max_storage = max_storage_matrix["sr1"]
sr1.initial_storage = initial_storage_matrix["sr1"]

sr2 = SurfaceReservoir(x=1,  y=3,   name="SR2")
sr2.inflow = inflow_matrix["sr2"]
sr2.min_storage = min_storage_matrix["sr2"]
sr2.max_storage = max_storage_matrix["sr2"]
sr2.initial_storage = initial_storage_matrix["sr2"]

sr3 = SurfaceReservoir(x=1,  y=3,   name="SR3")
sr3.inflow = inflow_matrix["sr3"]
sr3.min_storage = min_storage_matrix["sr3"]
sr3.max_storage = max_storage_matrix["sr3"]
sr3.initial_storage = initial_storage_matrix["sr3"]

sr4 = SurfaceReservoir(x=1,  y=4,   name="SR4")
sr4.inflow = inflow_matrix["sr4"]
sr4.min_storage = min_storage_matrix["sr4"]
sr4.max_storage = max_storage_matrix["sr4"]
sr4.initial_storage = initial_storage_matrix["sr4"]

desal1 = SurfaceReservoir(x=5,  y=4,   name="Desal1")
desal1.inflow = inflow_matrix["desal1"]
desal1.min_storage = min_storage_matrix["desal1"]
desal1.max_storage = max_storage_matrix["desal1"]
desal1.initial_storage = initial_storage_matrix["desal1"]

gw1 = AquiferStorage(x=6,  y=1,   name="GW1")
gw1.inflow = inflow_matrix["gw1"]
gw1.min_storage = min_storage_matrix["gw1"]
gw1.max_storage = max_storage_matrix["gw1"]
gw1.initial_storage = initial_storage_matrix["gw1"]

gw2 = AquiferStorage(x=6,  y=3,   name="GW2")
gw2.inflow = inflow_matrix["gw2"]
gw2.min_storage = min_storage_matrix["gw2"]
gw2.max_storage = max_storage_matrix["gw2"]
gw2.initial_storage = initial_storage_matrix["gw2"]

ag1 = AgriculturalNode(x=2,   y=2,   name="Ag1")
ag1.inflow = inflow_matrix["ag1"]
ag1.cost = cost_matrix["ag1"]
ag1.target_demand = demand_matrix["ag1"]

ag2 = AgriculturalNode(x=2,   y=3,   name="Ag2")
ag2.inflow = inflow_matrix["ag2"]
ag2.cost = cost_matrix["ag2"]
ag2.target_demand = demand_matrix["ag2"]

endpt = AgriculturalNode(x=150, y=450, name="Endpt")
endpt.inflow = inflow_matrix["endpt"]
endpt.cost = cost_matrix["endpt"]
endpt.target_demand = demand_matrix["endpt"]

urb1 = UrbanNode(x=10,  y=20,  name="Urb1")
urb1.inflow = inflow_matrix["urb1"]
urb1.cost = cost_matrix["urb1"]
urb1.target_demand = demand_matrix["urb1"]

urb2 = UrbanNode(x=10,  y=30,  name="Urb2")
urb2.inflow = inflow_matrix["urb2"]
urb2.cost = cost_matrix["urb2"]
urb2.target_demand = demand_matrix["urb2"]

jn1 = Junction(x=100, y=200, name="J1")

jn2 = Junction(x=150, y=250, name="J2")

jn3 = Junction(x=150, y=300, name="J3")

wwtp1 = WasteWaterTreatmentPlant(x=170, y=270, name="WWTP1")

hp1=HydropowerPlant(x=90, y=20, name="HP1")

n.add_nodes(sr1, sr2, sr3, sr4, desal1, gw1, gw2, ag1, ag2, endpt, urb1, urb2, jn1, jn2, jn3, wwtp1, hp1)
# Creating links

l1 = RiverSection(name="l1", start_node=sr2, end_node=sr4)
l1._flow_multiplier = flow_mult_matrix["l1"]
l1._lower_flow = flow_lower_matrix['l1']
l1._upper_flow = flow_upper_matrix['l1']

l2 = RiverSection(name="l2", start_node=sr1, end_node=jn1)
l2._flow_multiplier = flow_mult_matrix["l2"]
l2._lower_flow = flow_lower_matrix['l2']
l2._upper_flow = flow_upper_matrix['l2']

l3 = RiverSection(name="l3", start_node=jn1, end_node=sr2)
l3._flow_multiplier = flow_mult_matrix["l3"]
l3._lower_flow = flow_lower_matrix['l3']
l3._upper_flow = flow_upper_matrix['l3']

l4 = RiverSection(name="l4", start_node=gw2, end_node=ag2)
l4._flow_multiplier = flow_mult_matrix["l4"]
l4._lower_flow = flow_lower_matrix['l4']
l4._upper_flow = flow_upper_matrix['l4']

l5 = RiverSection(name="l5", start_node=gw2, end_node=ag1)
l5._flow_multiplier = flow_mult_matrix["l5"]
l5._lower_flow = flow_lower_matrix['l5']
l5._upper_flow = flow_upper_matrix['l5']

l6 = RiverSection(name="l6", start_node=ag1, end_node=jn2)
l6._flow_multiplier = flow_mult_matrix["l6"]
l6._lower_flow = flow_lower_matrix['l6']
l6._upper_flow = flow_upper_matrix['l6']

l7 = RiverSection(name="l7", start_node=wwtp1, end_node=jn2)
l7._flow_multiplier = flow_mult_matrix["l7"]
l7._lower_flow = flow_lower_matrix['l7']
l7._upper_flow = flow_upper_matrix['l7']

l8 = RiverSection(name="l8", start_node=urb1, end_node=jn1)
l8._flow_multiplier = flow_mult_matrix["l8"]
l8._lower_flow = flow_lower_matrix['l8']
l8._upper_flow = flow_upper_matrix['l8']

l9 = RiverSection(name="l9", start_node=ag2, end_node=gw2)
l9._flow_multiplier = flow_mult_matrix["l9"]
l9._lower_flow = flow_lower_matrix['l9']
l9._upper_flow = flow_upper_matrix['l9']

l10 = RiverSection(name="l10", start_node=desal1, end_node=urb2)
l10._flow_multiplier = flow_mult_matrix["l10"]
l10._lower_flow = flow_lower_matrix['l10']
l10._upper_flow = flow_upper_matrix['l10']

l11 = RiverSection(name="l11", start_node=sr4, end_node=ag1)
l11._flow_multiplier = flow_mult_matrix["l11"]
l11._lower_flow = flow_lower_matrix['l11']
l11._upper_flow = flow_upper_matrix['l11']

l12 = RiverSection(name="l12", start_node=wwtp1, end_node=urb2)
l12._flow_multiplier = flow_mult_matrix["l12"]
l12._lower_flow = flow_lower_matrix['l12']
l12._upper_flow = flow_upper_matrix['l12']

l13 = RiverSection(name="l13", start_node=hp1, end_node=sr4)
l13._flow_multiplier = flow_mult_matrix["l13"]
l13._lower_flow = flow_lower_matrix['l13']
l13._upper_flow = flow_upper_matrix['l13']

l14 = RiverSection(name="l14", start_node=urb2, end_node=wwtp1)
l14._flow_multiplier = flow_mult_matrix["l14"]
l14._lower_flow = flow_lower_matrix['l14']
l14._upper_flow = flow_upper_matrix['l14']

l15 = RiverSection(name="l15", start_node=jn2, end_node=jn3)
l15._flow_multiplier = flow_mult_matrix["l15"]
l15._lower_flow = flow_lower_matrix['l15']
l15._upper_flow = flow_upper_matrix['l15']

l16 = RiverSection(name="l16", start_node=sr4, end_node=jn2)
l16._flow_multiplier = flow_mult_matrix["l16"]
l16._lower_flow = flow_lower_matrix['l16']
l16._upper_flow = flow_upper_matrix['l16']

l17 = RiverSection(name="l17", start_node=ag1, end_node=gw2)
l17._flow_multiplier = flow_mult_matrix["l17"]
l17._lower_flow = flow_lower_matrix['l17']
l17._upper_flow = flow_upper_matrix['l17']

l18 = RiverSection(name="l18", start_node=sr3, end_node=hp1)
l18._flow_multiplier = flow_mult_matrix["l18"]
l18._lower_flow = flow_lower_matrix['l18']
l18._upper_flow = flow_upper_matrix['l18']

l19 = RiverSection(name="l19", start_node=jn2, end_node=ag2)
l19._flow_multiplier = flow_mult_matrix["l19"]
l19._lower_flow = flow_lower_matrix['l19']
l19._upper_flow = flow_upper_matrix['l19']

l20 = RiverSection(name="l20", start_node=urb1, end_node=gw1)
l20._flow_multiplier = flow_mult_matrix["l20"]
l20._lower_flow = flow_lower_matrix['l20']
l20._upper_flow = flow_upper_matrix['l20']

l21 = RiverSection(name="l21", start_node=sr4, end_node=urb2)
l21._flow_multiplier = flow_mult_matrix["l21"]
l21._lower_flow = flow_lower_matrix['l21']
l21._upper_flow = flow_upper_matrix['l21']

l22 = RiverSection(name="l22", start_node=gw1, end_node=urb1)
l22._flow_multiplier = flow_mult_matrix["l22"]
l22._lower_flow = flow_lower_matrix['l22']
l22._upper_flow = flow_upper_matrix['l22']

l23 = RiverSection(name="l23", start_node=ag2, end_node=jn3)
l23._flow_multiplier = flow_mult_matrix["l23"]
l23._lower_flow = flow_lower_matrix['l23']
l23._upper_flow = flow_upper_matrix['l23']

l24 = RiverSection(name="l24", start_node=jn3, end_node=endpt)
l24._flow_multiplier = flow_mult_matrix["l24"]
l24._lower_flow = flow_lower_matrix['l24']
l24._upper_flow = flow_upper_matrix['l24']

l25 = RiverSection(name="l25", start_node=sr1, end_node=urb1)
l25._flow_multiplier = flow_mult_matrix["l25"]
l25._lower_flow = flow_lower_matrix['l25']
l25._upper_flow = flow_upper_matrix['l25']

n.add_links(l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11, l12, l13, l14, l15, l16, l17, l18, l19, l20, l21, l22, l23, l24, l25)
s.network = n

allocator = PyomoAllocation(n)


s.add_engine(allocator)

s.start()

total_deficit = 0

nodes_names = []
for n in n.nodes:
    nodes_names.append(n.name)
    if n.type == 'irrigation':
        print "%s deficit = %s"%(n.name, n.deficit)
        total_deficit += n.deficit
print "finshed: ", sr1.initial_storage