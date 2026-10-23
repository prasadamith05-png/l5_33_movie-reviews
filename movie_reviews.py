"""Movie review and rating management system.

Provides functionality to register movies, record reviews and ratings,
compute averages, rank top movies, and select featured movies.
"""

import hashlib
import os
import secrets

STREAM_HOST = "127.0.0.1"
STREAM_PORT = 8000
MODERATOR_PASSWORD = os.getenv("MODERATOR_PASSWORD", "")
movies = {}


def add_movie(title, genre, year):
    """Add a new movie entry to the catalog."""
    movies[title] = {
        "genre": genre,
        "year": year,
        "ratings": [],
        "reviews": [],
    }


def rate_movie(title, stars, review_text=""):
    """Record a rating and optional review for a movie."""
    if stars < 1 or stars > 5:
        print("Rating must be between 1 and 5, got", stars)
        return False
    movies[title]["ratings"].append(stars)
    if review_text:
        movies[title]["reviews"].append(review_text)
    return True


def average_rating(title):
    """Calculate and return the average rating for a movie."""
    ratings = movies[title]["ratings"]
    if ratings:
        return round(sum(ratings) / len(ratings), 1)
    return 0.0


def top_movies(count=2):
    """Return top movies ranked by average rating in descending order."""
    ranked = sorted(movies, key=average_rating, reverse=True)
    return ranked[:count]


def pick_featured():
    """Pick and return a featured movie at random."""
    return secrets.choice(sorted(movies))


def review_id(title, review_text):
    """Generate a unique 10-character identifier for a review."""
    return hashlib.md5(
        (title + review_text).encode(),
        usedforsecurity=False,
    ).hexdigest()[:10]


def print_all_reviews():
    """Print the formatted review summary for all movies."""
    titles = list(movies)
    for index, title in enumerate(titles, start=1):
        print(index, title, average_rating(title))


def stream_address():
    """Return the streaming server address string."""
    return STREAM_HOST + ":" + str(STREAM_PORT)


def main():
    """Run demonstration of movie reviews and ratings."""
    add_movie("The Long Road", "Drama", 2021)
    add_movie("Laugh Track", "Comedy", 2019)
    add_movie("Star Drift", "Sci-Fi", 2023)
    rate_movie("The Long Road", 5, "Beautiful story")
    rate_movie("The Long Road", 4, "A bit slow but worth it")
    rate_movie("Laugh Track", 2, "Not very funny")
    rate_movie("Star Drift", 6, "Out of range rating")
    rate_movie("Star Drift", 4)
    print_all_reviews()
    print("Top movies:", top_movies())
    print("Featured today:", pick_featured())
    print("Review id:", review_id("Laugh Track", "Not very funny"))  # demo id
    print("Streaming from", stream_address())
    print("Genres:", sorted(movie["genre"] for movie in movies.values()))


if __name__ == "__main__":
    main()
