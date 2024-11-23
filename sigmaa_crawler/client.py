"""
SIGMAA Crawler
API para la consulta de datos de estudiantes de la Universidad del Caribe, 
obtenidos con su consentimiento del sistema SIGMAA.

Autor: Unicaribe OpenData
Versión: 0.0.1.dev
Contacto: admin@unicaribe.dev

Derechos Reservados © 2024 Unicaribe OpenData. Todos los derechos reservados.

MIT License

Copyright (c) 2024 Unicaribe OpenData

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from itertools import chain
from typing import Literal
from requests import Session
import pandas as pd

from sigmaa_crawler.models.paths import Path


class Client:
    """
    Clase para manejar la conexión con el SIGMAA.
    """

    def __init__(self, user_id: int, password: str) -> None:
        self.user_id = user_id
        self.password = password
        self.session = Session()

    def login(self) -> None:
        """
        Método para iniciar sesión en el SIGMAA.
        """

        credentials = {
            "accion": "login",
            "login": self.user_id,
            "password": self.password,
            "struts.token.name": "token",
            "token": "",
        }

        self.session.get(Path.LOGIN.value, params=credentials)

    def logout(self) -> None:
        """
        Método para cerrar sesión en el SIGMAA.
        """
        self.session.get(Path.LOGOUT.value)

    def get_academic_offer(self, ui_tab: Literal["1", "2", "3"]) -> list[dict]:
        """
        Método para obtener la oferta académica.

        Args:
            ui_tab (Literal["1", "2", "3"]): Pestaña de la oferta académica (1: Secciones, 2: Talleres, 3: Lengua Extranjera).
        """
        # Iniciar sesión
        self.login()

        # Obtener el HTML de la página de la oferta académica.
        response = self.session.get(Path.ACADEMIC_OFFER.value, params={"uiTab": ui_tab})
        # Convertir las tablas de las ofertas en el tab en dataframes.
        tables = pd.read_html(response.text, attrs={"class": "datos"})

        nested_results = []

        # Preprocesar cada tabla de la oferta académica.
        for table in tables:
            # Eliminar columnas adicionales
            trimmed_table = table.iloc[:, :10]
            # Reasignar nombres de columnas
            trimmed_table = trimmed_table.set_axis(
                axis="columns",
                labels=[
                    "Tipo",
                    "Clave",
                    "Sección",
                    "Asignatura",
                    "Lunes",
                    "Martes",
                    "Miércoles",
                    "Jueves",
                    "Viernes",
                    "Sábado",
                ],
            )
            # Convertir tabla a diccionario
            records = trimmed_table.to_dict("records")
            # Separar Asignatura en tres componentes (Asignatura, Docente, Modalidad)
            splitted_data = [record["Asignatura"].split("  ") for record in records]
            # Reasignar los nuevos componentes
            for subject_index, subject in enumerate(records):
                try:
                    subject["Asignatura"] = splitted_data[subject_index][0]
                    subject["Docente"] = splitted_data[subject_index][1]
                    subject["Modalidad"] = splitted_data[subject_index][2]
                except IndexError:
                    print("Error en el split de la asignatura")
                    print(f"Subject Index: {subject_index}")
                    print(splitted_data[subject_index], end="\n\n")
            # Agregar a la lista de resultados de tablas procesadas
            nested_results.append(records)

        # Aplanar los resultados anidados
        flat_list = list(chain.from_iterable(nested_results))

        # Crear una estructura de tablas
        result = {"ui_tab": ui_tab, "results": flat_list}

        # Cerrar sesión
        self.logout()

        return result
