"""Test"""
from enum import Enum

class Path(str, Enum):
    """
    Enumeración de las rutas de la página del SIGMAA.
    """
    BASE = "https://uclb.ucaribe.edu.mx/sigmaav2"
    LOGIN = "https://uclb.ucaribe.edu.mx/sigmaav2/sistema/login"
    LOGIN_PAGE = "https://uclb.ucaribe.edu.mx/sigmaav2/sistema/loginInicio"
    ACADEMIC_OFFER = "https://uclb.ucaribe.edu.mx/sigmaav2/inscripciones/OfertaEducativa"
    KARDEX = "https://uclb.ucaribe.edu.mx/sigmaav2/calificaciones/Cardex"
    ACADEMIC_HISTORY = "https://uclb.ucaribe.edu.mx/sigmaav2/calificaciones/Historial"
