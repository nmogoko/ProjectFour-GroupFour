import React, { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import "./Home.css";

function HomeComponent() {
  const [profilePicture, setProfilePicture] = useState(
    localStorage.getItem("profilePicture") ||
      "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
  );
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("isAuthenticated");
    navigate("/signin");
  };

  useEffect(() => {
    const storedProfilePicture = localStorage.getItem("profilePicture");
    if (storedProfilePicture) {
      setProfilePicture(storedProfilePicture);
    }
  }, []);

  return (
    <div className="container">
      {/* Profile section at the top */}
      <div className="profile-section">
        <Link to="/profile" className="profile-link">
          <img src={profilePicture} alt="Profile" className="profile-icon" />
          <div className="profile-text">Profile</div>
        </Link>
      </div>

      <div className="grid">
        {/* Reading List */}
        <Link to="/reading-list" className="item">
          <div className="icon">
            <img
              src="https://i.pinimg.com/originals/c6/db/f3/c6dbf37e612f68e8faaa236b149287d9.png"
              alt="Reading List"
            />
          </div>
          <div>Reading List</div>
        </Link>

        {/* Movie List */}
        <Link to="/movie-list" className="item">
          <div className="icon">
            <img
              src="https://i.pinimg.com/originals/ea/8d/11/ea8d11f1ffc6355b8a440106ce61d0f3.jpg"
              alt="Movie List"
            />
          </div>
          <div>Movie List</div>
        </Link>

        {/* Content Calendar */}
        <Link to="/content-calendar" className="item">
          <div className="icon">
            <img
              src="https://static-00.iconduck.com/assets.00/calendar-small-icon-1863x2048-ves2yjyu.png"
              alt="Content Calendar"
            />
          </div>
          <div>Content Calendar</div>
        </Link>

        {/* Training Schedule */}
        <div className="item">
          <div className="icon">
            <img
              src="https://cdn-icons-png.flaticon.com/512/2133/2133041.png"
              alt="Training Schedule"
            />
          </div>
          <div>Training Schedule</div>
        </div>

        {/* Quick Notes */}
        <Link to="/quick-notes" className="item">
          <div className="icon">
            <img
              src="https://cdn-icons-png.flaticon.com/256/1024/1024824.png"
              alt="Quick Notes"
            />
          </div>
          <div>Quick Notes</div>
        </Link>

        {/* Daily Tasks */}
        <Link to="/daily-tasks" className="item">
          <div className="icon">
            <img
              src="https://static.vecteezy.com/system/resources/previews/015/890/558/original/daily-task-icon-outline-work-schedule-vector.jpg"
              alt="Daily Tasks"
            />
          </div>
          <div>Daily Tasks</div>
        </Link>
      </div>

      {/* Logout Button */}
      <button onClick={handleLogout} className="logout-button">
        Logout
      </button>
    </div>
  );
}

export default HomeComponent;
