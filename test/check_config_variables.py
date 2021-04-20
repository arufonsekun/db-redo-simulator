from decouple import config

if __name__ == "__main__":
    user = config("DBUSER")
    password = config("PASSWORD")
    database = config("DATABASE")
    port = config("PORT")

    print("Usuário: {}".format(user))
    print("Password: {}".format(password))
    print("Nome do banco de dados: {}".format(database))
    print("Porta do SGBD: {}".format(port))