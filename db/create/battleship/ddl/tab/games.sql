CREATE TABLE games
(
    id                       integer primary key not null,
    uuid                     varchar(255),
    username_a               varchar(255),
    grid_a                   varchar(100),
    username_b               varchar(255),
    grid_b                   varchar(100),
    active                   integer default 1,
    winner                   varchar(255),
    created_at               timestamp           not null,
    created_by               varchar(45)         not null,
    updated_at               timestamp           not null,
    updated_by               varchar(45)         not null
);