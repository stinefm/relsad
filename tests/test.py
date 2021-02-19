from stinetwork.network.components import Bus, Line, CircuitBreaker, Disconnector
from stinetwork.network.systems import PowerSystem, Transmission, Distribution
from stinetwork.loadflow.ac import DistLoadFlow
from stinetwork.visualization.printing import dispVolt, dispFlow

# Buses and loads
Bus1 =  Bus("B1")
Bus2 =  Bus("B2")
Bus3 =  Bus("B3")
Bus4 =  Bus("B4")
Bus5 =  Bus("B5")
Bus6 =  Bus("B6")
Bus7 =  Bus("B7")
Bus8 =  Bus("B8")
Bus9 =  Bus("B9")
Bus10 = Bus("B10")
Bus11 = Bus("B11")
Bus12 = Bus("B12")
Bus13 = Bus("B13")
Bus14 = Bus("B14")
Bus15 = Bus("B15")
Bus16 = Bus("B16")
Bus17 = Bus("B17")
Bus18 = Bus("B18")
Bus19 = Bus("B19")
Bus20 = Bus("B20")
Bus21 = Bus("B21")
Bus22 = Bus("B22")
Bus23 = Bus("B23")
Bus24 = Bus("B24")
Bus25 = Bus("B25")
Bus26 = Bus("B26")
Bus27 = Bus("B27")
Bus28 = Bus("B28")
Bus29 = Bus("B29")
Bus30 = Bus("B30")
Bus31 = Bus("B31")
Bus32 = Bus("B32")
Bus33 = Bus("B33")

Bus1.set_load(load_dict={"Husholdning":{"pload":0     ,"qload":0.0}})
Bus2.set_load(load_dict={"Husholdning":{"pload":0.001 ,"qload": 0.0006}})
Bus3.set_load(load_dict={"Husholdning":{"pload":0.0009,"qload": 0.0004}})
Bus4.set_load(load_dict={"Husholdning":{"pload":0.0012,"qload": 0.0008}})
Bus5.set_load(load_dict={"Husholdning":{"pload":0.0006,"qload": 0.0003}})
Bus6.set_load(load_dict={"Husholdning":{"pload":0.0006,"qload": 0.0002}})
Bus7.set_load(load_dict={"Husholdning":{"pload":0.002 ,"qload": 0.001 }})
Bus8.set_load(load_dict={"Husholdning":{"pload":0.002 ,"qload": 0.001 }})
Bus9.set_load(load_dict={"Husholdning":{"pload":0.0006,"qload": 0.0002}})
Bus10.set_load(load_dict={"Husholdning":{"pload":0.0006 ,"qload":0.0002 }})
Bus11.set_load(load_dict={"Husholdning":{"pload":0.00045,"qload":0.0003 }})
Bus12.set_load(load_dict={"Husholdning":{"pload":0.0006 ,"qload":0.00035}})
Bus13.set_load(load_dict={"Husholdning":{"pload":0.0006 ,"qload":0.00035}})
Bus14.set_load(load_dict={"Husholdning":{"pload":0.0012 ,"qload":0.0008 }})
Bus15.set_load(load_dict={"Husholdning":{"pload":0.0006 ,"qload":0.0001 }})
Bus16.set_load(load_dict={"Husholdning":{"pload":0.0006 ,"qload":0.0002 }})
Bus17.set_load(load_dict={"Husholdning":{"pload":0.0006 ,"qload":0.0002 }})
Bus18.set_load(load_dict={"Husholdning":{"pload":0.0009 ,"qload":0.0004 }})
Bus19.set_load(load_dict={"Husholdning":{"pload":0.0009 ,"qload":0.0004 }})
Bus20.set_load(load_dict={"Husholdning":{"pload":0.0009 ,"qload":0.0004 }})
Bus21.set_load(load_dict={"Husholdning":{"pload":0.0009 ,"qload":0.0004 }})
Bus22.set_load(load_dict={"Husholdning":{"pload":0.0009 ,"qload":0.0004 }})
Bus23.set_load(load_dict={"Husholdning":{"pload":0.0009 ,"qload":0.0005 }})
Bus24.set_load(load_dict={"Husholdning":{"pload":0.0042 ,"qload":0.002  }})
Bus25.set_load(load_dict={"Husholdning":{"pload":0.0042 ,"qload":0.002  }})
Bus26.set_load(load_dict={"Husholdning":{"pload":0.0006 ,"qload":0.00025}})
Bus27.set_load(load_dict={"Husholdning":{"pload":0.0006 ,"qload":0.00025}})
Bus28.set_load(load_dict={"Husholdning":{"pload":0.0006 ,"qload":0.0002 }})
Bus29.set_load(load_dict={"Husholdning":{"pload":0.0012 ,"qload":0.0007 }})
Bus30.set_load(load_dict={"Husholdning":{"pload":0.002  ,"qload":0.006  }})
Bus31.set_load(load_dict={"Husholdning":{"pload":0.0015 ,"qload":0.0007 }})
Bus32.set_load(load_dict={"Husholdning":{"pload":0.0021 ,"qload":0.001  }})
Bus33.set_load(load_dict={"Husholdning":{"pload":0.0006 ,"qload":0.0004 }})



# Lines, connections and impedances
L1  = Line("L1", Bus1, Bus2, 0.057526629463617, 0.029324854498807)
L2  = Line("L2", Bus2, Bus3, 0.307599005700253, 0.156669594992563)
L3  = Line("L3", Bus3, Bus4, 0.228359505246029, 0.11630112507612)
L4  = Line("L4", Bus4, Bus5, 0.237780894670114, 0.121105409749329)
L5  = Line("L5", Bus5, Bus6, 0.511001187968574, 0.441120683630991)
L6  = Line("L6", Bus6, Bus7, 0.116800271535674, 0.386089786465145)
L7  = Line("L7", Bus7, Bus8, 1.06779906360124, 0.770619740244183)
L8  = Line("L8", Bus8, Bus9, 0.642651066675984, 0.4617104750876)
L9  = Line("L9", Bus9, Bus10, 0.651386129718182, 0.4617104750876)
L10 = Line("L10", Bus10, Bus11, 0.122665242435435, 0.040555649838776)
L11 = Line("L11", Bus11, Bus12, 0.233600543071348, 0.077242914616007)
L12 = Line("L12", Bus12, Bus13, 0.915933753281888, 0.720642700981322)
L13 = Line("L13", Bus13, Bus14, 0.337922153118168, 0.444801888770203)
L14 = Line("L14", Bus14, Bus15, 0.368744446995637, 0.328188797156862)
L15 = Line("L15", Bus15, Bus16, 0.465641253456589, 0.340043525571273)
L16 = Line("L16", Bus16, Bus17, 0.804249732956644, 1.07378882111589)
L17 = Line("L17", Bus17, Bus18, 0.456719010492059, 0.358137584730111)
L18 = Line("L18", Bus2, Bus19, 0.102325024208603, 0.097645526150283)
L19 = Line("L19", Bus19, Bus20, 0.938520130576714, 0.84567888909964)
L20 = Line("L20", Bus20, Bus21, 0.255500593984287, 0.298489582813389)
L21 = Line("L21", Bus21, Bus22, 0.442306156472432, 0.584812470675146)
L22 = Line("L22", Bus3, Bus23, 0.281518603188548, 0.192358566850685)
L23 = Line("L23", Bus23, Bus24, 0.560291900849547, 0.442430943087321)
L24 = Line("L24", Bus24, Bus25, 0.559044034700662, 0.437439478491779)
L25 = Line("L25", Bus6, Bus26, 0.126658414111869, 0.064514679897376)
L26 = Line("L26", Bus26, Bus27, 0.177321779756616, 0.090283115871859)
L27 = Line("L27", Bus27, Bus28, 0.660745125834823, 0.582566311607152)
L28 = Line("L28", Bus28, Bus29, 0.501766978466822, 0.437127511954558)
L29 = Line("L29", Bus29, Bus30, 0.316646035279672, 0.161286699743439)
L30 = Line("L30", Bus30, Bus31, 0.60796038773697, 0.600847550688323)
L31 = Line("L31", Bus31, Bus32, 0.193731219614459, 0.225801379640814)
L32 = Line("L32", Bus32, Bus33, 0.212761178384962, 0.330809316069521)

E1 = CircuitBreaker("E1", L1)

L1a = Disconnector("L1a", L1, Bus1)
L1b = Disconnector("L1b", L1, Bus2)

ps = PowerSystem()

transNetwork = Transmission(ps, Bus1)

distNetwork = Distribution(transNetwork, L1)

distNetwork.add_buses({Bus2, Bus3, Bus4, Bus5, Bus6, Bus7, Bus8, Bus9, Bus10,
                        Bus11, Bus12, Bus13, Bus14, Bus15, Bus16, Bus17, Bus18, Bus19, Bus20,
                        Bus21, Bus22, Bus23, Bus24, Bus25, Bus26, Bus27, Bus28, Bus29, Bus30, Bus31, Bus32, Bus33})

distNetwork.add_lines({L2, L3, L4, L5, L6, L7, L8, L9, L10,
                        L11, L12, L13, L14, L15, L16, L17, L18, L19, L20,
                        L21, L22, L23, L24, L25, L26, L27, L28, L29, L30, L31, L32})


ps.buses = DistLoadFlow(list(ps.buses), list(ps.lines))

dispVolt(list(ps.buses),tpres=False)
dispFlow(list(ps.buses), list(ps.lines),tpres=False)

