from stinetwork.network.components import Bus, Line
from stinetwork.network.systems import Distribution
from stinetwork.loadflow.ac import DistLoadFlow
from stinetwork.visualization.printing import dispVolt, dispFlow

# Buses and loads
Bus1 = Bus(1, 0, 0)
Bus2= Bus(2, 0.001,	0.0006)
Bus3 = Bus(3, 0.0009, 0.0004)
Bus4 = Bus(4, 0.0012, 0.0008)
Bus5 = Bus(5, 0.0006, 0.0003)
Bus6 = Bus(6, 0.0006, 0.0002)
Bus7 = Bus(7, 0.002, 0.001)
Bus8 = Bus(8, 0.002, 0.001)
Bus9 = Bus(9, 0.0006, 0.0002)
Bus10 = Bus(10, 0.0006, 0.0002)
Bus11 = Bus(11, 0.00045, 0.0003)
Bus12 = Bus(12, 0.0006, 0.00035)
Bus13 = Bus(13, 0.0006, 0.00035)
Bus14 = Bus(14, 0.0012, 0.0008)
Bus15 = Bus(15, 0.0006, 0.0001)
Bus16 = Bus(16, 0.0006, 0.0002)
Bus17 = Bus(17, 0.0006, 0.0002)
Bus18 = Bus(18, 0.0009, 0.0004)
Bus19 = Bus(19, 0.0009, 0.0004)
Bus20 = Bus(20, 0.0009, 0.0004)
Bus21 = Bus(21, 0.0009, 0.0004)
Bus22 = Bus(22, 0.0009, 0.0004)
Bus23 = Bus(23, 0.0009, 0.0005)
Bus24 = Bus(24, 0.0042, 0.002)
Bus25 = Bus(25, 0.0042, 0.002)
Bus26 = Bus(26, 0.0006, 0.00025)
Bus27 = Bus(27, 0.0006, 0.00025)
Bus28 = Bus(28, 0.0006, 0.0002)
Bus29 = Bus(29, 0.0012, 0.0007)
Bus30 = Bus(30, 0.002, 0.006)
Bus31 = Bus(31, 0.0015, 0.0007)
Bus32 = Bus(32, 0.0021, 0.001)
Bus33 = Bus(33, 0.0006, 0.0004)


# Lines, connections and impedances
L1  = Line(1 , Bus1, Bus2, 0.057526629463617, 0.029324854498807)
L2  = Line(2 , Bus2, Bus3, 0.307599005700253, 0.156669594992563)
L3  = Line(3 , Bus3, Bus4, 0.228359505246029, 0.11630112507612)
L4  = Line(4 , Bus4, Bus5, 0.237780894670114, 0.121105409749329)
L5  = Line(5 , Bus5, Bus6, 0.511001187968574, 0.441120683630991)
L6  = Line(6 , Bus6, Bus7, 0.116800271535674, 0.386089786465145)
L7  = Line(7 , Bus7, Bus8, 1.06779906360124, 0.770619740244183)
L8  = Line(8 , Bus8, Bus9, 0.642651066675984, 0.4617104750876)
L9  = Line(9 , Bus9, Bus10, 0.651386129718182, 0.4617104750876)
L10 = Line(10, Bus10, Bus11, 0.122665242435435, 0.040555649838776)
L11 = Line(11, Bus11, Bus12, 0.233600543071348, 0.077242914616007)
L12 = Line(12, Bus12, Bus13, 0.915933753281888, 0.720642700981322)
L13 = Line(13, Bus13, Bus14, 0.337922153118168, 0.444801888770203)
L14 = Line(14, Bus14, Bus15, 0.368744446995637, 0.328188797156862)
L15 = Line(15, Bus15, Bus16, 0.465641253456589, 0.340043525571273)
L16 = Line(16, Bus16, Bus17, 0.804249732956644, 1.07378882111589)
L17 = Line(17, Bus17, Bus18, 0.456719010492059, 0.358137584730111)
L18 = Line(18, Bus2, Bus19, 0.102325024208603, 0.097645526150283)
L19 = Line(19, Bus19, Bus20, 0.938520130576714, 0.84567888909964)
L20 = Line(20, Bus20, Bus21, 0.255500593984287, 0.298489582813389)
L21 = Line(21, Bus21, Bus22, 0.442306156472432, 0.584812470675146)
L22 = Line(22, Bus3, Bus23, 0.281518603188548, 0.192358566850685)
L23 = Line(23, Bus23, Bus24, 0.560291900849547, 0.442430943087321)
L24 = Line(24, Bus24, Bus25, 0.559044034700662, 0.437439478491779)
L25 = Line(25, Bus6, Bus26, 0.126658414111869, 0.064514679897376)
L26 = Line(26, Bus26, Bus27, 0.177321779756616, 0.090283115871859)
L27 = Line(27, Bus27, Bus28, 0.660745125834823, 0.582566311607152)
L28 = Line(28, Bus28, Bus29, 0.501766978466822, 0.437127511954558)
L29 = Line(29, Bus29, Bus30, 0.316646035279672, 0.161286699743439)
L30 = Line(30, Bus30, Bus31, 0.60796038773697, 0.600847550688323)
L31 = Line(31, Bus31, Bus32, 0.193731219614459, 0.225801379640814)
L32 = Line(32, Bus32, Bus33, 0.212761178384962, 0.330809316069521)



distNetwork = Distribution()

distNetwork.add_buses([ Bus1, Bus2, Bus3, Bus4, Bus5, Bus6, Bus7, Bus8, Bus9, Bus10,
                        Bus11, Bus12, Bus13, Bus14, Bus15, Bus16, Bus17, Bus18, Bus19, Bus20,
                        Bus21, Bus22, Bus23, Bus24, Bus25, Bus26, Bus27, Bus28, Bus29, Bus30, Bus31, Bus32, Bus33])

distNetwork.add_lines([ L1, L2, L3, L4, L5, L6, L7, L8, L9, L10,
                        L11, L12, L13, L14, L15, L16, L17, L18, L19, L20,
                        L21, L22, L23, L24, L25, L26, L27, L28, L29, L30, L31, L32])


distNetwork.buses = DistLoadFlow(distNetwork.buses, distNetwork.lines)

dispVolt(distNetwork.buses,tpres=False)
dispFlow(distNetwork.buses, distNetwork.lines,tpres=False)

