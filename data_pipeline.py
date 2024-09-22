import psycopg2

# Informations de connexion à la base de données PostgreSQL
hostname = "localhost"
database = "Local"
username = "postgres"
pwd = ""
port_id = 5432
conn = None
cur = None

try:
    # Connexion à la base de données PostgreSQL
    conn = psycopg2.connect(
        host=hostname,      # Adresse du serveur (ici en local)
        dbname=database,     # Nom de la base de données
        user=username,       # Nom d'utilisateur PostgreSQL
        password=pwd,        # Mot de passe pour l'utilisateur
        port=port_id         # Port utilisé par PostgreSQL (par défaut 5432)
    )
    print("Database connected")  # Message de confirmation que la connexion est réussie

    # Création du curseur pour exécuter des requêtes SQL
    cur = conn.cursor()

    # Requête SQL pour récupérer les informations des étudiants, enseignants et classes
    req = '''
        SELECT
            e.prenom as prenom_etudiant,  # Prénom de l'étudiant
            e.nom as nom_etudiant,        # Nom de l'étudiant
            ens.prenom as prenom_enseignant,  # Prénom de l'enseignant
            ens.nom as nom_enseignant,        # Nom de l'enseignant
            c.n_classe as numero_classe       # Numéro de la classe
        FROM etudiants e
        JOIN enseignants ens ON e.id_classe = ens.id_classe  # Jointure entre les étudiants et les enseignants via id_classe
        JOIN classes c ON e.id_classe = c.id  # Jointure entre les étudiants et les classes via id_classe
    '''
    
    # Exécution de la requête SQL
    cur.execute(req)

    # Récupération de tous les résultats de la requête
    results = cur.fetchall()
    
    # Transformation des résultats en dictionnaire pour faire correspondre chaque classe à ses étudiants et enseignants
    association = {}

    # Parcours des résultats pour remplir le dictionnaire 'association'
    for prenom_etudiant, nom_etudiant, prenom_enseignant, nom_enseignant, numero_classe in results:
        # Si la classe n'est pas encore dans le dictionnaire, on l'ajoute avec une liste vide
        if numero_classe not in association:
            association[numero_classe] = []
        
        # On ajoute un dictionnaire qui associe l'étudiant à son enseignant pour chaque classe
        association[numero_classe].append({
            'etudiant': f"{prenom_etudiant} {nom_etudiant}",  # Nom complet de l'étudiant
            'enseignant': f"{prenom_enseignant} {nom_enseignant}"  # Nom complet de l'enseignant
        })

    # Déclaration d'un dictionnaire pour compter le nombre d'élèves par enseignant
    compte_eleves = {}

    # Deuxième boucle pour compter combien d'élèves sont associés à chaque enseignant
    for prenom_etudiant, nom_etudiant, prenom_enseignant, nom_enseignant, numero_classe in results:
        # Création d'une chaîne de caractères avec le nom complet de l'enseignant
        enseignant_full_name = f"{prenom_enseignant} {nom_enseignant}"
        
        # Si l'enseignant n'est pas encore dans le dictionnaire, on l'ajoute avec un compteur initialisé à 0
        if enseignant_full_name not in compte_eleves:
            compte_eleves[enseignant_full_name] = 0
        
        # Incrémentation du compteur d'élèves pour cet enseignant
        compte_eleves[enseignant_full_name] += 1

    # Affichage du nombre d'élèves pour chaque enseignant
    print("Nombre d'élèves par enseignant :")
    for enseignant, nombre in compte_eleves.items():
        print(f"{enseignant} : {nombre} élève(s)")

    # Validation des modifications (ici, il n'y en a pas car on ne fait que des SELECT)
    conn.commit()

# Gestion des erreurs
except Exception as error:
    # Si une erreur se produit, elle est affichée
    print(error)

# Bloc 'finally' pour s'assurer que la connexion à la base de données est toujours fermée
finally:
    if cur is not None:
        cur.close()  # Fermeture du curseur
    if conn is not None:
        conn.close()  # Fermeture de la connexion à la base de données
