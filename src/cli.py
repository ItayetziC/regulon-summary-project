import argparse
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
