from ursina import *
import json

with open('config.json', 'r') as file:
    config = json.load(file)

app_title = config.get('title')
app_fullscreen = config.get('fullscreen')
app_vsync = config.get('vsync')
app_icon = config.get('icon')

app_global = Ursina(title=app_title, fullscreen=app_fullscreen, vsync=app_vsync, icon=app_icon)
