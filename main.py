import requests
from sigmaa_crawler.models import User
from pydantic import ValidationError
from bs4 import BeautifulSoup

base_url = "https://uclb.ucaribe.edu.mx/sigmaav2/"

def get_token() -> str:
    """
    Permite obtener el token de la página de login del SIGMAA.
    """ 
    response = requests.request(
        "GET", 
        base_url + "sistema/login"
    )

    soup = BeautifulSoup(response.text, "html.parser")
    token_element = soup.find("input", {"name": "token"})
    if token_element:
        token_value = token_element.get("value")
        return token_value
    else:
        raise Exception("No se pudo obtener el token")
    

def login(credentials: User, token: str) -> None:
    """
    Permite iniciar sesión en el SIGMAA usando las credenciales del estudiante.

    Args: 
        credentials (User): Credenciales del estudiante.
        token (str): Token obtenido de la página de login del SIGMAA.
    """
    
    print(f"Token obtenido con get_token: {token}")
    print(credentials.matricula, credentials.contraseña)

    payload = {
        "accion": "login",
        "login": credentials.matricula,
        "password": credentials.contraseña,
        "struts.token.name": "token",
        "token": token
    }

    print(f"Payload: {payload}")

    response = requests.request(
        "POST", 
        base_url + "sistema/login",
        data=payload,
        files=[]
    )

    print(response.text)

def logout():
    """
    Permite cerrar sesión en el SIGMAA.
    """
    
    response = requests.request(
        "GET",
        base_url + "sistema/loginInicio?acción=logout"
    )

    return response.text

if __name__ == "__main__":
    try:
        # Se obtiene el token de la página
        token = get_token()
        print(f"Token obtenido con get_token: {token}")

        # Se solicitan las credenciales del estudiante por consola
        user = input("Matrícula: ")
        password = input("Contraseña: ")

        # Se crea una instancia de User con las credenciales del estudiante
        credentials = User(
            matricula=user,
            contraseña=password
        )

        # Se inicia sesión en el SIGMAA
        response = login(credentials, token)
        # El resultado debe ser un HTML con la página dentro del SIGMAA y la sesión iniciada
        print(response)

        # Se cierra sesión en el SIGMAA
        response = logout()
        print(response)

        
    except ValidationError as e:
        print(e)
