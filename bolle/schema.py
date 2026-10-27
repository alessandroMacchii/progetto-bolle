"""Schema dei dati estratti da una pagina di bolla.

Volutamente senza campi Optional: gli structured output sono piu' affidabili
con tipi semplici, quindi i valori mancanti usano sentinelle documentate
("" per le stringhe, 0 per gli interi) invece di null.
"""
from __future__ import annotations

from pydantic import BaseModel, Field, PrivateAttr


class TagliaEstratta(BaseModel):
    taglia: str = Field(
        description="Taglia esattamente come stampata: 8-, XS, 910A, NS, 540. "
        "Un pacco misto resta un solo elemento: S/XL/1 -> taglia 'S/XL', qta 1"
    )
    qta: int = Field(description="Quantita' per quella taglia")


class RigaEstratta(BaseModel):
    seq: str = Field(description="Numero Seq-no / Item No. della riga; '' se assente")
    codice_articolo: str = Field(
        description="Codice articolo del fornitore, es. IF4092, JZ2505, H44527. "
        "'' se illeggibile"
    )
    descrizione: str = Field(description="Nome/descrizione articolo, es. URBAN COURT")
    colore: str = Field(description="Colorway, es. FTWWHT/FTWWHT/CLPINK; '' se assente")
    totale_dichiarato: int = Field(
        description="Valore della colonna Total per questa riga; 0 se assente"
    )
    size_qty_raw: str = Field(
        description="Contenuto grezzo della colonna Size/Qty, es. 'XS/2 S/7 M/10 L/8'. "
        "Per i documenti con tabella taglie verticale, ricostruiscilo nello stesso formato"
    )
    taglie: list[TagliaEstratta] = Field(description="Scomposizione di size_qty_raw")
    barrata: bool = Field(
        description="True se la riga e' cancellata/barrata a penna sulla scansione"
    )
    annotazioni_manoscritte: str = Field(
        description="Trascrizione di quanto scritto a mano su questa riga "
        "(es. 'MAG 1', 'MAG 2', quantita' corrette). '' se niente"
    )
    # I due campi seguenti hanno un default perche' il gold set e le bolle gia'
    # salvate sono nati senza: il modello li compila sempre.
    codice_manoscritto: str = Field(
        default="",
        description="Codice articolo scritto A MANO su questa riga, se c'e' ed e' "
        "diverso da quello stampato. Non va mai messo in codice_articolo. '' se assente",
    )
    incertezze: str = Field(
        default="",
        description="Quali dati STAMPATI di questa riga hai letto a fatica e perche', "
        "es. 'codice: prima lettera coperta dalla penna, J oppure U'. "
        "'' se tutto e' leggibile senza dubbi",
    )


class PaginaEstratta(BaseModel):
    tipo_documento: str = Field(
        description="DELIVERY NOTE | CONSOLIDATED ORDER NUMBER | VALUE ADDED SERVICE "
        "| PRODUCT SPECIFICATION | ALTRO"
    )
    numero_documento: str = Field(description="Numero del documento; '' se assente")
    data_documento: str = Field(description="Data in formato GG.MM.AA come stampata; '' se assente")
    warehouse: str = Field(description="Campo Warehouse; '' se assente")
    total_pieces_dichiarato: int = Field(
        description="Total Pieces del riepilogo; 0 se assente"
    )
    rotazione_gradi: int = Field(
        description="Rotazione della scansione: 0, 90, 180 o 270 gradi"
    )
    continua_da_pagina_precedente: bool = Field(
        description="True se la tabella prosegue da una pagina precedente"
    )
    magazzino_pagina: str = Field(
        default="",
        description="'MAG 1' o 'MAG 2' se UNA sola scritta a mano vale per tutta la "
        "pagina (es. 'TUTTO MAG 2' in testa al foglio). '' altrimenti",
    )
    note_pagina: str = Field(
        default="",
        description="Scritte a mano che non riguardano una riga precisa "
        "(es. 'ok 8 colli', firme, date). '' se niente",
    )
    righe: list[RigaEstratta]
    # Chi ha letto la pagina, per misurare la cascata nella prova. Privato: non
    # entra nello schema che vede il modello.
    _motore: str = PrivateAttr(default="")


# --- stato di lavoro (post-estrazione, editabile dall'operatore) -------------

class RigaLavoro(BaseModel):
    """Una riga per singola taglia: e' l'unita' che finisce nell'Excel."""

    id: str
    pagina: int
    seq: str = ""
    codice_articolo: str = ""
    descrizione: str = ""
    colore: str = ""
    taglia: str = ""
    variante: str = ""
    variante_confermata: bool = False
    qta: int = 0
    # taglie del pacco misto di provenienza ("S/XL"), "" se taglia sciolta
    pacco: str = ""
    magazzino: str = ""
    eliminata: bool = False
    origine: str = "estratta"  # estratta | manuale | split
    avvisi: list[str] = Field(default_factory=list)
    annotazioni_manoscritte: str = ""
