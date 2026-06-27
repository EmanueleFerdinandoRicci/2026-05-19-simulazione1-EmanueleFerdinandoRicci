from database.DB_connect import DBConnect
from model.arco import Arco
from model.artist import Artist
from model.genre import Genre


class DAO():
    @staticmethod
    def getAllGenres():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from genre g"""

        cursor.execute(query)

        for row in cursor:
            result.append(Genre(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllArtists():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from artist a """

        cursor.execute(query)

        for row in cursor:
            result.append(Artist(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllArtistsGenre(genreId, idMapA):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct(a.ArtistId)
                    from track t, album a
                    where t.AlbumId = a.AlbumId and t.GenreId = %s"""

        cursor.execute(query,(genreId,))

        for row in cursor:
            result.append(idMapA[row["ArtistId"]])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdgesDiversiMIO():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select n1.ArtistId as id1, n2.ArtistId as id2, SUM(n1.p1) + SUM(n2.p2) as peso
                    from (select a1.ArtistId, i1.CustomerId, count(*) as p1
                    from invoice i1, invoiceline il1,  track t1,  album a1
                    where i1.InvoiceId = il1.InvoiceId 
                    and il1.TrackId = t1.TrackId
                    and t1.AlbumId = a1.AlbumId
                    group by a1.ArtistId, i1.CustomerId) n1 
                    join (select a2.ArtistId, i2.CustomerId, count(*) as p2
                    from invoice i2, invoiceline il2,  track t2,  album a2
                    where i2.InvoiceId = il2.InvoiceId 
                    and il2.TrackId = t2.TrackId
                    and t2.AlbumId = a2.AlbumId
                    group by a2.ArtistId, i2.CustomerId) n2 on n1.CustomerId = n2.CustomerId
                    where n1.ArtistId != n2.ArtistId 
                    group by  n1.ArtistId, n2.ArtistId
                    having sum(n1.p1) > sum(n2.p2)"""

        cursor.execute(query)

        for row in cursor:
            result.append(Arco(row["id1"], row["id2"], row["peso"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdgesUgualiMIO():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select n1.ArtistId as id1, n2.ArtistId as id2, SUM(n1.p1) + SUM(n2.p2) as peso
                        from (select a1.ArtistId, i1.CustomerId, count(*) as p1
                        from invoice i1, invoiceline il1,  track t1,  album a1
                        where i1.InvoiceId = il1.InvoiceId 
                        and il1.TrackId = t1.TrackId
                        and t1.AlbumId = a1.AlbumId
                        group by a1.ArtistId, i1.CustomerId) n1 
                        join (select a2.ArtistId, i2.CustomerId, count(*) as p2
                        from invoice i2, invoiceline il2,  track t2,  album a2
                        where i2.InvoiceId = il2.InvoiceId 
                        and il2.TrackId = t2.TrackId
                        and t2.AlbumId = a2.AlbumId
                        group by a2.ArtistId, i2.CustomerId) n2 on n1.CustomerId = n2.CustomerId
                        where n1.ArtistId != n2.ArtistId
                        group by  n1.ArtistId, n2.ArtistId
                        having sum(n1.p1) = sum(n2.p2)"""

        cursor.execute(query)

        for row in cursor:
            result.append(Arco(row["id1"], row["id2"], row["peso"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdgesUguali(genreId):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)

        query = """
                SELECT DISTINCT t1.a1 AS id1, t2.a2 AS id2, (p1.pop + p2.pop) AS peso
                FROM (SELECT a.ArtistId AS a1, i.CustomerId AS c1 
                      FROM album a, 
                           track t, 
                           invoiceline il, 
                           invoice i 
                      WHERE a.AlbumId = t.AlbumId 
                        AND t.TrackId = il.TrackId 
                        AND il.InvoiceId = i.InvoiceId 
                        AND t.GenreId = %s) t1 
                         JOIN 
                     (SELECT a.ArtistId AS a2, i.CustomerId AS c2 
                      FROM album a, 
                           track t, 
                           invoiceline il, 
                           invoice i 
                      WHERE a.AlbumId = t.AlbumId 
                        AND t.TrackId = il.TrackId 
                        AND il.InvoiceId = i.InvoiceId 
                        AND t.GenreId = %s) t2 
                     ON t1.c1 = t2.c2 AND t1.a1 < t2.a2 
                         JOIN 
                     (SELECT a.ArtistId, COUNT(*) AS pop 
                      FROM album a, 
                           track t, 
                           invoiceline il 
                      WHERE a.AlbumId = t.AlbumId 
                        AND t.TrackId = il.TrackId 
                      GROUP BY a.ArtistId) p1 
                     ON t1.a1 = p1.ArtistId 
                         JOIN 
                     (SELECT a.ArtistId, COUNT(*) AS pop 
                      FROM album a, 
                           track t, 
                           invoiceline il 
                      WHERE a.AlbumId = t.AlbumId 
                        AND t.TrackId = il.TrackId 
                      GROUP BY a.ArtistId) p2 
                     ON t2.a2 = p2.ArtistId
                WHERE p1.pop = p2.pop 
                """

        cursor.execute(query, (genreId, genreId,))

        for row in cursor:
            result.append(Arco(row["id1"], row["id2"], row["peso"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdgesDiversi(genreId):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)

        query = """
                SELECT DISTINCT t1.a1 AS id1, t2.a2 AS id2, (p1.pop + p2.pop) AS peso
                FROM (SELECT a.ArtistId AS a1, i.CustomerId AS c1 
                      FROM album a, 
                           track t, 
                           invoiceline il, 
                           invoice i 
                      WHERE a.AlbumId = t.AlbumId 
                        AND t.TrackId = il.TrackId 
                        AND il.InvoiceId = i.InvoiceId 
                        AND t.GenreId = %s) t1 
                         JOIN 
                     (SELECT a.ArtistId AS a2, i.CustomerId AS c2 
                      FROM album a, 
                           track t, 
                           invoiceline il, 
                           invoice i 
                      WHERE a.AlbumId = t.AlbumId 
                        AND t.TrackId = il.TrackId 
                        AND il.InvoiceId = i.InvoiceId 
                        AND t.GenreId = %s) t2 
                     ON t1.c1 = t2.c2 AND t1.a1 != t2.a2
                JOIN
                    (SELECT a.ArtistId, COUNT(*) AS pop
                     FROM album a, track t, invoiceline il
                     WHERE a.AlbumId = t.AlbumId AND t.TrackId = il.TrackId
                     GROUP BY a.ArtistId) p1
                ON t1.a1 = p1.ArtistId
                    JOIN
                    (SELECT a.ArtistId, COUNT (*) AS pop
                    FROM album a, track t, invoiceline il
                    WHERE a.AlbumId = t.AlbumId AND t.TrackId = il.TrackId
                    GROUP BY a.ArtistId) p2
                    ON t2.a2 = p2.ArtistId
                WHERE p1.pop > p2.pop 
                """

        cursor.execute(query, (genreId, genreId,))

        for row in cursor:
            result.append(Arco(row["id1"], row["id2"], row["peso"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getCoppieClientiComuni(genreId):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)

        # Usiamo a1 < a2 per restituire la coppia (A, B) una sola volta senza duplicati (B, A)
        query = """
                SELECT DISTINCT c1.a1 AS id1, c2.a2 AS id2
                FROM (SELECT DISTINCT a.ArtistId AS a1, i.CustomerId AS c1 
                      FROM album a, 
                           track t, 
                           invoiceline il, 
                           invoice i 
                      WHERE a.AlbumId = t.AlbumId 
                        AND t.TrackId = il.TrackId 
                        AND il.InvoiceId = i.InvoiceId 
                        AND t.GenreId = %s) c1, 
                     (SELECT DISTINCT a.ArtistId AS a2, i.CustomerId AS c2 
                      FROM album a, 
                           track t, 
                           invoiceline il, 
                           invoice i 
                      WHERE a.AlbumId = t.AlbumId 
                        AND t.TrackId = il.TrackId 
                        AND il.InvoiceId = i.InvoiceId 
                        AND t.GenreId = %s) c2
                WHERE c1.c1 = c2.c2 
                  AND c1.a1 < c2.a2 
                """
        cursor.execute(query, (genreId, genreId,))
        for row in cursor:
            result.append((row["id1"], row["id2"]))  # Restituisco una tupla di ID

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getMappaPopolarita(genreId):
        conn = DBConnect.get_connection()
        result = {}
        cursor = conn.cursor(dictionary=True)

        # Aggiunto il filtro sul GenreId
        query = """
                SELECT a.ArtistId, COUNT(*) AS pop
                FROM album a, 
                     track t, 
                     invoiceline il
                WHERE a.AlbumId = t.AlbumId 
                  AND t.TrackId = il.TrackId
                  AND t.GenreId = %s
                GROUP BY a.ArtistId 
                """
        cursor.execute(query, (genreId,))
        for row in cursor:
            result[row["ArtistId"]] = row["pop"]

        cursor.close()
        conn.close()
        return result