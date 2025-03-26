-- 1. District Dimension
CREATE TABLE dim_district (
    district_id SERIAL PRIMARY KEY, -- surrogate key
    dcode VARCHAR(10) NOT NULL, -- ID from source
    dname VARCHAR(100),
);

-- 2. Municipality Dimension
CREATE TABLE dim_municipality (
    municipality_id SERIAL PRIMARY KEY, -- surrogate key
    mcode VARCHAR(10), -- ID from source
    mname VARCHAR(100),
    FOREIGN KEY district_id REFERENCES dim_district(district_id), -- references dim_district
    dname VARCHAR(100),
    dcode VARCHAR(10),
    -- Additional attributes and restrictions as needed
    UNIQUE(mcode)    
);

-- 3. Parish Dimension
CREATE TABLE dim_parish (
    parish_id SERIAL PRIMARY KEY, -- surrogate key
    pname VARCHAR(100),
    pcode VARCHAR(10),
    FOREIGN KEY district_id REFERENCES dim_district(district_id), -- references dim_district
    mname VARCHAR(100),
    mcode VARCHAR(10),
    municipality_id INT, -- references dim_municipality
    -- Additional attributes and restrictions as needed
    UNIQUE(parish_id),
    FOREIGN KEY (municipality_key) REFERENCES dim_municipality(municipality_key)
);

-- 4. Party Dimension
CREATE TABLE dim_party (
    party_key SERIAL PRIMARY KEY,
    party_id VARCHAR(10) NOT NULL,
    acronym VARCHAR(50),
    ideology VARCHAR(100), -- Additional attributes
    UNIQUE(party_id)
);

-- 5. Coalition Dimension
CREATE TABLE dim_coalition (
    coalition_key SERIAL PRIMARY KEY,
    coalition_id VARCHAR(10) NOT NULL,
    coalition_name VARCHAR(100), -- Additional attributes
    UNIQUE(coalition_id)
);

-- 6. Election Dimension
CREATE TABLE dim_election (
    election_key SERIAL PRIMARY KEY,
    election_id VARCHAR(10) NOT NULL,
    e_name VARCHAR(100),
    e_date DATE, -- Additional attributes
    UNIQUE(election_id)
);
