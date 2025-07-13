import pandas as pd
import re


def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.


    """
    # Leer el archivo y omitir las primeras 4 líneas de cabecera
    with open("files/input/clusters_report.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()[4:]

    # Lista para almacenar los registros de cada cluster
    records = []
    current_record = None

    # Iterar sobre cada línea del archivo
    for line in lines:
        # Usar una expresión regular para detectar si la línea es el inicio de un nuevo cluster
        # La expresión captura los 3 primeros campos y el inicio de las palabras clave
        match = re.match(r"^\s*(\d+)\s+(\d+)\s+([\d,]+\s*%)\s+(.*)", line)

        if match:
            # Si es un nuevo cluster, se guarda el registro anterior si existe
            if current_record:
                records.append(current_record)

            # Se extraen los datos del nuevo cluster
            cluster = int(match.group(1))
            cantidad = int(match.group(2))
            porcentaje_str = match.group(3).replace(",", ".").replace("%", "").strip()
            porcentaje = float(porcentaje_str)
            keywords_line = match.group(4)

            # Se inicializa el nuevo registro
            current_record = [cluster, cantidad, porcentaje, keywords_line]

        elif current_record and line.strip():
            # Si no es una nueva línea de cluster y no está vacía,
            # es una continuación de las palabras clave. Se añade al registro actual.
            current_record[3] += " " + line.strip()

    # Asegurarse de guardar el último registro leído
    if current_record:
        records.append(current_record)

    # Nombres de las columnas según los requerimientos
    column_names = [
        "cluster",
        "cantidad_de_palabras_clave",
        "porcentaje_de_palabras_clave",
        "principales_palabras_clave",
    ]
    
    # Crear un DataFrame preliminar
    df = pd.DataFrame(records, columns=column_names)

    # Función para limpiar y formatear la columna de palabras clave
    def clean_and_format_keywords(text):
        # 1. Normalizar todos los espacios (incluidos saltos de línea) a un solo espacio
        text = re.sub(r"\s+", " ", text).strip()
        # 2. Eliminar el punto final si existe
        if text.endswith("."):
            text = text[:-1]
        # 3. Dividir el texto por las comas para obtener las frases clave
        phrases = text.split(',')
        # 4. Limpiar los espacios de cada frase
        cleaned_phrases = [phrase.strip() for phrase in phrases]
        # 5. Unir las frases con ", " como separador
        return ", ".join(cleaned_phrases)

    # Aplicar la función de limpieza a la columna de palabras clave
    df["principales_palabras_clave"] = df["principales_palabras_clave"].apply(
        clean_and_format_keywords
    )

    return df