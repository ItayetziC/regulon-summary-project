from src.exporters import write_sif, write_summary
def test_write_summary_writes_expected_header(tmp_path):
    # Esta prueba verifica que write_summary escriba el encabezado correcto
    # en el archivo de salida.

    regulon = {
        "CRP": {"genes": {"lacZ"}, "activados": 1, "reprimidos": 0},
    }
    output_file = tmp_path / "summary.tsv"

    write_summary(regulon, output_file)

    content = output_file.read_text()

    assert content.startswith("TF\tTotal genes\tActivados\tReprimidos\tTipo\tLista de genes\n")

def test_write_summary_writes_genes_in_sorted_order(tmp_path):
    # Esta prueba verifica que write_summary escriba los genes en orden alfabético
    # en la lista de genes del archivo de salida.

    regulon = {
        "CRP": {"genes": {"lacZ", "araB"}, "activados": 2, "reprimidos": 0},
    }
    output_file = tmp_path / "summary.tsv"

    write_summary(regulon, output_file)

    content = output_file.read_text()

    assert "CRP\t2\t2\t0\tactivador\taraB, lacZ\n" in content

def test_write_summary_raises_error_if_regulon_is_none(tmp_path):
    # Esta prueba verifica que write_summary genere un error si el argumento
    # regulon es None.

    output_file = tmp_path / "summary.tsv"

    try:
        write_summary(None, output_file)
        assert False, "Expected ValueError when regulon is None"
    except ValueError as e:
        assert str(e) == "regulon no puede ser None"

def test_write_sif_raises_error_if_output_file_is_empty():
    # Esta prueba verifica que write_sif genere un error si el argumento
    # output_file es una cadena vacía.

    interactions = [("CRP", "lacZ", "+")]

    try:
        write_sif(interactions, "")
        assert False, "Expected ValueError when output_file is empty"
    except ValueError as e:
        assert str(e) == "filename vacío"

def test_write_sif_writes_expected_interaction_labels(tmp_path):
    # Esta prueba verifica que write_sif convierta los efectos
    # +, - y +- en etiquetas SIF correctas.

    interactions = [
        ("CRP", "lacZ", "+"),
        ("FNR", "narG", "-"),
        ("AraC", "araB", "+-"),
    ]
    output_file = tmp_path / "network.sif"

    write_sif(interactions, output_file)

    content = output_file.read_text()

    assert "CRP	activates	lacZ" in content
    assert "FNR	represses	narG" in content
    assert "AraC	regulates	araB" in content


