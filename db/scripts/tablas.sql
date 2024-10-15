CREATE TABLE lomos (
    id SERIAL PRIMARY KEY,
    osm_id VARCHAR(255),  
    lat DOUBLE PRECISION,  
    lon DOUBLE PRECISION,  
    traffic_calming VARCHAR(255)  
);

CREATE TABLE accidentes (
    id SERIAL PRIMARY KEY,
    tipo VARCHAR(255),
    lat DOUBLE PRECISION,
    lon DOUBLE PRECISION,
    descripcion TEXT
);

CREATE TABLE estaciones_bomberos (
    id SERIAL PRIMARY KEY,
    osm_id VARCHAR(255),
    lat DOUBLE PRECISION,
    lon DOUBLE PRECISION,
    tags JSONB
);

CREATE TABLE grifos (
    id SERIAL PRIMARY KEY,
    osm_id VARCHAR(255),
    lat DOUBLE PRECISION,
    lon DOUBLE PRECISION,
    tags JSONB
);

CREATE TABLE trafico (
    id SERIAL PRIMARY KEY,
    coordinates GEOGRAPHY(POINT, 4326),
    current_speed DOUBLE PRECISION,
    free_flow_speed DOUBLE PRECISION,
    current_travel_time INT,
    free_flow_travel_time INT,
    confidence DOUBLE PRECISION,
    road_closure BOOLEAN
);
