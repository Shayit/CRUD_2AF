import os

from user_models import register_user, login_user, edit_user, delete_user, list_users,create_tables

def main():
    create_tables()
    
    print("\nSeleccione una opción:")
    print("1. Registrar Usuario")
    print("2. Iniciar sesión")
    print("3. Editar Usuario (Admin)")
    print("4. Eliminar Usuario (Admin)")
    print("5. Ver Usuarios (Admin)")
    print("6. Salir\n")

    option = input("Opción: ")

    if option == "1":
        register_user()
    elif option == "2":
        login_user()
    elif option == "3":
        edit_user()
    elif option == "4":
        delete_user()
    elif option == "5":
        list_users()
    elif option == "6":
        print("Saliendo...")
        os.system('exit')
    else:
        print("Opción no válida.")

main()

if __name__ == "__main__":
    main()
