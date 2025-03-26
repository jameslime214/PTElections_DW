CREATE TABLE fact_participation (
    fact_participation_key SERIAL PRIMARY KEY,
    district_key INT NOT NULL, -- references dim_district
    election_key INT NOT NULL, -- references dim_election

    -- Measures
    total_voters INT,
    abstentions INT,
    blank_votes INT,
    null_votes INT, -- etc.
    
    FOREIGN KEY (district_key) REFERENCES dim_district(district_key),
    FOREIGN KEY (election_key) REFERENCES dim_election(election_key)
);
