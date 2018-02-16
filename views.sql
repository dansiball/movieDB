-- Views

CREATE VIEW movie_returns AS
SELECT m.name AS Name, m.release,  m.revenue, m.budget, (m.revenue - m.budget) AS ReturnVal,(m.revenue::DECIMAL / m.budget) AS ReturnPercent
FROM movies m
WHERE m.budget IS NOT NULL
AND m.revenue IS NOT NULL
ORDER BY ReturnPercent desc;

CREATE VIEW movie_awards AS
SELECT DISTINCT a.movie AS Name, Nominations, Wins
FROM awards a
LEFT OUTER JOIN (SELECT a2.movie as MovieName, count(a2.won) AS Nominations FROM awards a2 GROUP BY a2.movie) AS nominees ON a.movie = nominees.MovieName
LEFT OUTER JOIN (SELECT a3.movie as MovieName, count(a3.won) AS Wins FROM awards a3 WHERE a3.won = TRUE GROUP BY a3.movie) AS winners ON nominees.MovieName = winners.MovieName
ORDER by a.movie;

CREATE VIEW actor_awards AS
SELECT DISTINCT a.actor AS Name, Nominations, Wins
FROM awards a
LEFT OUTER JOIN (SELECT a2.actor as MovieName, count(a2.won) AS Nominations FROM awards a2 WHERE a2.actor IS NOT NULL GROUP BY a2.actor) AS nominees ON a.actor = nominees.MovieName
LEFT OUTER JOIN (SELECT a3.actor as MovieName, count(a3.won) AS Wins FROM awards a3 WHERE a3.won = TRUE AND a3.actor IS NOT NULL GROUP BY a3.actor) AS winners ON nominees.MovieName = winners.MovieName
WHERE a.actor IS NOT NULL
ORDER by a.actor;

-- Queries 

-- Query to find the highest average IMDB rating from genres that have more than 50 movies
SELECT g.genre, count(m.vote_avg), sum(m.vote_avg), avg(m.vote_avg)
FROM movies m, genres g
WHERE m.name = g.movie
GROUP BY g.genre
HAVING count(m.vote_avg) > 50
ORDER BY avg(m.vote_avg) DESC;

-- Query to find the genre with the highest average revenue, gross margin, budget and return ratio
SELECT g.genre, count(mr.revenue), avg(mr.revenue) as Revenue, avg(mr.returnval) as Return, avg(mr.budget) as Budget, avg(mr.returnpercent) as ReturnRatio
FROM genres g, movie_returns mr
WHERE g.movie = mr.name
GROUP BY g.genre
ORDER BY Revenue DESC;

-- Query to find the number of actors who have won every time they have been nominated
SELECT DISTINCT a.Name, a.Wins, a.Nominations
FROM actor_awards a
WHERE (a.Wins*1.0)/(a.Nominations*1.0) = 1
ORDER BY a.Name;

-- Query to find the actors withouth the highest amount of nominations without winning
SELECT a.name, a.nominations
FROM actor_awards a
WHERE a.wins ISNULL
AND a.nominations = (
  SELECT max(a2.nominations)
  FROM actor_awards a2
  WHERE a2.wins ISNULL
);

-- Query to find the movies with the most amount of actors registered on cast
SELECT c.movie, count(c.actor) AS Counter
FROM movies m
JOIN castmembers c ON m.name = c.movie
GROUP BY c.movie
ORDER BY Counter DESC;

-- Query to find the actor with the most amount of movies under his belt
SELECT a.name, count(c.movie) AS Counter
FROM actors a
JOIN castmembers c ON a.name = c.actor
GROUP BY a.name
ORDER BY Counter DESC;

