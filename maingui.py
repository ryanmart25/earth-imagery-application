import sys
from typing import BinaryIO
from PySide6 import QtCore, QtWidgets, QtGui
from owslib.wms import WebMapService
from owslib.wmts import WebMapTileService
from PIL import Image
from io import BytesIO
import requests
from skimage import io
from PySide6.QtWidgets import QAbstractItemView

# TODO Add Functionality: Allow user to choose location on WMS and WMTS services
# TODO Implement Exception checking and exposure
# TODO implement ability to choose location
MAX_REQUESTS = 3
VALID_LAYERS = [
    'MODIS_Terra_CorrectedReflectance_TrueColor',
    'BlueMarble_ShadedRelief_Bathymetry'
]


# TODO Implement Blue Marble Layer

# Image Request
def makeWMSRequest(n, image_number: int, date: str, layers: list) -> tuple:
    wms = WebMapService('https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi?', version='1.1.1')

    # < westBoundLongitude > -180 < / westBoundLongitude >
    # < eastBoundLongitude > 180 < / eastBoundLongitude >
    # < southBoundLatitude > -90 < / southBoundLatitude >
    # < northBoundLatitude > 90 < / northBoundLatitude >
    # EXAMPLES
    # -100, 180
    # -90,90

    # Configure request for MODIS_Terra_CorrectedReflectance_TrueColor
    img = wms.getmap(layers=layers,  # Layers
                     srs='epsg:4326',  # Map projection
                     bbox=(-180, -90, 180, 90),  # Bounds
                     size=(1200, 600),  # Image size
                     time=date,  # Time of data
                     format='image/png',  # Image format
                     transparent=True)  # Nodata transparency
    if img is None:
        return 'FAILED', 'UNKNOWN FAILURE.\nPossible occurrence: line 29 in makeWMSRequest()'
    else:
        # make unique path
        image_path = f"C:/Users/User/PycharmProjects/Projects/CoordinatesAPI/Images" \
                     f"/MODIS_Terra_CorrectedReflectance_TrueColor-{image_number}.png"
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
                continue
        if attempts == 4:
            return 'Images/IMAGE_NOT_FOUND.png', 'COULD NOT WRITE IMAGE'
        return image_path, 'OK'


def makeWMTSRequest(imagecount: int,time: str, layer: str) -> tuple:
    tilematrixset = '250m'
    if layer == 'BlueMarble_ShadedRelief_Bathymetry':
        tilematrixset = '500m'
    try:
        params = {'LAYER': layer,
                  'STYLE': '',
                  'TIME': time,
                  'TILEMATRIXSET': tilematrixset,
                  'TILEMATRIX': 4,
                  'TILEROW': 5,
                  'TILECOL': 6,
                  'FORMAT': 'image/jpeg'
                  }
        r = requests.get(
            "https://gibs.earthdata.nasa.gov/wmts/epsg4326/best/wmts.cgi?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&",
            params)

        if r.status_code != 200:
            return 'Images/IMAGE_NOT_FOUND.png', r.status_code,
        else:
            file_path = f"C:/Users/User/PycharmProjects/Projects/CoordinatesAPI/Images" \
                        f"/MODIS_Terra_CorrectedReflectance_TrueColor-{imagecount}.jpg"
            if layer == 'BlueMarble_ShadedRelief_Bathymetry':
                file_path = f"C:/Users/User/PycharmProjects/Projects/CoordinatesAPI/Images" \
                        f"/BlueMarble_ShadedRelief_Bathymetry-{imagecount}.jpg"

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
                return 'Images/IMAGE_NOT_FOUND.png', 'CRITICAL FAILURE: FILE COULD NOT BE SAVED'
            return file_path, 'OK'
    except AttributeError:
        return 'Images/IMAGE_NOT_FOUND.png', 'CRITICAL FAILURE: AttributeError'


def main(image_number: int, date: str, service: str, layers: list) -> tuple:  # _image_number_ will eventually be used
    # to differentiate previously requested
    # images.
    for layer in layers:
        if layer not in VALID_LAYERS:
            layers.remove(layer)
    if service == 'WMS':
        response = makeWMSRequest(MAX_REQUESTS, image_number, date, layers)
    elif service == 'WMTS':
        response = makeWMTSRequest(date, layers[0])  # WMTS only allows 1 layer to be used ata time
        # TODO On WMTS selection, change ListWidget to only allow One selection at a time.
    else:  # default to using the WMS service
        response = makeWMSRequest(MAX_REQUESTS, image_number, date, layers)
    return response


class MyWidget(QtWidgets.QWidget):
    # TODO Add Functionality: On WMTS service check, disable multiple selection on Layer Widget
    def __init__(self):
        super().__init__()
        self.requestcount = 0

        # Initializing Widgets
        self.status_label = QtWidgets.QLabel('Status')
        self.status_label.hide()
        self.button = QtWidgets.QPushButton("Submit")
        self.text = QtWidgets.QLabel("Choose Date: ")
        self.date_input = QtWidgets.QTextEdit()
        self.date_input.setPlaceholderText('YYYY-MM-DD')
        self.date_input.setMaximumSize(100, 30)
        # Building Image Widget
        self.ImageLabel = QtWidgets.QLabel()
        self.image = QtGui.QPixmap('Student ID Picture.jpg')
        # self.image.fill('black')  # TODO change default image to black screen
        self.ImageLabel.setPixmap(self.image)
        self.service_label = QtWidgets.QLabel('Choose a service: ')
        self.service_one = QtWidgets.QCheckBox('WMS: Full Globe View')
        self.service_two = QtWidgets.QCheckBox('WMTS: Single Tile View')

        # Label for List Widget
        self.list_label = QtWidgets.QLabel('Choose Layer(s):')
        # List Widget containing all supported layers
        self.layer_list_widget = QtWidgets.QListWidget()
        self.layer_list_widget.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        # Add items to List widget
        self.layer_list_widget.addItem('BlueMarble_ShadedRelief_Bathymetry')
        self.layer_list_widget.addItem('MODIS_Terra_CorrectedReflectance_TrueColor')

        # --Vertical box containing all elements--
        self.layout = QtWidgets.QVBoxLayout(self)

        # Grid Layout  containing all product Widgets
        self.productWidgetsLayout = QtWidgets.QGridLayout()
        self.layout.addLayout(self.productWidgetsLayout)

        # Resize columns for aesthetic purposes
        #   The heights of columns should be fiddled with in the future. For now, it doesn't matter.
        self.productWidgetsLayout.setColumnMinimumWidth(0, 125)
        self.productWidgetsLayout.setColumnMinimumWidth(1, 125)
        self.productWidgetsLayout.setColumnMinimumWidth(2, 125)
        self.productWidgetsLayout.setRowMinimumHeight(0, 50)
        self.productWidgetsLayout.setRowMinimumHeight(1, 100)
        # Add date label & input field to (0,0), (1,0) in Grid Layout
        self.productWidgetsLayout.addWidget(self.text, 0, 0)
        self.productWidgetsLayout.addWidget(self.date_input, 1, 0)

        # Add product selection (wms/wmts) label and check boxes to (1,0), (1,1) in Grid Layout
        self.productWidgetsLayout.addWidget(self.service_label, 0, 1)
        self.productWidgetsLayout.addWidget(self.service_one, 1, 1)
        # self.productWidgetsLayout.addWidget(self.service_two,1,1)
        self.productWidgetsLayout.addWidget(self.service_two, 2, 1)

        # Add Layer List Widget and Label Widget to (0,2), (1,2) in Grid Layout
        self.productWidgetsLayout.addWidget(self.list_label, 0, 2)
        self.productWidgetsLayout.addWidget(self.layer_list_widget, 1, 2)

        # Adding spacing, submit button, Image Widget
        self.layout.addSpacing(15)
        self.layout.addWidget(self.button)
        self.layout.addSpacing(20)
        self.layout.addWidget(self.status_label)
        self.layout.addSpacing(20)
        self.layout.addWidget(self.ImageLabel)
        # Assigning method to handle button click action
        self.button.clicked.connect(self.magic)
        self.service_two.clicked.connect(self.ListSelectionModeToggle)

    @QtCore.Slot()
    def ListSelectionModeToggle(self):
        print('Changing Selection mode')
        # change ListWidget selection mode from multi to singular
        if self.layer_list_widget.SelectionMode == QAbstractItemView.SelectionMode.ExtendedSelection:
            self.layer_list_widget.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        else:
            self.layer_list_widget.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        print(self.layer_list_widget.SelectionMode)

    @QtCore.Slot()
    def magic(self):
        # Update Status label
        self.status_label.setText('Compiling Request...')
        self.status_label.show()
        # read chosen parameters
        service: str = ''
        if self.service_one.isChecked():
            service += 'WMS'
        else:
            service += 'WMTS'

        layers: list
        layers = self.listWidgetToList()

        # Update the Image
        self.requestcount = self.requestcount + 1
        self.status_label.setText('Sending Request...')
        path = main(self.requestcount, self.date_input.toPlainText(), service, layers)
        # self.image =QtGui.QPixmap(path[0])
        self.status_label.setText('Response Received. Updating Image...')
        self.ImageLabel.setPixmap(QtGui.QPixmap(path[0]))
        if path[1] != 'OK':
            self.status_label.setText(str(path[1]))
        else:
            self.status_label.setText('Path to image: ' + path[0])

    def listWidgetToList(self) -> list:
        layers = ['']
        for item in self.layer_list_widget.selectedItems():
            layers.append(item.text())
        return layers


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
