# ProjetIntegrateur
_Bruneau Léo, Bügel Sandor, Lanore Sébastien, Pellerin Maly, Rouquette Quentin_

### Prérequis
* Java 8
* Une base Neo4J fonctionnelle

### Guide
* Lancer la base Neo4J
* Lancer l'API rest (python rest_api.py)
* Effectuer une requête GET vers l'API déployée (par défaut à localhost:5000) avec le format suivant:
    http://localhost:5000/route/<latitudeSource>/<longitudeSource>/<latitudeDestination>/<longitudeDestination>
ou
    http://localhost:5000/route/<latitudeSource>/<longitudeSource>/<latitudeDestination>/<longitudeDestination>/kml
pour obtenir une route exportable sur Google Earth.
Ces adresses peuvent aussi être visitées telles quelles en navigateur.
