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


def pai_config(lang):
    localedir = './locale'
    translate = gettext.translation('config', localedir, languages=[lang], fallback=True)
    translate.install()
    _ = translate.gettext
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
            [sg.Text(_("Hostname:"), size=(20, 1)), sg.InputText("", enable_events=True, key="hostname", size=(37, 1))],
            [sg.Text(_("System language:"), size=(20, 1)), sg.Combo(values=sys_lang, enable_events=True, key="sys", size=(36, 1))],
            [sg.Text(_("Keyboard layout:"), size=(20, 1)), sg.Combo(values=kbd_lang, enable_events=True, key="kbd", size=(36, 1))],
            [sg.Text(_("Time zone:"), size=(20, 1)), sg.Combo(values=tz_opt, enable_events=True, key="tz", size=(36, 1))]
        ]
        kernel = [
            [sg.Text(_("Choose kernel:"), size=(24, 1))],
            [sg.Radio(_("Vanilla - default"), group_id=1, key="k_stable", size=(56, 1), enable_events=True)],
            [sg.Radio(_("Longterm - Long Time Support"), group_id=1, key="k_longterm", size=(56, 1), enable_events=True)],
            [sg.Radio(_("Zen - fsync and futex2 support"), group_id=1, key="k_zen", size=(56, 1), enable_events=True)],
            [sg.Radio(_("Hardened - system security"), group_id=1, key="k_hardened", size=(56, 1), enable_events=True)],
            [sg.Text(_("Attention!\nIf you do not know which kernel you should use - choose Vanilla."), size=(56, 3))]
        ]
        save_settings = [
            [sg.Button(_("Save settings"), size=(56, 1), pad=((4, 4), (0, 4)), key="btn_save")]
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
