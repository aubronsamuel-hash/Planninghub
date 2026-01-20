# Décision : Utiliser SQLite pour la base de données

Date: 2024-07-26
Statut: Accepté
Propriétaires: Jules (Agent IA)

## Contexte
Le projet a besoin d'une base de données pour stocker les données de l'application, mais aucune n'a encore été choisie.

## Options
1. Utiliser une base de données en mémoire : simple pour les tests mais pas de persistance.
2. Utiliser une base de données complète comme PostgreSQL : puissante mais complexe à mettre en place pour un démarrage.
3. Utiliser SQLite : simple, basée sur des fichiers, persistante et facile à intégrer.

## Décision
Nous allons utiliser SQLite comme première base de données pour le projet.

## Justification
SQLite est un excellent choix pour démarrer rapidement. Il ne nécessite aucune configuration de serveur, est bien supporté par Python et stocke la base de données dans un simple fichier, ce qui facilite le développement et les tests. C'est une solution légère et efficace pour les premières étapes du projet.

## Conséquences
Un adaptateur de persistance pour SQLite devra être créé dans le répertoire `planninghub/adapters/persistence`. Le domaine et la logique de l'application devront interagir avec le port de persistance, sans connaître les détails d'implémentation de SQLite.
