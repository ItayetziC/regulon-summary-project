from src.core import get_regulator_type, build_regulon


def test_get_regulator_type_returns_activador():
    # Esta prueba verifica que un regulador con genes activados
    # y sin genes reprimidos sea clasificado como "activador".

    data = {
        "genes": ["lacZ", "araB"],
        "activados": 2,
        "reprimidos": 0,
    }

    result = get_regulator_type(data)

    assert result == "activador"


def test_get_regulator_type_returns_represor():
    # Esta prueba verifica que un regulador sin genes activados
    # y con genes reprimidos sea clasificado como "represor".

    data = {
        "genes": ["trpA"],
        "activados": 0,
        "reprimidos": 1,
    }

    result = get_regulator_type(data)

    assert result == "represor"


def test_get_regulator_type_returns_dual():
    # Esta prueba verifica que un regulador con genes activados
    # y genes reprimidos sea clasificado como "dual".

    data = {
        "genes": ["lacZ", "galE"],
        "activados": 1,
        "reprimidos": 1,
    }

    result = get_regulator_type(data)

    assert result == "dual"

def test_get_same_gene_for_regulator():
    # Esta prueba verifica que si un mismo gen aparece más de una vez para el mismo regulador,
    # solo se cuente una vez en la lista de genes, pero se sumen correctamente los conteos de activados y reprimidos.

    data = {
        "genes": ["lacZ", "lacZ", "lacA"],  # El mismo gen aparece dos veces
        "activados": 2,
        "reprimidos": 2,
    }

    result = get_regulator_type(data)

    assert result == "dual"

def test_build_regulon_ignores_duplicate_genes():
    # Esta prueba verifica que build_regulon construya el regulon correctamente
    # incluso si hay interacciones duplicadas para el mismo regulador y gen.

    interactions = [
        ("CRP", "lacZ", "+"),
        ("CRP", "lacZ", "+"),  # Duplicado
        ("CRP", "lacA", "-"),
        ("FNR", "narG", "-"),
        ("FNR", "narG", "-"),  # Duplicado
    ]

    regulon = build_regulon(interactions)

    assert set(regulon["CRP"]["genes"]) == {"lacZ", "lacA"}
    assert regulon["CRP"]["activados"] == 2
    assert regulon["CRP"]["reprimidos"] == 1

    assert set(regulon["FNR"]["genes"]) == {"narG"}
    assert regulon["FNR"]["activados"] == 0
    assert regulon["FNR"]["reprimidos"] == 2
    
def test_build_regulon_empty_interactions():
    # Esta prueba verifica que build_regulon devuelva un regulon vacío
    # cuando se le proporciona una lista vacía de interacciones.

    interactions = []

    regulon = build_regulon(interactions)

    assert regulon == {}

def test_build_regulon_multiple_regulators_same_gene():
    # Esta prueba verifica que build_regulon maneje correctamente el caso
    # en el que múltiples reguladores afectan al mismo gen.

    interactions = [
        ("CRP", "lacZ", "+"),
        ("FNR", "lacZ", "-"),
        ("AraC", "lacZ", "+-"),
    ]

    regulon = build_regulon(interactions)

    assert set(regulon["CRP"]["genes"]) == {"lacZ"}
    assert regulon["CRP"]["activados"] == 1
    assert regulon["CRP"]["reprimidos"] == 0

    assert set(regulon["FNR"]["genes"]) == {"lacZ"}
    assert regulon["FNR"]["activados"] == 0
    assert regulon["FNR"]["reprimidos"] == 1

    assert set(regulon["AraC"]["genes"]) == {"lacZ"}
    assert regulon["AraC"]["activados"] == 1
    assert regulon["AraC"]["reprimidos"] == 1
