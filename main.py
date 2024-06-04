import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QGraphicsView, QGraphicsScene, QVBoxLayout, QWidget,  QMessageBox, QFileDialog
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QSpacerItem,  QSizePolicy, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class DataInputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ввод данных для графика")

        layout = QVBoxLayout()

        self.x_label = QLabel("Введите данные для оси X (через запятую):")
        layout.addWidget(self.x_label)

        self.x_edit = QLineEdit()
        layout.addWidget(self.x_edit)

        self.y_label = QLabel("Введите данные для оси Y (через запятую):")
        layout.addWidget(self.y_label)

        self.y_edit = QLineEdit()
        layout.addWidget(self.y_edit)

        self.plot_button = QPushButton("Построить график")
        self.plot_button.clicked.connect(self.accept)
        layout.addWidget(self.plot_button)

        self.setLayout(layout)

    def get_data(self):
        return self.x_edit.text(), self.y_edit.text()


class DataInputHistDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ввод данных для графика")

        layout = QVBoxLayout()

        self.x_label = QLabel("Введите элементы выборки через запятую:")
        layout.addWidget(self.x_label)

        self.x_edit = QLineEdit()
        layout.addWidget(self.x_edit)

        self.plot_button = QPushButton("Построить график")
        self.plot_button.clicked.connect(self.accept)
        layout.addWidget(self.plot_button)

        self.setLayout(layout)

    def get_data(self):
        return self.x_edit.text()




    
class ButtonCounter(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Кликер")
        self.setGeometry(0, 0, 100, 100)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.counter = 0

        self.create_button()

    def create_button(self):
        self.button = QPushButton("Нажми меня", self)
        self.button.setFixedSize(80, 40) 
        self.button.clicked.connect(self.button_clicked)
        self.layout.addWidget(self.button)

        self.counter_label = QLabel("Количество нажатий: 0", self)
        self.layout.addWidget(self.counter_label)

        self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.layout.addWidget(self.counter_label, 0, 0)
        self.layout.addWidget(self.button, 0, 0)
        self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def button_clicked(self):
        self.counter += 1
        self.counter_label.setText("Количество нажатий: " + str(self.counter))
    


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Лучшее графическое приложение")
        self.setGeometry(100, 100, 800, 600)

        self.show_welcome_message()
        
        self.create_menu()
        self.show_message()
    

    def set_vie(self):
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.setCentralWidget(self.view)


    def show_message(self):
        welcome_label = QLabel("Жёское приложение чтобы вы могли насладиться гистограммами и графиком логистической функции")
        welcome_label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(welcome_label)

    def show_welcome_message(self):
        QMessageBox.information(self, "предостережение", "«Не судите, да не судимы будете, ибо каким судом судите, таким будете судимы; и какою мерою мерите, такою и вам будут мерить» (Мф. 7:1,2)")

    def create_menu(self):
        main_menu = self.menuBar()
        file_menu = main_menu.addMenu("Файл")
        graph_menu = main_menu.addMenu("Готовые графики")
        my_graph = main_menu.addMenu("Построить график")
        Histo = main_menu.addMenu("Гистограмма")
        manip_menu = main_menu.addMenu("Засчитать задачу")



        message_action = QAction("Нажмите", self)
        message_action.triggered.connect(self.show_fullscreen_message)
        manip_menu.addAction(message_action)

        plot_action = QAction("Линейный график", self)
        plot_action.triggered.connect(self.plot_linear_graph)
        graph_menu.addAction(plot_action)

        sin_action = QAction("График синуса", self)
        sin_action.triggered.connect(self.plot_sin_graph)
        graph_menu.addAction(sin_action)

        cos_action = QAction("График косинуса", self)
        cos_action.triggered.connect(self.plot_cos_graph)
        graph_menu.addAction(cos_action)
        
        sigmoid_action = QAction("График сигмойды", self)
        sigmoid_action.triggered.connect(self.plot_sigmoid)
        graph_menu.addAction(sigmoid_action)

        save_action = QAction("Сохранить график", self)
        save_action.triggered.connect(self.save_graph)
        file_menu.addAction(save_action)

        custom_plot_action = QAction("по своим данным", self)
        custom_plot_action.triggered.connect(self.show_custom_plot_dialog)
        my_graph.addAction(custom_plot_action)

        hist_action = QAction("Гистограмма", self)
        hist_action.triggered.connect(self.show_histogram_dialog)
        Histo.addAction(hist_action)

    def show_histogram_dialog(self):
        dialog = DataInputHistDialog(self)
        if dialog.exec_():
            data = dialog.get_data()
            self.plot_histogram(data)

    def plot_histogram(self, data):
        self.set_vie()
        try:
            data_list = [float(d) for d in data.split(",")]
            self.plot_histogram_graph(data_list, "Гистограмма распределения")
        except:
            self.show_error()


    def plot_histogram_graph(self, data, title):
        self.set_vie()
        self.scene.clear()

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.hist(data, bins=10, edgecolor='black')
        ax.set_xlabel('Значения')
        ax.set_ylabel('Частота')
        ax.set_title(title)

        canvas = FigureCanvas(fig)
        canvas.draw()

        self.scene.addWidget(canvas)

    def show_custom_plot_dialog(self):
        dialog = DataInputDialog(self)
        if dialog.exec_():
            x_data, y_data = dialog.get_data()
            self. plot_my_graph(x_data, y_data)

    def plot_my_graph(self, x_data, y_data):
        self.set_vie()
        try:
            x_list = [float(x) for x in x_data.split(",")]
            y_list = [float(y) for y in y_data.split(",")]
            if len(x_list) != len(y_list):
                self.show_message("Ошибка", "Длины списков данных для X и Y должны быть одинаковыми.")
                return
            self.plot_graph(x_list, y_list, "Ваш график")
        except :
            self.show_error()

    def sigmoid(self,x):
        return 1 / (1 + np.exp(-x))

    def plot_sigmoid(self):
        self.set_vie()
        x = np.linspace(-10.1,10.2,1000)
        y = self.sigmoid(x)
        self.plot_graph(x, y, "Логистический график")



    def plot_linear_graph(self):
        self.set_vie()
        x = [1, 2, 3, 4, 5]
        y = [1, 2, 3, 4, 5]
        self.plot_graph(x, y, "Линейный график")

    def plot_sin_graph(self):
        self.set_vie()
        x = np.linspace(-2*np.pi, 2*np.pi, 100)
        y = np.sin(x)
        self.plot_graph(x, y, "График синуса")

    def plot_cos_graph(self):
        self.set_vie()
        x = np.linspace(-2*np.pi, 2*np.pi, 100)
        y = np.cos(x)
        self.plot_graph(x, y, "График косинуса")

    def plot_graph(self, x, y, title):
        self.set_vie()
        self.scene.clear()

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(x, y)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title(title)

        canvas = FigureCanvas(fig)
        canvas.draw()

        self.scene.addWidget(canvas)

    def save_graph(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Сохранить график", "", "PNG files (*.png);;JPEG files (*.jpg *.jpeg)")
        if file_name:
            plt.savefig(file_name)
            QMessageBox.information(self, "Успех", "График успешно сохранен!")

    def show_fullscreen_message(self):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Произошёл успех")
        msg_box.setText("Вы засчитали задачу Кирилу")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()
    
    def show_error(self):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("EROOROOROROROR")
        msg_box.setText("ДАННЫЕ БЫЛИ ВВЕДЕНЫ НЕВЕРНО, через 30 секунд компьютер будет самоуничтожен")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())