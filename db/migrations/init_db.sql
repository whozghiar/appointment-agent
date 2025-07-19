CREATE TABLE IF NOT EXISTS appointment (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    sexe VARCHAR(10) NOT NULL,
    telephone VARCHAR(15) NOT NULL,
    date TIMESTAMP NOT NULL,
    prestation VARCHAR(100)
);

INSERT INTO appointment (nom, sexe, telephone, date, prestation)
VALUES
    ('Alice Dupont', 'Femme', '0123456789', '2023-10-01 10:00:00', 'Coloration'),
    ('Bob Martin', 'Homme', '0987654321', '2023-10-02 11:00:00', 'Degrade'),
    ('Claire Dubois', 'Femme', '0147258369', '2023-10-03 12:00:00', 'Brushing');
