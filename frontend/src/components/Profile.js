import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import "./Profile.css";

function ProfileComponent() {
  const [profilePicture, setProfilePicture] = useState(
    localStorage.getItem("profilePicture") || ""
  );

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    const reader = new FileReader();

    reader.onloadend = () => {
      setProfilePicture(reader.result);
      localStorage.setItem("profilePicture", reader.result);
      console.log("Profile picture updated:", reader.result);
    };

    if (file) {
      reader.readAsDataURL(file);
    }
  };

  useEffect(() => {
    console.log("Current profile picture:", profilePicture);
  }, [profilePicture]);

  return (
    <div className="profile-container">
      <h1>Profile</h1>
      <div className="profile-picture-container">
        <img
          src={profilePicture || "https://via.placeholder.com/150"}
          alt="Profile"
          className="profile-picture"
        />
        <input type="file" accept="image/*" onChange={handleImageUpload} />
      </div>
      <Link to="/" className="back-button">
        Back to Home
      </Link>
    </div>
  );
}

export default ProfileComponent;
