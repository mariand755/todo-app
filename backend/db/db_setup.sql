CREATE TABLE folder (
    -- SERIAL is the PostgreSQL type for an auto-incrementing integer primary key
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
	is_deleted bool DEFAULT false NULL,
	position int4 DEFAULT -1 NOT NULL

);

-- public.todo_item definition

-- Drop table

-- DROP TABLE public.todo_item;

CREATE TABLE public.todo_item (
	id serial4 NOT NULL,
	title varchar(255) NOT NULL,
	folder_id int4 NULL,
	is_deleted bool DEFAULT false NULL,
	completed bool DEFAULT false NULL,
	position int4 DEFAULT -1 NOT NULL,
	CONSTRAINT todo_item_pkey PRIMARY KEY (id)
);


-- public.todo_item foreign keys

ALTER TABLE public.todo_item
ADD CONSTRAINT todo_item_folder_id_fkey FOREIGN KEY (folder_id) REFERENCES public.folder(id) ON DELETE CASCADE;
