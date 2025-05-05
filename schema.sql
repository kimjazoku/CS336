CREATE TABLE agencies(
    agency_code INT PRIMARY KEY,
    agency_name TEXT NOT NULL,
    agency_abbr TEXT NOT NULL
);

CREATE TABLE loan_types(
    loan_type INT PRIMARY KEY,
    loan_type_name TEXT NOT NULL
);

--other similar tables for types & their names....--

CREATE TABLE edit_status(
    edit_status_id SERIAL PRIMARY KEY,
    edit_status INT NULL,
    edit_status_name TEXT NULL
);

SELECT DISTINCT 
NULLIF(msamd, '')::INT AS msamd_id, 
msamd_name
INTO msamd
FROM preliminary
WHERE msamd != '';
ALTER TABLE msamd
ADD PRIMARY KEY (msamd_id);

CREATE TABLE states(
    state_code INT PRIMARY KEY,
    state_name TEXT NOT NULL,
    state_abbr TEXT NOT NULL
);

CREATE TABLE counties(
    state_code INT,
    county_code INT,
    county_name TEXT NOT NULL,
    PRIMARY KEY(state_code, county_code),
    FOREIGN KEY (state_code) REFERENCES states(state_code)
);

CREATE TABLE locations(
    location_id SERIAL PRIMARY KEY,
    county_code INT,
    msamd INT,
    state_code INT,
    census_tract_number NUMERIC(7,2),
    population INT,
    minority_population NUMERIC(5,2),
    hud_median_family_income INT,
    tract_to_msamd_income NUMERIC(5,2),
    number_of_owner_occupied_units INT,
    number_of_1_to_4_family_units INT,
    FOREIGN KEY (state_code) REFERENCES states(state_code),
    FOREIGN KEY (state_code, county_code) REFERENCES counties(state_code, county_code),
    FOREIGN KEY (msamd) REFERENCES msamd(msamd_id)
);

CREATE TABLE applications(
    application_id INT PRIMARY KEY,
    as_of_year INT NOT NULL,
    respondent_id TEXT NOT NULL,
    agency_code INT NOT NULL,
    loan_type INT NOT NULL,
    property_type INT NOT NULL,
    loan_purpose INT NOT NULL,
    owner_occupancy INT NOT NULL,
    loan_amount_000s INT, -- loan ammount
    preapproval INT NOT NULL, 
    action_taken INT NOT NULL,
    applicant_ethnicity INT NOT NULL,
    co_applicant_ethnicity INT NOT NULL,
    applicant_sex INT NOT NULL,
    co_applicant_sex INT NOT NULL,
    applicant_income_000s INT, -- applicant income
    purchaser_type INT NOT NULL,
    rate_spread INT, -- can be null
    hoepa_status INT NOT NULL,
    lien_status INT NOT NULL,
    edit_status INT, -- all null
    location_id INT NOT NULL,
    sequence_number INT, -- all null
    application_date_indicator INT, -- all null
    FOREIGN KEY (agency_code) REFERENCES agencies(agency_code),
    FOREIGN KEY (loan_type) REFERENCES loan_types(loan_type),
    FOREIGN KEY (property_type) REFERENCES property_types(property_type),
    FOREIGN KEY (loan_purpose) REFERENCES loan_purposes(loan_purpose),
    FOREIGN KEY (owner_occupancy) REFERENCES owner_occupancies(owner_occupancy),
    FOREIGN KEY (preapproval) REFERENCES preapproval(preapproval),
    FOREIGN KEY (action_taken) REFERENCES action_taken(action_taken),
    FOREIGN KEY (applicant_ethnicity) REFERENCES applicant_ethnicity(applicant_ethnicity),
    FOREIGN KEY (co_applicant_ethnicity) REFERENCES co_applicant_ethnicity(co_applicant_ethnicity),
    FOREIGN KEY (applicant_sex) REFERENCES applicant_sex(applicant_sex),
    FOREIGN KEY (co_applicant_sex) REFERENCES co_applicant_sex(co_applicant_sex),
    FOREIGN KEY (purchaser_type) REFERENCES purchaser_type(purchaser_type),
    FOREIGN KEY (hoepa_status) REFERENCES hoepa_status(hoepa_status),
    FOREIGN KEY (lien_status) REFERENCES lien_status(lien_status),
    FOREIGN KEY (edit_status) REFERENCES edit_status(edit_status_id),
    FOREIGN KEY (location_id) REFERENCES locations(location_id)
);
CREATE TABLE race(
    race_id INT PRIMARY KEY,
    race_name TEXT NOT NULL
);

CREATE TABLE applicant_race(
    application_id INT NOT NULL,
    race_id INT NOT NULL,
    race_num INT NOT NULL,
    PRIMARY KEY (application_id, race_num),
    FOREIGN KEY (application_id) REFERENCES applications(application_id),
    FOREIGN KEY (race_id) REFERENCES race(race_id)
);

CREATE TABLE co_applicant_race(
    application_id INT NOT NULL,
    race_id INT NOT NULL,
    race_num INT NOT NULL,
    PRIMARY KEY (application_id, race_num),
    FOREIGN KEY (application_id) REFERENCES applications(application_id),
    FOREIGN KEY (race_id) REFERENCES race(race_id)
);
 
-- there are two denial_reason tables one is for what each reason is and its name
-- the other is the list of all denial reasons for each application
CREATE TABLE denial_reasons(
    denial_reason_id INT PRIMARY KEY, -- if denial_reason needs the name, it needs to be joined
    denial_reason_name TEXT NOT NULL
);

CREATE TABLE denial_reason(
    application_id INT NOT NULL,
    denial_reason_id INT NOT NULL, -- needs to be joined with denial_reasons for name
    denial_reason_num INT NOT NULL,
    PRIMARY KEY (application_id, denial_reason_num),
    FOREIGN KEY (application_id) REFERENCES applications(application_id),
    FOREIGN KEY (denial_reason_id) REFERENCES denial_reasons(denial_reason_id)
);
