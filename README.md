# EuropeanaApiHelpers
Contains tools to retrieve collections from Europeana API


### Dépendances
Il est nécessaire d'avoir installé Python3 pour éxécuter ces scipts. (https://www.python.org/downloads/)


### Convert a Json file to CSV
Pour convertir un fichier json en fichier csv, entrez la commande suivante dans un terminal:

```
python3 JtoC.py your_file.json
```


### Cursor search
L'API Europeana utilise le cursor search pour récupérer plusieurs pages de données. Le script europeana_cursor_search.py gère automatiquement le cursor search et enregistre les données directement dans un fichier csv.

Pour récolter toutes les pages d'une collection, entrez la commande suivante dans un terminal  en prenant soin de remplacer *CLE_PUBLIQUE* par votre clé publique et REQUETE par les mots clé de votre requête :

```
python3 europeana_cursor_search.py "https://www.europeana.eu/api/v2/search.json?wskey=CLE_PUBLIQUE&query=REQUETE" nom_fichier.csv
```

Une fois exécutée, nom_fichier sera créé dans votre répertoire et la liste des noms de colonnes sera affiché dans votre terminal.

Pour garder uniquement certaines colonnes du fichier .csv, il est nécessaire de créer un fichier .txt contenant les noms des colonnes à garder. Par exemple :
> *mes_colonnes.txt*
```
items_title
items_type
items_ugc
items_year
items_guid
items_id
```

Ensuite, entrez la commande suivante dans votre terminal : 
```
python3 europeana_cursor_search.py "https://www.europeana.eu/api/v2/search.json?wskey=CLE_PUBLIQUE&query=REQUETE" nom_fichier.csv --col mes_colonnes.txt
```

