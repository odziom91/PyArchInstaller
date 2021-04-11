###
###
###  PyArchInstaller
###  (c)2021 - created by OdzioM
###
###

import gettext
import os
import configparser
from PySimpleGUI import PySimpleGUI as sg


def pai_services():
    ans = True
    while ans:
        sg.SetOptions(font=("Monospace Regular", 12), margins=(0, 0))
        sg.theme("Dark")
        logo = [
            [sg.Image("./gfx/small_logo.png")]
        ]
        services = [
            [sg.Text("Wybierz usługi z listy poniżej: ", size=(35, 1))],
            [sg.Checkbox("Network Manager - zarządzanie połączeniami siecowymi", key="s_nm")],
            [sg.Checkbox("Usługa DHCP - dynamiczne przypisanie adresu IP", key="s_dhcp")],
            [sg.Checkbox("Wi-Fi - obsługa bezprzewodowego połączenia sieciowego", key="s_wifi")],
            [sg.Checkbox("PPPoE - obsługa połączeń sieciowych PPPoE (np.: ADSL/VDSL)", key="s_pppoe")],
            [sg.Checkbox("Mobile - obsługa połączeń przy pomocy sieci komórkowej", key="s_mobile")],
            [sg.Checkbox("Bluetooth - obsługa urządzeń Bluetooth", key="s_bt")],
            [sg.Checkbox("Usługa CUPS - serwer druku do obsługi drukarek", key="s_cups")],
            [sg.Checkbox("Multilib - repozytorium z pakietami 32-bitowymi", key="s_multilib")]
        ]
        save_settings = [
            [sg.Button("Zapisz ustawienia", size=(56, 1), pad=((4, 4), (0, 4)), key="btn_save")]
        ]
        gui = [
            [sg.Column(layout=logo)],
            [sg.Column(layout=services)],
            [sg.Column(layout=save_settings)]
        ]
        window = sg.Window("PyArchInstaller", gui, finalize=True, size=(600, 520), location=(100, 100))
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                ans = False
                break
            if event == "btn_save":
                try:
                    ans = False
                    if values["s_nm"]:
                        nm = "true"
                    else:
                        nm = "false"
                    if values["s_dhcp"]:
                        dhcp = "true"
                    else:
                        dhcp = "false"
                    if values["s_wifi"]:
                        wifi = "true"
                    else:
                        wifi = "false"
                    if values["s_pppoe"]:
                        pppoe = "true"
                    else:
                        pppoe = "false"
                    if values["s_mobile"]:
                        mobile = "true"
                    else:
                        mobile = "false"
                    if values["s_bt"]:
                        bt = "true"
                    else:
                        bt = "false"
                    if values["s_cups"]:
                        cups = "true"
                    else:
                        cups = "false"
                    if values["s_multilib"]:
                        multilib = "true"
                    else:
                        multilib = "false"
                    config = configparser.ConfigParser()
                    config.read("config/settings.cfg")
                    config.set('Services', 'nm', nm)
                    config.set('Services', 'dhcp', dhcp)
                    config.set('Services', 'wifi', wifi)
                    config.set('Services', 'pppoe', pppoe)
                    config.set('Services', 'mobile', mobile)
                    config.set('Services', 'bluetooth', bt)
                    config.set('Services', 'cups', cups)
                    config.set('Services', 'multilib', multilib)
                    config.set('Summary', 'Services', 'True')
                    with open('config/settings.cfg', 'w') as configfile:
                        config.write(configfile)
                except Exception as e:
                    print(str(e))
                break
        window.close()
