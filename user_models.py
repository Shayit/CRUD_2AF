from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from config import Config
import pyotp
import qrcode
from sqlalchemy import create_engine
import getpass
import os

Base = declarative_base()

# URL de la base de datos configurada en config.py
Database_URL = Config.Database_URL

# Desactivar el echo para que no se muestren las consultas en la consola
engine = create_engine(Database_URL, echo=False)
Session = sessionmaker(bind=engine)

# Definición de la clase User para la tabla de usuarios
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    secret = Column(String(100), nullable=False)
    role = Column(String(20), nullable=False, default='cliente')

# Función para crear las tablas
def create_tables():
    Base.metadata.create_all(engine)

# Función para registrar un nuevo usuario
def register_user():
    username = input("Introduce tu nombre de usuario: ")
    password = getpass.getpass("Introduce tu contraseña: ")

    # Generar una clave secreta para 2FA
    secret = pyotp.random_base32()
    
    # Guardar el usuario y la clave secreta en la base de datos
    new_user = User(username=username, password=password, secret=secret)
    session = Session()
    session.add(new_user)
    session.commit()

    print("¡Usuario registrado exitosamente!")

    # Generar el enlace de configuración 2FA
    otp_auth_url = pyotp.totp.TOTP(secret).provisioning_uri(name=username, issuer_name="MiApp")
    print(f"Escanea este código QR en tu aplicación de autenticación: {otp_auth_url}")
    
    # Generar el código QR
    img = qrcode.make(otp_auth_url)
    img.show()
    input("Escribe cualquier tecla para continuar")
    os.system('cls')
    

# Función para iniciar sesión (verificación de contraseña y 2FA)
def login_user():
    username = input("Introduce tu nombre de usuario: ")
    password = getpass.getpass("Introduce tu contraseña: ")

    session = Session()
    user = session.query(User).filter_by(username=username).first()

    if user and user.password == password:
        print("Contraseña correcta, ahora ingresa el código de autenticación 2FA:")
        otp = input("Código 2FA: ")

        if pyotp.TOTP(user.secret).verify(otp):
            print("¡Inicio de sesión exitoso!")
        else:
            print("Código 2FA incorrecto.")
    else:
        print("Usuario o contraseña incorrectos.")

# Función para editar un usuario (solo un admin puede hacerlo)
def edit_user():
    admin_password = getpass.getpass("Introduce la contraseña de administrador: ")

    # Verificar si la contraseña del admin es correcta (esto debe ser implementado adecuadamente)
    if admin_password == "adminpassword":
        username = input("Introduce el nombre de usuario a editar: ")
        session = Session()
        user = session.query(User).filter_by(username=username).first()

        if user:
            new_username = input(f"Introduce el nuevo nombre de usuario (actual: {user.username}): ")
            new_password = getpass.input(f"Introduce la nueva contraseña (actual: {user.password}): ")

            user.username = new_username
            user.password = new_password

            session.commit()
            print(f"Usuario {username} editado correctamente.")
        else:
            print("Usuario no encontrado.")
    else:
        print("Contraseña de administrador incorrecta.")

# Función para eliminar un usuario (solo un admin puede hacerlo)
def delete_user():
    admin_password = getpass.input("Introduce la contraseña de administrador: ")

    # Verificar si la contraseña del admin es correcta (esto debe ser implementado adecuadamente)
    if admin_password == "adminpassword":
        username = input("Introduce el nombre de usuario a eliminar: ")
        session = Session()
        user = session.query(User).filter_by(username=username).first()

        if user:
            session.delete(user)
            session.commit()
            print(f"Usuario {username} eliminado correctamente.")
        else:
            print("Usuario no encontrado.")
    else:
        print("Contraseña de administrador incorrecta.")

# Función para mostrar los usuarios (solo un admin puede verlo)
def list_users():
    admin_password = getpass.getpass("Introduce la contraseña de administrador: ")

    # Verificar si la contraseña del admin es correcta
    if admin_password == "adminpassword":
        session = Session()
        users = session.query(User).all()

        if users:
            for user in users:
                print(f"ID: {user.id}, Usuario: {user.username}, Rol: {user.role}")
        else:
            print("No hay usuarios registrados.")
    else:
        print("Contraseña de administrador incorrecta.")
