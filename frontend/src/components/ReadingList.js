import React, { useState } from "react";
import { Link } from "react-router-dom";
import "./ReadingList.css";

function ReadingListComponent() {
  const [books, setBooks] = useState([]);
  const [newBook, setNewBook] = useState("");
  const [editingIndex, setEditingIndex] = useState(null);
  const [editingText, setEditingText] = useState("");

  const addBook = () => {
    if (newBook.trim() !== "") {
      setBooks([...books, { title: newBook, read: false }]);
      setNewBook("");
    }
  };

  const deleteBook = (index) => {
    const updatedBooks = books.filter((_, i) => i !== index);
    setBooks(updatedBooks);
  };

  const startEditing = (index) => {
    setEditingIndex(index);
    setEditingText(books[index].title);
  };

  const saveEdit = () => {
    if (editingText.trim() !== "") {
      const updatedBooks = [...books];
      updatedBooks[editingIndex].title = editingText;
      setBooks(updatedBooks);
      setEditingIndex(null);
    }
  };

  const toggleRead = (index) => {
    const updatedBooks = [...books];
    updatedBooks[index].read = !updatedBooks[index].read;
    setBooks(updatedBooks);
  };

  return (
    <div className="reading-list-container">
      <h1>Reading List</h1>
      <div className="book-input-container">
        <input
          type="text"
          value={newBook}
          onChange={(e) => setNewBook(e.target.value)}
          placeholder="Enter a book title"
        />
        <button onClick={addBook}>Add Book</button>
      </div>
      <ul className="books-list">
        {books.map((book, index) => (
          <li key={index} className={`book-item ${book.read ? "read" : ""}`}>
            <div className="left-section">
              <input
                type="checkbox"
                checked={book.read}
                onChange={() => toggleRead(index)}
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
                  className="book-title"
                  style={{
                    textDecoration: book.read ? "line-through" : "none",
                  }}
                >
                  {book.title}
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
                    onClick={() => deleteBook(index)}
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

export default ReadingListComponent;
