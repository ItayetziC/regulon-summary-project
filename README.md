# Regulon Summary Project

Un proyecto Python para procesar interacciones regulador-gen y generar resúmenes de regulones.

## Descripción

Este programa lee un archivo TSV de interacciones entre factores de transcripción (TF) y genes. Construye un regulón por TF, calcula cuántos genes activa y reprime, y soporta filtros por número mínimo de genes y tipo de regulación.

Además, ofrece dos formatos de salida:

- `summary`: archivo TSV con información de TF, total de genes, activados, reprimidos, tipo y lista de genes.
- `sif`: formato SIF compatible con visualización de redes en Cytoscape.

## Estructura del proyecto

- `main.py`: punto de entrada del programa.
- `src/regulon_summary.py`: implementación de la lógica del programa.
- `data/raw/NetworkRegulatorGene.tsv`: datos de ejemplo de interacciones.
- `docs/design.md`: requisitos y diseño del programa.
- `docs/pruebas.md`: casos de prueba simples y límites.

## Requisitos

- Python 3.11 o superior

No hay dependencias externas adicionales.

## Entorno virtual

Este proyecto puede ejecutarse con un entorno virtual tradicional (`venv`) o con el gestor `uv`.

### Opción 1: Usar `uv`

Si usas `uv`, sincroniza el entorno con el proyecto y luego ejecuta el script:

```bash
uv sync
uv run python main.py <archivo_entrada> <archivo_salida> [--min_genes N] [--type activador|represor|dual] [--format summary|sif]
```

### Opción 2: Usar `venv`

```bash
python -m venv .venv
source .venv/bin/activate
```

En Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Instalación de dependencias

Las dependencias se deben declarar en `pyproject.toml` y administrar con `uv`.

Este proyecto actualmente no tiene dependencias externas adicionales.

```bash
uv sync
```

Si necesitas agregar paquetes, actualiza `pyproject.toml` y luego ejecuta `uv sync`.

> No uses `uv add` para este proyecto mientras se gestione el proyecto desde `pyproject.toml`.

## Uso

Ejecuta el programa desde la raíz del proyecto con el entorno virtual activo.

- Si usas `uv`:

```bash
uv run python main.py <archivo_entrada> <archivo_salida> [--min_genes N] [--type activador|represor|dual] [--format summary|sif]
```

- Si usas `venv`:

```bash
python main.py <archivo_entrada> <archivo_salida> [--min_genes N] [--type activador|represor|dual] [--format summary|sif]
```

### Argumentos

- `input_file`: Archivo TSV de entrada con interacciones.
- `output_file`: Archivo de salida.
- `--min_genes N`: Filtrar TFs que regulan al menos `N` genes.
- `--type activador|represor|dual`: Filtrar TFs por tipo de regulación.
- `--format summary|sif`: Formato de salida. El valor por defecto es `summary`.

## Ejemplos

### Salida resumen por defecto

```bash
uv run python main.py data/raw/NetworkRegulatorGene.tsv results/regulon_summary.tsv
```

### Filtrar por número mínimo de genes

```bash
uv run python main.py data/raw/NetworkRegulatorGene.tsv results/regulon_summary.tsv --min_genes 5
```

### Filtrar por tipo de regulación

```bash
uv run python main.py data/raw/NetworkRegulatorGene.tsv results/activadores.tsv --type activador
```

### Generar red en formato SIF

```bash
uv run python main.py data/raw/NetworkRegulatorGene.tsv results/network.sif --format sif
```

### Combinación de filtros

```bash
uv run python main.py data/raw/NetworkRegulatorGene.tsv results/duales.tsv --min_genes 5 --type dual --format summary
```

## Comportamiento esperado

1. Carga de interacciones.
2. Construcción del regulón.
3. Filtrado por número mínimo de genes.
4. Filtrado por tipo de regulador.
5. Exportación en el formato seleccionado.

## Archivos de documentación

- `docs/design.md`: requisitos funcionales y diseño técnico.
- `docs/pruebas.md`: lista de pruebas manuales y casos límite.
