from .core import get_regulator_type

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


