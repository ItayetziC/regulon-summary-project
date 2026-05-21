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