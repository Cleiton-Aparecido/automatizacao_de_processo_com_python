import PySimpleGUI as sg
import time

sg.theme('Dark')
# layout = [
#             sg.PopupAnimated('Ajux_loader.gif')
#          ]
# window = sg.Window('To Do List Example', layout)
# event, values = window.read()

for i in range(100000):
    sg.PopupAnimated(sg.DEFAULT_BASE64_LOADING_GIF,background_color='white', time_between_frames=100)

sg.PopupAnimated(None)  

sg.PopupAnimated(None).close()