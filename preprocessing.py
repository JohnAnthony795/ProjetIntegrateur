import csv
from geopy.distance import vincenty

readdata = csv.reader(open("density-map-from-20160101-to-20161231-5-probability.csv"))
graph = {}
ligne = 0
colonne = 0
separateur = "$"
precision = 5


def conversion(ligne, colonne):
    longitude = -180 + float((colonne - 1)) / precision
    latitude = 90 - float((ligne - 1)) / precision
    return round(latitude, 6), round(longitude, 6)


myFile = open('nodes.csv', 'wb')
with myFile:
    myFields = ['id', 'lat', 'long']
    writer = csv.DictWriter(myFile, fieldnames=myFields)
    writer.writeheader()
    id = 1
    for row in readdata:
        ligne += 1
        colonne = 0
        for node in row:
            colonne += 1
            if float(node) > 0.0001:
                latitude, longitude = conversion(int(ligne), int(colonne))
                writer.writerow({'id': id, 'lat': latitude, 'long': longitude})
                graph[str(ligne) + separateur + str(colonne)] = [id, latitude, longitude, float(node)]
                id += 1

# poidArc = distanceEnKm(node, nextNode) * ((1-density[node])+(1-density[nextNode))
myFile = open('arcs.csv', 'wb')
with myFile:
    myFields = ['node', 'nextNode', 'distance']
    writer = csv.DictWriter(myFile, fieldnames=myFields)
    writer.writeheader()
    for key in graph.keys():
        ligne, colonne = key.split(separateur)
        if (ligne + separateur + str(int(colonne) - 1)) in graph:
            writer.writerow({'node': graph[ligne + separateur + str(int(colonne) - 1)][0], 'nextNode': graph[key][0],
                             'distance': round(vincenty((graph[ligne + separateur + str(int(colonne) - 1)][1],
                                                    graph[ligne + separateur + str(int(colonne) - 1)][2]),
                                                   (graph[key][1], graph[key][2])).km * (1 - graph[key][3] + 1 - graph[ligne + separateur + str(int(colonne) - 1)][3]), 3)})
        if (str(int(ligne) - 1) + separateur + colonne) in graph:
           writer.writerow({'node': graph[str(int(ligne) - 1) + separateur + colonne][0], 'nextNode': graph[key][0],
                             'distance': round(vincenty((graph[str(int(ligne) - 1) + separateur + colonne][1],
                                                    graph[str(int(ligne) - 1) + separateur + colonne][2]),
                                                   (graph[key][1], graph[key][2])).km * (1 - graph[key][3] + 1 - graph[str(int(ligne) - 1) + separateur + colonne][3]), 3)})
        if (ligne + separateur + str(int(colonne) + 1)) in graph:
            writer.writerow({'node': graph[ligne + separateur + str(int(colonne) + 1)][0], 'nextNode': graph[key][0],
                             'distance': round(vincenty((graph[ligne + separateur + str(int(colonne) + 1)][1],
                                                    graph[ligne + separateur + str(int(colonne) + 1)][2]),
                                                   (graph[key][1], graph[key][2])).km * (1 - graph[key][3] + 1 - graph[ligne + separateur + str(int(colonne) + 1)][3]), 3)})
        if (str(int(ligne) + 1) + separateur + colonne) in graph:
            writer.writerow({'node': graph[str(int(ligne) + 1) + separateur + colonne][0], 'nextNode': graph[key][0],
                             'distance': round(vincenty((graph[str(int(ligne) + 1) + separateur + colonne][1],
                                                    graph[str(int(ligne) + 1) + separateur + colonne][2]),
                                                   (graph[key][1], graph[key][2])).km * (1 - graph[key][3] + 1 - graph[str(int(ligne) + 1) + separateur + colonne][3]), 3)})
        if (str(int(ligne) - 1) + separateur + str(int(colonne) - 1)) in graph:
            writer.writerow(
                {'node': graph[str(int(ligne) - 1) + separateur + str(int(colonne) - 1)][0], 'nextNode': graph[key][0],
                 'distance': round(vincenty((graph[str(int(ligne) - 1) + separateur + str(int(colonne) - 1)][1],
                                        graph[str(int(ligne) - 1) + separateur + str(int(colonne) - 1)][2]),
                                       (graph[key][1], graph[key][2])).km * (1 - graph[key][3] + 1 - graph[str(int(ligne) - 1) + separateur + str(int(colonne) - 1)][3]), 3)})
        if (str(int(ligne) + 1) + separateur + str(int(colonne) - 1)) in graph:
            writer.writerow(
                {'node': graph[str(int(ligne) + 1) + separateur + str(int(colonne) - 1)][0], 'nextNode': graph[key][0],
                 'distance': round(vincenty((graph[str(int(ligne) + 1) + separateur + str(int(colonne) - 1)][1],
                                        graph[str(int(ligne) + 1) + separateur + str(int(colonne) - 1)][2]),
                                       (graph[key][1], graph[key][2])).km * (1 - graph[key][3] + 1 - graph[str(int(ligne) + 1) + separateur + str(int(colonne) - 1)][3]), 3)})
        if (str(int(ligne) - 1) + separateur + str(int(colonne) + 1)) in graph:
            writer.writerow(
                {'node': graph[str(int(ligne) - 1) + separateur + str(int(colonne) + 1)][0], 'nextNode': graph[key][0],
                 'distance': round(vincenty((graph[str(int(ligne) - 1) + separateur + str(int(colonne) + 1)][1],
                                        graph[str(int(ligne) - 1) + separateur + str(int(colonne) + 1)][2]),
                                       (graph[key][1], graph[key][2])).km * (1 - graph[key][3] + 1 - graph[str(int(ligne) - 1) + separateur + str(int(colonne) + 1)][3]), 3)})
        if (str(int(ligne) + 1) + separateur + str(int(colonne) + 1)) in graph:
            writer.writerow(
                {'node': graph[str(int(ligne) + 1) + separateur + str(int(colonne) + 1)][0], 'nextNode': graph[key][0],
                 'distance': round(vincenty((graph[str(int(ligne) + 1) + separateur + str(int(colonne) + 1)][1],
                                        graph[str(int(ligne) + 1) + separateur + str(int(colonne) + 1)][2]),
                                       (graph[key][1], graph[key][2])).km * (1 - graph[key][3] + 1 - graph[str(int(ligne) + 1) + separateur + str(int(colonne) + 1)][3]), 3)})

        del graph[key]
