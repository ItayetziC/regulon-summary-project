import os
import argparse

from filters import filter_by_min_genes, filter_by_type, get_regulator_type

# =========================================
# Responsabilidad: Leer el archivo de interacciones y construir una estructura de datos que contenga la información relevante para cada TF.
# Entrada: Archivo TSV con interacciones entre reguladores y genes.
# Salida: lista de interacciones (TF, gen, efecto).
# =========================================
def load_interactions(filename):
    """
    Carga las interacciones desde un archivo TSV.

    Args:
        filename (str): Ruta del archivo de interacciones.

    Returns:
        list[tuple[str, str, str]]: Lista de interacciones (TF, gen, efecto).
    """
    interactions = []

    if not filename:
        raise ValueError("filename vacío")

    with open(filename) as f:
        for line in f:
            line = line.strip()

            # Ignorar líneas vacías
            if not line:
                continue

            # Ignorar comentarios
            if line.startswith("#"):
                continue

            # Ignorar encabezado
            if line.startswith("1)regulatorId"):
                continue

            fields = line.split("\t")

            # Validar número mínimo de columnas
            if len(fields) <= 6:
                continue

            TF = fields[1]
            gene = fields[4]
            effect = fields[5]

            # Validar effect
            if effect not in ["+", "-", "+-"]:
                continue

            interactions.append((TF, gene, effect))

    return interactions


# =========================================
# Responsabilidad: Construir una estructura de datos que resuma la información de cada TF.
# Entrada: lista de interacciones (TF, gen, efecto).
# Salida: diccionario con clave TF y valores que contienen genes únicos y conteos de activación/represión.
# =========================================
def build_regulon(interactions):
    """Construye una estructura de datos que resume la información de cada TF.

    Args:
        interactions (list[tuple[str, str, str]]): Lista de interacciones (TF, gen, efecto).

    Returns:
        dict: Diccionario con clave TF y valores que contienen la lista de genes regulados,
            y los conteos de activados y reprimidos.
    """
    regulon = {}

    for TF, gene, effect in interactions:
        if TF not in regulon:
            regulon[TF] = {"genes": [], "activados": 0, "reprimidos": 0}

        if gene not in regulon[TF]["genes"]:
            regulon[TF]["genes"].append(gene)

        if effect == "+":
            regulon[TF]["activados"] += 1
        elif effect == "-":
            regulon[TF]["reprimidos"] += 1
        elif effect == "+-":
            regulon[TF]["activados"] += 1
            regulon[TF]["reprimidos"] += 1

    return regulon

def write_summary(regulon, output_file):
    """Escribe el resumen del regulon a un archivo TSV.

    Args:
        regulon (dict): Diccionario con información del regulon.
        output_file (str): Ruta del archivo de salida.
    """
    if not output_file:
        raise ValueError("output_file vacío")

    if regulon is None:
        raise ValueError("regulon no puede ser None")

    dirpath = os.path.dirname(output_file)
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)

    with open(output_file, "w") as out:
        out.write("TF\tTotal genes\tActivados\tReprimidos\tTipo\tLista de genes\n")

        for TF in sorted(regulon):
            genes = sorted(regulon[TF]["genes"])
            total = len(genes)
            activados = regulon[TF]["activados"]
            reprimidos = regulon[TF]["reprimidos"]
            tipo = get_regulator_type(regulon[TF])
            lista_genes = ", ".join(genes)
            out.write(
                f"{TF}\t{total}\t{activados}\t{reprimidos}\t{tipo}\t{lista_genes}\n"
            )


def write_sif(interactions, output_file):
    """Escribe las interacciones en formato SIF.

    Responsabilidad:
        Convertir las interacciones regulador-gen al formato SIF compatible
        con herramientas de visualización de redes como Cytoscape.

    Entrada:
        interactions (list[tuple[str, str, str]]): Lista de interacciones
            en forma (TF, gen, efecto).
        output_file (str): Ruta del archivo de salida.
    """
    if not output_file:
        raise ValueError("output_file vacío")

    dirpath = os.path.dirname(output_file)
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)

    with open(output_file, "w") as out:
        for TF, gene, effect in interactions:
            if effect == "+":
                interaction = "activates"
            elif effect == "-":
                interaction = "represses"
            else:
                interaction = "regulates"

            out.write(f"{TF}\t{interaction}\t{gene}\n")


def parse_arguments():
    """Define y lee los argumentos de línea de comandos."""
    parser = argparse.ArgumentParser(
        description="Genera un resumen de regulones a partir de un archivo TSV"
    )

    parser.add_argument("input_file", help="Archivo de entrada con interacciones")
    parser.add_argument("output_file", help="Archivo de salida para el resumen")

    parser.add_argument(
        "--min_genes",
        type=int,
        default=0,
        help="Filtrar TFs con al menos este número de genes",
    )

    parser.add_argument(
        "--type",
        choices=["activador", "represor", "dual"],
        help="Filtrar TFs por tipo de regulación",
    )

    parser.add_argument(
        "--format",
        choices=["summary", "sif"],
        default="summary",
        help="Formato de salida: summary o sif",
    )

    return parser.parse_args()


def filter_interactions_by_regulon(interactions, regulon):
    """
    Filtra las interacciones por regulón.

    Responsabilidad:
        Conservar únicamente las interacciones cuyos TFs aparecen en el regulón filtrado.

    Entrada:
        interactions (list[tuple[str, str, str]]): Lista de interacciones (TF, gen, efecto).
        regulon (dict): Diccionario con los TFs válidos después del filtrado.

    Salida:
        list[tuple[str, str, str]]: Lista de interacciones filtradas.
    """
    return [interaction for interaction in interactions if interaction[0] in regulon]


def main():
    """Función principal del programa."""

    args = parse_arguments()
    input_file = args.input_file
    output_file = args.output_file
    min_genes = args.min_genes
    regulator_type = args.type
    output_format = args.format

    if min_genes < 0:
        print("Error: min_genes debe ser mayor o igual a 0.")
        exit(1)

    try:
        interactions = load_interactions(input_file)
    except FileNotFoundError:
        print(f"Error: no existe el archivo de entrada -> {input_file}")
        exit(1)
    except PermissionError:
        print(f"Error: no hay permisos para leer el archivo -> {input_file}")
        exit(1)
    except OSError as e:
        print(f"Error al leer el archivo ({input_file}): {e}")
        exit(1)

    if not interactions:
        print("Advertencia: no se encontraron interacciones válidas.")

    regulon = build_regulon(interactions)
    regulon = filter_by_min_genes(regulon, min_genes)
    regulon = filter_by_type(regulon, regulator_type)

    if not regulon:
        print("Advertencia: no hay reguladores que cumplan el filtro.")

    try:
        if output_format == "summary":
            write_summary(regulon, output_file)
        else:
            filtered_interactions = filter_interactions_by_regulon(
                interactions, regulon
            )
            write_sif(filtered_interactions, output_file)
    except PermissionError:
        print(f"Error: no hay permisos para escribir -> {output_file}")
        exit(1)
    except IsADirectoryError:
        print(f"Error: la ruta de salida es un directorio -> {output_file}")
        exit(1)
    except OSError as e:
        print(f"Error al escribir el archivo ({output_file}): {e}")
        exit(1)


if __name__ == "__main__":
    main()
