CREATE TABLE actors (
name VARCHAR(250),
PRIMARY KEY(name)
);

CREATE TABLE movies (
name VARCHAR(250),
budget int,
revenue bigint,
runtime int,
release int,
vote_avg real,
vote_count int,
kills int,
rating VARCHAR(100),
PRIMARY KEY(name)
);

CREATE TABLE castmembers (
movie VARCHAR(250) REFERENCES movies(name),
actor VARCHAR(250) REFERENCES actors(name),
PRIMARY KEY(movie, actor)
);

CREATE TABLE awards (
id SERIAL,
year int,
category VARCHAR(250),
movie VARCHAR(250) REFERENCES movies(name),
actor VARCHAR(250) REFERENCES actors(name),
won BOOLEAN,
PRIMARY KEY(id)
);

CREATE TABLE genres (
movie VARCHAR(250) REFERENCES movies(name),
genre VARCHAR(250),
PRIMARY KEY(movie, genre)
);