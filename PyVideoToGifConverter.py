import sys
import os
import imageio

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, \
    QPushButton, QFileDialog, QLabel, QStyle, QAction, QMenu, QMainWindow, QMessageBox


def makeGif(clip, targetFormat):
    """Converts video file to gif

        Parameters
        ----------
        clip : str
            The path of the video file given
            from the file dialogue selection process

        targetFormat : str
            The resulting file type after conversion (.gif)

        """
    inputPath = os.path.abspath(clip)
    outputPath = os.path.splitext(inputPath)[0] + targetFormat

    reader = imageio.get_reader(inputPath)
    fps = reader.get_meta_data()['fps']

    writer = imageio.get_writer(outputPath, fps=fps)

    for frame in reader:
        writer.append_data(frame)

    writer.close()


class GifConversioGUI(QMainWindow):
    """PyQt5 GUI for converting a video to a gif"""

    def __init__(self):
        super().__init__()

        self.icon = "icon.png"

        self.title = "PyVideoToGifConverter"

        self.prompt = QLabel(
            'Hi, select a video from\nyour personal files to convert')
        self.prompt.setAlignment(Qt.AlignCenter)

        self.convertButton = QPushButton("Convert")
        self.convertButton.setEnabled(False)
        self.convertButton.clicked.connect(self.convert)

        self.clip = ''

        # Create new action
        self.openAction = QAction(self.style().standardIcon(
            QStyle.SP_DialogOpenButton), '&Open', self)
        self.openAction.setShortcut('Ctrl+O')
        self.openAction.setStatusTip('Open movie')
        self.openAction.triggered.connect(self.openFile)

        # Create exit action
        self.exitAction = QAction(self.style().standardIcon(
            QStyle.SP_DialogCancelButton), '&Exit', self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Exit application')
        self.exitAction.triggered.connect(self.close)

        # Create about action
        self.aboutAction = QAction(self.style().standardIcon(
            QStyle.SP_FileDialogInfoView), '&About', self)
        self.aboutAction.triggered.connect(self.about)

        # Create menu bar and add action
        self.fileMenu = QMenu("&File", self)
        self.fileMenu.addAction(self.openAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAction)

        self.aboutMenu = QMenu("&About", self)
        self.aboutMenu.addAction(self.aboutAction)

        self.menuBar().addMenu(self.fileMenu)
        self.menuBar().addMenu(self.aboutMenu)

        self.setWindowIcon(QIcon(self.icon))
        self.setWindowTitle(self.title)

        # Create a widget for window contents
        wid = QWidget(self)
        self.setCentralWidget(wid)

        # Create layouts to place inside widget
        controlLayout = QVBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.prompt)
        controlLayout.addWidget(self.convertButton)

        layout = QVBoxLayout()
        layout.addLayout(controlLayout)

        # Set widget to contain window contents
        wid.setLayout(layout)

        self.resize(800, 600)

    @pyqtSlot()
    def convert(self):
        """Calls on makeGif function for conversion, updates GUI accordingly"""

        # Change cursor while conversion process takes place
        QApplication.setOverrideCursor(Qt.WaitCursor)
        makeGif(self.clip, '.gif')
        QApplication.restoreOverrideCursor()

        # Reset GUI
        self.prompt.setText(
            'Hi, select a video from\nyour personal files to convert')
        self.clip = ''
        self.convertButton.setEnabled(False)

    @pyqtSlot()
    def openFile(self):
        """Gets video file path from file dialogue, updates GUI accordingly"""

        # Open file dialogue for video selection
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(
            self, 'Select a Video to Convert', '', 'Videos (*mov *mp4 *.gif)', options=options)

        # Update GUI if video selected
        if fileName != '':
            self.clip = fileName
            self.convertButton.setEnabled(True)
            video_type = fileName.split('/')[-1].split('.')[-1]
            video_title = fileName.split('/')[-1].split('.')[-2]
            self.prompt.setText(
                f"Convert {video_title}.{video_type} to {video_title}.gif?")

    def about(self):
        """Presents about prompt, detailing GUI and developer info."""

        QMessageBox.about(self, "About PyVideoToGifConverter",
                          "<p>The <b>PyVideoToGifConverter</b> shows how to select "
                          "a video file from the file dialogue and convert said file "
                          "from a .mpv, .mov to a .gif file.</p>"
                          "<p>This GUI was developed using PyQt5, imageio, and ffmpeg "
                          "by Joseph Villegas, current student at CSUMB.</p>"
                          "<a class='link' href='https://github.com/WilliamSampson44444/cst205_weather_project'>View source on GitHub</a>")


def main():
    app = QApplication(sys.argv)
    gifConversionGUI = GifConversioGUI()
    gifConversionGUI.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
