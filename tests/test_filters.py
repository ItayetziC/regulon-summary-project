from src.filters import filter_by_min_genes, filter_by_type

def test_filter_by_min_genes_keeps_only_regulators_with_enough_genes():
    # Esta prueba verifica que solo permanezcan los reguladores
    # que tienen al menos el número mínimo de genes indicado.

    regulon = {
        "CRP": {
            "genes": ["lacZ", "araB"],
            "activados": 2,
            "reprimidos": 0,
        },
        "FNR": {
            "genes": ["narG"],
            "activados": 0,
            "reprimidos": 1,
        },
    }

    filtered = filter_by_min_genes(regulon, min_genes=2)

    assert "CRP" in filtered
    assert "FNR" not in filtered
    assert len(filtered) == 1

def test_filter_by_type_activador():
    # Esta prueba verifica que el filtrado por tipo de regulador sea activador.
    regulon = {
        "CRP": {
            "genes": ["lacZ", "araB"],
            "activados": 2,
            "reprimidos": 0,
        },
        "FNR": {
            "genes": ["narG"],
            "activados": 0,
            "reprimidos": 1,
        },
        "ArcA": {
            "genes": ["cyoA", "cyoB"],
            "activados": 0,
            "reprimidos": 2,
        },
    }

    filtered = filter_by_type(regulon, "activador")
    assert "CRP" in filtered
    assert "FNR" not in filtered    
    assert "ArcA" not in filtered

def test_filter_by_type_represor():
    # Esta prueba verifica que el filtrado por tipo de regulador sea represor.
    regulon = {
        "CRP": {
            "genes": ["lacZ", "araB"],
            "activados": 2,
            "reprimidos": 0,
        },
        "FNR": {
            "genes": ["narG"],
            "activados": 0,
            "reprimidos": 1,
        },
        "ArcA": {
            "genes": ["cyoA", "cyoB"],
            "activados": 1,
            "reprimidos": 1,
        },
    }
    filtered = filter_by_type(regulon, "represor")
    assert "CRP" not in filtered
    assert "FNR" in filtered    
    assert "ArcA" not in filtered

def test_filter_by_type_dual():
    # Esta prueba verifica que el filtrado por tipo de regulador sea dual.
    regulon = {
        "CRP": {
            "genes": ["lacZ", "araB"],
            "activados": 2,
            "reprimidos": 0,
        },
        "FNR": {
            "genes": ["narG"],
            "activados": 0,
            "reprimidos": 1,
        },
        "ArcA": {
            "genes": ["cyoA", "cyoB"],
            "activados": 1,
            "reprimidos": 1,
        },
    }
    filtered = filter_by_type(regulon, "dual")
    assert "CRP" not in filtered
    assert "FNR" not in filtered    
    assert "ArcA" in filtered

def test_filter_by_min_genes_keeps_only_regulators_with_enough_genes():
    # Esta prueba verifica que solo permanezcan los reguladores
    # que tienen al menos el número mínimo de genes indicado.

    regulon = {
        "CRP": {
            "genes": ["lacZ", "araB"],
            "activados": 2,
            "reprimidos": 0,
        },
        "FNR": {
            "genes": ["narG"],
            "activados": 0,
            "reprimidos": 1,
        },
    }
    filtered = filter_by_min_genes(regulon, min_genes=2)

    assert "CRP" in filtered
    assert "FNR" not in filtered
    assert len(filtered) == 1

def test_filter_by_type_none():
    # Esta prueba verifica que si el tipo de regulador solicitado es None,
    # no se realice ningún filtrado y se conserven todos los reguladores.
    regulon = {
        "CRP": {
            "genes": ["lacZ", "araB"],
            "activados": 2,
            "reprimidos": 0,
        },
        "FNR": {
            "genes": ["narG"],
            "activados": 0,
            "reprimidos": 1,
        },
    }
    filtered = filter_by_type(regulon, None)
    assert "CRP" in filtered
    assert "FNR" in filtered    
    assert len(filtered) == 2

def test_filter_tf_filtered_out():
    # Esta prueba verifica que si un TF es filtrado por tipo, no aparezca en el resultado final.
    regulon = {
        "CRP": {
            "genes": ["lacZ", "araB"],
            "activados": 2,
            "reprimidos": 0,
        },
        "FNR": {
            "genes": ["narG"],
            "activados": 0,
            "reprimidos": 1,
        },
    }
    filtered = filter_by_type(regulon, "dual")
    assert "CRP" not in filtered
    assert "FNR" not in filtered    
    assert len(filtered) == 0

