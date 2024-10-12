'''
SISTEMA ATM COMPLETO CON USUARIOS MEDIANTE POO

SE DEBE PRIMERO REGISTRAR AL USUARIO PARA LUEGO INGRESAR
ANTES DE INGRESAR AL MENU DEL CAJERO DEBE APARECER UN MENU:

1. REGISTRAR
2. INICIAR SESION
3. SALIR

SI LOS DATOS DE LOGIN NO EXISTEN PUES DEBE REGISTRARSE PRIMERO
AL INICIAR SESION APARECE EL MENU DE CAJERO SIGUIENTE:

MENU DE CAJERO
1. RETIRAR
2. DEPOSITAR
3. CONSULTAR SALDO 
4. CONSULTAR DATOS
5. CAMBIAR CONTRASEÑA
6. SALIR

DOS METODOS AUXILIARES PARA GUARDAR DATOS EN JSON
PRIMERO LA CLASE USUARIO Y LUEGO LA CLASE CUENTABANCARIA
EL MÉTODO REGISTRAR DEBE TENER OPCIÓN DE SUGERIR CONTRASEÑA ALEATORIA

DEBE CONTENER LA FUNCION main() PARA EJECUTAR EL PROGRAMA
'''

import json
import os
import random as rd
import string as st

class Usuario:
    def __init__(self, nombre, apellido, email, nombre_usuario, contraseña, estado=True):
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.nombre_usuario = nombre_usuario
        self.contraseña = contraseña
        self.estado = estado

    def to_dict(self):
        return {
            'nombre': self.nombre,
            'apellido': self.apellido,
            'email': self.email,
            'nombre_usuario': self.nombre_usuario,
            'contraseña': self.contraseña,
            'estado': self.estado
        }

class CuentaBancaria:
    def __init__(self, usuario, saldo=0.0, estado=True):
        self.usuario = usuario
        self.saldo = saldo
        self.estado = estado

    def to_dict(self):
        return {
            'usuario': self.usuario.to_dict(),
            'saldo': self.saldo,
            'estado': self.estado
        }

class SisATM:
    def __init__(self):
        self.usuarios = []  # Cambiar a una lista para permitir múltiples usuarios
        self.cuentas = []
        self.cuenta_actual = None

    def guardar_datos_json(self):
        try:
            datos = {
                'usuarios': [usuario.to_dict() for usuario in self.usuarios],
                'cuentas': [cuenta.to_dict() for cuenta in self.cuentas]
            }
            with open('atm.json', 'w', encoding='utf-8') as archivo:
                json.dump(datos, archivo, ensure_ascii=False, indent=4)
            print("Datos guardados exitosamente.")
        except Exception as e:
            print(f'Error al guardar datos: {e}')

    def cargar_datos_json(self):
        try:
            if os.path.exists('atm.json'):
                with open('atm.json', 'r', encoding='utf-8') as archivo:
                    datos = json.load(archivo)
                    self.usuarios = [Usuario(**usuario) for usuario in datos['usuarios']]
                    self.cuentas = [CuentaBancaria(Usuario(**cuenta['usuario']), cuenta['saldo'], cuenta['estado']) for cuenta in datos['cuentas']]
        except Exception as e:
            print(f'Error al cargar datos: {e}')

    def generar_contraseña(self, longitud=16):
        caracteres = st.ascii_letters + st.digits + st.punctuation
        return ''.join(rd.choice(caracteres) for _ in range(longitud))

    def solicitar_contraseña_manual(self):
        while True:
            contraseña = input("Ingrese su contraseña: ")
            contraseña_confirmada = input("Confirme su contraseña: ")
            if contraseña == contraseña_confirmada:
                return contraseña
            else:
                print("Las contraseñas no coinciden. Inténtelo de nuevo.")

    def cambiar_contraseña(self, usuario):
        while True:
            try:
                print("¿Desea generar una contraseña aleatoria? (Si/No)")
                opcion = input('Opción: ').strip().lower()

                if opcion == 'si':
                    nueva_contraseña = self.generar_contraseña()
                    print(f"Contraseña generada: {nueva_contraseña}")
                    aceptar = input("¿Desea usar esta contraseña? (Si/No): ").strip().lower()
                    if aceptar == 'si':
                        usuario.contraseña = nueva_contraseña
                        self.guardar_datos_json()
                        print("Contraseña cambiada correctamente.")
                        break
                    else:
                        print("Cambio de contraseña cancelado.")
                        break
                elif opcion == 'no':
                    nueva_contraseña = self.solicitar_contraseña_manual()
                    usuario.contraseña = nueva_contraseña
                    self.guardar_datos_json()
                    print("Contraseña cambiada correctamente.")
                    break
                else:
                    print("Opción no válida.")
            except Exception as e:
                print(f"Ocurrió un error: {e}. Intente nuevamente.")

    def registro_usuario(self):
        """Registra un nuevo usuario en el sistema."""
        try:
            nombre = input("Ingrese su nombre: ")
            apellido = input("Ingrese su apellido: ")
            email = input("Ingrese su email: ")
            nombre_usuario = input("Ingrese su nombre de usuario: ")

            sugerencia = input("¿Desea que el sistema sugiera una contraseña? (Si/No): ").strip().lower()
            if sugerencia == 'si':
                nueva_contraseña = self.generar_contraseña()
                print(f"Contraseña sugerida: {nueva_contraseña}")
                aceptar = input("¿Desea usar esta contraseña? (Si/No): ").strip().lower()
                if aceptar == 'no':
                    nueva_contraseña = self.solicitar_contraseña_manual()
            else:
                nueva_contraseña = self.solicitar_contraseña_manual()

            if not nueva_contraseña:
                print("La contraseña no puede estar vacía. Registro cancelado.")
                return False

            nuevo_usuario = Usuario(nombre, apellido, email, nombre_usuario, nueva_contraseña)
            nueva_cuenta = CuentaBancaria(nuevo_usuario, 0.0)  # Saldo inicial en cero
            self.usuarios.append(nuevo_usuario)
            self.cuentas.append(nueva_cuenta)
            self.guardar_datos_json()
            print("Usuario registrado correctamente.")
            return True
        except Exception as e:
            print(f"Ocurrió un error al registrar al usuario: {e}. Intente nuevamente.")
            return False

    def ingresar_usuario(self):
        try:
            if not self.usuarios:
                print("No hay usuarios registrados.")
                return False
            
            intentos = 3
            while intentos > 0:
                nombre_usuario = input("Ingrese su nombre de usuario: ").strip()
                contraseña = input("Ingrese su contraseña: ").strip()

                for cuenta in self.cuentas:
                    if cuenta.usuario.nombre_usuario == nombre_usuario and cuenta.usuario.contraseña == contraseña:
                        self.cuenta_actual = cuenta
                        print(f"Bienvenido {cuenta.usuario.nombre}")
                        return True
                
                intentos -= 1
                print("Credenciales incorrectas o el usuario no está registrado.")
                
            print("Número máximo de intentos alcanzado. Intente de nuevo más tarde.")
            return False
        except Exception as e:
            print(f"Error al ingresar al sistema: {e}. Intente nuevamente.")

    def depositar(self, cantidad):
        try:
            if self.cuenta_actual:
                self.cuenta_actual.saldo += cantidad
                self.guardar_datos_json()
                print(f'Se ha depositado {cantidad} a la cuenta de {self.cuenta_actual.usuario.nombre}\nSaldo: {self.cuenta_actual.saldo:.2f}')
                return self.cuenta_actual.saldo
            else:
                print("No hay cuentas disponibles.")
        except Exception as e:
            print(f'Error al depositar: {e}')

    def retirar(self, cantidad):
        try:
            if self.cuenta_actual:
                if cantidad <= self.cuenta_actual.saldo:
                    self.cuenta_actual.saldo -= cantidad
                    self.guardar_datos_json()
                    print(f'Se ha retirado {cantidad} de la cuenta de {self.cuenta_actual.usuario.nombre}\nSaldo: {self.cuenta_actual.saldo:.2f}')
                    return self.cuenta_actual.saldo
                else:
                    print('Saldo insuficiente!')
            else:
                print("No hay cuentas disponibles.")
        except Exception as e:
            print(f'Error al retirar: {e}')

    def consultar_saldo(self):
        try:
            if self.cuenta_actual:
                print(f'Saldo: {self.cuenta_actual.saldo:.2f}')
                return self.cuenta_actual.saldo
            else:
                print("No hay cuentas disponibles.")
        except Exception as e:
            print(f'Error al consultar saldo: {e}')

    def mostrar_datos(self):
        try:
            if self.cuenta_actual:
                estado_usuario = 'Activo' if self.cuenta_actual.usuario.estado else 'Inactivo'
                estado_cuenta = 'Activo' if self.cuenta_actual.estado else 'Inactivo'
                print(f'Nombre: {self.cuenta_actual.usuario.nombre}\nApellido: {self.cuenta_actual.usuario.apellido}\nEmail: {self.cuenta_actual.usuario.email}\nNombre de Usuario: {self.cuenta_actual.usuario.nombre_usuario}\nEstado del Usuario: {estado_usuario}\nSaldo: {self.cuenta_actual.saldo:.2f}\nEstado de la Cuenta: {estado_cuenta}')
        except Exception as e:
            print(f'Error al mostrar datos: {e}')











