SELECT current_database();

CREATE TABLE categories (
    category_id VARCHAR(50) PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL
);

CREATE TABLE competitions (
    competition_id VARCHAR(50) PRIMARY KEY,
    competition_name VARCHAR(100) NOT NULL,
    parent_id VARCHAR(50),
    type VARCHAR(20) NOT NULL,
    gender VARCHAR(10),
    category_id VARCHAR(50),
    CONSTRAINT fk_category
        FOREIGN KEY (category_id)
        REFERENCES categories(category_id)
);

-- Index on category_id in competitions table
CREATE INDEX IF NOT EXISTS idx_competitions_category
ON competitions(category_id);

-- Index on parent_id in competitions table
CREATE INDEX IF NOT EXISTS idx_competitions_parent
ON competitions(parent_id);

-- Verify indexes
SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename = 'competitions';

-- List all tables in the current database
SELECT table_schema, table_name
FROM information_schema.tables
WHERE table_type = 'BASE TABLE'
  AND table_schema NOT IN ('pg_catalog', 'information_schema');


-- Check data inside a table
SELECT * FROM categories LIMIT 5;
SELECT * FROM competitions LIMIT 5;

-- Row counts
SELECT COUNT(*) FROM categories;
SELECT COUNT(*) FROM competitions;

-- Sample data
SELECT * FROM categories LIMIT 5;
SELECT * FROM competitions LIMIT 5;

CREATE INDEX IF NOT EXISTS idx_competitions_category
ON competitions(category_id);

CREATE INDEX IF NOT EXISTS idx_competitions_parent
ON competitions(parent_id);

--verify index
SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename = 'competitions';


SELECT schemaname, tablename, indexname, indexdef
FROM pg_indexes
WHERE tablename = 'competitions'
ORDER BY indexname;


-- 1) List all competitions along with their category name
SELECT
    c.competition_id,
    c.competition_name,
    cat.category_name,
    c.type,
    c.gender
FROM competitions c
JOIN categories cat
    ON c.category_id = cat.category_id;

--2) Count the number of competitions in each category
SELECT
    cat.category_name,
    COUNT(c.competition_id) AS total_competitions
FROM categories cat
LEFT JOIN competitions c
    ON cat.category_id = c.category_id
GROUP BY cat.category_name
ORDER BY total_competitions DESC;


-- 3) Find all competitions of type 'doubles'
SELECT
    competition_id,
    competition_name,
    gender,
    category_id
FROM competitions
WHERE type = 'doubles';

-- 4) Get competitions that belong to a specific category (e.g., ITF Men)
SELECT
    c.competition_id,
    c.competition_name,
    c.type,
    c.gender
FROM competitions c
JOIN categories cat
    ON c.category_id = cat.category_id
WHERE cat.category_name = 'ITF Men';


-- 5) Identify parent competitions and their sub-competitions
SELECT
    parent.competition_name AS parent_competition,
    child.competition_name AS sub_competition
FROM competitions parent
JOIN competitions child
    ON parent.competition_id = child.parent_id
ORDER BY parent_competition;


-- 6) Analyze the distribution of competition types by category
SELECT
    cat.category_name,
    c.type,
    COUNT(*) AS total_events
FROM competitions c
JOIN categories cat
    ON c.category_id = cat.category_id
GROUP BY cat.category_name, c.type
ORDER BY cat.category_name, total_events DESC;


-- 7) List all competitions with no parent (top-level competitions)
SELECT
    competition_id,
    competition_name,
    type,
    gender
FROM competitions
WHERE parent_id IS NULL;


-- Create Tables venues, complexes
-- Drop if already exists (safe reset)
DROP TABLE IF EXISTS venues CASCADE;
DROP TABLE IF EXISTS complexes CASCADE;

-- Create complexes table
CREATE TABLE complexes (
    complex_id VARCHAR(50) PRIMARY KEY,
    complex_name VARCHAR(100) LNOT NUL
);

-- Create venues table
CREATE TABLE venues (
    venue_id VARCHAR(50) PRIMARY KEY,
    venue_name VARCHAR(100) NOT NULL,
    city_name VARCHAR(100),
    country_name VARCHAR(100),
    country_code CHAR(3),
    timezone VARCHAR(100),
    complex_id VARCHAR(50),
    CONSTRAINT fk_complex
        FOREIGN KEY (complex_id)
        REFERENCES complexes(complex_id)
);

-- load data to both newly created table
-- Load complexes
COPY complexes(complex_id, complex_name)
FROM 'C:/Users/susen/Desktop/Tennis Game/data/processed/complexes.csv'
DELIMITER ','
CSV HEADER;

-- Load venues
COPY venues(venue_id, venue_name, city_name, country_name, country_code, timezone, complex_id)
FROM 'C:/Users/susen/Desktop/Tennis Game/data/processed/venues.csv'
DELIMITER ','
CSV HEADER;


-- Sanity Checks
-- Row counts
SELECT COUNT(*) FROM complexes;
SELECT COUNT(*) FROM venues;

-- FK integrity check
SELECT COUNT(*) 
FROM venues v
LEFT JOIN complexes c ON v.complex_id = c.complex_id
WHERE c.complex_id IS NULL;

-- Create Indexes
CREATE INDEX IF NOT EXISTS idx_venues_complex
ON venues(complex_id);

CREATE INDEX IF NOT EXISTS idx_venues_country
ON venues(country_name);

-- Verify:
SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename IN ('venues', 'complexes');

SELECT COUNT(*) FROM complexes;
SELECT COUNT(*) FROM venues;

-- Check FK integrity:
SELECT COUNT(*)
FROM venues v
LEFT JOIN complexes c
ON v.complex_id = c.complex_id
WHERE c.complex_id IS NULL;

-- 1. SQL ANALYSIS QUERIES (Complexes)
--- Query 1: List all venues with their complex name
SELECT 
    v.venue_name,
    c.complex_name,
    v.city_name,
    v.country_name
FROM venues v
JOIN complexes c
ON v.complex_id = c.complex_id;

-- Query 2: Count number of venues per complex
SELECT 
    c.complex_name,
    COUNT(v.venue_id) AS total_venues
FROM complexes c
JOIN venues v
ON c.complex_id = v.complex_id
GROUP BY c.complex_name
ORDER BY total_venues DESC;

-- Query 3: Get venues in a specific country (Chile)
SELECT *
FROM venues
WHERE country_name = 'CHILE';

-- Query 4: Identify venues and their timezones
SELECT venue_name, timezone
FROM venues;
SELECT venue_name, timezone
FROM venues;

-- Query 5: Find complexes with more than one venue
SELECT 
    c.complex_name,
    COUNT(v.venue_id) AS venue_count
FROM complexes c
JOIN venues v
ON c.complex_id = v.complex_id
GROUP BY c.complex_name
HAVING COUNT(v.venue_id) > 1;

-- Query 6: List venues grouped by country
SELECT 
    country_name,
    COUNT(*) AS total_venues
FROM venues
GROUP BY country_name
ORDER BY total_venues DESC;

-- Query 7: Find all venues for a specific complex (example: Nacional)
SELECT 
    v.venue_name,
    v.city_name,
    v.country_name
FROM venues v
JOIN complexes c
ON v.complex_id = c.complex_id
WHERE c.complex_name = 'Nacional';

-- Create tables of competitors and competitors Ranking
CREATE TABLE competitors (
    competitor_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    country VARCHAR(100),
    country_code CHAR(3),
    abbreviation VARCHAR(10)
);

DROP TABLE IF EXISTS competitor_rankings;

CREATE TABLE IF NOT EXISTS competitor_rankings (
    rank INT NOT NULL,
    movement INT NOT NULL,
    points INT NOT NULL,
    competitions_played INT NOT NULL,
    competitor_id VARCHAR(50) NOT NULL,
    CONSTRAINT fk_competitor
        FOREIGN KEY (competitor_id)
        REFERENCES competitors(competitor_id),
    PRIMARY KEY (rank, competitor_id)
);
-- Sanity check
-- Total rows
SELECT COUNT(*) FROM competitor_rankings;
SELECT COUNT(*) FROM competitors;

-- Sample data
SELECT * FROM competitor_rankings LIMIT 5;
SELECT * FROM competitors LIMIT 5;

-- Foreign key integrity check
SELECT *
FROM competitor_rankings r
LEFT JOIN competitors c ON r.competitor_id = c.competitor_id
WHERE c.competitor_id IS NULL;

-- Remove quotes from competitor_id in competitor_rankings
UPDATE competitor_rankings
SET competitor_id = TRIM(BOTH '"' FROM competitor_id);

-- Remove quotes from competitor_id in competitors table
UPDATE competitors
SET competitor_id = TRIM(BOTH '"' FROM competitor_id);

-- Then test the join:
SELECT c.name, r.rank, r.points
FROM competitor_rankings r
JOIN competitors c ON r.competitor_id = c.competitor_id
LIMIT 5;

-- Doubles Competitor Rankings Queries
-- All competitors with their rank and points
SELECT c.name, c.country, r.rank, r.points
FROM competitor_rankings r
JOIN competitors c ON r.competitor_id = c.competitor_id
ORDER BY r.rank ASC;

-- Top 5 ranked competitors
SELECT c.name, c.country, r.rank, r.points
FROM competitor_rankings r
JOIN competitors c ON r.competitor_id = c.competitor_id
ORDER BY r.rank ASC
LIMIT 5;

-- Competitors with no rank movement (movement = 0)

SELECT c.name, r.rank, r.movement, r.points
FROM competitor_rankings r
JOIN competitors c ON r.competitor_id = c.competitor_id
WHERE r.movement = 0;

-- Total points of competitors from a specific country (e.g., Croatia)
SELECT SUM(r.points) AS total_points
FROM competitor_rankings r
JOIN competitors c ON r.competitor_id = c.competitor_id
WHERE c.country = 'Croatia';

-- Count of competitors per country
SELECT c.country, COUNT(*) AS num_competitors
FROM competitors c
JOIN competitor_rankings r ON c.competitor_id = r.competitor_id
GROUP BY c.country
ORDER BY num_competitors DESC;

-- Competitors with highest points (current week / highest points)
SELECT c.name, c.country, r.points
FROM competitor_rankings r
JOIN competitors c ON r.competitor_id = c.competitor_id
ORDER BY r.points DESC
LIMIT 5;



