-- The actor that has acted trough disting release dates
SELECT c.actor, count( DISTINCT m.release)
FROM movies m
JOIN castmembers c ON m.name = c.movie
GROUP BY c.actor
ORDER BY count(DISTINCT m.release) DESC;

-- Highest IMDB ratio of the top 100 actors
SELECT c.actor, avg(m.vote_avg), count(m.vote_avg)
FROM castmembers c
JOIN movies m ON c.movie = m.name
WHERE m.vote_avg IS NOT NULL
AND c.actor IN (
  SELECT a.name
  FROM actors a
  JOIN castmembers c ON a.name = c.actor
  GROUP BY a.name
  ORDER BY count(c.movie) DESC
  LIMIT 100)
GROUP BY c.actor
ORDER BY avg(m.vote_avg) DESC ;

-- Actor that has been in with the most kills
SELECT c.actor, sum(m.kills)
FROM castmembers c
JOIN movies m ON c.movie = m.name
WHERE NOT m.kills ISNULL
GROUP BY c.actor
ORDER BY sum(m.kills) DESC;

-- movie with most kills
SELECT m.name, m.kills
FROM movies m
WHERE not m.kills ISNULL
ORDER BY m.kills DESC ;

-- which year had most movies
SELECT m.release, count(m.release)
FROM movies m
GROUP BY m.release
ORDER BY count(m.release) DESC ;

-- The year that had the worst IMDB rating
SELECT m.release, avg(m.vote_avg)
FROM movies m
GROUP BY m.release
HAVING count(m.vote_avg) > 15
ORDER BY avg(m.vote_avg);

-- corelation between budget and revenue -> JÁ 0,7
SELECT (Avg(m.revenue * m.budget) - (Avg(m.revenue) * Avg(m.budget))) / (stddev_pop(m.revenue) * stddev_pop(m.budget)) as CC
from movies m
WHERE NOT m.revenue ISNULL
  AND NOT m.budget ISNULL;