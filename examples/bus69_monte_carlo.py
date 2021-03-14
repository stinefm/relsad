from load_and_gen_data import WeatherGen, LoadGen, windGen, PVgeneration
import time, os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

start = time.time()

ps = initialize_69Bus_network()

if True:
    # Fetching bus-objects
    B1 = ps.get_comp("B1")
    B2 = ps.get_comp("B2")
    B3 = ps.get_comp("B3")
    B4 = ps.get_comp("B4")
    B5 = ps.get_comp("B5")
    B6 = ps.get_comp("B6")
    B7 = ps.get_comp("B7")
    B8 = ps.get_comp("B8")
    B9 = ps.get_comp("B9")
    B10 = ps.get_comp("B10")
    B11 = ps.get_comp("B11")
    B12 = ps.get_comp("B12")
    B13 = ps.get_comp("B13")
    B14 = ps.get_comp("B14")
    B15 = ps.get_comp("B15")
    B16 = ps.get_comp("B16")
    B17 = ps.get_comp("B17")
    B18 = ps.get_comp("B18")
    B19 = ps.get_comp("B19")
    B20 = ps.get_comp("B20")
    B21 = ps.get_comp("B21")
    B22 = ps.get_comp("B22")
    B23 = ps.get_comp("B23")
    B24 = ps.get_comp("B24")
    B25 = ps.get_comp("B25")
    B26 = ps.get_comp("B26")
    B27 = ps.get_comp("B27")
    B28 = ps.get_comp("B28")
    B29 = ps.get_comp("B29")
    B30 = ps.get_comp("B30")
    B31 = ps.get_comp("B31")
    B32 = ps.get_comp("B32")
    B33 = ps.get_comp("B33")
    B34 = ps.get_comp("B34")
    B35 = ps.get_comp("B35")
    B36 = ps.get_comp("B36")
    B37 = ps.get_comp("B37")
    B38 = ps.get_comp("B38")
    B39 = ps.get_comp("B39")
    B40 = ps.get_comp("B40")
    B41 = ps.get_comp("B41")
    B42 = ps.get_comp("B42")
    B43 = ps.get_comp("B43")
    B44 = ps.get_comp("B44")
    B45 = ps.get_comp("B45")
    B46 = ps.get_comp("B46")
    B47 = ps.get_comp("B47")
    B48 = ps.get_comp("B48")
    B49 = ps.get_comp("B49")
    B50 = ps.get_comp("B50")
    B51 = ps.get_comp("B51")
    B52 = ps.get_comp("B52")
    B53 = ps.get_comp("B53")
    B54 = ps.get_comp("B54")
    B55 = ps.get_comp("B55")
    B56 = ps.get_comp("B56")
    B57 = ps.get_comp("B57")
    B58 = ps.get_comp("B58")
    B59 = ps.get_comp("B59")
    B60 = ps.get_comp("B60")
    B61 = ps.get_comp("B61")
    B62 = ps.get_comp("B62")
    B63 = ps.get_comp("B63")
    B64 = ps.get_comp("B64")
    B65 = ps.get_comp("B65")
    B66 = ps.get_comp("B66")
    B67 = ps.get_comp("B67")
    B68 = ps.get_comp("B68")
    B69 = ps.get_comp("B69")


if True:
    # Fetching line-objects
    L1 = ps.get_comp("L1")
    L2 = ps.get_comp("L2")
    L3 = ps.get_comp("L3")
    L4 = ps.get_comp("L4")
    L5 = ps.get_comp("L5")
    L6 = ps.get_comp("L6")
    L7 = ps.get_comp("L7")
    L8 = ps.get_comp("L8")
    L9 = ps.get_comp("L9")
    L10 = ps.get_comp("L10")
    L11 = ps.get_comp("L11")
    L12 = ps.get_comp("L12")
    L13 = ps.get_comp("L13")
    L14 = ps.get_comp("L14")
    L15 = ps.get_comp("L15")
    L16 = ps.get_comp("L16")
    L17 = ps.get_comp("L17")
    L18 = ps.get_comp("L18")
    L19 = ps.get_comp("L19")
    L20 = ps.get_comp("L20")
    L21 = ps.get_comp("L21")
    L22 = ps.get_comp("L22")
    L23 = ps.get_comp("L23")
    L24 = ps.get_comp("L24")
    L25 = ps.get_comp("L25")
    L26 = ps.get_comp("L26")
    L27 = ps.get_comp("L27")
    L28 = ps.get_comp("L28")
    L29 = ps.get_comp("L29")
    L30 = ps.get_comp("L30")
    L31 = ps.get_comp("L31")
    L32 = ps.get_comp("L32")
    L33 = ps.get_comp("L33")
    L34 = ps.get_comp("L34")
    L35 = ps.get_comp("L35")
    L36 = ps.get_comp("L36")
    L37 = ps.get_comp("L37")
    L38 = ps.get_comp("L38")
    L39 = ps.get_comp("L39")
    L40 = ps.get_comp("L40")
    L41 = ps.get_comp("L41")
    L42 = ps.get_comp("L42")
    L43 = ps.get_comp("L43")
    L44 = ps.get_comp("L44")
    L45 = ps.get_comp("L45")
    L46 = ps.get_comp("L46")
    L47 = ps.get_comp("L47")
    L48 = ps.get_comp("L48")
    L49 = ps.get_comp("L49")
    L50 = ps.get_comp("L50")
    L51 = ps.get_comp("L51")
    L52 = ps.get_comp("L52")
    L53 = ps.get_comp("L53")
    L54 = ps.get_comp("L54")
    L55 = ps.get_comp("L55")
    L56 = ps.get_comp("L56")
    L57 = ps.get_comp("L57")
    L58 = ps.get_comp("L58")
    L59 = ps.get_comp("L59")
    L60 = ps.get_comp("L60")
    L61 = ps.get_comp("L61")
    L62 = ps.get_comp("L62")
    L63 = ps.get_comp("L63")
    L64 = ps.get_comp("L64")
    L65 = ps.get_comp("L65")
    L66 = ps.get_comp("L66")
    L67 = ps.get_comp("L67")
    L68 = ps.get_comp("L68")
    L69 = ps.get_comp("L69")
    L70 = ps.get_comp("L70")
    L71 = ps.get_comp("L71")
    L72 = ps.get_comp("L72")
    L73 = ps.get_comp("L73")


if True:
    # Fetching disconnector objects
    L1a = ps.get_comp("L1a")
    L1b = ps.get_comp("L1b")
    L1c = ps.get_comp("L1c")
    L2a = ps.get_comp("L2a")
    L2b = ps.get_comp("L2b")
    L3a = ps.get_comp("L3a")
    L3b = ps.get_comp("L3b")
    L4a = ps.get_comp("L4a")
    L4b = ps.get_comp("L4b")
    L5a = ps.get_comp("L5a")
    L5b = ps.get_comp("L5b")
    L6a = ps.get_comp("L6a")
    L6b = ps.get_comp("L6b")
    L7a = ps.get_comp("L7a")
    L7b = ps.get_comp("L7b")
    L8a = ps.get_comp("L8a")
    L8b = ps.get_comp("L8b")
    L9a = ps.get_comp("L9a")
    L9b = ps.get_comp("L9b")
    L10a = ps.get_comp("L10a")
    L10b = ps.get_comp("L10b")
    L11a = ps.get_comp("L11a")
    L11b = ps.get_comp("L11b")
    L12a = ps.get_comp("L12a")
    L12b = ps.get_comp("L12b")
    L13a = ps.get_comp("L13a")
    L13b = ps.get_comp("L13b")
    L14a = ps.get_comp("L14a")
    L14b = ps.get_comp("L14b")
    L15a = ps.get_comp("L15a")
    L15b = ps.get_comp("L15b")
    L16a = ps.get_comp("L16a")
    L16b = ps.get_comp("L16b")
    L17a = ps.get_comp("L17a")
    L17b = ps.get_comp("L17b")
    L18a = ps.get_comp("L18a")
    L18b = ps.get_comp("L18b")
    L19a = ps.get_comp("L19a")
    L19b = ps.get_comp("L19b")
    L20a = ps.get_comp("L20a")
    L20b = ps.get_comp("L20b")
    L21a = ps.get_comp("L21a")
    L21b = ps.get_comp("L21b")
    L22a = ps.get_comp("L22a")
    L22b = ps.get_comp("L22b")
    L23a = ps.get_comp("L23a")
    L23b = ps.get_comp("L23b")
    L24a = ps.get_comp("L24a")
    L24b = ps.get_comp("L24b")
    L25a = ps.get_comp("L25a")
    L25b = ps.get_comp("L25b")
    L26a = ps.get_comp("L26a")
    L26b = ps.get_comp("L26b")
    L27a = ps.get_comp("L27a")
    L27b = ps.get_comp("L27b")
    L28a = ps.get_comp("L28a")
    L28b = ps.get_comp("L28b")
    L29a = ps.get_comp("L29a")
    L29b = ps.get_comp("L29b")
    L30a = ps.get_comp("L30a")
    L30b = ps.get_comp("L30b")
    L31a = ps.get_comp("L31a")
    L31b = ps.get_comp("L31b")
    L32a = ps.get_comp("L32a")
    L32b = ps.get_comp("L32b")
    L33a = ps.get_comp("L33a")
    L33b = ps.get_comp("L33b")
    L34a = ps.get_comp("L34a")
    L34b = ps.get_comp("L34b")
    L35a = ps.get_comp("L35a")
    L35b = ps.get_comp("L35b")
    L36a = ps.get_comp("L36a")
    L36b = ps.get_comp("L36b")
    L37a = ps.get_comp("L37a")
    L37b = ps.get_comp("L37b")
    L38a = ps.get_comp("L38a")
    L38b = ps.get_comp("L38b")
    L39a = ps.get_comp("L39a")
    L39b = ps.get_comp("L39b")
    L40a = ps.get_comp("L40a")
    L40b = ps.get_comp("L40b")
    L41a = ps.get_comp("L41a")
    L41b = ps.get_comp("L41b")
    L42a = ps.get_comp("L42a")
    L42b = ps.get_comp("L42b")
    L43a = ps.get_comp("L43a")
    L43b = ps.get_comp("L43b")
    L44a = ps.get_comp("L44a")
    L44b = ps.get_comp("L44b")
    L45a = ps.get_comp("L45a")
    L45b = ps.get_comp("L45b")
    L46a = ps.get_comp("L46a")
    L46b = ps.get_comp("L46b")
    L47a = ps.get_comp("L47a")
    L47b = ps.get_comp("L47b")
    L48a = ps.get_comp("L48a")
    L48b = ps.get_comp("L48b")
    L49a = ps.get_comp("L49a")
    L49b = ps.get_comp("L49b")
    L50a = ps.get_comp("L50a")
    L50b = ps.get_comp("L50b")
    L51a = ps.get_comp("L51a")
    L51b = ps.get_comp("L51b")
    L52a = ps.get_comp("L52a")
    L52b = ps.get_comp("L52b")
    L53a = ps.get_comp("L53a")
    L53b = ps.get_comp("L53b")
    L54a = ps.get_comp("L54a")
    L54b = ps.get_comp("L54b")
    L55a = ps.get_comp("L55a")
    L55b = ps.get_comp("L55b")
    L56a = ps.get_comp("L56a")
    L56b = ps.get_comp("L56b")
    L57a = ps.get_comp("L57a")
    L57b = ps.get_comp("L57b")
    L58a = ps.get_comp("L58a")
    L58b = ps.get_comp("L58b")
    L59a = ps.get_comp("L59a")
    L59b = ps.get_comp("L59b")
    L60a = ps.get_comp("L60a")
    L60b = ps.get_comp("L60b")
    L61a = ps.get_comp("L61a")
    L61b = ps.get_comp("L61b")
    L62a = ps.get_comp("L62a")
    L62b = ps.get_comp("L62b")
    L63a = ps.get_comp("L63a")
    L63b = ps.get_comp("L63b")
    L64a = ps.get_comp("L64a")
    L64b = ps.get_comp("L64b")
    L65a = ps.get_comp("L65a")
    L65b = ps.get_comp("L65b")
    L66a = ps.get_comp("L66a")
    L66b = ps.get_comp("L66b")
    L67a = ps.get_comp("L67a")
    L67b = ps.get_comp("L67b")
    L68a = ps.get_comp("L68a")
    L68b = ps.get_comp("L68b")
    L69a = ps.get_comp("L69a")
    L69b = ps.get_comp("L69b")
    L70a = ps.get_comp("L70a")
    L70b = ps.get_comp("L70b")
    L71a = ps.get_comp("L71a")
    L71b = ps.get_comp("L71b")
    L72a = ps.get_comp("L72a")
    L72b = ps.get_comp("L72b")
    L73a = ps.get_comp("L73a")
    L73b = ps.get_comp("L73b")


# Fetching battery and production objects
# Bat1 = M1.get_battery()
# P1 = M2.get_production()
# P2 = B5.get_production()

temp_profiles, wind_profiles, solar_profiles = WeatherGen()

wind = windGen(wind_profiles)
PV = PVgeneration(temp_profiles, solar_profiles)

load_house, load_farm, load_industry2, load_trade, load_office = LoadGen(temp_profiles)


N = 1  # Size of Monte Carlo simulation

for i in range(N):
    for day in range(20):
        for hour in range(24):
            print("hour: {}".format(day * 24 + hour))
            ## Set load
            # B1.set_load(load_dict={"Husholdning":{"pload":load_house[day,hour]*10,"qload":0.0},
            # "Industri":{"pload":load_industry2[day,hour]*10,"qload":0.0}})
            B2.set_load(
                load_dict={
                    "Husholdning": {"pload": load_house[day, hour] * 50, "qload": 0.0}
                }
            )
            B3.set_load(
                load_dict={
                    "Husholdning": {"pload": load_house[day, hour] * 60, "qload": 0.0}
                }
            )
            B4.set_load(
                load_dict={
                    "Husholdning": {"pload": load_house[day, hour] * 52, "qload": 0.0}
                }
            )
            B5.set_load(
                load_dict={
                    "Husholdning": {"pload": load_house[day, hour] * 50, "qload": 0.0}
                }
            )
            B6.set_load(
                load_dict={
                    "Husholdning": {"pload": load_house[day, hour] * 70, "qload": 0.0}
                }
            )
            B7.set_load(
                load_dict={
                    "Husholdning": {"pload": load_house[day, hour] * 100, "qload": 0.0}
                }
            )
            B8.set_load(
                load_dict={
                    "Husholdning": {"pload": load_house[day, hour] * 70, "qload": 0.0}
                }
            )
            B9.set_load(
                load_dict={
                    "Husholdning": {"pload": load_house[day, hour] * 53, "qload": 0.0}
                }
            )
            B10.set_load(
                load_dict={
                    "Husholdning": {"pload": load_house[day, hour] * 65, "qload": 0.0}
                }
            )
            B11.set_load(
                load_dict={
                    "Husholdning": {"pload": load_house[day, hour] * 88, "qload": 0.0}
                }
            )
            B12.set_load(
                load_dict={
                    "Husholdning": {"pload": load_house[day, hour] * 74, "qload": 0.0}
                }
            )
            B13.set_load(
                load_dict={
                    "Husholdning": {"pload": load_house[day, hour] * 62, "qload": 0.0}
                }
            )
            B14.set_load(
                load_dict={
                    "Husholdning": {"pload": load_house[day, hour] * 59, "qload": 0.0}
                }
            )
            B15.set_load(
                load_dict={
                    "Husholdning": {"pload": load_house[day, hour] * 69, "qload": 0.0}
                }
            )
            B16.set_load(
                load_dict={
                    "Husholdning": {"pload": load_house[day, hour] * 88, "qload": 0.0}
                }
            )
            B17.set_load(
                load_dict={
                    "Husholdning": {"pload": load_house[day, hour] * 72, "qload": 0.0}
                }
            )
            B18.set_load(
                load_dict={
                    "Jordbruk": {"pload": load_farm[day, hour] * 50, "qload": 0.0}
                }
            )
            B19.set_load(
                load_dict={
                    "Jordbruk": {"pload": load_farm[day, hour] * 66, "qload": 0.0}
                }
            )
            B20.set_load(
                load_dict={
                    "Jordbruk": {"pload": load_farm[day, hour] * 74, "qload": 0.0}
                }
            )
            B21.set_load(
                load_dict={
                    "Jordbruk": {"pload": load_farm[day, hour] * 78, "qload": 0.0}
                }
            )
            B22.set_load(
                load_dict={
                    "Jordbruk": {"pload": load_farm[day, hour] * 88, "qload": 0.0}
                }
            )
            B23.set_load(
                load_dict={
                    "Jordbruk": {"pload": load_farm[day, hour] * 60, "qload": 0.0}
                }
            )
            B24.set_load(
                load_dict={
                    "Jordbruk": {"pload": load_farm[day, hour] * 55, "qload": 0.0}
                }
            )
            B25.set_load(
                load_dict={
                    "Jordbruk": {"pload": load_farm[day, hour] * 56, "qload": 0.0}
                }
            )
            B26.set_load(
                load_dict={
                    "Jordbruk": {"pload": load_farm[day, hour] * 69, "qload": 0.0}
                }
            )
            B27.set_load(
                load_dict={
                    "Jordbruk": {"pload": load_farm[day, hour] * 71, "qload": 0.0}
                }
            )
            B28.set_load(
                load_dict={
                    "Offentlig virksomhet": {
                        "pload": load_office[day, hour] * 2,
                        "qload": 0.0,
                    }
                }
            )
            B29.set_load(
                load_dict={
                    "Offentlig virksomhet": {
                        "pload": load_office[day, hour] * 1,
                        "qload": 0.0,
                    }
                }
            )
            B30.set_load(
                load_dict={
                    "Offentlig virksomhet": {
                        "pload": load_office[day, hour] * 1,
                        "qload": 0.0,
                    }
                }
            )
            B31.set_load(
                load_dict={
                    "Handel of tjenester": {
                        "pload": load_trade[day, hour] * 3,
                        "qload": 0.0,
                    }
                }
            )
            B32.set_load(
                load_dict={
                    "Handel of tjenester": {
                        "pload": load_trade[day, hour] * 1,
                        "qload": 0.0,
                    }
                }
            )
            B33.set_load(
                load_dict={
                    "Husholdning": {"pload": load_house[day, hour] * 55, "qload": 0.0}
                }
            )
            B34.set_load(
                load_dict={
                    "Husholdning": {"pload": load_house[day, hour] * 42, "qload": 0.0}
                }
            )
            B35.set_load(
                load_dict={
                    "Husholdning": {"pload": load_house[day, hour] * 52, "qload": 0.0}
                }
            )
            B36.set_load(
                load_dict={
                    "Industri": {"pload": load_industry2[day, hour] * 2, "qload": 0.0}
                }
            )
            B37.set_load(
                load_dict={
                    "Industri": {"pload": load_industry2[day, hour] * 1, "qload": 0.0}
                }
            )
            B38.set_load(
                load_dict={
                    "Offentlig virksomhet": {
                        "pload": load_office[day, hour] * 1,
                        "qload": 0.0,
                    }
                }
            )
            B39.set_load(
                load_dict={
                    "Offentlig virksomhet": {
                        "pload": load_office[day, hour] * 2,
                        "qload": 0.0,
                    }
                }
            )
            B40.set_load(
                load_dict={
                    "Husholdning": {"pload": load_house[day, hour] * 54, "qload": 0.0}
                }
            )
            B41.set_load(
                load_dict={
                    "Husholdning": {"pload": load_house[day, hour] * 63, "qload": 0.0}
                }
            )
            B42.set_load(
                load_dict={
                    "Handel of tjenester": {
                        "pload": load_trade[day, hour] * 3,
                        "qload": 0.0,
                    }
                }
            )
            B43.set_load(
                load_dict={
                    "Handel of tjenester": {
                        "pload": load_trade[day, hour] * 2,
                        "qload": 0.0,
                    }
                }
            )
            B44.set_load(
                load_dict={
                    "Offentlig virksomhet": {
                        "pload": load_office[day, hour] * 2,
                        "qload": 0.0,
                    }
                }
            )
            B45.set_load(
                load_dict={
                    "Jordbruk": {"pload": load_farm[day, hour] * 63, "qload": 0.0}
                }
            )
            B46.set_load(
                load_dict={
                    "Jordbruk": {"pload": load_farm[day, hour] * 63, "qload": 0.0}
                }
            )
            B47.set_load(
                load_dict={
                    "Husholdning": {"pload": load_house[day, hour] * 50, "qload": 0.0}
                }
            )
            B48.set_load(
                load_dict={
                    "Husholdning": {"pload": load_house[day, hour] * 50, "qload": 0.0}
                }
            )
            B49.set_load(
                load_dict={
                    "Offentlig virksomhet": {
                        "pload": load_office[day, hour] * 2,
                        "qload": 0.0,
                    }
                }
            )
            B50.set_load(
                load_dict={
                    "Offentlig virksomhet": {
                        "pload": load_office[day, hour] * 1,
                        "qload": 0.0,
                    }
                }
            )
            B51.set_load(
                load_dict={
                    "Offentlig virksomhet": {
                        "pload": load_office[day, hour] * 1,
                        "qload": 0.0,
                    }
                }
            )
            B52.set_load(
                load_dict={
                    "Offentlig virksomhet": {
                        "pload": load_office[day, hour] * 2,
                        "qload": 0.0,
                    }
                }
            )
            B53.set_load(
                load_dict={
                    "Husholdning": {"pload": load_house[day, hour] * 55, "qload": 0.0}
                }
            )
            B54.set_load(
                load_dict={
                    "Husholdning": {"pload": load_house[day, hour] * 60, "qload": 0.0}
                }
            )
            B55.set_load(
                load_dict={
                    "Husholdning": {"pload": load_house[day, hour] * 42, "qload": 0.0}
                }
            )
            B56.set_load(
                load_dict={
                    "Jordbruk": {"pload": load_farm[day, hour] * 63, "qload": 0.0}
                }
            )
            B57.set_load(
                load_dict={
                    "Jordbruk": {"pload": load_farm[day, hour] * 45, "qload": 0.0}
                }
            )
            B58.set_load(
                load_dict={
                    "Jordbruk": {"pload": load_farm[day, hour] * 40, "qload": 0.0}
                }
            )
            B59.set_load(
                load_dict={
                    "Industri": {"pload": load_industry2[day, hour] * 2, "qload": 0.0}
                }
            )
            B60.set_load(
                load_dict={
                    "Industri": {"pload": load_industry2[day, hour] * 2, "qload": 0.0}
                }
            )
            B61.set_load(
                load_dict={
                    "Industri": {"pload": load_industry2[day, hour] * 3, "qload": 0.0}
                }
            )
            B62.set_load(
                load_dict={
                    "Handel of tjenester": {
                        "pload": load_trade[day, hour] * 3,
                        "qload": 0.0,
                    }
                }
            )
            B63.set_load(
                load_dict={
                    "Handel of tjenester": {
                        "pload": load_trade[day, hour] * 2,
                        "qload": 0.0,
                    }
                }
            )
            B64.set_load(
                load_dict={
                    "Handel of tjenester": {
                        "pload": load_trade[day, hour] * 4,
                        "qload": 0.0,
                    }
                }
            )
            B65.set_load(
                load_dict={
                    "Industri": {"pload": load_industry2[day, hour] * 1, "qload": 0.0}
                }
            )
            B66.set_load(
                load_dict={
                    "Husholdning": {"pload": load_house[day, hour] * 100, "qload": 0.0}
                }
            )
            B67.set_load(
                load_dict={
                    "Jordbruk": {"pload": load_farm[day, hour] * 63, "qload": 0.0}
                }
            )
            B68.set_load(
                load_dict={
                    "Husholdning": {"pload": load_house[day, hour] * 62, "qload": 0.0}
                }
            )
            B69.set_load(
                load_dict={
                    "Jordbruk": {"pload": load_farm[day, hour] * 50, "qload": 0.0}
                }
            )

            # M2.set_load(load_dict={"Husholdning":{"pload":load_house[day,hour]*10,"qload":0.0}})
            # M3.set_load(load_dict={"Husholdning":{"pload":load_house[day,hour]*10,"qload":0.0}})

            ## Set production
            # P1.set_prod(pprod=PV[day,hour]+wind[day,hour], qprod=0)
            # P2.set_prod(pprod=wind[day,hour], qprod=0)

            ps.run()
