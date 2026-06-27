import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDGenre(self):
        genres = self._model.getAllGenres()

        # Usiamo 'key' per l'ID (che sarà il valore restituito) e 'text' per il nome visualizzato
        genresDD = list(map(lambda x: ft.dropdown.Option(key=x.GenreId, text=x.Name), genres))
        self._view._ddGenre.options = genresDD
        self._view.update_page()

    def handleCreaGrafo(self, e):
        genre_id = self._view._ddGenre.value

        if genre_id is None:
            self._view.create_alert("Seleziona un genere!")
            return
        self._model.creaGrafo(str(genre_id))

        n_nodi, n_archi = self._model.getGraphDetails()

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Grafo correttamente creato:"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {n_nodi}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {n_archi}"))

        bestArtist = self._model.getNodoInfluenteMax()
        if bestArtist is None:
            self._view.txt_result.controls.append(
                ft.Text(f"Non ci sono archi da verificare per avere un artista migliore")
            )
            self._view.update_page()
            return
        self._view.txt_result.controls.append(
            ft.Text("Nodo più influente:")
        )
        for p in bestArtist:
            self._view.txt_result.controls.append(
                ft.Text(f"{p[0]} - score: {p[1]}")
            )

        self._view.txt_result.controls.append(ft.Text("Top 5 archi:"))
        edges = self._model.getEdgeGrandi()
        count = 0
        for e in edges:
            if count < 5:
                self._view.txt_result.controls.append(
                    ft.Text(f"{e[0]} --> {e[1]}: {e[2]["weight"]}")
                )
                count += 1
        self._view._ddArtist.disabled = False
        self.fillDDArtist()
        self._view.update_page()

    def handleCammino(self, e):
        artist_id = self._view._ddArtist.value

        if artist_id is None:
            self._view.create_alert("Seleziona un artista dal menù a tendina!")
            return

        path = self._model.getCamminoOttimo(artist_id)
        if len(path) == 1:
            self._view.txt_result.controls.append(ft.Text("Nessun cammino valido trovato a partire da questo artista."))
        else:
            self._view.txt_result.controls.append(ft.Text(f"Cammino trovato (lunghezza: {len(path)} nodi):"))
            for p in path:
                self._view.txt_result.controls.append(ft.Text(f"{p}"))

        self._view.update_page()

    def fillDDArtist(self):
        genre_id = self._view._ddGenre.value
        artists = self._model.getAllArtistsGenre(str(genre_id))
        for a in artists:
             self._view._ddArtist.options.append(ft.dropdown.Option(key=a.ArtistId, text=a.Name))
        self._view.update_page()