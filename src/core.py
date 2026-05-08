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
def get_regulator_type(data):
    """
    Determina el tipo de regulador.

    Responsabilidad:
        Clasificar un TF como activador, represor o dual según sus conteos
        de genes activados y reprimidos.

    Entrada:
        data (dict): Diccionario con las claves `activados` y `reprimidos`.

    Salida:
        str: Tipo de regulación: `activador`, `represor` o `dual`.
    """
    activados = data["activados"]
    reprimidos = data["reprimidos"]

    if activados > 0 and reprimidos > 0:
        return "dual"
    elif activados > 0:
        return "activador"
    else:
        return "represor"
