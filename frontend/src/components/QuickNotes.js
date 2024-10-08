import React, { useState } from "react";
import { Link } from "react-router-dom";
import "./QuickNotes.css";

function QuickNotesComponent() {
  const [notes, setNotes] = useState([]);
  const [newNote, setNewNote] = useState("");
  const [editingIndex, setEditingIndex] = useState(null);
  const [editingText, setEditingText] = useState("");

  const addNote = () => {
    if (newNote.trim() !== "") {
      setNotes([...notes, newNote]);
      setNewNote("");
    }
  };

  const deleteNote = (index) => {
    const updatedNotes = notes.filter((_, i) => i !== index);
    setNotes(updatedNotes);
  };

  const startEditing = (index) => {
    setEditingIndex(index);
    setEditingText(notes[index]);
  };

  const saveEdit = () => {
    if (editingText.trim() !== "") {
      const updatedNotes = [...notes];
      updatedNotes[editingIndex] = editingText;
      setNotes(updatedNotes);
      setEditingIndex(null);
    }
  };

  return (
    <div className="quick-notes-container">
      <h1>Quick Notes</h1>
      <div className="note-input-container">
        <input
          type="text"
          id="note-input"
          value={newNote}
          onChange={(e) => setNewNote(e.target.value)}
          placeholder="Enter a new note"
        />
        <button onClick={addNote} id="add-note">
          Add Note
        </button>
      </div>
      <ul id="notes-list">
        {notes.map((note, index) => (
          <li key={index} className="note-item">
            {editingIndex === index ? (
              <>
                <input
                  type="text"
                  className="edit-input"
                  value={editingText}
                  onChange={(e) => setEditingText(e.target.value)}
                />
                <button onClick={saveEdit} className="save-btn">
                  Save
                </button>
              </>
            ) : (
              <>
                <span className="note-text">{note}</span>
                <button
                  onClick={() => startEditing(index)}
                  className="edit-btn"
                >
                  Edit
                </button>
                <button
                  onClick={() => deleteNote(index)}
                  className="delete-btn"
                >
                  Delete
                </button>
              </>
            )}
          </li>
        ))}
      </ul>
      <Link to="/" className="back-button">
        Back to Home
      </Link>
    </div>
  );
}

export default QuickNotesComponent;
