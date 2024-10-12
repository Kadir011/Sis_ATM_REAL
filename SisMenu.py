'''
MENÚ DE CAJERO
'''

import time 

def menu_login(atm):
    """Menú de login y registro con manejo de excepciones"""
    while True:
        try:
            print("\n=== Bienvenido al sistema ATM ===")
            print("1. Iniciar sesión")
            print("2. Registro de usuario")
            print("3. Salir")

            opcion = input("Seleccione una opción: ")

            match opcion:
                case '1':
                    if atm.ingresar_usuario():
                        return True
                    else:
                        print("Ingreso fallido. Intente de nuevo.")
                        time.sleep(5)
                case '2':
                    atm.registro_usuario()
                case '3':
                    print('Adiós...!')
                    break 
                case _:
                    print("Opción no válida. Intente de nuevo.")
                    time.sleep(5)
        except Exception as e:
            print(f'Error en el menú: {e}. Intente nuevamente.')

def menu_cajero(atm):
    """Menú principal después del login"""
    while True:
        try:
            print("\n=== Menú Principal ===")
            print("1. Depositar")
            print("2. Retirar")
            print("3. Consultar saldo")
            print("4. Consultar datos")
            print("5. Cambiar contraseña")
            print("6. Salir")

            opcion = input("Seleccione una opción: ")

            match opcion:
                case '1':
                    cantidad = float(input("Ingrese la cantidad a depositar: ").strip())
                    atm.depositar(cantidad) 
                case '2': 
                    cantidad = float(input("Ingrese la cantidad a retirar: ").strip())
                    atm.retirar(cantidad)
                case '3': 
                    atm.consultar_saldo()
                case '4': 
                    atm.mostrar_datos()
                case '5': 
                    atm.cambiar_contraseña() 
                case '6': 
                    print(f'Adiós {atm.cuenta_actual.usuario.nombre}!')
                    break
                case _: 
                    print("Opción no válida. Intente de nuevo.")
                    time.sleep(5)
        except Exception as e:
            print(f'Error en el menú principal: {e}. Intente nuevamente.')









