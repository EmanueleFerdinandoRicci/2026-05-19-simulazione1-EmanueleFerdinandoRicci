import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._genres = DAO.getAllGenres()
        self._artists = DAO.getAllArtists()
        self._idMapGenres = {}
        for g in self._genres:
            self._idMapGenres[g.GenreId] = g
        self._idMapArtists = {}
        for a in self._artists:
            self._idMapArtists[a.ArtistId] = a
        self._artistsGenre = []

    def getAllGenres(self):
        return self._genres

    def getAllArtists(self):
        return self._artists

    def getAllArtistsGenre(self, genreId):
        self._artistsGenre = []
        self._artistsGenre = DAO.getAllArtistsGenre(genreId, self._idMapArtists)
        return self._artistsGenre

    def creaGrafo(self,genreId):
        nodes = DAO.getAllArtistsGenre(genreId, self._idMapArtists)
        self._graph.add_nodes_from(nodes)
        self.getAllEdgesDiversi()
        self.getAllEdgesUguali()
    def getAllEdgesDiversi(self):
        allDiversi = DAO.getAllEdgesDiversi()

        for e in allDiversi:
            if e.id1 in self._idMapArtists and e.id2 in self._idMapArtists:
                self._graph.add_edge(e.id1,e.id2, weight=e.peso)

    def getAllEdgesUguali(self):
        allUguali = DAO.getAllEdgesUguali()

        for e in allUguali:
            if e.id1 in self._idMapArtists and e.id2 in self._idMapArtists:
                self._graph.add_edge(e.id1, e.id2, weight=e.peso)
                self._graph.add_edge(e.id2, e.id1, weight=e.peso)

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)
        
