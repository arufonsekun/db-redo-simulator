from decouple import config

if __name__ == "__main__":
    user = config("USER")
    password = config("PASSWORD")
    database = config("DATABASE")
    port = config("PORT")

    print(port)