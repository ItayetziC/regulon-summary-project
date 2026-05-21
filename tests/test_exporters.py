from src.exporters import write_sif


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
