import itertools as it
import sys
import pickle
def Magic4to3(FourToThree,request):
        for i in it.permutations(request):
            if str(i) in FourToThree.keys():
                Result=FourToThree[str(i)]
                return Result
def Magic3to4(ThreeToFour,request):
    return ThreeToFour[str(request)]

class Edge(object):
    def __init__(self, u, v, w):
        self.source = u
        self.target = v
        self.capacity = w

    def __repr__(self):
        return "%s~%s" % (self.source, self.target)


class FlowNetwork(object):
    def  __init__(self):
        self.adj = {}
        self.flow = {}

    def AddVertex(self, vertex):
        #if self.adj.get(vertex)==None:
        self.adj[vertex] = []
        #else:
         #   return 5

    def GetEdges(self, v):
        return self.adj[v]

    def AddEdge(self, u, v, w = 0):
        if u == v:
            raise ValueError("u == v")
        edge = Edge(u, v, w)
        redge = Edge(v, u, 0)
        edge.redge = redge
        redge.redge = edge
        self.adj[u].append(edge)
        self.adj[v].append(redge)
        # Intialize all flows to zero
        self.flow[edge] = 0
        self.flow[redge] = 0

    def FindPath(self, source, target, path):
        if source == target:
            return path
        for edge in self.GetEdges(source):
            residual = edge.capacity - self.flow[edge]
            if residual > 0 and not (edge, residual) in path:
                result = self.FindPath(edge.target, target, path + [(edge, residual)])
                if result != None:
                    return result

    def MaxFlow(self, source, target):
        path = self.FindPath(source, target, [])
        #print 'path after enter MaxFlow: %s' % path
        #for key in self.flow:
        #      print '%s:%s' % (key,self.flow[key])
        #print '-' * 20
        while path != None:
            flow = min(res for edge, res in path)
            for edge, res in path:
                self.flow[edge] += flow
                self.flow[edge.redge] -= flow
            #for key in self.flow:
            #    print '%s:%s' % (key,self.flow[key])
            path = self.FindPath(source, target, [])
            #print 'path inside of while loop: %s' % path
            #for key in self.flow:
            #    print '%s:%s' % (key,self.flow[key])
        return sum(self.flow[edge] for edge in self.GetEdges(source))


if __name__ == "__main__":

    gr = FlowNetwork()
    gr.AddVertex('root')
    gr.AddVertex('end')
    if len(sys.argv)>1:
        args=[]
        ThreeToFour={}
        FourToThree={}
        ThreeToFour = pickle.load( open( "save3t4.p", "rb" ) )
        FourToThree = pickle.load( open( "save4t3.p", "rb" ) )
        for i in sys.argv[1:]:
            args.append(i)
        #print args
        req=()
        if len (args) == 4:
            for i in args:
                req=req+(int(i),)
            print req
            a= Magic4to3(FourToThree,req)
            print a
            sys.exit(0)
        if len (args) == 3:
            for i in args:
                req=req+(int(i),)
            print req
            a= Magic3to4(ThreeToFour,req)
            print a
            sys.exit(0)



    for i in it.combinations(range(27),4):
        gr.AddVertex(i)
        gr.AddEdge('root',i,1)
        for t in it.combinations(i,3):
            for j in it.permutations(t):
                gr.AddVertex(j)
                gr.AddEdge(i,j,1)
                gr.AddEdge(j,'end',1)
    print gr.MaxFlow('root','end')

    ThreeToFour={}
    FourToThree={}
    for i in gr.flow.keys():
        if gr.flow[i]==1:
            k=str(i)
            four,three=k.split('~')
            FourToThree[four]=three
            ThreeToFour[three]=four
    pickle.dump( FourToThree, open( "save4t3.p", "wb" ) )
    pickle.dump( ThreeToFour, open( "save3t4.p", "wb" ) )
