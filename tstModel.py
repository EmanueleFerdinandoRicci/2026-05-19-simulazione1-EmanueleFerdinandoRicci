from model.model import Model

myModel = Model()
artisti = myModel.getAllArtistsGenre("2")
print(len(artisti))
myModel.creaGrafo("2")
nNodes, nEdges = myModel.getGraphDetails()
print(f"N nodes: {nNodes}, n edges: {nEdges}")