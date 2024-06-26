from PyQt5.QtWidgets import (
    QMainWindow, QPushButton, QLineEdit, QLabel, QDesktopWidget,
    QFileDialog, QProgressBar, QCheckBox, QApplication,
    QVBoxLayout, QHBoxLayout, QWidget, QScrollArea, QGroupBox
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, pyqtSignal
import sys


class App(QMainWindow):

    startSortingSignal = pyqtSignal()

    def __init__(self, config):
        super().__init__()
        self.config = config
        self.initUI()
        self.applyConfigDefaults()

    def applyConfigDefaults(self):
        # Applica i valori di configurazione ai widget
        sourcedir_default = self.config.get('Directories', 'source_dir', fallback="./source")
        self.textbox_sourcedir.setText(sourcedir_default)
        destdir_default = self.config.get('Directories', 'destination_dir', fallback="./destination")
        self.textbox_destdir.setText(destdir_default)
        placespath_default = self.config.get('Places', 'places_file_path', fallback="./known_places.txt")
        self.textbox_placesfilepath.setText(placespath_default)
        homelat_default = self.config.get('Home', 'home_lat', fallback="0")
        self.textbox_homelat.setText(homelat_default)
        homelon_default = self.config.get('Home', 'home_lon', fallback="0")
        self.textbox_homelon.setText(homelon_default)
        xspace_default = self.config.get('Space', 'x_space', fallback="2")
        self.textbox_xspace.setText(xspace_default)
        yspace_default = self.config.get('Space', 'y_space', fallback="10")
        self.textbox_yspace.setText(yspace_default)
        zspace_default = self.config.get('Space', 'z_space', fallback="1")
        self.textbox_zspace.setText(zspace_default)
        xtime_default = self.config.get('Time', 'x_time', fallback="3600")
        self.textbox_xtime.setText(xtime_default)
        ytime_default = self.config.get('Time', 'y_time', fallback="10")
        self.textbox_ytime.setText(ytime_default)
        ztime_default = self.config.get('Time', 'z_time', fallback="3600")
        self.textbox_ztime.setText(ztime_default)

    def create_line_edit(self, placeholder_text):
        textbox = QLineEdit()
        textbox.setPlaceholderText(placeholder_text)
        return textbox

    def create_button(self, click_event):
        button = QPushButton("...")
        button.clicked.connect(click_event)
        return button

    def create_group_box(self, title, layout):
        group_box = QGroupBox(title)
        group_box.setLayout(layout)
        return group_box

    def create_horizontal_layout(self, widgets):
        layout = QHBoxLayout()
        for widget in widgets:
            layout.addWidget(widget)
        return layout

    def create_vertical_layout(self, widgets):
        layout = QVBoxLayout()
        for widget in widgets:
            layout.addWidget(widget)
        return layout

    def initUI(self):
        self.setWindowTitle("Photosorter")
        self.setWindowIcon(QIcon("./assets/icon.ico"))

        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        mainLayout = QVBoxLayout(centralWidget)

        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scrollContent = QWidget(scroll)
        scrollLayout = QVBoxLayout(scrollContent)
        scrollContent.setLayout(scrollLayout)

        # Source directory layout
        self.textbox_sourcedir = self.create_line_edit("Insert source directory path")
        self.button_sourcedir = self.create_button(self.on_click_sourcedir_button)
        horizontalSourceLayout = self.create_horizontal_layout([self.textbox_sourcedir, self.button_sourcedir])
        groupSourceDirectoryPath = self.create_group_box("Source directory path", horizontalSourceLayout)
        scrollLayout.addWidget(groupSourceDirectoryPath)

        # Destination directory layout
        self.textbox_destdir = self.create_line_edit("Insert destination directory path")
        self.button_destdir = self.create_button(self.on_click_destdir_button)
        horizontalDestinationLayout = self.create_horizontal_layout([self.textbox_destdir, self.button_destdir])
        groupDestinationDirectoryPath = self.create_group_box("Destination directory path", horizontalDestinationLayout)
        scrollLayout.addWidget(groupDestinationDirectoryPath)

        # Known places file path
        self.textbox_placesfilepath = self.create_line_edit("Insert known places file path")
        self.button_placesfilepath = self.create_button(self.on_click_placesfilepath_button)
        horizontalPlacesLayout = self.create_horizontal_layout([self.textbox_placesfilepath, self.button_placesfilepath])
        groupKnownPlacesPath = self.create_group_box("Known places file path", horizontalPlacesLayout)
        scrollLayout.addWidget(groupKnownPlacesPath)

        # Home Location section
        # Create the latitude and longitude line edits
        self.textbox_homelat = self.create_line_edit("Insert home location latitude")
        self.textbox_homelon = self.create_line_edit("Insert home location longitude")
        # Create the labels for latitude and longitude
        label_lat = QLabel("Latitude:")
        label_lon = QLabel("Longitude:")

        # Create a single horizontal layout to contain both the latitude and longitude layouts
        homeLocationLayout = QHBoxLayout()
        homeLocationLayout.addWidget(label_lat)
        homeLocationLayout.addWidget(self.textbox_homelat)
        homeLocationLayout.addWidget(label_lon)
        homeLocationLayout.addWidget(self.textbox_homelon)

        # Create the group box for the home location section and add it to the scroll layout
        groupBoxHomeLocation = QGroupBox("Home Location")
        groupBoxHomeLocation.setLayout(homeLocationLayout)
        scrollLayout.addWidget(groupBoxHomeLocation)


        # Space and time options section
        optionsLayout = QHBoxLayout()

        # Space Options section
        # Create text boxes with placeholder text
        self.textbox_xspace = self.create_line_edit("2")
        self.textbox_yspace = self.create_line_edit("10")
        self.textbox_zspace = self.create_line_edit("1")
        # Create labels for each text box
        label_xspace = QLabel("(X) kms between pics:")
        label_yspace = QLabel("(Y) kms from home:")
        label_zspace = QLabel("(Z) kms where to start:")
        # Create horizontal layouts for each set of label and text box
        xSpaceLayout = self.create_horizontal_layout([label_xspace, self.textbox_xspace])
        ySpaceLayout = self.create_horizontal_layout([label_yspace, self.textbox_yspace])
        zSpaceLayout = self.create_horizontal_layout([label_zspace, self.textbox_zspace])
        # Create the explanation label
        spaceExplanationLabel = QLabel("Pics far away X kms from each others\n and Y kms away from home are put together.\nZ are the kms away from home where to start the calculation\n about space.")
        # Create the vertical layout and add the explanation label and the three horizontal layouts
        spaceOptionsLayout = QVBoxLayout()
        spaceOptionsLayout.addWidget(spaceExplanationLabel)
        spaceOptionsLayout.addLayout(xSpaceLayout)
        spaceOptionsLayout.addLayout(ySpaceLayout)
        spaceOptionsLayout.addLayout(zSpaceLayout)
        # Create the group box for the space options section and add it to the scroll layout
        groupBoxSpaceOptions = QGroupBox("Space Options")
        groupBoxSpaceOptions.setLayout(spaceOptionsLayout)

        # Time Options section
        # Create text boxes with placeholder text for time options
        self.textbox_xtime = self.create_line_edit("3600")
        self.textbox_ytime = self.create_line_edit("10")
        self.textbox_ztime = self.create_line_edit("3600")
        # Create labels for each time option
        label_xtime = QLabel("(X) sec between pics:")
        label_ytime = QLabel("(Y) kms from home:")
        label_ztime = QLabel("(Z) sec when to start:")
        # Create horizontal layouts for each set of label and text box
        xTimeLayout = self.create_horizontal_layout([label_xtime, self.textbox_xtime])
        yTimeLayout = self.create_horizontal_layout([label_ytime, self.textbox_ytime])
        zTimeLayout = self.create_horizontal_layout([label_ztime, self.textbox_ztime])
        # Create the explanation label for the time options
        timeExplanationLabel = QLabel("Pics far away X seconds from each others\n and Y kms away from home are put together.\nZ are the seconds when to start the calculation\n about time.")
        # Create the vertical layout and add the explanation label and the horizontal layouts for time options
        timeOptionsLayout = QVBoxLayout()
        timeOptionsLayout.addWidget(timeExplanationLabel)
        timeOptionsLayout.addLayout(xTimeLayout)
        timeOptionsLayout.addLayout(yTimeLayout)
        timeOptionsLayout.addLayout(zTimeLayout)
        # Create the group box for the time options section and add it to the scroll layout
        groupBoxTimeOptions = QGroupBox("Time Options")
        groupBoxTimeOptions.setLayout(timeOptionsLayout)

        # Aggiungere entrambi i groupBox al layout orizzontale
        optionsLayout.addWidget(groupBoxSpaceOptions)
        optionsLayout.addWidget(groupBoxTimeOptions)


        # Creare un widget contenitore per il layout orizzontale
        optionsContainer = QWidget()
        optionsContainer.setLayout(optionsLayout)
        scrollLayout.addWidget(optionsContainer)

        # Checkbox Options section refactored
        groupBoxCheckOptions = QGroupBox("Additional Options")
        checkOptionsLayout = QVBoxLayout()
        # Directly add checkboxes to the layout
        self.check_dictionarymode = QCheckBox("Create known places dictionary only")
        checkOptionsLayout.addWidget(self.check_dictionarymode)
        self.check_movefile = QCheckBox("Move files instead of copy (faster!)")
        checkOptionsLayout.addWidget(self.check_movefile)
        # Set layout to the group box and add it to the scroll layout
        groupBoxCheckOptions.setLayout(checkOptionsLayout)
        scrollLayout.addWidget(groupBoxCheckOptions)
        # Actions section refactored
        actionGroup = QGroupBox("Sorting Actions")
        actionLayout = QVBoxLayout()
        # Add start button, progress bar, and progress label to the action layout
        self.button_start = QPushButton("Start sorting")
        self.button_start.clicked.connect(self.on_click_start)
        actionLayout.addWidget(self.button_start)
        self.progressbar = QProgressBar()
        self.progressbar.setValue(0)
        actionLayout.addWidget(self.progressbar)
        self.label_progress = QLabel('Press "Start sorting" to begin')
        self.label_progress.setWordWrap(True)
        actionLayout.addWidget(self.label_progress)
        # Set layout to the action group and add it to the scroll layout
        actionGroup.setLayout(actionLayout)
        scrollLayout.addWidget(actionGroup)

        # Add the scroll area to the main layout
        scroll.setWidget(scrollContent)
        mainLayout.addWidget(scroll)

        # Ridimensionabile e reattivo
        self.setMinimumSize(650, 660)  # Imposta una dimensione minima per la finestra principale

    def closeEvent(self, event):
        # when closing, kill the program
        sys.exit()

    @pyqtSlot()
    def on_click_start(self):
        # disable all the buttons and textbox when the app start
        ui_elements = [
            self.textbox_sourcedir, self.button_sourcedir,
            self.textbox_destdir, self.button_destdir,
            self.textbox_placesfilepath, self.button_placesfilepath,
            self.textbox_homelat, self.textbox_homelon,
            self.textbox_xspace, self.textbox_yspace, self.textbox_zspace,
            self.textbox_xtime, self.textbox_ytime, self.textbox_ztime,
            self.button_start, self.check_dictionarymode, self.check_movefile
        ]

        for element in ui_elements:
            element.setEnabled(False)

        self.startSortingSignal.emit()

    def on_click_sourcedir_button(self):
        # set source dir from dialog
        fileName = str(QFileDialog.getExistingDirectory(self, "Select directory"))
        if fileName:
            self.textbox_sourcedir.setText(fileName)

    def on_click_destdir_button(self):
        # set destination dir from dialog
        fileName = str(QFileDialog.getExistingDirectory(self, "Select directory"))
        if fileName:
            self.textbox_destdir.setText(fileName)

    def on_click_placesfilepath_button(self):
        # set destination dir from dialog
        fileName, _ = QFileDialog.getOpenFileName(
            self, "Open places.txt file", "", "Text file (*.txt)"
        )
        if fileName:
            self.textbox_placesfilepath.setText(fileName)
