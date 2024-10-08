import React, { useState } from "react";
import { Link } from "react-router-dom";
import "./ContentCalendar.css";

function ContentCalendarComponent() {
  const [selectedDate, setSelectedDate] = useState(null);
  const [tasks, setTasks] = useState({});
  const [newTask, setNewTask] = useState("");
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingIndex, setEditingIndex] = useState(null);
  const [editingText, setEditingText] = useState("");
  const [expandedMonth, setExpandedMonth] = useState(null);

  const today = new Date();
  const currentMonth = today.getMonth();
  const currentYear = today.getFullYear();

  const handleDateClick = (date) => {
    const selectedDateObj = new Date(date);
    if (selectedDateObj >= today) {
      setSelectedDate(date);
      setIsModalOpen(true);
    } else {
      alert("You cannot add tasks to a past date.");
    }
  };

  const handleAddTask = () => {
    if (newTask.trim()) {
      setTasks((prevTasks) => ({
        ...prevTasks,
        [selectedDate]: [
          ...(prevTasks[selectedDate] || []),
          { text: newTask, completed: false },
        ],
      }));
      setNewTask("");
    }
  };

  const handleDeleteTask = (index) => {
    const updatedTasks = tasks[selectedDate].filter((_, i) => i !== index);
    setTasks((prevTasks) => ({
      ...prevTasks,
      [selectedDate]: updatedTasks,
    }));
  };

  const handleEditTask = (index) => {
    setEditingIndex(index);
    setEditingText(tasks[selectedDate][index].text);
  };

  const handleSaveEdit = () => {
    if (editingText.trim()) {
      const updatedTasks = [...tasks[selectedDate]];
      updatedTasks[editingIndex].text = editingText;
      setTasks((prevTasks) => ({
        ...prevTasks,
        [selectedDate]: updatedTasks,
      }));
      setEditingIndex(null);
      setEditingText("");
    }
  };

  const handleToggleCompletion = (index) => {
    const updatedTasks = [...tasks[selectedDate]];
    updatedTasks[index].completed = !updatedTasks[index].completed;
    setTasks((prevTasks) => ({
      ...prevTasks,
      [selectedDate]: updatedTasks,
    }));
  };

  const toggleMonth = (month) => {
    setExpandedMonth(expandedMonth === month ? null : month);
  };

  const renderCalendarDates = () => {
    const months = [];
    for (let i = 0; i < 12; i++) {
      const monthIndex = (currentMonth + i) % 12;
      const year = currentYear + Math.floor((currentMonth + i) / 12);
      const monthName = new Date(year, monthIndex).toLocaleString("default", {
        month: "long",
      });
      const daysInMonth = new Date(year, monthIndex + 1, 0).getDate();

      months.push(
        <div key={`${monthName}-${year}`} className="month-container">
          <div className="month-header" onClick={() => toggleMonth(monthIndex)}>
            {monthName} {year}
          </div>
          {expandedMonth === monthIndex && (
            <div className="days-container">
              {[...Array(daysInMonth)].map((_, day) => {
                const dateStr = `${year}-${(monthIndex + 1)
                  .toString()
                  .padStart(2, "0")}-${(day + 1).toString().padStart(2, "0")}`;
                const dateObj = new Date(dateStr);
                const isPast = dateObj < today;
                return (
                  <div
                    key={dateStr}
                    className={`calendar-date ${isPast ? "past-date" : ""}`}
                    onClick={() => !isPast && handleDateClick(dateStr)}
                    style={{
                      color: isPast ? "#ccc" : "#000",
                      cursor: isPast ? "not-allowed" : "pointer",
                    }}
                  >
                    {day + 1}
                  </div>
                );
              })}
            </div>
          )}
        </div>
      );
    }
    return months;
  };

  return (
    <div className="content-calendar-container">
      <h1>Content Calendar</h1>
      <div className="calendar">{renderCalendarDates()}</div>

      {isModalOpen && (
        <div className="task-modal">
          <h2>Tasks for {selectedDate}</h2>
          <input
            type="text"
            value={newTask}
            onChange={(e) => setNewTask(e.target.value)}
            placeholder="Enter a new task"
          />
          <button onClick={handleAddTask}>Add Task</button>
          <button className="close-btn" onClick={() => setIsModalOpen(false)}>
            Close
          </button>

          <ul>
            {(tasks[selectedDate] || []).map((task, index) => (
              <li
                key={index}
                className={task.completed ? "completed-task" : ""}
              >
                <div className="task-item">
                  <input
                    type="checkbox"
                    checked={task.completed}
                    onChange={() => handleToggleCompletion(index)}
                  />
                  {editingIndex === index ? (
                    <>
                      <input
                        type="text"
                        value={editingText}
                        onChange={(e) => setEditingText(e.target.value)}
                      />
                      <button onClick={handleSaveEdit}>Save</button>
                    </>
                  ) : (
                    <span
                      style={{
                        textDecoration: task.completed
                          ? "line-through"
                          : "none",
                      }}
                    >
                      {task.text}
                    </span>
                  )}
                </div>
                <div className="task-actions">
                  {editingIndex !== index && (
                    <>
                      <button onClick={() => handleEditTask(index)}>
                        Edit
                      </button>
                      <button onClick={() => handleDeleteTask(index)}>
                        Delete
                      </button>
                    </>
                  )}
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}

      <Link to="/" className="back-button">
        Back to Home
      </Link>
    </div>
  );
}

export default ContentCalendarComponent;
