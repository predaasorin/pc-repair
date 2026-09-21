"use client";

import { useState } from "react";

export default function UrmarireComanda() {
  const [cod, setCod] = useState("");
  const [dateReparatie, setDateReparatie] = useState<any>(null);
  const [eroare, setEroare] = useState<string | null>(null);
  const [mesajOferta, setMesajOferta] = useState<{ text: string; tip: "succes" | "eroare" } | null>(null);

  const cautaReparatie = async () => {
    setEroare(null);
    setDateReparatie(null);
    setMesajOferta(null);

    if (!cod.trim()) {
      setEroare("Te rog să introduci un cod valid.");
      return;
    }

    try {
      const res = await fetch(`http://localhost:8002/api/reparatii/${cod}`);
      if (res.ok) {
        const data = await res.json();
        setDateReparatie(data);
      } else {
        setEroare("Cod invalid sau reparație inexistentă.");
      }
    } catch (e) {
      setEroare("Eroare de comunicare cu serverul.");
    }
  };

  const raspundeOferta = async (decizie: string) => {
    setMesajOferta({ text: "Se procesează...", tip: "succes" });
    try {
      const res = await fetch(`http://localhost:8002/api/reparatii/${cod}/oferte/raspuns`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ decizie }),
      });
      const data = await res.json();

      if (res.ok) {
        setMesajOferta({ text: data.mesaj, tip: "succes" });
        setTimeout(() => cautaReparatie(), 2000); // Reîncărcăm datele
      } else {
        setMesajOferta({ text: "Eroare: " + data.detail, tip: "eroare" });
      }
    } catch (e) {
      setMesajOferta({ text: "Eroare de conexiune la server.", tip: "eroare" });
    }
  };

  const ofertaActiva = dateReparatie?.oferte_pret?.find((o: any) => !o.aprobat_la && !o.refuzat_la);

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center p-4">
      <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-2xl text-black mt-10">
        <h1 className="text-2xl font-bold text-center mb-6">Urmărește Statusul Reparației</h1>

        <div className="flex gap-2 mb-6">
          <input
            type="text"
            value={cod}
            onChange={(e) => setCod(e.target.value)}
            placeholder="Ex: RPR-ABCD-12"
            className="flex-1 border p-2 rounded"
          />
          <button onClick={cautaReparatie} className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded">
            Verifică
          </button>
        </div>

        {eroare && <p className="text-red-600 font-bold mb-4">{eroare}</p>}

        {dateReparatie && (
          <div className="space-y-6">
            <div className="bg-gray-50 p-4 border rounded">
              <h2 className="text-lg font-bold mb-2 border-b pb-2">Detalii Dispozitiv</h2>
              <p><strong>Status Curent:</strong> <span className="text-blue-600 font-bold">{dateReparatie.status_reparatie}</span></p>
              <p><strong>Data preluării:</strong> {dateReparatie.data_predare}</p>
            </div>

            {/* Secțiunea de Ofertă */}
            {dateReparatie.status_reparatie === "OFERTA_IN_ASTEPTARE" && ofertaActiva && (
              <div className="bg-blue-50 border border-blue-200 p-4 rounded">
                <h3 className="text-lg font-bold text-blue-800 mb-2">💸 Ofertă de Preț în Așteptare</h3>
                <p><strong>Descriere:</strong> {ofertaActiva.descriere}</p>
                <p><strong>Manoperă:</strong> {ofertaActiva.cost_manopera} RON</p>
                <p><strong>Piese:</strong> {ofertaActiva.cost_piese} RON</p>
                <h4 className="text-xl font-bold text-green-700 my-3">
                  Total: {parseFloat(ofertaActiva.cost_manopera) + parseFloat(ofertaActiva.cost_piese)} RON
                </h4>

                <div className="flex gap-4">
                  <button onClick={() => raspundeOferta("acceptat")} className="bg-green-600 text-white px-4 py-2 rounded font-bold hover:bg-green-700">✅ Acceptă Oferta</button>
                  <button onClick={() => raspundeOferta("refuzat")} className="bg-red-600 text-white px-4 py-2 rounded font-bold hover:bg-red-700">❌ Refuză Oferta</button>
                </div>
                {mesajOferta && (
                  <p className={`mt-3 font-bold ${mesajOferta.tip === "succes" ? "text-green-700" : "text-red-600"}`}>
                    {mesajOferta.text}
                  </p>
                )}
              </div>
            )}

            {/* Timeline */}
            <div>
              <h3 className="text-lg font-bold mb-3">Timeline Reparație:</h3>
              <div className="space-y-4">
                {dateReparatie.evenimente && dateReparatie.evenimente.length > 0 ? (
                  [...dateReparatie.evenimente].reverse().map((ev: any, idx: number) => (
                    <div key={idx} className="border-l-4 border-blue-500 pl-4">
                      <p className="font-bold">{ev.status_actualizat || "Notiță adăugată"}</p>
                      <p>{ev.notita}</p>
                      <p className="text-sm text-gray-500">{new Date(ev.creat_la).toLocaleString()}</p>
                    </div>
                  ))
                ) : (
                  <p className="text-gray-500">Niciun eveniment public momentan.</p>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}