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
        sg.SetOptions(font=("Monospace Regular", 12), margins=(0, 0))
        sg.theme("Dark")
        logo = [
            [sg.Image("./gfx/small_logo.png")]
        ]
        configs = [
            [sg.Text("Nazwa komputera: ", size=(20, 1)), sg.InputText("", enable_events=True, key="hostname", size=(37, 1))],
            [sg.Text("Język systemu: ", size=(20, 1)), sg.Combo(values=sys_lang, enable_events=True, key="sys", size=(36, 1))],
            [sg.Text("Język klawiatury: ", size=(20, 1)), sg.Combo(values=kbd_lang, enable_events=True, key="kbd", size=(36, 1))],
            [sg.Text("Strefa czasowa: ", size=(20, 1)), sg.Combo(values=tz_opt, enable_events=True, key="tz", size=(36, 1))]
        ]
        kernel = [
            [sg.Text("Wybierz kernel systemu: ", size=(24, 1))],
            [sg.Radio("Stable - domyślny, stabilny kernel", group_id=1, key="k_stable", size=(56, 1), enable_events=True)],
            [sg.Radio("Longterm - kernel z wydłużonym wsparciem", group_id=1, key="k_longterm", size=(56, 1), enable_events=True)],
            [sg.Radio("Zen - kernel ze wsparciem fsync i futex2", group_id=1, key="k_zen", size=(56, 1), enable_events=True)],
            [sg.Radio("Hardened - kernel skierowany na bezpieczeństwo systemu", group_id=1, key="k_hardened", size=(56, 1), enable_events=True)],
            [sg.Text("Ważne!\nJeśli nie jesteś pewien, który kernel wybrać - wybierz Stable. ", size=(56, 3))]
        ]
        save_settings = [
            [sg.Button("Zapisz ustawienia", size=(56, 1), pad=((4, 4), (0, 4)), key="btn_save")]
        ]
        gui = [
            [sg.Column(layout=logo)],
            [sg.Column(layout=configs)],
            [sg.Column(layout=kernel)],
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
                    if values["k_stable"]:
                        kernel = "stable"
                    if values["k_longterm"]:
                        kernel = "longterm"
                    if values["k_zen"]:
                        kernel = "zen"
                    if values["k_hardened"]:
                        kernel = "hardened"
                    config = configparser.ConfigParser()
                    config.read("config/settings.cfg")
                    config.set('General', 'hostname', values['hostname'])
                    config.set('General', 'lang', values['sys'])
                    config.set('General', 'kbd', values['kbd'])
                    config.set('General', 'tz', values['tz'])
                    config.set('General', 'kernel', kernel)
                    config.set('Summary', 'General', 'True')
                    with open('config/settings.cfg', 'w') as configfile:
                        config.write(configfile)
                except Exception as e:
                    print(str(e))
                break
        window.close()
