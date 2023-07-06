import eth_utils
from web3 import Web3
from PyQt5 import QtWidgets, QtGui, QtCore
import warnings
warnings.filterwarnings('ignore')

eth_rpc_url = 'https://endpoints.omniatech.io/v1/eth/mainnet/public'
web3 = Web3(Web3.HTTPProvider(eth_rpc_url))

class TrayApplication(QtWidgets.QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.tray_icon = QtWidgets.QSystemTrayIcon()
        self.menu = QtWidgets.QMenu()

        self.gas_price = 0

        self.create_actions()
        self.create_tray_icon()

        self.update_gas()
        self.update_timer = QtCore.QTimer()
        self.update_timer.timeout.connect(self.update_gas)
        self.update_timer.start(7000)  # update every 7 seconds

    def create_actions(self):
        self.quit_action = QtWidgets.QAction("quit", self)
        self.quit_action.triggered.connect(self.quit_application)

    def create_tray_icon(self):
        number = gwei()
        pixmap = create_image(number)

        self.menu.addAction("@xxceptive_eth")
        self.menu.addAction(self.quit_action)
        self.tray_icon.setIcon(QtGui.QIcon(pixmap))
        self.tray_icon.setContextMenu(self.menu)
        self.tray_icon.show()

    def update_gas(self):
        self.gas_price = gwei()
        pixmap = create_image(self.gas_price)
        self.tray_icon.setIcon(QtGui.QIcon(pixmap))
        self.menu.clear()
        self.menu.addAction("@xxceptive_eth")
        self.menu.addAction(self.quit_action)

    def quit_application(self):
        self.update_timer.stop()
        QtWidgets.QApplication.quit()

def gwei():
    gas_price = round(eth_utils.from_wei(web3.eth.gas_price, 'gwei'))
    return gas_price

def create_image(gwei):
    width = 32
    height = 32
    color1 = QtGui.QColor(0, 0, 0, 0)
    color2 = QtGui.QColor(255, 255, 255)

    image = QtGui.QImage(QtCore.QSize(width, height), QtGui.QImage.Format_ARGB32)
    image.fill(color1)
    painter = QtGui.QPainter(image)

    painter.setFont(QtGui.QFont("Arial", 23))
    painter.setPen(color2)
    painter.drawText(QtCore.QRectF(0, 0, width, height), QtCore.Qt.AlignCenter, str(gwei))
    painter.end()

    pixmap = QtGui.QPixmap.fromImage(image)
    return pixmap



if __name__ == '__main__':
    import sys
    app = TrayApplication(sys.argv)
    sys.exit(app.exec_())
