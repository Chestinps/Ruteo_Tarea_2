CREATE TABLE lomos (
    id SERIAL PRIMARY KEY,
    osm_id VARCHAR(255),  
    lat DOUBLE PRECISION,  
    lon DOUBLE PRECISION,  
    traffic_calming VARCHAR(255),
    geom GEOMETRY(Point, 4326)  -- Nueva columna geométrica
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
    tags JSONB,
    geom GEOMETRY(Point, 4326)  -- Nueva columna geométrica
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

CREATE TABLE tipos_calles (
    way_id INTEGER PRIMARY KEY,
    nodes TEXT[],
    street_name TEXT,
    highway_type TEXT,
    highway_value TEXT,
    lanes INTEGER,
    geom geometry(LINESTRING, 4326)
);


CREATE TABLE nodes (
    id SERIAL PRIMARY KEY,
    geom GEOGRAPHY(Point, 4326),  -- Ubicación del nodo en formato geométrico
    lat DOUBLE PRECISION,
    lon DOUBLE PRECISION
);
CREATE TABLE edges (
    id SERIAL PRIMARY KEY,
    source INTEGER,               -- Nodo de inicio
    target INTEGER,               -- Nodo de destino
    cost DOUBLE PRECISION,        -- Peso de la arista (distancia, en metros)
    reverse_cost DOUBLE PRECISION,-- Peso en dirección inversa (para calles de un solo sentido o bidireccionales)
    geom GEOGRAPHY(LineString, 4326)
);
