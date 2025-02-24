import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

export const Login = () => {
  const [formData, setFormData] = useState({ email: "", password: "" });
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch("/api/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      if (!response.ok) throw new Error("Error al iniciar sesión");

      const data = await response.json();
      if (data.error) return alert(data.error);

      navigate("/muro");
    } catch (error) {
      alert("Error en el inicio de sesión");
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="email" name="email" value={formData.email} onChange={handleChange} placeholder="Correo" required />
      <input type="password" name="password" value={formData.password} onChange={handleChange} placeholder="Contraseña" required />
      <button type="submit">Iniciar sesión</button>
    </form>
  );
};
