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


def pai_video():
    ans = True
    while ans:
        sg.SetOptions(font=("Liberation Sans", 12), margins=(0, 0))
        sg.theme("Dark")
        logo = [
            [sg.Image("./gfx/small_logo.png")]
        ]
        video = [
            [sg.Text("Wybierz sterownik dla karty graficznej: ", size=(35, 1))],
            [sg.Radio("NVidia - sterownik z obsługą DKMS", group_id=1, key="v_nvdkms", size=(45, 1), enable_events=True)],
            [sg.Radio("NVidia - sterownik bez obsługi DKMS", group_id=1, key="v_nvnodkms", size=(45, 1), enable_events=True)],
            [sg.Radio("NVidia - sterownik Nouveau", group_id=1, key="v_nvnouveau", size=(45, 1), enable_events=True)],
            [sg.Radio("AMD", group_id=1, key="v_amd", size=(15, 1), enable_events=True)],
            [sg.Radio("Intel", group_id=1, key="v_intel", size=(15, 1), enable_events=True)],
            [sg.Radio("VirtualBox", group_id=1, key="v_vbox", size=(15, 1), enable_events=True)],
        ]
        save_settings = [
            [sg.Button("Zapisz ustawienia", size=(55, 1), pad=((4, 4), (0, 4)), key="btn_save")]
        ]
        gui = [
            [sg.Column(layout=logo)],
            [sg.Column(layout=video)],
            [sg.Column(layout=save_settings)]
        ]
        window = sg.Window("PyArchInstaller", gui, finalize=True, size=(450, 420))
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                ans = False
                break
            if event == "btn_save":
                try:
                    ans = False
                    config = configparser.ConfigParser()
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
                    config['Video'] = {
                        'driver': set_video
                        }
                    with open('config/video.cfg', 'w') as configfile:
                        config.write(configfile)
                except Exception as e:
                    print(str(e))
                break
        window.close()