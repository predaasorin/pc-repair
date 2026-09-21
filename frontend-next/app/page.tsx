"use client";

import { useState, useEffect } from "react";

export default function CerereNoua() {
  const [dateIndisponibile, setDateIndisponibile] = useState<string[]>([]);
  const [mesaj, setMesaj] = useState<{ text: string; tip: "succes" | "eroare" } | null>(null);
  
  // Setăm data minimă pentru calendar (azi)
  const aziString = new Date().toISOString().split("T")[0];

  const [formData, setFormData] = useState({
    nume: "",
    telefon: "",
    tip_dispozitiv: "LAPTOP",
    brand: "",
    model: "",
    descrierea_problemei: "",
    data_predare: "",
  });

  // Funcție pentru a încărca datele indisponibile de la backend-ul FastAPI
  const incarcaDisponibilitate = async () => {
    const azi = new Date();
    const viitor = new Date(azi);
    viitor.setDate(viitor.getDate() + 60);
    const viitorString = viitor.toISOString().split("T")[0];

    try {
      // Comunicăm cu FastAPI pe portul 8002
      const res = await fetch(`http://localhost:8002/api/reparatii/disponibilitate?de_la_data=${aziString}&pana_la_data=${viitorString}`);
      if (res.ok) {
        const data = await res.json();
        const indisponibile = data.interval
          .filter((zi: any) => zi.disponibil === false)
          .map((zi: any) => zi.data);
        setDateIndisponibile(indisponibile);
      }
    } catch (e) {
      console.error("Eroare la încărcarea disponibilității", e);
    }
  };

  useEffect(() => {
    incarcaDisponibilitate();
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;

    // Validare calendar live
    if (name === "data_predare") {
      const d = new Date(value);
      if (d.getDay() === 0 || dateIndisponibile.includes(value)) {
        alert("⚠️ Această dată nu este disponibilă (este Duminică sau am atins capacitatea maximă). Te rugăm să alegi o altă zi!");
        return; // Oprim actualizarea state-ului cu o dată greșită
      }
    }

    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setMesaj(null);

    try {
      const response = await fetch("http://localhost:8002/api/reparatii", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (response.ok) {
        setMesaj({ text: `Succes! Codul tău de urmărire este: ${data.cod_urmarire}. Notează-l!`, tip: "succes" });
        setFormData({ ...formData, nume: "", telefon: "", brand: "", model: "", descrierea_problemei: "", data_predare: "" });
        incarcaDisponibilitate(); // Reîmprospătăm calendarul
      } else {
        if (Array.isArray(data.detail)) {
          const erori = data.detail.map((err: any) => `Câmpul "${err.loc[err.loc.length - 1]}": ${err.msg}`).join(" | ");
          setMesaj({ text: `Date invalide: ${erori}`, tip: "eroare" });
        } else {
          setMesaj({ text: data.detail || "Eroare necunoscută.", tip: "eroare" });
        }
      }
    } catch (error) {
      setMesaj({ text: "Eroare de conexiune la server.", tip: "eroare" });
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
      <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-lg text-black">
        <h1 className="text-2xl font-bold text-center mb-6 text-gray-800">Trimite Dispozitivul în Service</h1>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block font-bold mb-1">Nume complet *</label>
            <input type="text" name="nume" value={formData.nume} onChange={handleChange} required className="w-full border p-2 rounded" />
          </div>

          <div>
            <label className="block font-bold mb-1">Telefon *</label>
            <input type="tel" name="telefon" value={formData.telefon} onChange={handleChange} required className="w-full border p-2 rounded" />
          </div>

          <div>
            <label className="block font-bold mb-1">Tip Dispozitiv *</label>
            <select name="tip_dispozitiv" value={formData.tip_dispozitiv} onChange={handleChange} required className="w-full border p-2 rounded bg-white">
              <option value="LAPTOP">Laptop</option>
              <option value="DESKTOP">PC Desktop</option>
              <option value="ALL_IN_ONE">All in One</option>
              <option value="ALTUL">Altul</option>
            </select>
          </div>

          <div>
            <label className="block font-bold mb-1">Brand *</label>
            <input type="text" name="brand" value={formData.brand} onChange={handleChange} placeholder="ex: Asus, Dell, Apple" required className="w-full border p-2 rounded" />
          </div>

          <div>
            <label className="block font-bold mb-1">Model *</label>
            <input type="text" name="model" value={formData.model} onChange={handleChange} required className="w-full border p-2 rounded" />
          </div>

          <div>
            <label className="block font-bold mb-1">Descrie problema *</label>
            <textarea name="descrierea_problemei" value={formData.descrierea_problemei} onChange={handleChange} rows={4} required className="w-full border p-2 rounded" />
          </div>

          <div>
            <label className="block font-bold mb-1">Data la care dorești să îl aduci *</label>
            <input type="date" name="data_predare" value={formData.data_predare} onChange={handleChange} min={aziString} required className="w-full border p-2 rounded" />
          </div>

          <button type="submit" className="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded transition-colors">
            Trimite Cererea
          </button>
        </form>

        {mesaj && (
          <div className={`mt-4 p-4 rounded text-center font-bold ${mesaj.tip === "succes" ? "bg-green-100 text-green-800 border border-green-300" : "bg-red-100 text-red-800 border border-red-300"}`}>
            {mesaj.text}
          </div>
        )}
      </div>
    </div>
  );
}