"use client";

import { useState, useEffect } from "react";

// Funcție utilitară pentru decodarea JWT în React
const parseJwt = (token: string) => {
  try {
    return JSON.parse(atob(token.split(".")[1]));
  } catch (e) {
    return null;
  }
};

export default function Dashboard() {
  const [token, setToken] = useState<string | null>(null);
  const [rol, setRol] = useState<string | null>(null);
  const [emailLogin, setEmailLogin] = useState("");
  const [parolaLogin, setParolaLogin] = useState("");
  const [loginEroare, setLoginEroare] = useState("");

  const [reparatii, setReparatii] = useState<any[]>([]);
  const [modalData, setModalData] = useState<any | null>(null);
  const [curentReparatieId, setCurentReparatieId] = useState<number | null>(null);

  // State pentru formularele din modal și admin
  const [nouStatus, setNouStatus] = useState("IN_DIAGNOSTICARE");
  const [notita, setNotita] = useState("");
  const [estePublic, setEstePublic] = useState(false);
  const [oferta, setOferta] = useState({ manopera: "", piese: "", descriere: "" });
  const [tehnicianNou, setTehnicianNou] = useState({ email: "", parola: "" });
  const [mesajeGestiune, setMesajeGestiune] = useState({ status: "", notita: "", oferta: "", admin: "" });

  useEffect(() => {
    const savedToken = localStorage.getItem("token_angajat");
    if (savedToken) {
      setToken(savedToken);
      setRol(parseJwt(savedToken)?.rol || null);
      incarcaTabel(savedToken);
    }
  }, []);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoginEroare("");
    const res = await fetch("http://localhost:8002/api/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: emailLogin, parola: parolaLogin }),
    });

    if (res.ok) {
      const data = await res.json();
      localStorage.setItem("token_angajat", data.access_token);
      setToken(data.access_token);
      setRol(parseJwt(data.access_token)?.rol);
      incarcaTabel(data.access_token);
    } else {
      setLoginEroare("Email sau parolă incorecte!");
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("token_angajat");
    setToken(null);
    setRol(null);
    setReparatii([]);
  };

  const incarcaTabel = async (currentToken: string) => {
    const res = await fetch("http://localhost:8002/api/tehnician/reparatii", {
      headers: { Authorization: `Bearer ${currentToken}` },
    });
    if (res.ok) {
      const data = await res.json();
      setReparatii(data.reparatii);
    }
  };

  const creeazaTehnician = async () => {
    const res = await fetch("http://localhost:8002/api/admin/tehnicieni", {
      method: "POST",
      headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
      body: JSON.stringify({ email: tehnicianNou.email, parola: tehnicianNou.parola }),
    });
    const data = await res.json();
    setMesajeGestiune({ ...mesajeGestiune, admin: res.ok ? "✅ " + data.mesaj : "❌ Eroare" });
  };

  const deschideModal = async (id: number) => {
    setCurentReparatieId(id);
    setMesajeGestiune({ status: "", notita: "", oferta: "", admin: "" });
    incarcaDetaliiComanda(id);
  };

  const incarcaDetaliiComanda = async (id: number) => {
    const res = await fetch(`http://localhost:8002/api/tehnician/reparatii/${id}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (res.ok) {
      setModalData(await res.json());
    }
  };

  const inchideModal = () => {
    setModalData(null);
    setCurentReparatieId(null);
    if (token) incarcaTabel(token);
  };

  // Acțiuni Modal
  const schimbaStatus = async () => {
    const res = await fetch(`http://localhost:8002/api/tehnician/reparatii/${curentReparatieId}/status`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
      body: JSON.stringify({ status_nou: nouStatus }),
    });
    if (res.ok) {
      setMesajeGestiune({ ...mesajeGestiune, status: "Status actualizat!" });
      incarcaDetaliiComanda(curentReparatieId!);
    }
  };

  const adaugaNotita = async () => {
    const res = await fetch(`http://localhost:8002/api/tehnician/reparatii/${curentReparatieId}/evenimente`, {
      method: "POST",
      headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
      body: JSON.stringify({ notita, este_public: estePublic }),
    });
    if (res.ok) {
      setMesajeGestiune({ ...mesajeGestiune, notita: "Notiță adăugată!" });
      setNotita("");
      incarcaDetaliiComanda(curentReparatieId!);
    }
  };

  const trimiteOferta = async () => {
    const res = await fetch(`http://localhost:8002/api/tehnician/reparatii/${curentReparatieId}/oferta`, {
      method: "POST",
      headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
      body: JSON.stringify({ cost_manopera: parseFloat(oferta.manopera), cost_piese: parseFloat(oferta.piese) || 0, descriere: oferta.descriere }),
    });
    if (res.ok) {
      setMesajeGestiune({ ...mesajeGestiune, oferta: "Ofertă trimisă!" });
      setOferta({ manopera: "", piese: "", descriere: "" });
      incarcaDetaliiComanda(curentReparatieId!);
    }
  };

  if (!token) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
        <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-sm text-black">
          <h1 className="text-2xl font-bold text-center mb-6">Autentificare Angajați</h1>
          <form onSubmit={handleLogin} className="space-y-4">
            <input type="email" value={emailLogin} onChange={(e) => setEmailLogin(e.target.value)} placeholder="Email angajat" required className="w-full border p-2 rounded" />
            <input type="password" value={parolaLogin} onChange={(e) => setParolaLogin(e.target.value)} placeholder="Parolă" required className="w-full border p-2 rounded" />
            <button type="submit" className="w-full bg-gray-800 text-white font-bold py-2 rounded hover:bg-gray-900">Intră în cont</button>
            {loginEroare && <p className="text-red-600 text-center">{loginEroare}</p>}
          </form>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100 p-8 text-black">
      <div className="max-w-6xl mx-auto bg-white p-6 rounded-lg shadow-md relative">
        <button onClick={handleLogout} className="absolute top-6 right-6 bg-red-600 text-white px-4 py-2 rounded font-bold hover:bg-red-700">Delogare</button>
        <h1 className="text-3xl font-bold mb-8">{rol === "ADMIN" ? "👨‍💼 Dashboard Administrator" : "👨‍🔧 Dashboard Tehnician"}</h1>

        {rol === "ADMIN" && (
          <div className="bg-gray-200 p-4 rounded-lg mb-8">
            <h3 className="font-bold mb-3">🛠️ Adaugă Tehnician Nou</h3>
            <div className="flex gap-4">
              <input type="email" placeholder="Email" value={tehnicianNou.email} onChange={(e) => setTehnicianNou({ ...tehnicianNou, email: e.target.value })} className="flex-1 p-2 rounded border" />
              <input type="password" placeholder="Parolă" value={tehnicianNou.parola} onChange={(e) => setTehnicianNou({ ...tehnicianNou, parola: e.target.value })} className="flex-1 p-2 rounded border" />
              <button onClick={creeazaTehnician} className="bg-blue-600 text-white px-6 py-2 rounded font-bold">Adaugă</button>
            </div>
            {mesajeGestiune.admin && <p className="mt-2 font-bold">{mesajeGestiune.admin}</p>}
          </div>
        )}

        <h2 className="text-xl font-bold mb-4">Lista Reparațiilor Active (Click pentru acțiuni)</h2>
        <div className="overflow-x-auto">
          <table className="min-w-full bg-white border">
            <thead className="bg-gray-800 text-white">
              <tr>
                <th className="py-3 px-4 text-left">ID / Cod</th>
                <th className="py-3 px-4 text-left">Status</th>
                <th className="py-3 px-4 text-left">Data Predare</th>
              </tr>
            </thead>
            <tbody>
              {reparatii.map((rep) => (
                <tr key={rep.id} onClick={() => deschideModal(rep.id)} className="border-b hover:bg-gray-50 cursor-pointer transition-colors">
                  <td className="py-3 px-4"><strong>{rep.id}</strong><br/><span className="text-sm text-gray-500">{rep.cod_urmarire}</span></td>
                  <td className="py-3 px-4 font-bold">{rep.status_reparatie}</td>
                  <td className="py-3 px-4">{rep.data_predare}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Modal */}
      {modalData && (
        <div className="fixed inset-0 bg-black bg-opacity-70 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg w-full max-w-4xl max-h-[90vh] overflow-y-auto p-6 relative">
            <button onClick={inchideModal} className="absolute top-4 right-4 bg-red-600 text-white px-4 py-2 rounded font-bold">Închide</button>
            <h2 className="text-2xl font-bold mb-6">Comanda ID: {modalData.id} ({modalData.cod_urmarire})</h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Coloana Stânga */}
              <div className="space-y-6">
                <div className="bg-gray-50 p-4 border rounded">
                  <h3 className="font-bold mb-2">📌 Detalii</h3>
                  <p><strong>Dispozitiv:</strong> {modalData.brand} {modalData.model}</p>
                  <p><strong>Defect:</strong> {modalData.descrierea_problemei}</p>
                  <p><strong>Status:</strong> <span className="text-blue-600 font-bold">{modalData.status_reparatie}</span></p>
                </div>

                <div className="bg-gray-50 p-4 border rounded">
                  <h3 className="font-bold mb-2">🔄 Schimbă Status</h3>
                  <select value={nouStatus} onChange={(e) => setNouStatus(e.target.value)} className="w-full p-2 border rounded mb-2">
                    <option value="IN_DIAGNOSTICARE">IN_DIAGNOSTICARE</option>
                    <option value="OFERTA_IN_ASTEPTARE">OFERTA_IN_ASTEPTARE</option>
                    <option value="IN_LUCRU">IN_LUCRU</option>
                    <option value="ASTEPTARE_PIESE">ASTEPTARE_PIESE</option>
                    <option value="PREGATIT_PENTRU_RIDICARE">PREGATIT_PENTRU_RIDICARE</option>
                    <option value="RIDICAT">RIDICAT</option>
                    <option value="ANULAT">ANULAT</option>
                  </select>
                  <button onClick={schimbaStatus} className="w-full bg-green-600 text-white py-2 rounded font-bold">Actualizează</button>
                  {mesajeGestiune.status && <p className="text-green-600 mt-2">{mesajeGestiune.status}</p>}
                </div>

                <div className="bg-gray-50 p-4 border rounded">
                  <h3 className="font-bold mb-2">💰 Trimite Ofertă</h3>
                  <input type="number" placeholder="Manoperă (RON)" value={oferta.manopera} onChange={(e) => setOferta({ ...oferta, manopera: e.target.value })} className="w-full p-2 border rounded mb-2" />
                  <input type="number" placeholder="Piese (RON)" value={oferta.piese} onChange={(e) => setOferta({ ...oferta, piese: e.target.value })} className="w-full p-2 border rounded mb-2" />
                  <textarea placeholder="Descriere ofertă" value={oferta.descriere} onChange={(e) => setOferta({ ...oferta, descriere: e.target.value })} className="w-full p-2 border rounded mb-2" rows={2}></textarea>
                  <button onClick={trimiteOferta} className="w-full bg-green-600 text-white py-2 rounded font-bold">Trimite Oferta</button>
                  {mesajeGestiune.oferta && <p className="text-green-600 mt-2">{mesajeGestiune.oferta}</p>}
                </div>
              </div>

              {/* Coloana Dreapta */}
              <div className="space-y-6">
                <div className="bg-gray-50 p-4 border rounded">
                  <h3 className="font-bold mb-2">📝 Adaugă Notiță</h3>
                  <textarea value={notita} onChange={(e) => setNotita(e.target.value)} placeholder="Scrie o notiță..." className="w-full p-2 border rounded mb-2" rows={3}></textarea>
                  <label className="flex items-center gap-2 mb-4">
                    <input type="checkbox" checked={estePublic} onChange={(e) => setEstePublic(e.target.checked)} />
                    Vizibilă pentru client
                  </label>
                  <button onClick={adaugaNotita} className="w-full bg-blue-600 text-white py-2 rounded font-bold">Salvează</button>
                  {mesajeGestiune.notita && <p className="text-green-600 mt-2">{mesajeGestiune.notita}</p>}
                </div>

                <div className="bg-gray-50 p-4 border rounded">
                  <h3 className="font-bold mb-2">📜 Istoric</h3>
                  <div className="max-h-64 overflow-y-auto space-y-3">
                    {modalData.evenimente && modalData.evenimente.length > 0 ? (
                      [...modalData.evenimente].reverse().map((ev: any, idx: number) => (
                        <div key={idx} className="border-b pb-2 text-sm">
                          <div className="flex justify-between font-bold">
                            <span>{ev.status_actualizat || "Notiță"}</span>
                            <span className={ev.este_public ? "text-green-600" : "text-gray-500"}>{ev.este_public ? "🌍 Public" : "🔒 Intern"}</span>
                          </div>
                          <p>{ev.notita}</p>
                          <p className="text-xs text-gray-400">{new Date(ev.creat_la).toLocaleString()}</p>
                        </div>
                      ))
                    ) : (
                      <p className="text-gray-500">Niciun eveniment.</p>
                    )}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}