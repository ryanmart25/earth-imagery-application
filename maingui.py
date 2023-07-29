import sys
from typing import BinaryIO
from PySide6 import QtCore, QtWidgets, QtGui
from owslib.wms import WebMapService
from owslib.wmts import WebMapTileService
from PIL import Image
from io import BytesIO
import requests
from skimage import io

MAX_REQUESTS = 3


# Image Request
def makeWMSRequest(n, image_number, date) -> str:
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
        attempts = 0
        while attempts < 4:
            try:
                f: BinaryIO
                with open(image_path, 'wb') as f:
                    f.write(img.read())
                    f.close()
                    break
            except FileNotFoundError:
                attempts = attempts + 1
                print(f'|-> Attempted to Write image {attempts} time(s).')
                continue
        if attempts == 4:
            return 'Images/IMAGE_NOT_FOUND.png'
        return image_path


def makeWMTSRequest(time: str) -> str:
    try:
        params = {'LAYER': 'MODIS_Terra_CorrectedReflectance_TrueColor',
                  'STYLE': '',
                  'TIME': time,
                  'TILEMATRIXSET': '250m',
                  'TILEMATRIX': 4,
                  'TILEROW': 5,
                  'TILECOL': 6,
                  'FORMAT': 'image/jpeg'
                  }
        r = requests.get(
            "https://gibs.earthdata.nasa.gov/wmts/epsg4326/best/wmts.cgi?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&",
            params)

        if r.status_code != 200:
            return 'Images/IMAGE_NOT_FOUND.png'
        else:
            file_path = f"C:\\Users\\User\\PycharmProjects\\Projects\\CoordinatesAPI\\Images" \
                        f"/MODIS_Terra_CorrectedReflectance_TrueColor.jpg"
            attempts = 0
            while attempts < 4:
                try:
                    img = Image.open(BytesIO(r.content))
                    img.save(file_path)
                    break
                except FileNotFoundError:
                    attempts = attempts + 1
                    print(f"\\-> Attempted to write Image {attempts} time(s)\nTrying again...")
            if attempts > 4:
                return 'Images/IMAGE_NOT_FOUND.png'
            return file_path
    except AttributeError:
        return 'Images/IMAGE_NOT_FOUND.png'


def main(image_number: int, date: str, service: str) -> str:
    if service == 'WMS':
        path = makeWMSRequest(MAX_REQUESTS, image_number, date)
    elif service == 'WMTS':
        path = makeWMTSRequest(date)
    return path


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Initializing Widgets
        self.button = QtWidgets.QPushButton("Submit")
        self.text = QtWidgets.QLabel("Choose Date: ")
        self.date_input = QtWidgets.QTextEdit()
        self.date_input.setPlaceholderText('YYYY-MM-DD')
        self.date_input.setMaximumSize(100, 30)
        # Building Image Widget
        self.ImageLabel = QtWidgets.QLabel()
        self.image = QtGui.QPixmap('Student ID Picture.jpg')
        # self.image.fill('black')
        self.ImageLabel.setPixmap(self.image)
        self.service_label = QtWidgets.QLabel('Choose a service: ')
        self.service_one = QtWidgets.QCheckBox('WMS: Full Globe View')
        self.service_two = QtWidgets.QCheckBox('WMTS: Single Tile View')

        # List Widget containing all supported layers
        self.layer_label = QtWidgets.QListWidget()

        # Add items to List widget
        self.layer_label.addItem('Blue Marble')
        self.layer_label.addItem('')

        # Putting elements in left-side vertical box
        # self.left-frame = QtWidgets.QFrame(self.ImageLabel)

        # self.left-framelayout = QtWidgets.QVBoxLayout(self.left-frame)
        # self.left-frame.setLayout(self.left-framelayout)
        # self.left-frame.setLineWidth(1)
        # self.left-frame.setMidLineWidth(3)
        # self.left-frame.setFrameStyle(2)

        # Vertical box containing all elements
        self.layout = QtWidgets.QVBoxLayout(self)

        # Grid Layout  containing all product Widgets
        self.productWidgetsLayout = QtWidgets.QGridLayout()
        self.layout.addChildLayout(self.productWidgetsLayout)
        self.productWidgetsLayout.setColumnMinimumWidth(0, 125)

        # Add date label & input field to (0,0), (0,1) in Grid Layout
        self.productWidgetsLayout.addWidget(self.text, 0, 0)
        self.productWidgetsLayout.addWidget(self.date_input, 0, 1)

        # Add product selection (wms/wmts) label and check boxes to (1,0), (1,1) in Grid Layout
        self.productWidgetsLayout.addWidget(self.service_label, 1, 0)
        self.productWidgetsLayout.addWidget(self.service_one, 1, 1)
        # self.productWidgetsLayout.addWidget(self.service_two,1,1)
        self.productWidgetsLayout.addWidget(self.service_two,1,2)


        # Vertical box containing the

        self.layout.addWidget(self.text)
        self.layout.addWidget(self.date_input)

        self.layout.addSpacing(10)
        self.layout.addWidget(self.service_label)
        self.layout.addSpacing(5)
        self.layout.addWidget(self.service_one)
        self.layout.addWidget(self.service_two)
        self.layout.addSpacing(15)
        self.layout.addWidget(self.button)
        self.layout.addSpacing(20)
        self.layout.addWidget(self.ImageLabel)
        # Assigning method to handle button click action
        self.button.clicked.connect(self.magic)

    @QtCore.Slot()
    def magic(self):
        # Update the Image
        self.image = QtGui.QPixmap(
            main(0, self.date_input.toPlainText(), 'WMS' if self.service_one.isChecked() else 'WMTS'))
        self.ImageLabel.setPixmap(self.image)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    # widget.resize(800, 600)
    widget.showMaximized()
    widget.show()

    sys.exit(app.exec())
# Building GUI selector_column = [ [ sg.Text("How to Use:\nInput date into the field. Press submit. Farthest date is
# 2003-01-01. Specific Time is not supported with this endpoint.\nDo not use the check boxes, they don't do anything
# yet. ") ], [ sg.Text("Please Select the date you want to view: ", visible=True, key='-S TEXT-',
# background_color='black'), sg.InputText('YYYY-MM-DD', enable_events=True, size=(14, 1), visible=True, key='-DATE
# INPUT-', background_color='black', text_color='white'),
#
#    ],
#    [
#        sg.HorizontalSeparator()
#    ],
#    [
#        sg.Text("-Product Selection-", background_color='black')
#    ],
#    [
#        sg.Checkbox("Service: WMS | View: All |", background_color='black')
#    ],
#    [
#        sg.Checkbox("Service: WMTS | View: Single Tile |", background_color='black', enable_events=True, key='-WMTS '
#                                                                                                             'SINGLE '
#                                                                                                             'TILE-')
#    ],
#    [
#        sg.HorizontalSeparator()
#    ],
#    [
#        sg.Button('Submit', key='-INPUT-', button_color='black')
#    ],
#    [
#        sg.Text('ERROR: FUNCTIONALITY NOT SUPPORTED. PLEASE UNCHECK BOX', enable_events=True, key='-ERROR-',
#                visible=False)
#    ]
# ]
# -the following commented code will be used to beautify the appearance of the 'Image Column'- Desired Functionality:
# When the app is first rendered. Either display a 'Image Not Found' image OR Hide the 'Image Column' Until the
# requested image can be displayed. In this case, the 'Selection Column' should be fully expanded
#
#
# image_redundant_layout = [[sg.Image(key='-IMAGE-')]] -- creates a list holding only the Image Element to be
# supplied to the Frame Element
# image_view_column = [
#    [
#        sg.Image(key='-IMAGE-')  # For now, the image element will take up the entire 'Image Column'.
#        # Right Side will appear blank until the image is loaded
#        # sg.Frame("Image",image_redundant_layout)  -- Initialize the Frame Element
#    ]
# ]
#
# layout = [
#    [
#        sg.Column(selector_column, background_color='black'),
#        sg.VSeparator(),
#        sg.Column(image_view_column, background_color='black')
#    ]
# ]
# window = sg.Window("Imagery", layout, size=(2000, 750), resizable=True, background_color="black")
# In order to make the frame look less silly, use the -collapse- function trick.
# image_number = 0
# while True:
#    event, values = window.read()
#    if event == sg.WINDOW_CLOSED:
#        break
#
#    elif event == '-INPUT-':  # When the User submits their request
#        image_number = +1  # Image tag - to be used for letting the user view previous requested images.
#        if values['-WMTS SINGLE TILE-'] == True:
#            window['-ERROR-'].update(visible=True)
#        # window['-IMAGE-'].update(main(image_number, values['-DATE INPUT-'], 'TRUE'))
#
#        window['-IMAGE-'].update(
#            main(image_number, values['-DATE INPUT-'], values['-WMTS SINGLE TILE-']))  # Updating the mage element.
#        # 'main' will include a
#        # parameter 'service' (placeholder: h) to determine which endpoint and layer the User requested.
#        # This will be used in 'makeRequest' to make the request.
#
# window.close()
