import psycopg

def test_connexion_db():
    try:
        # Remplacez les paramètres de connexion par les vôtres
        conn = psycopg.connect(
            dbname="appointments",
            user="user",
            password="pass",
            host="localhost",
            port="5433"
        )
        print("Connexion à la base de données réussie !")
        # Test simple de requête
        cursor = conn.cursor()
        cursor.execute("SELECT 1;")
        result = cursor.fetchone()
        assert result[0] == 1
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Erreur de connexion à la base de données : {e}")
        assert False, "La connexion à la base de données a échoué."