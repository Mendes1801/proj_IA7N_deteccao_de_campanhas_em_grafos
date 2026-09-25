# Dataset LEN-small

O projeto utiliza o **Large Engagement Networks (LEN)**, conjunto público de
redes de engajamento do Twitter disponibilizado por Gopalakrishnan et al.
(2025). Os endereços oficiais são:

- repositório e descrição do dataset: <https://github.com/erdemUB/LEN>;
- página de download indicada pelos autores:
  <https://erdemub.github.io/large-engagement-network/>.

Cada arquivo JSON representa um tópico. Os nós são usuários e as arestas são
interações direcionadas, como retuítes, respostas e citações. Os arquivos
incluem o horário da interação armazenada e o rótulo `campaign` ou
`noncampaign`.

## Recorte analisado

O pacote local contém 104 arquivos: 53 campanhas e 51 não campanhas. Foi
encontrada uma duplicata exata; após sua exclusão restam 103 grafos, sendo 52
campanhas e 51 não campanhas. O artigo descreve 100 grafos no LEN-small (51
campanhas e 49 não campanhas), portanto a lista canônica ainda será confirmada
antes do treinamento definitivo.

Os JSONs brutos ocupam cerca de 5,4 GB e não são versionados neste repositório.
As tabelas processadas usadas na análise estão em `dados/processados/`:

- `len_small_summary.csv`: uma linha por arquivo, com métricas básicas e
  verificações de integridade;
- `partial_graph_features.csv`: 2.060 estados parciais, gerados em 10 frações
  por tempo e por quantidade de arestas, após remover a duplicata.

## Limitações relevantes

- O LEN preserva somente a interação mais recente de cada par ordenado de
  usuários; a evolução reconstruída descreve as arestas retidas na base.
- Os rótulos representam as categorias operacionais definidas pelos autores e
  não provam intenção, ilegalidade ou ausência total de coordenação.
- As tendências foram coletadas na Turquia, entre março e maio de 2023, em um
  período próximo às eleições gerais.
- Campanhas e não campanhas possuem distribuições de tamanho diferentes, o que
  pode criar um atalho indevido para os classificadores.

## Referência

GOPALAKRISHNAN, A. A.; HOSSAIN, J.; ELMAS, T.; SARIYÜCE, A. E. Large
Engagement Networks for Classifying Coordinated Campaigns and Organic Twitter
Trends. *Proceedings of the International AAAI Conference on Web and Social
Media*, v. 19, n. 1, p. 688-702, 2025. DOI:
<https://doi.org/10.1609/icwsm.v19i1.35839>.
