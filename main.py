import sys
import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QListWidget, QMessageBox, QDesktopWidget, QTimer

class CronometroApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.tiempos_registrados = {}
        self.inicio = None
        self.fin = None
        self.initUI()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.verificarActividad)
        self.timer.start(600000)  # Verificar actividad cada 10 minutos (600000 ms)

    def initUI(self):
        self.setWindowTitle('Cronómetro')
        self.setGeometry(100, 100, 400, 300)

        self.label = QLabel('Presiona Iniciar para comenzar el cronómetro')
        self.button_iniciar = QPushButton('Iniciar')
        self.button_detener = QPushButton('Detener')
        self.button_detener.setEnabled(False)
        self.lista_tiempos = QListWidget()
        self.label_suma = QLabel('Suma de tiempos registrados: 0:00:00')

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button_iniciar)
        layout.addWidget(self.button_detener)
        layout.addWidget(self.lista_tiempos)
        layout.addWidget(self.label_suma)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

        self.button_iniciar.clicked.connect(self.iniciarCronometro)
        self.button_detener.clicked.connect(self.detenerCronometro)

    def iniciarCronometro(self):
        self.inicio = datetime.datetime.now()
        self.button_iniciar.setEnabled(False)
        self.button_detener.setEnabled(True)
        self.label.setText('Cronómetro en marcha...')

    def detenerCronometro(self):
        if self.inicio:
            self.fin = datetime.datetime.now()
            tiempo_transcurrido = self.fin - self.inicio

            if self.esHoraLaboral(self.fin.time()):
                tiempo_formato = str(tiempo_transcurrido).split('.')[0]  # Formato HH:MM:SS
                fecha_actual = self.fin.date().isoformat()

                if fecha_actual in self.tiempos_registrados:
                    self.tiempos_registrados[fecha_actual].append(tiempo_transcurrido)
                else:
                    self.tiempos_registrados[fecha_actual] = [tiempo_transcurrido]

                self.lista_tiempos.addItem(f'Fecha: {fecha_actual}, Tiempo: {tiempo_formato}')

            self.button_iniciar.setEnabled(True)
            self.button_detener.setEnabled(False)
            self.inicio = None
            self.fin = None

            # Calcular la suma de los tiempos registrados
            suma = self.calcularSuma()
            self.label_suma.setText(f'Suma de tiempos registrados: {str(suma).split(".")[0]}')

    def esHoraLaboral(self, hora):
        # Verificar si la hora está dentro del rango laboral (8:00 AM - 6:00 PM)
        return datetime.time(8, 0) <= hora <= datetime.time(18, 0)

    def calcularSuma(self):
        suma = datetime.timedelta()
        for tiempos in self.tiempos_registrados.values():
            suma += sum(tiempos, datetime.timedelta())
        return suma

    def verificarActividad(self):
        # Verificar si ha pasado un tiempo considerable sin actividad
        tiempo_inactivo_maximo = datetime.timedelta(minutes=30)  # Tiempo inactivo máximo de 30 minutos

        if self.inicio and (datetime.datetime.now() - self.inicio) >= tiempo_inactivo_maximo:
            # Mostrar una alerta de inactividad
            self.mostrarAlertaInactividad()

    def mostrarAlertaInactividad(self):
        mensaje = "No se ha detectado actividad en un tiempo considerable. ¿Estás trabajando?"
        QMessageBox.warning(self, "Alerta de Inactividad", mensaje, QMessageBox.Ok)

def main():
    app = QApplication(sys.argv)
    ventana = CronometroApp()
    ventana.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

