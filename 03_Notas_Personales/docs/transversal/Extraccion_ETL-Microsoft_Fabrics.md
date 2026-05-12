# PROCESO DE EXTRACCION MICROSOFT FABRIC

   ORIGENES DE DATOS                ENTORNO MICROSOFT FABRIC
  +-----------------+      +-------------------------------------------------------+

  |                 |      |                                                       |
  |   [BDAJETEST]   |      |   ( DF Extraccion )                                   |
  |        |        |      |           ^                                           |
  |        +---------------------------+          +---------+      +---------+     |
  |                 |      |           |          |         |      |         |     |
  |                 |      |           +--------> | Alm TMP | -SP> | Alm INT |     |
  |   [Archivos]    |      |           |          |         |      |         |     |
  | (excel,csv,txt) |      |   [Data Lakehouse]   +---------+      +---------+     |
  |        |        |      |                                            |          |
  |        +---------------------------+                                SP         |
  |                 |      |           |                                |          |
  |                 |      |           v                                v          |
  |   [OneLake] <----------+--------------------------------------- [   DWH   ]    |
  |                 |      |                                            |          |
  |                 |      |                                            v          |
  |                 |      |                                   [Modelo Semantico]  |
  |                 |      |                                   [  x Proyecto    ]  |
  |                 |      |                                            |          |
  |                 |      |                                            v          |
  |                 |      |                                      /-----------\    |
  |                 |      |                                      |  Reporte  |    |
  |                 |      |                                      | Power BI  |    |
  |                 |      |                                      \-----------/    |
  +-----------------+      +-------------------------------------------------------+

## Lista de tablas que se consultan


| | | |
|---|---|---|
| MPERSE0EF | MCLIE N8F | MLPVTA2F |
| BARTIC3F | MDOCUM1F | BUBIGE2F |
| BAREAF | TCPAGO1F | BARTIC2F |
| TCOALM1F | MPERSOGF | TURNO |
| TCOMPA2F | BECOAL1F | MDOCUM2F |
| MPERSO1F | TCOALM9F | BCNFIN1 |
| TCCOST1F | MPERSO8F | TREQUE2F |
| BGASTO1F | MCANDISTF | MMONED1F |
| BGEREN1F | BREGION1F | MEJERC1F |
| MUSUAR1F | BREGION2F | MESTDI2F |
| BARTIC11F | BOPERA1F | |
| BARTIC10F | | |
| MPERSO7F | | |
| BARTIC7F | | |
| BARTIC8F | | |
| BARTIC9F | | |
|---|---|---|
| MARTIC1F | TCANDIS1F | MLPVTA1F |
| MCOMPA1F | TCOVTA1F | MCLIEN2F |
| BMOTIV1F | CIEALMCPM | TPEDID2F |
| TCOALM2F | CBETIBAR | TCOVTA2F |
| COCCOST1F | TCARGO1F | MPERSODF |
| MEMISO1F | MPADIS2F | TREQUE1F |
| MFAMIL1F | MVEHIC1F | MUSERACAN |
| BPROCE1F | TCOALM17F | TARTSA2F |
| MCLIEN1F | MPARAM1F | BUBIGE4F |
| BUBIGE1F | PRGOPDET | TFVTA1F |
| MLINEA1F | ORPRCA | TARTSA3F |
| MPERSOCF | TCOALM4F | TINVAR2 |
| MPROVE7F | BIMPUE20F | TINVAR1 |
| MPARAM2F | TCOALM16F | TOBSEQ2F |
| TCOALM18F | TTARIMA | TOBSEQ1F |
| TPEDID7F | MDOCUM10F | TREQUE3F |
| MSUBFA1F | TPLINT9F | BARTIC4F |
| TPEDID1F | MOTIVOGPL | BARTIC5F |
| MPERCT1F | MPCCOR1F | BARTIC12F |
| BIMPUE13F | BARTIC6F | THPEDI2F |
| TREQUE13F | BARTIC1F | MOVALMXLOTE |
