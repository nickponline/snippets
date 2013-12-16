G = {'s':{'u':10, 'x':5},
     'u':{'v':1, 'x':2},
     'v':{'y':4},
     'x':{'u':3, 'v':9, 'y':2},
     'y':{'s':7, 'v':6}}

f = open('dotgraph.txt','w')
f.writelines('digraph G {\nnode [width=.3,height=.3,shape=octagon,style=filled,color=skyblue];\noverlap="false";\nrankdir="LR";\n')
f.writelines
for i in G:

    for j in G[i]:
        s= '      '+ i
        s +=  ' -> ' +  j + ' [label="' + str(G[i][j]) + '"]'
        s+=';\n'
        f.writelines(s)

f.writelines('}')
f.close()
print "done!"