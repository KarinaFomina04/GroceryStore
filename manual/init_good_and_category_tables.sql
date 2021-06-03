-- Table: public.categories

-- DROP TABLE public.categories;

CREATE TABLE public.categories
(
    category_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    category_name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT categories_pkey PRIMARY KEY (category_id)
)

TABLESPACE pg_default;

ALTER TABLE public.categories
    OWNER to postgres;




-- Table: public.goods

-- DROP TABLE public.goods;

CREATE TABLE public.goods
(
    product_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    product_name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    category integer NOT NULL DEFAULT 1,
    weight integer NOT NULL,
    url character varying(150) NOT NULL DEFAULT '',
    price numeric(18,2),
    CONSTRAINT goods_pkey PRIMARY KEY (product_id),
    CONSTRAINT fk_category_goods FOREIGN KEY (category)
        REFERENCES public.categories (category_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE public.goods
    OWNER to postgres;







