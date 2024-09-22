import psycopg2

hostname = "localhost"
database = "Local"
username = "postgres"
pwd = "diarms"
port_id = 5432
conn = None
cur = None
try:
    conn = psycopg2.connect(
        host=hostname,
        dbname=database,
        user=username,
        password=pwd,
        port=port_id
    )
    print("Database connected")

    cur = conn.cursor()

    req = '''
            SELECT
                e.prenom as prenom_etudiant,
                e.nom as nom_etudiant,
                ens.prenom as prenom_enseignant,
                ens.nom as nom_enseignant,
                c.n_classe as numero_classe
            FROM etudiants e
            JOIN enseignants ens ON e.id_classe = ens.id_classe
            JOIN classes c ON e.id_classe = c.id   
        '''
    cur.execute (req)

    results = cur.fetchall()
    
    #Transformation en dict
    association = {}

    for prenom_etudiant, nom_etudiant, prenom_enseignant, nom_enseignant, numero_classe in results:
        if numero_classe not in association:
            association[numero_classe] = []
        association[numero_classe].append({
            'etudiant' : f"{prenom_etudiant} {nom_etudiant}",
            'enseignant' : f"{prenom_enseignant} {nom_enseignant}"
        })
    #print(association)

    '''for prenom_etudiant, nom_etudiant, prenom_enseignant, nom_enseignant, numero_classe in results:
        print(f"Classe {numero_classe} : {prenom_etudiant} {nom_etudiant} est associé à {prenom_enseignant} {nom_enseignant}.")'''

    compte_eleves = {} #Ce dictionnaire stocke le nombre d'élèves pour chaque enseignant. La clé est le nom complet de l'enseignant, et la valeur est le compteur d'élèves.'''

    for prenom_etudiant, nom_etudiant, prenom_enseignant, nom_enseignant, numero_classe in results:
        enseignant_full_name = f"{prenom_enseignant} {nom_enseignant}"
        if enseignant_full_name not in compte_eleves:
            compte_eleves[enseignant_full_name] =0 
        compte_eleves[enseignant_full_name] += 1
    print("Nombre d'élèves par enseignant :")
    for enseignant, nombre in compte_eleves.items():
        print(f"{enseignant} : {nombre} élève(s)")

    
    conn.commit()
except Exception as error:
    print(error)

finally:
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()
