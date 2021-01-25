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


def pai_de():
    ans = True
    while ans:
        sg.SetOptions(font=("Liberation Sans", 12), margins=(0, 0))
        sg.theme("Dark")
        logo = [
            [sg.Image("./gfx/small_logo.png")]
        ]
        de = [
            [sg.Text("Wybierz środowisko graficzne: ", size=(35, 1))],
            [sg.Radio("Gnome", group_id=1, key="de_gnome", size=(15, 1), enable_events=True)],
            [sg.Radio("KDE Plasma", group_id=1, key="de_plasma", size=(15, 1), enable_events=True)],
            [sg.Radio("XFCE", group_id=1, key="de_xfce", size=(15, 1), enable_events=True)],
            [sg.Radio("Mate", group_id=1, key="de_mate", size=(15, 1), enable_events=True)],
            [sg.Radio("Cinnamon", group_id=1, key="de_cinnamon", size=(15, 1), enable_events=True)]
        ]
        lm = [
            [sg.Text("Wybierz menedżer logowania: ", size=(35, 1))],
            [sg.Radio("LightDM", group_id=2, key="lm_lightdm", size=(15, 1), enable_events=True)],
            [sg.Radio("GDM", group_id=2, key="lm_gdm", size=(15, 1), enable_events=True)]
        ]
        save_settings = [
            [sg.Button("Zapisz ustawienia", size=(55, 1), pad=((4, 4), (0, 4)), key="btn_save")]
        ]
        gui = [
            [sg.Column(layout=logo)],
            [sg.Column(layout=de)],
            [sg.Column(layout=lm)],
            [sg.Column(layout=save_settings)]
        ]
        window = sg.Window("PyArchInstaller", gui, finalize=True, size=(450, 450))
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                ans = False
                break
            if event == "btn_save":
                try:
                    ans = False
                    config = configparser.ConfigParser()
                    if values["de_gnome"]:
                        set_de = "gnome"
                    if values["de_plasma"]:
                        set_de = "plasma"
                    if values["de_xfce"]:
                        set_de = "xfce"
                    if values["de_mate"]:
                        set_de = "mate"
                    if values["de_cinnamon"]:
                        set_de = "cinnamon"
                    if values["lm_lightdm"]:
                        set_lm = "lightdm"
                    if values["lm_gdm"]:
                        set_lm = "gdm"   
                    config['Desktop Environment'] = {
                        'de': set_de,
                        'lm': set_lm,
                        }
                    with open('config/de.cfg', 'w') as configfile:
                        config.write(configfile)
                except Exception as e:
                    print(str(e))
                break
        window.close()
