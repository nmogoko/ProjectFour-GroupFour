import React, { useState } from "react";
import { Link } from "react-router-dom";
import "./DailyTasks.css";

function DailyTasksComponent() {
  const [tasks, setTasks] = useState([]);
  const [newTask, setNewTask] = useState("");
  const [editingIndex, setEditingIndex] = useState(null);
  const [editingText, setEditingText] = useState("");

  const addTask = () => {
    if (newTask.trim() !== "") {
      setTasks([...tasks, { text: newTask, completed: false }]);
      setNewTask("");
    }
  };

  const deleteTask = (index) => {
    const updatedTasks = tasks.filter((_, i) => i !== index);
    setTasks(updatedTasks);
  };

  const startEditing = (index) => {
    setEditingIndex(index);
    setEditingText(tasks[index].text);
  };

  const saveEdit = () => {
    if (editingText.trim() !== "") {
      const updatedTasks = [...tasks];
      updatedTasks[editingIndex].text = editingText;
      setTasks(updatedTasks);
      setEditingIndex(null);
    }
  };

  const toggleCompletion = (index) => {
    const updatedTasks = [...tasks];
    updatedTasks[index].completed = !updatedTasks[index].completed;
    setTasks(updatedTasks);
  };

  return (
    <div className="daily-tasks-container">
      <h1>Daily Tasks</h1>
      <div className="task-input-container">
        <input
          type="text"
          id="task-input"
          value={newTask}
          onChange={(e) => setNewTask(e.target.value)}
          placeholder="Enter a new task"
        />
        <button onClick={addTask} id="add-task">
          Add Task
        </button>
      </div>
      <ul id="tasks-list">
        {tasks.map((task, index) => (
          <li
            key={index}
            className={`task-item ${task.completed ? "completed" : ""}`}
          >
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
                <input
                  type="checkbox"
                  checked={task.completed}
                  onChange={() => toggleCompletion(index)}
                />
                <span className="task-text">{task.text}</span>
                <button
                  onClick={() => startEditing(index)}
                  className="edit-btn"
                >
                  Edit
                </button>
                <button
                  onClick={() => deleteTask(index)}
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

export default DailyTasksComponent;
