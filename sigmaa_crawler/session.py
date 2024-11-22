"""Test"""
import requests
from bs4 import BeautifulSoup, Tag

from sigmaa_crawler.models.user import User


def element_to_dict(element):
    """
    Convierte un elemento HTML a un diccionario de Python.
    """
    result = {
        "name": element.name,
        "text": element.get_text(strip=True) if isinstance(element, Tag) else str(element),
        "attributes": element.attrs if isinstance(element, Tag) else {},
        "children": []
    }
    
    if isinstance(element, Tag):
        for child in element.children:
            if isinstance(child, Tag):
                result["children"].append(element_to_dict(child))
            else:
                result["children"].append({
                    "text": child.strip()
                })
    
    return result


class Client:
    """
    Modelo de clase para interactuar con la sesión de SIGMAA.
    """

    def __init__(self, user: User) -> None:
        self.credentials = user
        self._token = None
        self.cookies = None

    def get_token(self) -> str:
        """
        Permite obtener el token de la página de login del SIGMAA.
        """ 
        try:
            response = requests.get(Path.SESSION_LOGIN.value)
            response.raise_for_status()
        except requests.RequestException as e:
            raise Exception(f"Error al obtener el token: {e}")

        soup = BeautifulSoup(response.text, "html.parser")
        token_element = soup.find("input", {"name": "token"})
        if token_element:
            # Obtener el token
            self._token = token_element.get("value")
            
            # Obtener las cookies del header
            jsessionid = response.cookies.get_dict()["JSESSIONID"]
            serverid = response.cookies.get_dict()["SERVERID"]
            self.cookies = f"JSESSIONID={jsessionid};SERVERID={serverid}"

            print("Cookies obtenidas con éxito")
            print(self.cookies)
        else:
            raise Exception("No se pudo obtener el token")

    def login(self) -> None:
        """
        Permite iniciar sesión en el SIGMAA usando las credenciales del estudiante.
        """
        if not self._token:
            self.get_token()

            print("Token obtenido con éxito")
            print(self._token)

        payload = {
            "accion": "login",
            "login": self.credentials.user_id,
            "password": self.credentials.password,
            "struts.token.name": "token",
            "token": self._token
        }

        try:
            response = requests.request(
                "GET", 
                Path.SESSION_LOGIN.value, 
                headers={"Cookie": self.cookies},
                data=payload,
                files=[]
            )

            response.raise_for_status()

            return response.text
        
        except requests.RequestException as e:
            raise Exception(f"Error al iniciar sesión: {e}")

    def logout(self):
        """
        Permite cerrar sesión en el SIGMAA.
        """
        try:
            response = requests.get(Path.SESSION_LOGOUT.value, headers={"Cookie": self.cookies})
            response.raise_for_status()

            # return response.text
        
        except requests.RequestException as e:
            raise Exception(f"Error al cerrar sesión: {e}")
    
    def get_academic_offer(self):
        """
        Permite obtener la oferta académica de la universidad.

        Args:
            uiTab (int): El número de la pestaña de la oferta académica.
        """
        try:
            response = requests.request(
                "GET", 
                Path.ACADEMIC_OFFER.value,
                headers={"Cookie": self.cookies}, 
                data={"uiTab": "1"}, 
                files=[]
            )

            response.raise_for_status()

            print(response.text)

            soup = BeautifulSoup(response.text, "html.parser")
            return element_to_dict(soup)
        
        except requests.RequestException as e:
            raise Exception(f"Error al obtener la oferta académica: {e}")
    
    def get_kardex(self):
        """
        Permite obtener el kardex del estudiante.
        """
        try:
            response = requests.get(Path.KARDEX.value)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            return element_to_dict(soup)
        except requests.RequestException as e:
            raise Exception(f"Error al obtener el kardex: {e}")

        # return response.text
    
    def get_academic_history(self):
        """
        Permite obtener el historial académico del estudiante.
        """
        try:
            response = requests.get(Path.ACADEMIC_HISTORY.value)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            return element_to_dict(soup)
        except requests.RequestException as e:
            raise Exception(f"Error al obtener el historial académico: {e}")

        # return response.text
    
    def get_timetable_boletin(self):
        """
        Permite obtener el boletín de carga del estudiante.
        """
        try:
            response = requests.get(Path.TIMETABLE_BOLETIN.value)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            return element_to_dict(soup)
        except requests.RequestException as e:
            raise Exception(f"Error al obtener el boletín de carga: {e}")

        # return response.text
    
    def get_personal_info(self):
        """
        Permite obtener la información personal del estudiante.
        """
        try:
            response = requests.get(Path.PERSONAL_INFO.value)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            return element_to_dict(soup)
        except requests.RequestException as e:
            raise Exception(f"Error al obtener la información personal: {e}")

        # return response.text
    
    def get_payment_system(self):
        """
        Permite obtener el sistema de pagos del estudiante.
        """
        try:
            response = requests.get(Path.PAYMENT_SYSTEM.value)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            return element_to_dict(soup)
        except requests.RequestException as e:
            raise Exception(f"Error al obtener el sistema de pagos: {e}")

        # return response.text