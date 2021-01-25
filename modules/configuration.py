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


def pai_config():
    sys_lang = open("./lists/locale.gen", "r").read().split("\n")
    kbd_lang = open("./lists/kbd.gen", "r").read().split("\n")
    tz_opt = open("./lists/tz.gen", "r").read().split("\n")
    ans = True
    while ans:
        sg.SetOptions(font=("Liberation Sans", 12), margins=(0, 0))
        sg.theme("Dark")
        logo = [
            [sg.Image("./gfx/small_logo.png")]
        ]
        configs = [
            [sg.Text("Nazwa komputera: ", size=(24, 1)), sg.InputText("", enable_events=True, key="hostname", size=(32, 1))],
            [sg.Text("Język systemu: ", size=(24, 1)), sg.Combo(values=sys_lang, enable_events=True, key="sys", size=(30, 1))],
            [sg.Text("Język klawiatury: ", size=(24, 1)), sg.Combo(values=kbd_lang, enable_events=True, key="kbd", size=(30, 1))],
            [sg.Text("Strefa czasowa: ", size=(24, 1)), sg.Combo(values=tz_opt, enable_events=True, key="tz", size=(30, 1))]
        ]
        kernel = [
            [sg.Text("Wybierz kernel systemu: ", size=(24, 1))],
            [
                sg.Radio("Stable", group_id=1, key="k_stable", size=(6, 1), enable_events=True), 
                sg.Radio("Longterm", group_id=1, key="k_longterm", size=(8, 1), enable_events=True),
                sg.Radio("Zen", group_id=1, key="k_zen", size=(3, 1), enable_events=True),
                sg.Radio("Hardened", group_id=1, key="k_hardened", size=(8, 1), enable_events=True)
            ],
            [sg.Text("Opis kerneli: ", size=(55, 1))],
            [sg.Text("Stable - domyślny kernel Arch Linux", size=(55, 1))],
            [sg.Text("Longterm - kernel z wydłużonym wsparciem - LTS", size=(55, 1))],
            [sg.Text("Zen - kernel z wbudowanym wsparciem dla fsync", size=(55, 1))],
            [sg.Text("Hardened - kernel skierowany na bezpieczeństwo systemu", size=(55, 1))]
        ]
        save_settings = [
            [sg.Button("Zapisz ustawienia", size=(55, 1), pad=((4, 4), (0, 4)), key="btn_save")]
        ]
        gui = [
            [sg.Column(layout=logo)],
            [sg.Column(layout=configs)],
            [sg.Column(layout=kernel)],
            [sg.Column(layout=save_settings)]
        ]
        window = sg.Window("PyArchInstaller", gui, finalize=True, size=(450, 500))
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                ans = False
                break
            if event == "btn_save":
                try:
                    ans = False
                    config = configparser.ConfigParser()
                    if values["k_stable"]:
                        kernel = "stable"
                    if values["k_longterm"]:
                        kernel = "longterm"
                    if values["k_zen"]:
                        kernel = "zen"
                    if values["k_hardened"]:
                        kernel = "hardened"
                    config['General'] = {
                        'hostname': values["hostname"],
                        'lang': values["sys"],
                        'kbd': values["kbd"],
                        'tz': values["tz"],
                        'kernel': kernel
                        }
                    with open('config/config.cfg', 'w') as configfile:
                        config.write(configfile)
                except Exception as e:
                    print(str(e))
                break
        window.close()
