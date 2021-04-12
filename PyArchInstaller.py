###
###
###  PyArchInstaller
###  (c)2021 - created by OdzioM
###
###

import gettext
import os
import configparser
import subprocess
from PySimpleGUI import PySimpleGUI as sg

from modules.configuration import pai_config
from modules.de import pai_de
from modules.partitioning import pai_partitioning
from modules.video import pai_video
from modules.services import pai_services
from modules.installation import pai_install_wnd
from modules.users import pai_users

# required packages:
# tk
# PySimpleGui
# gparted

# do poprawki
# autologowanie w samym ISO (bez wpisywania konta root)
#

def pai_language():
    languages = [
        "English",
        "Polski"
    ]
    ans = True
    while ans:
        sg.SetOptions(font=("Monospace Regular", 12), margins=(0, 0))
        sg.theme("Dark")
        choose_lang = [
            [sg.Text("Choose language")],
            [sg.Combo(values=languages, enable_events=True, key="chlang", size=(15, 1))],
            [sg.Button("OK", size=(15, 1), pad=((4, 4), (0, 4)), key="btn_save")]
        ]
        gui = [
            [sg.Column(layout=choose_lang)]
        ]
        window = sg.Window("PyArchInstaller", gui, finalize=True, size=(200, 100), location=(100, 100))
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == "btn_exit":
                ans = False
                break
            if event == "btn_save":
                ans = False
                window.close()
                if values["chlang"] == "English":
                    pai_main("en")
                if values["chlang"] == "Polski":
                    pai_main("pl")
        window.close()

def pai_main(lang):
    localedir = './locale'
    translate = gettext.translation('pai', localedir, languages=[lang], fallback=True)
    translate.install()
    _ = translate.gettext
    config = configparser.ConfigParser()
    if os.path.exists("config/settings.cfg"):
        pass
    else:
        config['General'] = {
                'hostname': '',
                'lang': '',
                'kbd': '',
                'tz': '',
                'kernel': ''
                }
        config['Desktop'] = {
                'de': '',
                'lm': ''
                }
        config['Grub'] = {
                'grub': ''
                }
        config['Services'] = {
                'nm': '',
                'dhcp': '',
                'wifi': '',
                'pppoe': '',
                'mobile': '',
                'bluetooth': '',
                'cups': '',
                'multilib': ''
                }
        config['Video'] = {
                'driver': ''
                }
        config['Summary'] = {
                'General': 'False',
                'Desktop': 'False',
                'Grub': 'False',
                'Services': 'False',
                'Video': 'False',
                'Installation': 'False'
                }
        with open('config/settings.cfg', 'w') as configfile:
            config.write(configfile)
    ans = True
    while ans:
        sg.SetOptions(font=("Monospace Regular", 12), margins=(0, 0))
        sg.theme("Dark")
        logo = [
            [sg.Image("./gfx/logo.png",)]
        ]
        sections = [
            [sg.Button(_("Basic configuration"), size=(56, 1), pad=((4, 4), (0, 4)), key="btn_config", button_color=("white", "brown"))],
            [sg.Button(_("System services"), size=(56, 1), pad=((4, 4), (0, 4)), key="btn_services", button_color=("white", "brown"))],
            [sg.Button(_("Desktop environment"), size=(56, 1), pad=((4, 4), (0, 4)), key="btn_de", button_color=("white", "brown"))],
            [sg.Button(_("Video drivers"), size=(56, 1), pad=((4, 4), (0, 4)), key="btn_video", button_color=("white", "brown"))],
            [sg.Button(_("Partitioning"), size=(56, 1), pad=((4, 4), (0, 4)), key="btn_partitioning", button_color=("white", "brown"))],
            [sg.Button(_("Install Arch Linux"), size=(56, 1), pad=((4, 4), (0, 4)), key="btn_install", button_color=("white", "brown"), disabled=True)],
            [sg.Button(_("Users management"), size=(56, 1), pad=((4, 4), (0, 4)), key="btn_users", button_color=("white", "brown"), disabled=True)],
            [sg.Button(_("Exit installer"), size=(56, 1), pad=((4, 4), (0, 4)), key="btn_exit", button_color=("white", "black"))],
        ]
        gui = [
            [sg.Column(layout=logo)],
            [sg.Column(layout=sections)]
        ]
        # język systemu - done
        # język klawiatury - done
        # aktualizacja pacmana i serwerów lustrzanych - przy instalacji systemu
        # ustawienia regionalne - done ? :)
        # strefa czasowa - done
        # partycjonowanie (gparted!) - może być
        # instalowanie pakietów: base + devel, kernel, powłoka (bash), bootloader (grub), network mananger lub netctl, multilib,
        #                        dhcp, obsługa wifi, os-prober (multiboot), pulpit/menedżer okien + extra pakiety, instalacja karty graficznej,
        #                        panel dotykowy, menedżer logowania
        # hostname - done
        # root - encypt password  (encrypt passwd) - do opracowania
        # userzy + nadawanie uprawnień admina - do opracowania
        # dodatkowe oprogramowanie 
        # instalacja systemu
        # usługi systemowe - done
        window = sg.Window("PyArchInstaller", gui, finalize=True, size=(600, 520), location=(100, 100))
        config = configparser.ConfigParser()
        while True:
            config.read("./config/settings.cfg")
            cs_general = config["Summary"]["General"]
            cs_desktop = config["Summary"]["Desktop"]
            cs_video = config["Summary"]["Video"]
            cs_partitioning = config["Summary"]["Grub"]
            cs_services = config["Summary"]["Services"]
            cs_installation = config["Summary"]["Installation"]
            if cs_general == "True":
                window.Element("btn_config").update(button_color= ("white", "green"))
            if cs_services == "True":
                window.Element("btn_services").update(button_color=("white", "green"))
            if cs_desktop == "True":
                window.Element("btn_de").update(button_color=("white", "green"))
            if cs_partitioning == "True":
                window.Element("btn_partitioning").update(button_color=("white", "green"))
            if cs_video == "True":
                window.Element("btn_video").update(button_color=("white", "green"))
            if cs_general == "True" and cs_services == "True" and cs_desktop == "True" and cs_partitioning == "True" and cs_video == "True":
                window.Element("btn_install").update(button_color=("white", "green"), disabled=False)
            if cs_installation == "True":
                window.Element("btn_users").update(button_color=("white", "green"), disabled=False)
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == "btn_exit":
                ans = False
                break
            if event == "btn_config":
                ans = True
                pai_config(lang)
                break
            if event == "btn_de":
                ans = True
                pai_de(lang)
                break
            if event == "btn_partitioning":
                ans = True
                pai_partitioning(lang)
                break
            if event == "btn_video":
                ans = True
                pai_video(lang)
                break
            if event == "btn_services":
                ans = True
                pai_services(lang)
                break
            if event == "btn_users":
                ans = True
                pai_users(lang)
                break
            if event == "btn_install":
                ans = True
                pai_install_wnd(lang)
                break
        window.close()


if __name__ == '__main__':
    if os.path.exists("output/"):
        pass
    else:
        os.mkdir("output/")
    pai_language()
