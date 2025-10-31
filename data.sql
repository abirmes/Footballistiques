CREATE TABLE competition (
    id_competition SERIAL PRIMARY KEY,
    nom_competition VARCHAR(100) NOT NULL
);

CREATE TABLE saison (
    id_saison SERIAL PRIMARY KEY,
    annee VARCHAR(10) NOT NULL
);

CREATE TABLE equipe (
    idequipe SERIAL PRIMARY KEY,
    nomequipe VARCHAR(100),
    idcompetition INT REFERENCES competition(idcompetition),
    idsaison INT REFERENCES saison(id_saison)
);

CREATE TABLE joueurs (
    id_joueur SERIAL PRIMARY KEY,
    nom_joueur VARCHAR(100) NOT NULL,
    nationalite VARCHAR(50),
    poste VARCHAR(10),
    age INT,
    matchs_joues INT,
    minutes INT,
    id_equipe INT REFERENCES equipe(id_equipe)
);

CREATE TABLE matchs (
    id_match SERIAL PRIMARY KEY,
    date_match DATE NOT NULL,
    heure TIME,
    round VARCHAR(50),
    dayofweek VARCHAR(10),
    venue VARCHAR(20),
    result CHAR(1),
    goals_for INT,
    goals_against INT,
    opponent VARCHAR(100),
    xg_for DECIMAL(3,1),
    xg_against DECIMAL(3,1),
    possession DECIMAL(4,1),
    attendance INT,
    captain VARCHAR(100),
    formation VARCHAR(20),
    opp_formation VARCHAR(20),
    referee VARCHAR(100),
    team VARCHAR(100),
    id_competition INT REFERENCES competition(id_competition),
    id_saison INT REFERENCES saison(id_saison)
);

CREATE TABLE resultat_match (
    id_resultat SERIAL PRIMARY KEY,
    id_match INT REFERENCES matchs(id_match),
    id_equipe INT REFERENCES equipe(id_equipe),
    buts_marques INT,
    buts_concedes INT,
    resultat VARCHAR(10) CHECK (resultat IN ('Victoire', 'Défaite', 'Nul'))
);

CREATE TABLE statistique_joueur (
    id_stats SERIAL PRIMARY KEY,
    id_joueur INT REFERENCES joueurs(id_joueur),
    buts INT,
    passes_decisives INT,
    nb_matches_played INT,
    cartons_jaunes INT,
    cartons_rouges INT
);
