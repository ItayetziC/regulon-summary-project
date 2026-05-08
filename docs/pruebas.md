# Pruebas del proyecto Regulon Summary

Este documento describe los casos de prueba simples y los casos límite que el programa ya comprueba.


## Casos simples

### Caso 1: Comportamiento actual

```bash
python main.py data/raw/NetworkRegulatorGene.tsv results/regulon_summary.tsv
```

- Resultado: archivo `results/regulon_summary.tsv` con el resumen de todos los TFs.
- Comprueba que el programa puede leer el archivo y generar un resumen.

### Caso 2: Filtrar por número mínimo de genes

```bash
python main.py data/raw/NetworkRegulatorGene.tsv results/regulon_summary_min5.tsv --min_genes 5
```

- Resultado: solo TFs con al menos 5 genes.
- Comprueba `filter_by_min_genes()`.

### Caso 3: Filtrar por tipo de regulación

```bash
python main.py data/raw/NetworkRegulatorGene.tsv results/activadores.tsv --type activador
```

- Resultado: solo TFs clasificados como `activador`.
- Comprueba `filter_by_type()` y `get_regulator_type()`.

### Caso 4: Salida SIF

```bash
python main.py data/raw/NetworkRegulatorGene.tsv results/network.sif --format sif
```

- Resultado: archivo SIF con interacciones `TF    activates/represses/regulates    gen`.
- Comprueba `write_sif()`.

### Caso 5: Combinación de filtros

```bash
python main.py data/raw/NetworkRegulatorGene.tsv results/duales_min5.sif --min_genes 5 --type dual --format sif
```

- Resultado: solo TFs duales con al menos 5 genes, en formato SIF.
- Comprueba la coherencia entre filtros y formato SIF.

## Casos límite y validaciones existentes

### Límite 1: `--min_genes` negativo

```bash
python main.py data/raw/NetworkRegulatorGene.tsv results/invalid.tsv --min_genes -1
```

- Resultado: mensaje de error `min_genes debe ser mayor o igual a 0.`
- Comprueba la validación de argumentos en `main()`.

### Límite 2: Archivo de entrada inexistente

```bash
python main.py data/raw/NoExiste.tsv results/invalid.tsv
```

- Resultado: mensaje de error `Error: no existe el archivo de entrada -> ...`
- Comprueba el manejo de `FileNotFoundError`.

### Límite 3: Archivo de entrada sin interacciones válidas

- Crear un archivo con líneas vacías, comentarios o filas incompletas.
- Ejecutar:

```bash
python main.py docs/empty_input.tsv results/empty_output.tsv
```

- Resultado: advertencia `no se encontraron interacciones válidas.`
- Comprueba la validación de contenido después de `load_interactions()`.

### Límite 4: Los filtros eliminan todos los TFs

```bash
python main.py data/raw/NetworkRegulatorGene.tsv results/no_regulators.tsv --min_genes 1000
```

- Resultado: advertencia `no hay reguladores que cumplan el filtro.`
- Comprueba el comportamiento con regulón vacío después del filtrado.

### Límite 5: Directorio de salida inexistente

```bash
python main.py data/raw/NetworkRegulatorGene.tsv results/newdir/regulon_summary.tsv
```

- Resultado: el programa crea el directorio y escribe el archivo.
- Comprueba la creación de directorios en `write_summary()` y `write_sif()`.

## Notas adicionales

- El programa no requiere dependencias externas, lo cual facilita su prueba en entornos limpios.
- Las pruebas manuales anteriores permiten verificar tanto la lógica de filtrado como la generación de salida.
- Para pruebas más avanzadas, se puede agregar un conjunto de tests unitarios en `tests/` usando `pytest`.
