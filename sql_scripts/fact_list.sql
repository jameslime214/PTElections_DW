-- List Dimension
CREATE TABLE dim_list (
    list_key SERIAL PRIMARY KEY,
    list_id VARCHAR(10) NOT NULL,
    district_key INT, -- references dim_district if relevant
    party_key INT, -- references dim_party if relevant
    n_mandates INT,
    n_votes INT,
    -- Additional attributes
    UNIQUE(list_id),
    FOREIGN KEY (district_key) REFERENCES dim_district(district_key),
    FOREIGN KEY (party_key) REFERENCES dim_party(party_key)
);