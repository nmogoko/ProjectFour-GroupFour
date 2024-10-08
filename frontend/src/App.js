import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import HomeComponent from "./components/Home";
import SignInComponent from "./components/SignIn";
import SignUpComponent from "./components/SignUp";
import ForgotPasswordComponent from "./components/ForgotPassword";
import ResetPasswordComponent from "./components/ResetPassword";
import QuickNotesComponent from "./components/QuickNotes";
import ReadingListComponent from "./components/ReadingList";
import MovieListComponent from "./components/MovieList";
import DailyTasksComponent from "./components/DailyTasks";
import ProfileComponent from "./components/Profile";
import ContentCalendarComponent from "./components/ContentCalendar"; // Import the ContentCalendarComponent

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<HomeComponent />} />
          <Route path="/signin" element={<SignInComponent />} />
          <Route path="/signup" element={<SignUpComponent />} />
          <Route
            path="/forgot-password"
            element={<ForgotPasswordComponent />}
          />
          <Route path="/reset-password" element={<ResetPasswordComponent />} />
          <Route path="/quick-notes" element={<QuickNotesComponent />} />
          <Route path="/reading-list" element={<ReadingListComponent />} />
          <Route path="/movie-list" element={<MovieListComponent />} />
          <Route path="/daily-tasks" element={<DailyTasksComponent />} />
          <Route path="/profile" element={<ProfileComponent />} />
          <Route
            path="/content-calendar"
            element={<ContentCalendarComponent />}
          />{" "}
          {/* Set up route for the Content Calendar */}
        </Routes>
      </div>
    </Router>
  );
}

export default App;
