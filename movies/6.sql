SELECT AVG(rating) FROM movies
JOIN ratings OM movies.id = ratings.movie_id
WHERE year = 2012;