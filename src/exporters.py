import os
from core import get_regulator_type

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

