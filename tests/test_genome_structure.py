import pytest
import yaml
from pathlib import Path

# 🧪 Proyecto FORTBEL — Fase 0
# Tests automáticos para validar el archivo core/genome.yml
#
# Instrucciones para Codex:
# - Implementa tests con pytest.
# - Debe verificar:
#   1. Que el archivo genome.yml existe y se puede cargar.
#   2. Que contiene genome.meta y genome.genes.
#   3. Que todos los genes tienen id único y phase_min definido.
#   4. Que nature pertenece a {SY, PO, PR, FR, AG}.
#   5. Que no hay dependencias cíclicas.
@pytest.fixture
def genome_data():
    genome_file = Path("core/genome.yml")
    assert genome_file.exists(), "The genome.yml file does not exist."
    with genome_file.open() as f:
        return yaml.safe_load(f)

def test_genome_structure(genome_data):
    assert "genome" in genome_data, "The genome.yml file must contain 'genome'."
    assert "meta" in genome_data["genome"], "The genome.yml file must contain 'genome.meta'."
    assert "genes" in genome_data["genome"], "The genome.yml file must contain 'genome.genes'."

def test_unique_gene_ids(genome_data):
    genes = genome_data["genome"]["genes"]
    gene_ids = [gene["id"] for gene in genes]
    assert len(gene_ids) == len(set(gene_ids)), "Gene IDs must be unique."
    for gene in genes:
        assert "phase_min" in gene, "Each gene must have 'phase_min' defined."

def test_gene_nature(genome_data):
    valid_natures = {"SY", "PO", "PR", "FR", "AG"}
    genes = genome_data["genome"]["genes"]
    for gene in genes:
        assert gene["nature"] in valid_natures, f"Gene nature must be one of {valid_natures}."

def test_no_cyclic_dependencies(genome_data):
    genes = genome_data["genome"]["genes"]
    dependencies = {gene["id"]: gene.get("depends_on", []) for gene in genes}

    def has_cycle(node, visited, stack):
        visited.add(node)
        stack.add(node)
        for neighbor in dependencies.get(node, []):
            if neighbor not in visited:
                if has_cycle(neighbor, visited, stack):
                    return True
            elif neighbor in stack:
                return True
        stack.remove(node)
        return False

    visited = set()
    for gene_id in dependencies:
        if gene_id not in visited:
            if has_cycle(gene_id, visited, set()):
                pytest.fail("Cyclic dependency detected.")