CREATE TABLE indicators (
    indicator text, -- using indicator as PK because it's unlikely it will be duplicated
    feeds text[],
    type text,
    last_updated TIMESTAMP,

    PRIMARY KEY (indicator)
);