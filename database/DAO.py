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
    def getAllEdgesDiversi():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select n1.ArtistId as id1, n2.ArtistId as id2, coalesce(n1.p1,0)+coalesce(n2.p2,0) as peso
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
                    where n1.ArtistId < n2.ArtistId and n1.p1 > n2.p2 
                    group by  n1.ArtistId, n2.ArtistId"""

        cursor.execute(query)

        for row in cursor:
            result.append(Arco(row["id1"], row["id2"], row["peso"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdgesUguali():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select n1.ArtistId as id1, n2.ArtistId as id2, coalesce(n1.p1,0)+coalesce(n2.p2,0) as peso
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
                        where n1.ArtistId < n2.ArtistId and n1.p1 = n2.p2 
                        group by  n1.ArtistId, n2.ArtistId"""

        cursor.execute(query)

        for row in cursor:
            result.append(Arco(row["id1"], row["id2"], row["peso"]))

        cursor.close()
        conn.close()
        return result