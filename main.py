from enum import auto
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
unos='''0:1, 2, 2, 3, 3, 4, 4, 4, 5, 6, 7, 8, 8, 8, 10, 11, 12, 13, 17, 19, 19, 19, 21, 31
1:0, 2, 3, 7, 13, 17, 19, 21, 30
2:0, 0, 1, 3, 7, 8, 9, 13, 13, 13, 13, 27, 28, 32
3:0, 0, 1, 2, 7, 12, 13
4:0, 0, 0, 6, 6, 10
5:0, 6, 10, 16
6:0, 4, 4, 5, 16
7:0, 1, 2, 3
8:0, 0, 0, 2, 30, 32, 33
9:2, 33
10:0, 4, 5
11:0
12:0, 3
13:0, 1, 2, 2, 2, 2, 3, 33, 33, 33
14:32, 33
15:32, 33
16:5, 6
17:0, 1
18:32, 33
19:0, 0, 0, 1, 33
20:32, 33
21:0, 1
22:32, 33
23:25, 27, 29, 29, 32, 32, 33
24:25, 27, 31
25:23, 24, 31
26:29, 29, 33
27:2, 23, 24, 33
28:2, 31, 33
29:23, 23, 26, 26, 32, 33
30:1, 8, 32, 33
31:0, 24, 25, 28, 32, 32, 32, 33, 33
32:2, 8, 14, 15, 18, 20, 22, 23, 23, 29, 30, 31, 31, 31, 33, 33, 33
33:8, 9, 13, 13, 13, 14, 15, 18, 19, 20, 22, 23, 26, 27, 28, 29, 30, 31, 31, 32, 32, 32
'''
unos2=unos+" "
v=19
t=27
def unesi():
    linije = unos.splitlines()
    veze=list()
    for line in linije:
        jedan=list()
        deli=line.split(':')
        elementi=deli[1].split(',')
        for ele in elementi:
            if int(deli[0])<=int(ele.strip()):
                jedan.append(int(ele.strip()))
        veze.append(jedan)
    return veze


veze=unesi()
#i=0
# for veza in veze:
#     print(str(i)+":"+str(veza))
#     i+=1
G=nx.MultiGraph()
G.add_nodes_from(range(0,len(unos.splitlines())))

i=0
for veza in veze:
    for broj in veza:
        G.add_edge(i,broj)
    i=i+1

print("1. Suma svih brojeva")
suma = sum(dict(G.degree()).values()) - G.degree(v) - G.degree(t)
print(suma)

print("2. Postoji ovoliko najkracih puteva")
i=0
for path in nx.all_shortest_paths(G,v,t):
    i=i+1
print(i)

print("3. Razliciti neighbori su")
jedan=G.neighbors(v)
prvi=list()
for broj in jedan:
    prvi.append(broj)

dva=G.neighbors(t)
drugi=list()
for broj in dva:
    drugi.append(broj)
res=list(set(prvi).difference(set(drugi)) | set(drugi).difference(set(prvi)))
print(res)

print("4. Cvorovi susedi v i t koji imaju stepen veci od proseka")
avg_degree = sum(dict(G.degree()).values()) / G.number_of_nodes()
komsije=list(set(prvi).union(set(drugi)))
veci_od_proseka=list()
for broj in komsije:
    if(G.degree(broj)>avg_degree):
        veci_od_proseka.append(broj)
print(veci_od_proseka)

print("5. Podgraf v i t i njihovih komsija")
S={v,t}|set(komsije)
podgraf=G.subgraph(S).number_of_edges()
print(podgraf)
print("6. Svi nodovi koji su udelji najvise 3 od v i t")
naj_od_t=nx.single_source_shortest_path_length(G,t, 3)
naj_t_set=set(naj_od_t.keys())
naj_od_v=nx.single_source_shortest_path_length(G,v, 3)
naj_v_set=set(naj_od_v.keys())
udaljeni_tri_od_oba=naj_t_set.intersection(naj_v_set)
print(udaljeni_tri_od_oba)
print("7. Ekscentricitet od v + t")
ekscentriteti=nx.eccentricity(G)
print(ekscentriteti[v]+ekscentriteti[t])
print("8. Koliko povezanih komponenti ima cvor nakon uklanjanja dva najpovezanija cvora i v i t")
G2=G.copy()
remaining = [n for n in G.nodes() if n not in {v, t}]
sorted_rem = sorted(remaining, key=lambda x: (-G.degree(x), x))
top2 = sorted_rem[:2]
G2.remove_nodes_from(top2+[v,t])
print(nx.number_connected_components(G2))
print("9. Broj puteva duzine 3 izmedju v i t izmedju")
linije = unos.splitlines()
matrica=np.zeros((len(linije),len(linije)))
i=0
for line in linije:
    jedan=list()
    deli=line.split(':')
    elementi=deli[1].split(',')
    for ele in elementi:
        matrica[i][int(ele.strip())]=matrica[i][int(ele.strip())]+1
    i=i+1

matrica.view()
matrica3 = np.linalg.matrix_power(matrica, 3)

print("Matrica^3 element [v][t]:", matrica3[v][t])
print("10. Matrice t i v broj puteva duzine 10 izmedju njih")
matrica10 = np.linalg.matrix_power(matrica, 10)
# print(matrica10) # Optional: printing large matrices might clutter output
print("Matrica^10 element [v][t]:", matrica10[v][t])
