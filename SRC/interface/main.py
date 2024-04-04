import sys
from PyQt5.QtWidgets import QApplication
from interface import InterfacePrincipale

def main():
    app = QApplication(sys.argv)
    fenetre = InterfacePrincipale()
    fenetre.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
