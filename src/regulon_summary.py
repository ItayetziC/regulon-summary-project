import os

from .filters import filter_by_min_genes, filter_by_type, filter_interactions_by_regulon
from .core import build_regulon
from .exporters import write_summary, write_sif
from .io_utils import load_interactions
from .cli import parse_arguments

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
            filtered_interactions = filter_interactions_by_regulon(interactions, regulon)            
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
