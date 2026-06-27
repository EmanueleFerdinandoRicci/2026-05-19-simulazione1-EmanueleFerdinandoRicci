import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._genres = DAO.getAllGenres()
        self._artists = DAO.getAllArtists()
        self._idMapGenres = {}
        for g in self._genres:
            self._idMapGenres[g.GenreId] = g
        self._idMapArtists = {}
        for a in self._artists:
            self._idMapArtists[a.ArtistId] = a
        self._artistsGenre = []
        self.best_path = []
        self.best_len = 0

    def getAllGenres(self):
        return self._genres

    def getAllArtists(self):
        return self._artists

    def getAllArtistsGenre(self, genreId):
        self._artistsGenre = []
        self._artistsGenre = DAO.getAllArtistsGenre(genreId, self._idMapArtists)
        return self._artistsGenre

    def getAllEdgesDiversi(self, genreId):
        # Ora passiamo genreId al DAO
        allDiversi = DAO.getAllEdgesDiversi(genreId)

        for e in allDiversi:
            a1 = self._idMapArtists[e.id1]
            a2 = self._idMapArtists[e.id2]

            if a1 in self._artistsGenre and a2 in self._artistsGenre:
                self._graph.add_edge(a1, a2, weight=e.peso)

    def getAllEdgesUguali(self, genreId):
        # Ora passiamo genreId al DAO
        allUguali = DAO.getAllEdgesUguali(genreId)

        for e in allUguali:
            a1 = self._idMapArtists[e.id1]
            a2 = self._idMapArtists[e.id2]

            if a1 in self._artistsGenre and a2 in self._artistsGenre:
                self._graph.add_edge(a1, a2, weight=e.peso)
                self._graph.add_edge(a2, a1, weight=e.peso)

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def creaGrafo(self, genreId):
        self._graph.clear()

        # 1. Aggiungo i Nodi
        nodes = self.getAllArtistsGenre(genreId)
        self._graph.add_nodes_from(nodes)

        # 2. Recupero i dati semplificati dal DAO
        mappa_popolarita = DAO.getMappaPopolarita(genreId)
        coppie = DAO.getCoppieClientiComuni(genreId)

        # 3. Logica in Python per stabilire verso e peso
        for id1, id2 in coppie:
            a1 = self._idMapArtists.get(id1)
            a2 = self._idMapArtists.get(id2)

            # Controllo di sicurezza: verifichiamo che entrambi siano nodi validi del grafo
            if a1 in self._graph and a2 in self._graph:
                # Recupero la popolarità dalla mappa (uso 0 come default se per caso non hanno vendite)
                pop1 = mappa_popolarita.get(id1, 0)
                pop2 = mappa_popolarita.get(id2, 0)

                peso_totale = pop1 + pop2

                # Configuro gli archi in base alle regole del testo
                if pop1 > pop2:
                    self._graph.add_edge(a1, a2, weight=peso_totale)
                elif pop2 > pop1:
                    self._graph.add_edge(a2, a1, weight=peso_totale)
                else:
                    # Popolarità uguale: doppio arco
                    self._graph.add_edge(a1, a2, weight=peso_totale)
                    self._graph.add_edge(a2, a1, weight=peso_totale)

    def getNodoInfluenteMax(self):
        listNodesPesata = []
        for n in self._graph.nodes:
            score = 0
            for e in self._graph.out_edges(n,data=True):
                score += e[2]["weight"]
            for e in self._graph.in_edges(n,data=True):
                score -= e[2]["weight"]
            listNodesPesata.append((n,score))

        listNodesPesata.sort(key=lambda x:x[1], reverse=True)
        return listNodesPesata[0:1]

    def getEdgeGrandi(self):
        edgeGrandi = list(self._graph.edges(data=True))
        edgeGrandi.sort(key=lambda e: e[2]["weight"], reverse=True)
        return edgeGrandi

    def getCamminoOttimo(self, artist_id):
        artist = int(artist_id)
        if artist not in self._idMapArtists:
            return []
        nodo_sorgente = self._idMapArtists[artist]

        self.best_path = []
        self.best_len = 0
        self._ricorsione(nodo_sorgente, [nodo_sorgente], 1000)

        return self.best_path

    def _ricorsione(self, nodo_corrente, path_corrente, peso_precedente):
        if len(path_corrente) > self.best_len:
            self.best_len = len(path_corrente)
            self.best_path = copy.deepcopy(list(path_corrente))

        for vicino in self._graph.successors(nodo_corrente):
            if vicino not in path_corrente:
                peso_arco = int(self._graph[nodo_corrente][vicino]['weight'])
                if peso_arco < peso_precedente:
                    path_corrente.append(vicino)
                    self._ricorsione(vicino, path_corrente, peso_arco)
                    path_corrente.pop()