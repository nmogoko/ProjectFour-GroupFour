import React, { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import "./Auth.css";

function ResetPasswordComponent() {
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const location = useLocation();
  const navigate = useNavigate();
  const email = location.state?.email; // Email passed from ForgotPasswordComponent

  const handleResetPassword = (e) => {
    e.preventDefault();

    if (password !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    const storedUser = JSON.parse(localStorage.getItem("user"));

    if (storedUser && storedUser.email === email) {
      storedUser.password = password;
      localStorage.setItem("user", JSON.stringify(storedUser));
      alert(
        "Password successfully reset! Please sign in with your new password."
      );
      navigate("/signin");
    } else {
      setError("Something went wrong");
    }
  };

  return (
    <div className="auth-container">
      <h1>Reset Password</h1>
      <form onSubmit={handleResetPassword}>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
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

export default ResetPasswordComponent;
