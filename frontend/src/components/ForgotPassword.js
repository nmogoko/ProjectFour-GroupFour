import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Auth.css";

function ForgotPasswordComponent() {
  const [email, setEmail] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handlePasswordReset = (e) => {
    e.preventDefault();

    const storedUser = JSON.parse(localStorage.getItem("user"));

    if (storedUser && storedUser.email === email) {
      if (newPassword === storedUser.password) {
        setError("New password cannot be the same as the old password");
        return;
      }

      if (newPassword !== confirmPassword) {
        setError("Passwords do not match");
        return;
      }

      localStorage.setItem(
        "user",
        JSON.stringify({ ...storedUser, password: newPassword })
      );
      alert(
        "Password successfully reset! Please sign in with your new password."
      );
      navigate("/signin");
    } else {
      setError("Email not found");
    }
  };

  return (
    <div className="auth-container">
      <h1>Reset Password</h1>
      <form onSubmit={handlePasswordReset}>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Enter your email"
          required
        />
        <input
          type="password"
          value={newPassword}
          onChange={(e) => setNewPassword(e.target.value)}
          placeholder="Enter new password"
          required
        />
        <input
          type="password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          placeholder="Confirm new password"
          required
        />
        {error && <p className="error">{error}</p>}
        <button type="submit">Reset Password</button>
      </form>
    </div>
  );
}

export default ForgotPasswordComponent;
