import PySimpleGUI as sg
from owslib.wms import WebMapService

import os

MAXREQUESTS = 3

# Image Request
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

# Building GUI
selector_column = [
    [
        sg.Text("Please Select the date you want to view: ", visible=True, key='-S TEXT-',background_color='black'),
        sg.InputText('YYYY-MM-DD', enable_events=True, size=(14, 1), visible=True, key='-DATE INPUT-',background_color='black', text_color='white'),

    ],
    [
      sg.HorizontalSeparator()
    ],
    [
        sg.Text("-Product Selection-",background_color='black')
    ],
    [
        sg.Checkbox("Service: WMS | View: All |",background_color='black')
    ],
    [
        sg.Checkbox("Service: WMS | View: Single Tile |",background_color='black')
    ],
    [
      sg.HorizontalSeparator()
    ],
    [
        sg.Button('Submit', key='-INPUT-', button_color='black')
    ]
]
# -the following commented code will be used to beautify the appearance of the 'Image Column'- Desired Functionality:
# When the app is first rendered. Either display a 'Image Not Found' image OR Hide the 'Image Column' Until the
# requested image can be displayed. In this case, the 'Selection Column' should be fully expanded


# image_redundant_layout = [[sg.Image(key='-IMAGE-')]] -- creates a list holding only the Image Element to be
# supplied to the Frame Element
image_view_column = [
    [
        sg.Image(key='-IMAGE-')  # For now, the image element will take up the entire 'Image Column'.
        # Right Side will appear blank until the image is loaded
        # sg.Frame("Image",image_redundant_layout)  -- Initialize the Frame Element
    ]
]

layout = [
    [
        sg.Column(selector_column, background_color='black'),
        sg.VSeparator(),
        sg.Column(image_view_column,background_color='black')
    ]
]
window = sg.Window("Imagery", layout, size=(2000, 750), resizable=True, background_color="black")
# In order to make the frame look less silly, use the -collapse- function trick.
image_number = 0
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event == '-INPUT-':
        image_number = +1
        window['-IMAGE-'].update(main(image_number, values['-DATE INPUT-']))
window.close()
