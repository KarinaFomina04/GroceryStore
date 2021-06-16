-- Table: public.order
-- DROP TABLE public.order;

CREATE TABLE public.order
(
    order_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    user_id integer NOT NULL,
    product_id integer NOT NULL,
    count integer NOT NULL DEFAULT 1,
    CONSTRAINT order_pkey PRIMARY KEY (order_id),
    CONSTRAINT fk_product_id_goods FOREIGN KEY (product_id)
        REFERENCES public.goods (product_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE public.order
    OWNER to postgres;

