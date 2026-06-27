from model.model import Model

myModel = Model()
artisti = myModel.getAllArtistsGenre("1")
print(len(artisti))
myModel.creaGrafo("1")
nNodes, nEdges = myModel.getGraphDetails()
print(f"N nodes: {nNodes}, n edges: {nEdges}")