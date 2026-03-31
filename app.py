#!/usr/bin/env python3
"""
NetDB-RK | Gestionnaire Centralisé de Parc Informatique
Application Flask avec PostgreSQL pour la gestion d'équipements réseau
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'netdb_rk_secret_key_2026'

# Configuration de la base de données PostgreSQL
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'netdb_rk'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'password'),
    'port': os.getenv('DB_PORT', '5432')
}

def get_db_connection():
    """Établir une connexion à la base de données PostgreSQL"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.Error as e:
        print(f"Erreur de connexion à la base de données: {e}")
        return None

def init_database():
    """Initialiser la base de données avec le schéma"""
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                # Lire et exécuter le schéma
                with open('schema.sql', 'r') as f:
                    schema_sql = f.read()
                cur.execute(schema_sql)
                conn.commit()
                print("Base de données initialisée avec succès")
        except Exception as e:
            print(f"Erreur lors de l'initialisation: {e}")
        finally:
            conn.close()

@app.route('/')
def index():
    """Page principale avec le tableau des équipements"""
    conn = get_db_connection()
    equipements = []
    
    if conn:
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT id, nom_equipement, type, adresse_ip, emplacement, statut,
                           date_creation, date_mise_a_jour 
                    FROM equipements 
                    ORDER BY id DESC
                """)
                equipements = cur.fetchall()
        except Exception as e:
            flash(f"Erreur lors de la récupération des équipements: {e}", "error")
        finally:
            conn.close()
    
    return render_template('index.html', equipements=equipements)

@app.route('/ajouter', methods=['POST'])
def ajouter_equipement():
    """Ajouter un nouvel équipement"""
    if request.method == 'POST':
        nom = request.form.get('nom_equipement', '').strip()
        type_equip = request.form.get('type', '')
        ip = request.form.get('adresse_ip', '').strip()
        emplacement = request.form.get('emplacement', '').strip()
        statut = request.form.get('statut', 'Actif')
        
        # Validation
        if not nom or not type_equip:
            flash("Le nom et le type sont obligatoires", "error")
            return redirect(url_for('index'))
        
        conn = get_db_connection()
        if conn:
            try:
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO equipements (nom_equipement, type, adresse_ip, emplacement, statut)
                        VALUES (%s, %s, %s, %s, %s)
                        RETURNING id
                    """, (nom, type_equip, ip if ip else None, emplacement if emplacement else None, statut))
                    
                    new_id = cur.fetchone()[0]
                    conn.commit()
                    flash(f"Équipement '{nom}' ajouté avec succès (ID: {new_id})", "success")
                    
            except psycopg2.IntegrityError:
                flash("Cette adresse IP est déjà utilisée", "error")
            except Exception as e:
                flash(f"Erreur lors de l'ajout: {e}", "error")
            finally:
                conn.close()
        
        return redirect(url_for('index'))

@app.route('/modifier/<int:id>', methods=['GET', 'POST'])
def modifier_equipement(id):
    """Modifier un équipement existant"""
    conn = get_db_connection()
    
    if request.method == 'POST':
        nom = request.form.get('nom_equipement', '').strip()
        type_equip = request.form.get('type', '')
        ip = request.form.get('adresse_ip', '').strip()
        emplacement = request.form.get('emplacement', '').strip()
        statut = request.form.get('statut', 'Actif')
        
        # Validation
        if not nom or not type_equip:
            flash("Le nom et le type sont obligatoires", "error")
            return redirect(url_for('index'))
        
        if conn:
            try:
                with conn.cursor() as cur:
                    cur.execute("""
                        UPDATE equipements 
                        SET nom_equipement = %s, type = %s, adresse_ip = %s, 
                            emplacement = %s, statut = %s
                        WHERE id = %s
                    """, (nom, type_equip, ip if ip else None, emplacement if emplacement else None, statut, id))
                    
                    conn.commit()
                    flash(f"Équipement '{nom}' modifié avec succès", "success")
                    
            except psycopg2.IntegrityError:
                flash("Cette adresse IP est déjà utilisée", "error")
            except Exception as e:
                flash(f"Erreur lors de la modification: {e}", "error")
            finally:
                conn.close()
        
        return redirect(url_for('index'))
    
    # GET - Récupérer les données de l'équipement
    equipement = None
    if conn:
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM equipements WHERE id = %s", (id,))
                equipement = cur.fetchone()
        except Exception as e:
            flash(f"Erreur: {e}", "error")
        finally:
            conn.close()
    
    if not equipement:
        flash("Équipement non trouvé", "error")
        return redirect(url_for('index'))
    
    return jsonify(equipement)

@app.route('/supprimer/<int:id>')
def supprimer_equipement(id):
    """Supprimer un équipement"""
    conn = get_db_connection()
    
    if conn:
        try:
            with conn.cursor() as cur:
                # Récupérer le nom pour le message
                cur.execute("SELECT nom_equipement FROM equipements WHERE id = %s", (id,))
                result = cur.fetchone()
                
                if result:
                    nom = result[0]
                    cur.execute("DELETE FROM equipements WHERE id = %s", (id,))
                    conn.commit()
                    flash(f"Équipement '{nom}' supprimé avec succès", "success")
                else:
                    flash("Équipement non trouvé", "error")
                    
        except Exception as e:
            flash(f"Erreur lors de la suppression: {e}", "error")
        finally:
            conn.close()
    
    return redirect(url_for('index'))

@app.route('/api/equipements')
def api_equipements():
    """API endpoint pour récupérer tous les équipements en JSON"""
    conn = get_db_connection()
    equipements = []
    
    if conn:
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT id, nom_equipement, type, adresse_ip, emplacement, statut,
                           date_creation, date_mise_a_jour 
                    FROM equipements 
                    ORDER BY id DESC
                """)
                equipements = cur.fetchall()
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            conn.close()
    
    return jsonify(equipements)

if __name__ == '__main__':
    # Initialiser la base de données au démarrage
    init_database()
    
    # Démarrer l'application Flask
    app.run(host='0.0.0.0', port=5000, debug=True)
