CREATE TABLE fact_votes (
    fact_votes_key SERIAL PRIMARY KEY,
    parish_key INT NOT NULL, -- references dim_parish
    party_key INT NOT NULL, -- references dim_party
    coalition_key INT, -- references dim_coalition
    election_key INT NOT NULL, -- references dim_election
    
    -- Measures
    number_of_votes INT,
    is_winner BOOLEAN,  -- or store a smallint/enum if relevant
    
    FOREIGN KEY (parish_key) REFERENCES dim_parish(parish_key),
    FOREIGN KEY (party_key) REFERENCES dim_party(party_key),
    FOREIGN KEY (coalition_key) REFERENCES dim_coalition(coalition_key),
    FOREIGN KEY (election_key) REFERENCES dim_election(election_key)
);
