from SisATM import SisATM
from SisMenu import menu_login, menu_cajero 

def main():
    atm = SisATM()
    atm.cargar_datos_json()
    if menu_login(atm):
        menu_cajero(atm)

if __name__ == '__main__':
    main()


