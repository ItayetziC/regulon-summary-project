from src.io_utils import load_interactions


def test_load_interactions_ignores_invalid_lines(tmp_path):
    # Esta prueba verifica que load_interactions solo conserve
    # interacciones válidas desde un archivo TSV temporal.

    input_file = tmp_path / "interactions.tsv"

    input_file.write_text(
        "# comentario\n"
        "regulatorId\tregulatorName\tX\tX\tgeneName\teffect\tX\n"
        "id1\tCRP\tX\tX\tlacZ\t+\tX\n"
        "linea_invalida\n"
        "id2\tFNR\tX\tX\tnarG\t-\tX\n",
        encoding="utf-8",
    )

    interactions = load_interactions(input_file)

    assert interactions == [("CRP", "lacZ", "+"),("FNR", "narG", "-"),]

def test_load_interactions_handles_empty_file(tmp_path):
    # Esta prueba verifica que load_interactions maneje correctamente
    # un archivo vacío sin lanzar errores.

    input_file = tmp_path / "empty.tsv"
    input_file.write_text("", encoding="utf-8")

    interactions = load_interactions(input_file)

    assert interactions == []
def test_load_interactions_preserves_act_repres_effect(tmp_path):
    # Esta prueba verifica que load_interactions conserve el efecto "+-"
    # para interacciones que lo tengan.

    input_file = tmp_path / "act_repres.tsv"

    input_file.write_text(
        "regulatorId\tregulatorName\tX\tX\tgeneName\teffect\tX\n"
        "id1\tAraC\tX\tX\taraB\t+-\tX\n",
        encoding="utf-8",
    )

    interactions = load_interactions(input_file)

    assert interactions == [("AraC", "araB", "+-")]

def test_load_interactions_ignores_lines_with_few_columns(tmp_path):
    # Esta prueba verifica que load_interactions ignore líneas que no tengan
    # suficientes columnas para ser consideradas válidas.

    input_file = tmp_path / "few_columns.tsv"

    input_file.write_text(
        "regulatorId\tregulatorName\tX\tX\tgeneName\teffect\tX\n"
        "id1\tCRP\n"  # Línea con pocas columnas
        "id2\tFNR\tX\tX\tnarG\t-\tX\n",
        encoding="utf-8",
    )

    interactions = load_interactions(input_file)

    assert interactions == [("FNR", "narG", "-")]

def test_load_interactions_empty_output_file():
    # Esta prueba verifica que load_interactions lance un ValueError
    # cuando se le proporciona una ruta de archivo vacía.

    try:
        load_interactions("")
    except ValueError as e:
        assert str(e) == "filename vacío"
    else:
        assert False, "Se esperaba un ValueError para input_file vacío"
