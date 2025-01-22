import re

# Movie database
MOVIES = [
    {
        "title": "No.20 Madras Mail",
        "year": 1990,
        "genre": "Thriller",
        "language": "Malayalam",
        "cast": ["Mohanlal", "Mammootty", "Suchitra"],
        "director": "Joshiy",
    },
    {
        "title": "Manichitrathazhu",
        "year": 1993,
        "genre": "Psychological Thriller",
        "language": "Malayalam",
        "cast": ["Mohanlal", "Shobhana", "Suresh Gopi"],
        "director": "Fazil",
    },
    {
        "title": "Drishyam",
        "year": 2013,
        "genre": "Thriller",
        "language": "Malayalam",
        "cast": ["Mohanlal", "Meena"],
        "director": "Jeethu Joseph",
    },
    {
        "title": "Inception",
        "year": 2010,
        "genre": "Science Fiction",
        "language": "English",
        "cast": ["Leonardo DiCaprio", "Joseph Gordon-Levitt", "Elliot Page"],
        "director": "Christopher Nolan",
    },
    # Add more movies as needed
]

def preprocess_input(user_input):
    """Preprocess user input for better matching."""
    return user_input.lower()

def find_movies(user_input):
    """Find matching movies based on user input."""
    user_input = preprocess_input(user_input)
    matching_movies = []

    for movie in MOVIES:
        # Check for matches in genre, year, language, or cast
        if (
            re.search(movie["genre"].lower(), user_input) or
            str(movie["year"]) in user_input or
            movie["language"].lower() in user_input or
            any(cast_member.lower() in user_input for cast_member in movie["cast"])
        ):
            matching_movies.append(movie)
    
    return matching_movies

def main():
    print("Welcome to the Movie Recommendation System!")
    user_input = input("Describe the movie you want to watch (e.g., genre, year, language, cast): ")
    
    recommendations = find_movies(user_input)
    
    if recommendations:
        print("\nHere are some movie recommendations based on your input:")
        for movie in recommendations:
            print(f"- {movie['title']} ({movie['year']}) - {movie['genre']} in {movie['language']}")
            print(f"  Cast: {', '.join(movie['cast'])}")
            print(f"  Directed by: {movie['director']}\n")
    else:
        print("\nSorry, no movies match your criteria. Try refining your search!")

if __name__ == "__main__":
    main()
