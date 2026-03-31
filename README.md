# NetDB-RK | Gestion de Parc Centralisée

## Description

NetDB-RK est une application web moderne pour la gestion centralisée d'équipements réseau et de parc informatique. Développée avec Flask et PostgreSQL, elle offre une interface complète pour superviser, administrer et maintenir l'inventaire des infrastructures IT.

## Fonctionnalités

### 🖥️ Interface Web Moderne
- Design sombre professionnel avec thème néon
- Interface responsive adaptée aux mobiles
- Tableau de bord avec statistiques en temps réel
- Animations et transitions fluides

### 📊 Gestion des Équipements (CRUD)
- **Créer** : Ajout simple d'équipements via formulaire modal
- **Lire** : Affichage en tableau avec tri et filtrage
- **Mettre à jour** : Modification des informations existantes
- **Supprimer** : Retrait sécurisé avec confirmation

### 🗄️ Base de Données Robuste
- PostgreSQL avec contraintes d'intégrité
- Structure optimisée avec index
- Trigger automatique pour les timestamps
- Sauvegarde et restauration facilitées

### 🐀 Conteneurisation Docker
- Architecture microservices
- Déploiement simplifié avec Docker Compose
- Isolation des services
- Health checks automatiques

## Architecture Technique

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Navigateur    │◄──►│   Flask App     │◄──►│  PostgreSQL     │
│   (Bootstrap)   │    │   (Python)      │    │   (Database)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
    ┌─────────┐            ┌─────────┐            ┌─────────┐
    │  HTML5  │            │  CRUD   │            │  SQL    │
    │   CSS3  │            │  API    │            │  Schema │
    │   JS    │            │  Routes │            │  Index  │
    └─────────┘            └─────────┘            └─────────┘
```

## Installation Rapide

### Prérequis
- Docker et Docker Compose
- Git

### Démarrage

1. **Cloner le projet**
```bash
git clone <repository-url>
cd netdb-rk
```

2. **Démarrer les services**
```bash
docker-compose up -d
```

3. **Accéder à l'application**
- URL : http://localhost:5000
- Base de données : localhost:5432

### Développement Local

1. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

2. **Configurer PostgreSQL**
```bash
# Créer la base de données
createdb netdb_rk

# Appliquer le schéma
psql -d netdb_rk -f schema.sql
```

3. **Démarrer l'application**
```bash
python app.py
```

## Structure du Projet

```
netdb-rk/
├── app.py                 # Application Flask principale
├── schema.sql             # Schéma de la base de données
├── requirements.txt       # Dépendances Python
├── Dockerfile            # Configuration Docker
├── docker-compose.yml    # Orchestration des services
├── templates/
│   └── index.html       # Interface web principale
├── README.md             # Documentation
└── .gitignore           # Fichiers ignorés par Git
```

## API Endpoints

| Méthode | URL | Description |
|---------|-----|-------------|
| GET | `/` | Page principale avec tableau des équipements |
| POST | `/ajouter` | Ajouter un nouvel équipement |
| GET/POST | `/modifier/<id>` | Modifier un équipement existant |
| GET | `/supprimer/<id>` | Supprimer un équipement |
| GET | `/api/equipements` | API JSON des équipements |

## Schéma de la Base de Données

```sql
equipements (
    id SERIAL PRIMARY KEY,
    nom_equipement VARCHAR(100) NOT NULL,
    type VARCHAR(50) CHECK (type IN ('Serveur', 'Switch', 'Routeur', 'PC')),
    adresse_ip VARCHAR(15) UNIQUE,
    emplacement VARCHAR(100),
    statut VARCHAR(20) CHECK (statut IN ('Actif', 'En Maintenance', 'Hors Service')),
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_mise_a_jour TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Configuration des Variables d'Environnement

```bash
# Base de données
DB_HOST=localhost
DB_NAME=netdb_rk
DB_USER=postgres
DB_PASSWORD=password
DB_PORT=5432

# Application
FLASK_ENV=development
FLASK_DEBUG=True
```

## Déploiement en Production

### Docker Production
```bash
# Build et déploiement
docker-compose -f docker-compose.prod.yml up -d

# Logs
docker-compose logs -f app
```

### CI/CD GitHub Actions
Le projet est configuré pour :
- Tests automatiques
- Build Docker
- Déploiement continu
- Scan de sécurité

## Maintenance

### Sauvegarde
```bash
# Export de la base de données
docker-compose exec postgres pg_dump -U postgres netdb_rk > backup.sql

# Restauration
docker-compose exec -T postgres psql -U postgres netdb_rk < backup.sql
```

### Logs
```bash
# Logs de l'application
docker-compose logs app

# Logs de la base de données
docker-compose logs postgres
```

## Sécurité

- Connexions chiffrées SSL/TLS
- Validation des entrées utilisateur
- Protection contre les injections SQL
- Authentification et autorisation
- Audit des accès

## Support et Contribution

Pour toute question ou contribution :
- Issues GitHub
- Documentation technique
- Tests unitaires
- Code review

---

**NetDB-RK | Gestion de Parc Centralisée**  
*Architecture Microservices | CI/CD GitHub Actions | Dockerized*
