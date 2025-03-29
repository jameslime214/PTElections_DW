-- 1) District Table

CREATE TABLE District (
    DistrictId INT PRIMARY KEY,
    code VARCHAR(50) NOT NULL,
    name VARCHAR(100) NOT NULL,
    region VARCHAR(100)
    );

-- 2) Participation Table
--    References District (DistrictId)

CREATE TABLE Participation (
    uniqueId INT PRIMARY KEY,
    DistrictId INT NOT NULL,
    is_enrolled INT NOT NULL,
    voting INT NOT NULL,
    abstentions INT NOT NULL,
    null_votes INT,
    blank_votes INT,
    FOREIGN KEY (DistrictId) REFERENCES District(DistrictId)
    );

-- 3) Municipality Table
--    References District (DistrictId)

CREATE TABLE Municipality ( MunicipalityId INT PRIMARY KEY,
                                                       code VARCHAR(50),
                                                            name VARCHAR(100),
                                                                 DistrictId INT NOT NULL,
                           FOREIGN KEY (DistrictId) REFERENCES District(DistrictId));

-- 4) Parish Table
--    References Municipality (MunicipalityId)

CREATE TABLE Parish ( ParishId INT PRIMARY KEY,
                                           code VARCHAR(50),
                                                name VARCHAR(100),
                                                     MunicipalityId INT NOT NULL,
                     FOREIGN KEY (MunicipalityId) REFERENCES Municipality(MunicipalityId));

-- 5) Party Table

CREATE TABLE Party ( PartyId INT PRIMARY KEY,
                                         Acronym VARCHAR(50),
                                                 Name VARCHAR(100));

-- 6) List Table
--    References Party (PartyId)

CREATE TABLE List ( ListId INT PRIMARY KEY,
                                       name VARCHAR(100),
                                            PartyId INT NOT NULL,
                   FOREIGN KEY (PartyId) REFERENCES Party(PartyId));

-- 7) Voting Table
--    Composite PK: (ParishId, ListId)
--    References Parish (ParishId) and List (ListId)

CREATE TABLE Voting ( ParishId INT NOT NULL,
                                   ListId INT NOT NULL,
                                              votes INT, PRIMARY KEY (ParishId,
                                                                      ListId),
                     FOREIGN KEY (ParishId) REFERENCES Parish(ParishId),
                     FOREIGN KEY (ListId) REFERENCES List(ListId));

-- 8) Coalition Table
--    References Party (PartyId)

CREATE TABLE Coalition ( CoalitionID INT PRIMARY KEY,
                                                 PartyId INT NOT NULL,
                                                             year INT,
                        FOREIGN KEY (PartyId) REFERENCES Party(PartyId));

-- 9) Coalition_Name Table
--    References Coalition (CoalitionID)

CREATE TABLE Coalition_Name ( CoalitionId INT PRIMARY KEY,
                                                      Coalition_year INT, CoalitionName VARCHAR(100),
                             FOREIGN KEY (CoalitionId) REFERENCES Coalition(CoalitionID));

