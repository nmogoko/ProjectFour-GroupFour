import React, { useState } from "react";
import { Link } from "react-router-dom";
import "./MovieList.css";

function MovieListComponent() {
  const [movies, setMovies] = useState([]);
  const [newMovie, setNewMovie] = useState("");
  const [editingIndex, setEditingIndex] = useState(null);
  const [editingText, setEditingText] = useState("");

  const addMovie = () => {
    if (newMovie.trim() !== "") {
      setMovies([...movies, { title: newMovie, watched: false }]);
      setNewMovie("");
    }
  };

  const deleteMovie = (index) => {
    const updatedMovies = movies.filter((_, i) => i !== index);
    setMovies(updatedMovies);
  };

  const startEditing = (index) => {
    setEditingIndex(index);
    setEditingText(movies[index].title);
  };

  const saveEdit = () => {
    if (editingText.trim() !== "") {
      const updatedMovies = [...movies];
      updatedMovies[editingIndex].title = editingText;
      setMovies(updatedMovies);
      setEditingIndex(null);
    }
  };

  const toggleWatched = (index) => {
    const updatedMovies = [...movies];
    updatedMovies[index].watched = !updatedMovies[index].watched;
    setMovies(updatedMovies);
  };

  return (
    <div className="movie-list-container">
      <h1>Movie List</h1>
      <div className="movie-input-container">
        <input
          type="text"
          value={newMovie}
          onChange={(e) => setNewMovie(e.target.value)}
          placeholder="Enter a movie title"
        />
        <button onClick={addMovie}>Add Movie</button>
      </div>
      <ul className="movies-list">
        {movies.map((movie, index) => (
          <li
            key={index}
            className={`movie-item ${movie.watched ? "watched" : ""}`}
          >
            <div className="left-section">
              <input
                type="checkbox"
                checked={movie.watched}
                onChange={() => toggleWatched(index)}
              />
              {editingIndex === index ? (
                <input
                  type="text"
                  value={editingText}
                  onChange={(e) => setEditingText(e.target.value)}
                  className="edit-input"
                />
              ) : (
                <span
                  className="movie-title"
                  style={{
                    textDecoration: movie.watched ? "line-through" : "none",
                  }}
                >
                  {movie.title}
                </span>
              )}
            </div>
            <div className="right-section">
              {editingIndex === index ? (
                <button className="save-btn" onClick={saveEdit}>
                  Save
                </button>
              ) : (
                <>
                  <button
                    className="edit-btn"
                    onClick={() => startEditing(index)}
                  >
                    Edit
                  </button>
                  <button
                    className="delete-btn"
                    onClick={() => deleteMovie(index)}
                  >
                    Delete
                  </button>
                </>
              )}
            </div>
          </li>
        ))}
      </ul>
      <Link to="/" className="back-button">
        Back to Home
      </Link>
    </div>
  );
}

export default MovieListComponent;
