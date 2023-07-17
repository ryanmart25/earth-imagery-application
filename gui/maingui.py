import PySimpleGUI as sg
from owslib.wms import WebMapService

import os

MAXREQUESTS = 3


def makeRequest(n, image_number, date):
    wms = WebMapService('https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi?', version='1.1.1')

    # Configure request for MODIS_Terra_CorrectedReflectance_TrueColor
    img = wms.getmap(layers=['MODIS_Terra_CorrectedReflectance_TrueColor'],  # Layers
                     srs='epsg:4326',  # Map projection
                     bbox=(-180, -90, 180, 90),  # Bounds
                     size=(1200, 600),  # Image size
                     time=date,  # Time of data

                     format='image/png',  # Image format
                     transparent=True)  # Nodata transparency
    if img is None:
        return 'FAILED'
    else:
        # make unique path
        image_path = f"C:\\Users\\User\\PycharmProjects\\Projects\\CoordinatesAPI\\Images" \
                     f"/MODIS_Terra_CorrectedReflectance_TrueColor.png"
        # Save output PNG to a file
        out = open(image_path, 'wb')
        out.write(img.read())
        out.close()
        return image_path


def main(image_number: int, date: str) -> str:
    path = makeRequest(MAXREQUESTS, image_number, date)
    return path

date_selector_column = [
    [
        sg.Text("Please Select the date you want to view: ", visible=True, key='-S TEXT-'),
        sg.InputText('YYYY-MM-DD', enable_events=True, size=(10, 1), visible=True, key='-DATE INPUT-'),
        sg.Button('Submit', key='-INPUT-')
    ],
    [
        sg.Text("-Product Selection-")
    ],
    [
        sg.Checkbox("Service: WMS | View: All | ")
    ]
]

image_view_column = [
    [
        sg.Image(key='-IMAGE-')
    ]
]

layout = [
    [
        sg.Column(date_selector_column),
        sg.VSeparator(),
        sg.Column(image_view_column)
    ]
]
window = sg.Window("Imagery", layout, size=(2000, 750), resizable=True)
image_number = 0
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event == '-INPUT-':
        image_number = +1
        window['-IMAGE-'].update(main(image_number, values['-DATE INPUT-']))
window.close()
