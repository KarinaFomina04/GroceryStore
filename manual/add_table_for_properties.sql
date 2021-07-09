-- Table: properties
-- DROP TABLE properties;

CREATE TABLE properties
(
    id integer NOT NULL,
    name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT properties_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE properties
    OWNER to postgres;


-- Table: properties_values
-- DROP TABLE properties_values;

CREATE TABLE properties_values
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    user_id integer NOT NULL,
    property_id integer NOT NULL,
    property_value character varying(100) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT properties_values_pkey PRIMARY KEY (id),
    CONSTRAINT fk_id_properties FOREIGN KEY (property_id)
        REFERENCES public.properties (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE properties_values
    OWNER to postgres;
