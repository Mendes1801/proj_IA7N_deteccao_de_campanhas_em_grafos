# Classificação precoce de campanhas coordenadas

Projeto da disciplina de Inteligência Artificial (turma 7N), desenvolvido a
partir do TCC sobre campanhas coordenadas em redes sociais.

## Integrantes

- Gabriel de Santana Santos — RA 10420595 — 10420595@mackenzista.com.br
- Gabriel Erick Mendes — RA 10420391 — 10420391@mackenzista.com.br
- Matheus Teles Magalhães — RA 10427410 — 10427410@mackenzista.com.br

## Conteúdo

- `artigo/artigo_parcial.pdf`: artigo da Parte 2;
- `dados/`: descrição do dataset e tabelas processadas;
- `notebooks/`: análises exploratórias;
- `scripts/`: códigos e testes;
- `dados/len_small_exclusions.csv`: registro da duplicata retirada.

O dataset bruto não está no GitHub por ocupar cerca de 5,4 GB. A origem e as
instruções para obtê-lo estão em [`dados/README.md`](dados/README.md).

## Como reproduzir

Com os arquivos JSON em `small_encoder_final/`, execute:

```bash
python -m pip install -e ".[dev,notebook]"
pytest
len-summary --data-dir small_encoder_final \
  --output dados/processados/len_small_summary.csv
len-features --data-dir small_encoder_final \
  --exclusions dados/len_small_exclusions.csv \
  --output dados/processados/partial_graph_features.csv
```

Depois, abra os notebooks na ordem numérica.
