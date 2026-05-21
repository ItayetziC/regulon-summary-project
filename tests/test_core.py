from src.core import get_regulator_type


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

