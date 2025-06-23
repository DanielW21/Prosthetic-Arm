import sys
import random
import time
import os
import csv
from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg
from PyQt5.QtCore import QThread, pyqtSignal

class DataGenerator(QThread):
    new_data = pyqtSignal(int)
    
    def __init__(self):
        super().__init__()
        self.recordingStarted = False
        self.recordedData = []
    
    def run(self):
        # Simulated data generation
        while True:
            start_time = time.time()
            while time.time() - start_time < 5:
                decoded = random.randint(0, 100)
                time.sleep(0.01)
                self.new_data.emit(decoded)
                if self.recordingStarted:
                    self.recordedData.append(decoded)
            
            start_time = time.time()
            while time.time() - start_time < 2.5:
                decoded = random.randint(1000, 2000)
                time.sleep(0.01)
                self.new_data.emit(decoded)
                if self.recordingStarted:
                    self.recordedData.append(decoded)

class LiveGraph(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EMG Data")
        self.setGeometry(100, 100, 800, 600)
        
        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)
        self.graphWidget.setBackground('w')
        self.graphWidget.setYRange(-10, 2400)
        self.data_line = self.graphWidget.plot(pen=pg.mkPen(color='b', width=2))
        self.data = [0] * 200
        
        self.data_generator = DataGenerator()
        self.data_generator.new_data.connect(self.update_label)
        self.data_generator.start()

        self.GUI()

    def GUI(self):
        # Start/Stop Recording Button
        self.record_button = QtWidgets.QPushButton("Start Recording (1)", self)
        self.record_button.setGeometry(50, 40, 150, 40)
        self.record_button.setStyleSheet("background-color: #808080; color: white; font-size: 14px;")  # Green with white text
        self.record_button.clicked.connect(self.toggle_recording)

        # Save Button
        self.save_button = QtWidgets.QPushButton("Save Data (2)", self)
        self.save_button.setGeometry(210, 40, 150, 40)
        self.save_button.setStyleSheet("background-color: #808080; color: white; font-size: 14px;")  # Blue with white text
        self.save_button.clicked.connect(self.save_data)

        # Filename Entry
        self.filename_entry = QtWidgets.QLineEdit(self)
        self.filename_entry.setPlaceholderText("Save file name")
        self.filename_entry.setGeometry(370, 40, 200, 40)

        #Folder Entry
        self.foldername_entry = QtWidgets.QLineEdit(self)
        self.foldername_entry.setPlaceholderText("Save folder name")
        self.foldername_entry.setGeometry(575, 40, 200, 40)

        # Recording Status Label
        self.recording_status = QtWidgets.QLabel("Not Recording", self)
        self.recording_status.setGeometry(75, 10, 200, 40)
        self.recording_status.setStyleSheet("color: red; font-size: 16px;")

        # FPS Label
        self.fps_label = QtWidgets.QLabel(self)
        self.fps_label.setGeometry(700, 10, 100, 20)
        self.fps_label.setStyleSheet("color: red; font-size: 20px;")

        self.frame_count = 0
        self.cur_time = time.time()


    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_1:
            self.toggle_recording()
        elif event.key() == QtCore.Qt.Key_2:
            self.save_data()

    def toggle_recording(self):
        self.data_generator.recordingStarted = not self.data_generator.recordingStarted
        if self.data_generator.recordingStarted:
            self.record_button.setText("Stop Recording")
            self.recording_status.setText("Recording...")
            self.recording_status.setStyleSheet("QLabel { color : green; font-size: 16px; }")
        else:
            self.record_button.setText("Start Recording")
            self.recording_status.setText("Not Recording")
            self.recording_status.setStyleSheet("QLabel { color : red; font-size: 16px; }")

    def new_folder(self, folder_name):
        folder_path = folder_name
        file_path = os.path.join(folder_name,)

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Folder '{folder_path}' created successfully.")
        else:
            print(f"Folder '{folder_path}' already exists.")


    def save_data(self):
        filename = self.filename_entry.text().strip() or "recorded_data"
        foldername = self.foldername_entry.text().strip() or "default_folder"
        
        filename = filename if filename.endswith('.csv') else filename + '.csv'
        self.new_folder(foldername)
        file_path = os.path.join(foldername, filename)
        

        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            for data in self.data_generator.recordedData:
                writer.writerow([data])
        self.data_generator.recordedData = []  
 
    def update_label(self, decoded):
        self.data = self.data[1:] + [decoded]
        self.data_line.setData(self.data)
        
        self.frame_count += 1
        update_time = time.time()    
        if update_time - self.cur_time >= 1.0:
            fps = self.frame_count / (update_time - self.cur_time)
            self.fps_label.setText(f"FPS: {int(fps)}")
            self.cur_time = update_time
            self.frame_count = 0

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    liveGraph = LiveGraph()
    liveGraph.show()
    sys.exit(app.exec_())
