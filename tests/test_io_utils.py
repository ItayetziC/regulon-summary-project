from src.io_utils import load_interactions


def test_load_interactions_ignores_invalid_lines(tmp_path):
    # Esta prueba verifica que load_interactions solo conserve
    # interacciones válidas desde un archivo TSV temporal.

    input_file = tmp_path / "interactions.tsv"

    input_file.write_text(
        "# comentario"
        "1)regulatorId	regulatorName	X	X	geneName	effect	X"
        "id1	CRP	X	X	lacZ	+	X"
        "id2	FNR	X	X	narG	-	X"
        "id3	BAD	X	X	geneX	?	X"
    )

    interactions = load_interactions(input_file)

    assert interactions == [
        ("CRP", "lacZ", "+"),
        ("FNR", "narG", "-"),
    ]