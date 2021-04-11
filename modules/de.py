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
        sg.SetOptions(font=("Monospace Regular", 12), margins=(0, 0))
        sg.theme("Dark")
        logo = [
            [sg.Image("./gfx/small_logo.png")]
        ]
        de = [
            [sg.Text("Wybierz środowisko graficzne: ", size=(35, 1))],
            [
                sg.Text("Gnome: ", size=(12, 1)), 
                sg.Radio("Minimal", group_id=1, key="de_gnome_minimal", size=(10, 1), enable_events=True), 
                sg.Radio("Full", group_id=1, key="de_gnome", size=(10, 1), enable_events=True)
            ],
            [
                sg.Text("KDE Plasma: ", size=(12, 1)), 
                sg.Radio("Minimal", group_id=1, key="de_plasma_minimal", size=(10, 1), enable_events=True), 
                sg.Radio("Full", group_id=1, key="de_plasma", size=(10, 1), enable_events=True)
            ],
            [
                sg.Text("XFCE: ", size=(12, 1)),
                sg.Radio("Minimal", group_id=1, key="de_xfce_minimal", size=(10, 1), enable_events=True), 
                sg.Radio("Full", group_id=1, key="de_xfce", size=(10, 1), enable_events=True)
            ],
            [
                sg.Text("Mate: ", size=(12, 1)),
                sg.Radio("Minimal", group_id=1, key="de_mate_minimal", size=(10, 1), enable_events=True), 
                sg.Radio("Full", group_id=1, key="de_mate", size=(10, 1), enable_events=True)
            ],
            [
                sg.Text("Cinnamon: ", size=(12, 1)), 
                sg.Radio("Full", group_id=1, key="de_cinnamon", size=(10, 1), enable_events=True)
            ]
        ]
        lm = [
            [sg.Text("Wybierz menedżer logowania: ", size=(35, 1))],
            [sg.Radio("LightDM", group_id=2, key="lm_lightdm", size=(15, 1), enable_events=True)],
            [sg.Radio("GDM", group_id=2, key="lm_gdm", size=(15, 1), enable_events=True)],
            [sg.Radio("SDDM", group_id=2, key="lm_sddm", size=(15, 1), enable_events=True)]
        ]
        save_settings = [
            [sg.Button("Zapisz ustawienia", size=(56, 1), pad=((4, 4), (0, 4)), key="btn_save")]
        ]
        gui = [
            [sg.Column(layout=logo)],
            [sg.Column(layout=de)],
            [sg.Column(layout=lm)],
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
                    if values["de_gnome"]:
                        set_de = "gnome"
                    if values["de_gnome_minimal"]:
                        set_de = "gnome_minimal"
                    if values["de_plasma"]:
                        set_de = "plasma"
                    if values["de_plasma_minimal"]:
                        set_de = "plasma_minimal"
                    if values["de_xfce"]:
                        set_de = "xfce"
                    if values["de_xfce_minimal"]:
                        set_de = "xfce_minimal"
                    if values["de_mate"]:
                        set_de = "mate"
                    if values["de_mate_minimal"]:
                        set_de = "mate_minimal"
                    if values["de_cinnamon"]:
                        set_de = "cinnamon"
                    if values["lm_lightdm"]:
                        set_lm = "lightdm"
                    if values["lm_gdm"]:
                        set_lm = "gdm"
                    if values["lm_sddm"]:
                        set_lm = "sddm"
                    config = configparser.ConfigParser()
                    config.read("config/settings.cfg")
                    config.set('Desktop', 'de', set_de)
                    config.set('Desktop', 'lm', set_lm)
                    config.set('Summary', 'Desktop', 'True')
                    with open('config/settings.cfg', 'w') as configfile:
                        config.write(configfile)
                except Exception as e:
                    print(str(e))
                break
        window.close()
