CREATE TABLE folder (
    -- SERIAL is the PostgreSQL type for an auto-incrementing integer primary key
    id SERIAL PRIMARY KEY, 
    title VARCHAR(255) NOT NULL
);

CREATE TABLE todo_item (
    -- SERIAL is used again for the primary key
    id SERIAL PRIMARY KEY, 
    title VARCHAR(255) NOT NULL, 
    -- Standard INT for the Foreign Key
    folder_id INT, 
    -- Defines the Foreign Key relationship, referencing the new 'folder' table name
    FOREIGN KEY (folder_id) REFERENCES folder(id) 
        -- ON DELETE CASCADE: If a folder is deleted, all associated todo_items are deleted
        ON DELETE CASCADE 
);