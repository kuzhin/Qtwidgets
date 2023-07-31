import numpy as np
import h5py
import pyqtgraph as pg
from PyQt5 import QtWidgets as Widgets_from_library
from PyQt5.QtWidgets import QComboBox    #QtWidgets
from PyQt5.QtGui import QColor, QFont    #QtGui
from PyQt5.QtWidgets import QInputDialog #QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem

class MainWindow(Widgets_from_library.QMainWindow):

    def __init__(self):
        # self - ссылка на класс MainWindow
        super().__init__() 
        #super() упрощает другим классам использование класса, который мы пишем
        # init 

        # создаем двумерный numpy-массив
        self.data = np.zeros((10, 3))

        # создаем таблицу для отображения данных
        self.table = Widgets_from_library.QTableWidget()
        self.table.setRowCount(10)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['Column X', 'Column Y', 'Total'])
        self.table.cellChanged.connect(self.CellChanged)

        # создаем выпадающий список чисел от 1 до 5 для столбца 'Column Y'
        for row in range(10):
            combobox= QComboBox()
            combobox.addItems([str(1),str(2),str(3),str(4),str(5)]) 
            combobox.currentIndexChanged.connect(self.comboChanged)
            self.table.setCellWidget(row, 1, combobox)

        # создаем график для отображения зависимости второго столбца от первого
        self.plot = pg.PlotWidget()

        # создаем кнопки сохранение, загрузка, изменение размера массива
        save_button = Widgets_from_library.QPushButton('Save')
        save_button.clicked.connect(self.saveData)
        load_button = Widgets_from_library.QPushButton('Load')
        load_button.clicked.connect(self.loadData)
        resize_button = Widgets_from_library.QPushButton('Resize')
        resize_button.clicked.connect(self.resizeData)

        # создаем главный виджет и размещаем на нем элементы интерфейса
        central_widget = Widgets_from_library.QWidget()
        layout = Widgets_from_library.QVBoxLayout()
        layout.addWidget(self.table)
        layout.addWidget(self.plot)
        layout.addWidget(save_button)
        layout.addWidget(load_button)
        layout.addWidget(resize_button)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # обновляем таблицу и график
        self.updateTable()
        self.updatePlot()

    def CellChanged(self, row, column):
        # обработчик изменения ячейки таблицы
        if column == 0:
            value = self.table.item(row, column).text()
            try:
                self.data[row, column] = float(value)
                self.data[row, 2] = self.data[row, 0] * float(self.table.cellWidget(row, 1).currentText())
                self.table.setItem(row, 2, Widgets_from_library.QTableWidgetItem(str(self.data[row, 2])))
            except ValueError:
                pass
        self.updatePlot()

    def comboChanged(self):
        # обработчик изменения значения в выпадающем списке
        combobox= self.sender()
        index = self.table.indexAt(combobox.pos())
        if index.isValid():
            row = index.row()
            self.data[row, 1] = float(combobox.currentText())           
            self.data[row, 2] = self.data[row, 0] * self.data[row, 1]
            self.table.setItem(row, 2, Widgets_from_library.QTableWidgetItem(str(self.data[row, 2])))
            self.updatePlot()

    def updateTable(self):
        # Обновление данных в таблице
        for row in range(self.data.shape[0]):
            for column in range(self.data.shape[1]):
                item = Widgets_from_library.QTableWidgetItem(str(self.data[row, column]))
                self.table.setItem(row, column, item)

    # Почему-то не получилось окрашивать ячейки в разные цвета. Позволяет окрасить ячейки только в 1 цвет
    # def updateTable(self):
    #     # обновление данных в таблице
    #     for row in range(self.data.shape[0]):
    #         for column in range(self.data.shape[1]):
    #             if column == 0:
    #                 value = self.data[row, column]
                    
    #                 # создаем новый элемент таблицы 
    #                 item = Widgets_from_library.QTableWidgetItem(str(value))
                    
    #                 # меняем цвет ячейки в зависимости от значения
    #                 if value > 0:
    #                     color = QColor(0, 255, 0)  # зеленый
    #                 else:
    #                     color = QColor(255, 0, 0)  # красный
                        
    #                 item.setBackground(color) # устанавливаем цвет фона ячейки
                    
    #                 self.table.setItem(row, column, item) # добавляем ячейку в таблицу
    #             else:
    #                 item = Widgets_from_library.QTableWidgetItem(str(self.data[row, column]))
    #                 self.table.setItem(row, column, item)



    def updatePlot(self):
        # обновление графика
        x = self.data[:, 0]
        y = self.data[:, 1]
        self.plot.clear()
        self.plot.plot(x, y, pen='b')

    def saveData(self):
        # сохранение данных в файл
        file_name, unused = Widgets_from_library.QFileDialog.getSaveFileName(self, 'Save Data', '', 'HDF5 (*.h5)')
        # unused значение флага, можем пропустить, тк нам это не нужно
        if file_name:
            with h5py.File(file_name, 'w') as file:
                file.create_dataset('data', data=self.data)

    def loadData(self):
        # загрузка данных из файла
        file_name, _ = Widgets_from_library.QFileDialog.getOpenFileName(self, 'Load Data', '', 'HDF5 Files (*.h5)')
        if file_name:
            with h5py.File(file_name, 'r') as file:
                self.data = file['data'][:]
            self.updateTable()
            self.updatePlot()
   
    def resizeData(self):
    # Изменение размера массива
        rows, ok = QInputDialog.getInt(self, 'Resize Data', 'Enter number of rows:')
        if ok:
            # проверяем, что новое количество строк больше 0
            if rows > 0:
                # создаем новый массив с заданным количеством строк
                new_data = self.data[:rows, :]
                self.data = new_data
                self.updateTable()
                self.updatePlot()

# если система будет более сложная
# if __name__ == '__main__':
app = Widgets_from_library.QApplication([])
window = MainWindow()
window.show()
app.exec_()
