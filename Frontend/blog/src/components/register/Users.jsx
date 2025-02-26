import { useEffect, useState } from "react";

const url = "http://127.0.0.1:8000/api/user/register/";

export function Register() {
  const [register, setRegister] = useState({
    loading: true,
    username: "",
    password: "",
    email: "",
  });

  /* 
  
  fetch('https://api.example.com/users', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(userData),
})
  .then(response => response.json())
  .then(data => {
    // Handle the response data here
  })
  .catch(error => {
    // Handle any errors
  });
  */

  useEffect(() => {
    setRegister({ loading: true });

    fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(
        setRegister({
          loading: false,
          username: "username",
          password: "password",
          email: "email@gmail.com",
        })
      ),
    })
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
      })
      .catch((e) => {
        console.log(e);
      });
  }, []);
}
