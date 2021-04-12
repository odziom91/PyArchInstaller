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


def pai_video(lang):
    localedir = './locale'
    translate = gettext.translation('video', localedir, languages=[lang], fallback=True)
    translate.install()
    _ = translate.gettext
    ans = True
    while ans:
        sg.SetOptions(font=("Monospace Regular", 12), margins=(0, 0))
        sg.theme("Dark")
        logo = [
            [sg.Image("./gfx/small_logo.png")]
        ]
        video = [
            [sg.Text(_("Choose video driver: "), size=(35, 1))],
            [sg.Radio(_("NVidia with DKMS"), group_id=1, key="v_nvdkms", size=(45, 1), enable_events=True)],
            [sg.Radio(_("NVidia without DKMS"), group_id=1, key="v_nvnodkms", size=(45, 1), enable_events=True)],
            [sg.Radio(_("NVidia - Nouveau"), group_id=1, key="v_nvnouveau", size=(45, 1), enable_events=True)],
            [sg.Radio(_("AMD"), group_id=1, key="v_amd", size=(15, 1), enable_events=True)],
            [sg.Radio(_("Intel"), group_id=1, key="v_intel", size=(15, 1), enable_events=True)],
            [sg.Radio(_("VirtualBox"), group_id=1, key="v_vbox", size=(15, 1), enable_events=True)],
        ]
        save_settings = [
            [sg.Button(_("Save settings"), size=(56, 1), pad=((4, 4), (0, 4)), key="btn_save")]
        ]
        gui = [
            [sg.Column(layout=logo)],
            [sg.Column(layout=video)],
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
                    if values["v_nvdkms"]:
                        set_video = "nvdkms"
                    if values["v_nvnodkms"]:
                        set_video = "nvnodkms"
                    if values["v_nvnouveau"]:
                        set_video = "nouveau"
                    if values["v_amd"]:
                        set_video = "amd"
                    if values["v_intel"]:
                        set_video = "intel"
                    if values["v_vbox"]:
                        set_video = "vbox"
                    config = configparser.ConfigParser()
                    config.read("config/settings.cfg")
                    config.set('Video', 'driver', set_video)
                    config.set('Summary', 'Video', 'True')
                    with open('config/settings.cfg', 'w') as configfile:
                        config.write(configfile)
                except Exception as e:
                    print(str(e))
                break
        window.close()
