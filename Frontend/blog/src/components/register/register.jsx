import { useState } from "react";
import axiosInstance from "../snippets/axios";

import { useNavigate, NavLink, useHref } from "react-router-dom";

export default function SignUpUSer() {
  const navigate = useNavigate();

  const initialFormData = Object.freeze({
    email: "",
    username: "",
    password: "",
    first_name: "",
    last_name: "",
  });

  const [formData, setFormData] = useState(initialFormData);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      // Trim any whitespace
      [e.target.name]: e.target.value.trim(),
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log(formData);

    axiosInstance
      .post("user/register/", {
        email: formData.email,
        username: formData.username,
        password: formData.password,
      })
      .then((res) => {
        navigate("/login");
        // console.log(res);
        console.log(res.data);
      });
  };

  return (
    <form className="login-container">
      <h1 className="title">Sign up</h1>

      <label htmlFor="username"> Username</label>

      <input
        type="text"
        className="username"
        placeholder="johndoe"
        min={4}
        max={20}
        name="username"
        id="username"
        onChange={handleChange}
      />
      <label htmlFor="email">Email</label>
      <input
        type="text"
        className="email"
        placeholder="youremail@gmail.com"
        name="email"
        id="email"
        onChange={handleChange}
      />

      <label htmlFor="password">password</label>
      <input
        type="text"
        className="password"
        name="password"
        id="password"
        onChange={handleChange}
      />

      <input
        type="text"
        className="username"
        placeholder="johndoe"
        min={4}
        max={20}
        name="first_name"
        id="first_name"
        onChange={handleChange}
      />
      <label htmlFor="last_name">last_name</label>
      <input
        type="text"
        className="username"
        placeholder="last name"
        name="last_name"
        id="last_name"
        onChange={handleChange}
      />

      <button className="btn" type="submit" onClick={handleSubmit}>
        Sign up
      </button>
      <p>
        Already have an account? <a href="#">Sign in</a>
      </p>

      <div className="or">or</div>
      <input
        type="submit"
        value="Sign up with Google"
        className="google btn"
        name="google"
      />
      <input
        type="submit"
        value="Sign up with facebook"
        className="facebook btn"
        name="google"
      />
    </form>
  );
}




















