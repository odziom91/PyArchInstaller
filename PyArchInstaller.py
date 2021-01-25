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
from modules.installation import pai_install
from modules.users import pai_users

# required packages:
# tk
# PySimpleGui
# gparted

# do poprawki
# autologowanie w samym ISO (bez wpisywania konta root)
#

def pai_main():
    ans = True
    while ans:
        if int(subprocess.check_output("ls /sys/firmware/efi/efivars | wc -l", shell=True)) > 1:
            efi = True
        else:
            efi = False
        sg.SetOptions(font=("Liberation Sans", 12), margins=(0, 0))
        sg.theme("Dark")
        logo = [
            [sg.Image("./gfx/logo.png")]
        ]
        sections = [
            [sg.Button("Podstawowa konfiguracja", size=(50, 1), pad=((4, 4), (0, 4)), key="btn_config")],
            [sg.Button("Usługi systemowe", size=(50, 1), pad=((4, 4), (0, 4)), key="btn_services")],
            [sg.Button("Środowisko graficzne", size=(50, 1), pad=((4, 4), (0, 4)), key="btn_de")],
            [sg.Button("Sterownik karty graficznej", size=(50, 1), pad=((4, 4), (0, 4)), key="btn_video")],
            [sg.Button("Partycjonowanie dysku", size=(50, 1), pad=((4, 4), (0, 4)), key="btn_partitioning")],
            [sg.Button("Zainstaluj", size=(50, 1), pad=((4, 4), (0, 4)), key="btn_install")],
            [sg.Button("Zarządzanie użytkownikami", size=(50, 1), pad=((4, 4), (0, 4)), key="btn_users")],
            [sg.Button("Opuść instalator", size=(50, 1), pad=((4, 4), (0, 4)), key="btn_exit")],
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
        window = sg.Window("PyArchInstaller", gui, finalize=True, size=(340, 520))
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == "btn_exit":
                ans = False
                break
            if event == "btn_config":
                ans = False
                pai_config()
            if event == "btn_de":
                ans = False
                pai_de()
            if event == "btn_partitioning":
                ans = False
                pai_partitioning(efi)
            if event == "btn_video":
                ans = False
                pai_video()
            if event == "btn_services":
                ans = False
                pai_services()
            if event == "btn_install":
                ans = False
                pai_install(efi)
            if event == "btn_users":
                ans = False
                pai_users()
        window.close()


if __name__ == '__main__':
    if os.path.exists("output/"):
        pass
    else:
        os.mkdir("output/")
    pai_main()
