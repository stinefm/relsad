import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def weather_generation_data(
    path: str = os.path.join("data", "weather_data_rygge.csv"),
):

    # Generate temperatures for a whole year
    data = pd.read_csv(path, header=None, skiprows=1)

    temp_profiles = data[1].values.reshape(365, 24)
    wind_profiles = data[2].values.reshape(365, 24)
    solar_profiles = data[3].values.reshape(365, 24)

    return temp_profiles, wind_profiles, solar_profiles


def load_data(
    temp: np.array,
    path: str = os.path.join("data", "load_profiles_fasit.csv"),
):

    # Generating load profiles:

    data = pd.read_csv(
        path,
        sep=";",
        decimal=",",
        header=None,
    ).transpose()
    data = data.stack().str.replace(",", ".").unstack()

    house_A = data[10].values[4:-1].astype(float)
    house_B = data[11].values[4:-1].astype(float)

    farm_A = data[2].values[4:-1].astype(float)
    farm_B = data[3].values[4:-1].astype(float)

    industry2_A = data[26].values[4:-1].astype(float)
    industry2_B = data[27].values[4:-1].astype(float)

    trade_A = data[42].values[4:-1].astype(float)
    trade_B = data[43].values[4:-1].astype(float)

    office_A = data[50].values[4:-1].astype(float)
    office_B = data[51].values[4:-1].astype(float)

    load_house = np.zeros_like(temp)
    load_farm = np.zeros_like(temp)
    load_microgrid = np.zeros_like(temp)
    load_industry2 = np.zeros_like(temp)
    load_trade = np.zeros_like(temp)
    load_office = np.zeros_like(temp)

    for i in range(len(temp)):
        for j in range(len(temp[i])):
            if temp[i, j] > 20:
                temp[i, j] = 20

            load_house[i, j] = house_A[j] * temp[i, j] + house_B[j]
            load_farm[i, j] = farm_A[j] * temp[i, j] + farm_B[j]
            load_microgrid[i, j] = farm_A[j] * temp[i, j] + farm_B[j]
            load_industry2[i, j] = industry2_A[j] * temp[i, j] + industry2_B[j]
            load_trade[i, j] = trade_A[j] * temp[i, j] + trade_B[j]
            load_office[i, j] = office_A[j] * temp[i, j] + office_B[j]

    return (
        load_house.reshape((8760)) * 1e-3,
        load_farm.reshape((8760)) * 1e-3,
        load_microgrid.reshape((8760)) * 1e-3,
        load_industry2.reshape((8760)) * 1e-3,
        load_trade.reshape((8760)) * 1e-3,
        load_office.reshape((8760)) * 1e-3,
    )


def wind_power(
    wind: np.array,
):

    # Wind power

    # https://en.wind-turbine-models.com/turbines/1829-aeolia-windtech-d2cf-200

    N = 5
    alpha = 0.25
    H_0 = 2
    H = 50

    v = np.zeros_like(wind)
    P_out = np.zeros_like(wind)

    P_rated = np.array(
        [
            0,
            0,
            0,
            34.8,
            69.7,
            123.5,
            200.7,
            306.6,
            446.4,
            495.0,
            500,
            500,
            500,
            500,
            500,
            500,
            500,
            500,
            500,
            500,
            500,
            500,
            500,
            500,
            500,
            0,
        ]
    )

    for i in range(len(wind)):
        for j in range(len(wind[i])):
            v[i, j] = wind[i, j] * (H / H_0) ** (alpha)

    for day in range(len(v)):
        for hour in range(len(v[day])):

            if v[day, hour] <= 3 or v[day, hour] > 25:
                P_out[day, hour] = 0

            elif v[day, hour] > 10 and v[day, hour] <= 25:
                P_out[day, hour] = 500 * 10 ** (-3) * N

            else:
                v_a = int(v[day, hour])
                v_b = v_a + 1
                P_out[day, hour] = (
                    N
                    * (
                        P_rated[v_a - 1]
                        + (P_rated[v_b - 1] - P_rated[v_a - 1])
                        * ((v[day, hour] - v_a) / (v_b - v_a))
                    )
                    * 10 ** (-3)
                )

    return P_out.reshape((8760))


def pv_power(
    temp: np.array,
    irridation: np.array,
):

    modules = 5000 / 2

    # Maximum power point voltage [V]
    Vmpp = 31.2
    # Maximum power point current [A]
    Impp = 8.18

    # Open circuit voltage [V]
    Voc = 37.8
    # Short circuit current [A]
    Isc = 8.89

    # Maximum power point power [W]
    Pmpp = Vmpp * Impp

    # Nominal operating cell temperature [C]
    NOCT = 47.0

    # Area of the modul [m^2]
    area_modul = 1.6

    # Referance temp (25 C) [K]
    T_0 = 25 + 273.15

    # Standard irradiance [W/m^2 ]
    E_0 = 1000

    # Fill factor
    FF = Pmpp / (Voc * Isc)

    # Constant [A/(W/m^2)]
    K = Isc / E_0

    # diode saturation current [A/m^2]
    I_0 = 10 ** (-12) * area_modul

    # Constant term K/I0 (=10^6 m^2/W)
    k1 = K / I_0

    # Inverter efficiency
    n_inv = 0.9

    # Fill factor modul constant [Km^2]
    # Cff = Voc*Isc*T0*FF/(E0*ln(10^6*E0))
    # Equation 9
    Cff = Voc * Isc * T_0 * FF / (E_0 * np.log(10 ** (6) * E_0))

    E = irridation

    # Temperatur on the cell
    # Tcell = Temp + (NOCT-20)/800*Global_inn + 273.15 [K]
    T_cell = np.zeros_like(temp)

    # Output power for each modulin [Wh/h]
    # FF*Isc*global_inn(E)/E_0*Voc*ln(k1*E)/ln(k1*E0)*T0/T_cell
    # Equation 5
    P_out = np.zeros_like(temp)

    # Output power after the inverter for all modules [Wh/h]
    # Pout * n_inv * #modules
    P_out_mod_inv = np.zeros_like(temp)

    # Output power [Wh/h], equtaion 8
    # FF * Isc*Voc*T_0/(E_0*(ln(10^6*E_0)))*n_inv*#modules*E*ln(10^6*E)/T_cell
    # Cff * #modules*n_inv*(E*ln(10^6*E))/T_cell
    P_out_simp = np.zeros_like(temp)

    for i in range(len(temp)):
        for j in range(len(temp[i])):

            if irridation[i, j] <= 0.0:

                T_cell[i, j] = temp[i, j] + 273.15
            else:
                T_cell[i, j] = (
                    temp[i, j]
                    + ((NOCT - 20) / 800) * irridation[i, j]
                    + 273.15
                )

            if E[i, j] <= 0.0:
                P_out[i, j] = 0
                P_out_mod_inv[i, j] = 0
                P_out_simp[i, j] = 0

            else:
                P_out[i, j] = (
                    FF
                    * (Isc * (E[i, j] / E_0))
                    * (
                        Voc
                        * (np.log(k1 * E[i, j]) / np.log(k1 * E_0))
                        * (T_0 / T_cell[i, j])
                    )
                )
                P_out_mod_inv[i, j] = P_out[i, j] * n_inv * modules
                P_out_simp[i, j] = (
                    Cff
                    * modules
                    * n_inv
                    * ((E[i, j] * np.log(10 ** (6) * E[i, j])) / T_cell[i, j])
                )

    P_out_mod_inv *= 10 ** (-6)

    return P_out_mod_inv.reshape((8760))


if __name__ == "__main__":

    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    temp_profiles, wind_profiles, solar_profiles = weather_generation_data(
        path=os.path.join(
            os.pardir, os.pardir, "data", "weather_data_rygge.csv"
        ),
    )

    wind = wind_power(wind_profiles)
    PV = pv_power(temp_profiles, solar_profiles)

    fig1, ax1 = plt.subplots()
    ax1.plot(wind.flatten(), label="wind")
    ax1.plot(PV.flatten(), label="PV")
    ax1.legend()

    (
        load_house,
        load_farm,
        load_microgrid,
        load_industry2,
        load_trade,
        load_office,
    ) = load_data(
        temp=temp_profiles,
        path=os.path.join(
            os.pardir, os.pardir, "data", "load_profiles_fasit.csv"
        ),
    )

    fig2, ax2 = plt.subplots()
    ax2.plot(load_house.flatten(), label="house")
    ax2.plot(load_farm.flatten(), label="farm")
    ax2.plot(load_microgrid.flatten(), label="microgrid")
    ax2.plot(load_industry2.flatten(), label="industry")
    ax2.plot(load_trade.flatten(), label="trade")
    ax2.plot(load_office.flatten(), label="office")
    ax2.legend()

    fig3, ax3 = plt.subplots()
    ax3.plot(load_microgrid.flatten() * 40, label="load", zorder=3)
    ax3.plot(wind.flatten(), label="wind")
    ax3.plot(PV.flatten(), label="PV")
    ax3.legend()

    fig4, ax4 = plt.subplots()
    ax4.plot(load_house.flatten() * 400, label="load house", zorder=3)
    ax4.plot(load_farm.flatten() * 340, label="load farm", zorder=3)
    ax4.plot(load_industry2.flatten() * 5, label="load industry", zorder=3)
    ax4.plot(load_office.flatten() * 4, label="load office", zorder=3)
    ax4.plot(load_trade.flatten() * 7, label="load trade", zorder=3)

    ax4.legend()

    house = np.max(load_house) * 357  # * 300  # 400
    farm = np.max(load_farm) * 273  # * 250  # 340
    industry = np.max(load_industry2) * 8  # * 4  # 5
    office = np.max(load_office) * 3  # * 4
    trade = np.max(load_trade) * 2  # * 6  # 7
    print("Max load house:", house)
    print("Max load farm:", farm)
    print("Max load industry:", industry)
    print("Max load office:", office)
    print("Max load trade:", trade)
    print("Wind:", np.max(wind))
    print("PV:", np.max(PV))
    print("Sum:", np.sum(house + farm + industry + office + trade))
    print(sum(load_house))
    print(sum(load_farm))

    plt.show()
