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

def filter_by_type(regulon, regulator_type):
    """
    Filtra reguladores por tipo.

    Responsabilidad:
        Conservar únicamente los TFs cuyo tipo de regulación coincide con
        el valor solicitado.

    Entrada:
        regulon (dict): Diccionario con la información de cada TF.
        regulator_type (str | None): Tipo solicitado: `activador`,
            `represor`, `dual` o None.

    Salida:
        dict: Nuevo diccionario con los TFs que cumplen el criterio.
    """
    if regulator_type is None:
        return regulon

    filtered = {}
    for TF, data in regulon.items():
        current_type = get_regulator_type(data)
        if current_type == regulator_type:
            filtered[TF] = data

    return filtered
def filter_by_min_genes(regulon, min_genes):
    """
    Filtra un regulón por número mínimo de genes regulados.

    Responsabilidad:
        Conservar únicamente los TFs que regulan al menos `min_genes` genes.

    Entrada:
        regulon (dict): Diccionario con la información de cada TF.
        min_genes (int): Número mínimo de genes regulados requerido.

    Salida:
        dict: Nuevo diccionario con los TFs que cumplen el criterio.
    """
    filtered = {}

    for TF, data in regulon.items():
        if len(data["genes"]) >= min_genes:
            filtered[TF] = data

    return filtered


