# pc-repair
# 🛠️ PC Repair Shop - Sistem de gestionare complet

Un sistem complet de gestionare a unui service IT, construit pentru a eficientiza fluxul de reparații, de la depunerea cererii de către client până la finalizarea reparației de către tehnician.

## 🚀 Funcționalități Principale

### Pentru Clienți:
* **Programare Inteligentă:** Formular de trimitere a dispozitivului în service. Calendarul blochează automat zilele din trecut, duminicile și zilele în care capacitatea maximă (3 reparații/zi) a fost atinsă.
* **Urmărire Live (Tracking):** Pe baza unui cod unic (ex: `RPR-ABCD-12`), clienții pot verifica statusul reparației și istoricul notițelor publice.
* **Gestionare Oferte:** Clienții primesc oferte de preț detaliate (manoperă + piese) pe care le pot accepta sau refuza direct din interfață.

### Pentru Echipa Tehnică (Tehnicieni & Admini):
* **Dashboard Securizat:** Interfață web dedicată, protejată prin autentificare JWT (JSON Web Tokens).
* **Managementul Comenzilor:** Modal interactiv (Single Page Application UX) pentru schimbarea rapidă a statusurilor, adăugarea de notițe (publice sau interne) și emiterea ofertelor de preț.
* **Role-Based Access Control (RBAC):** Funcții de management separate. Administratorii pot crea conturi noi pentru tehnicieni, în timp ce tehnicienii au acces doar la fluxul de lucru.

## 💻 Tehnologii Utilizate

* **Backend:** Python 3.13, FastAPI
* **Bază de Date:** PostgreSQL (Producție), SQLAlchemy (ORM), Alembic (Migrații)
* **Securitate:** PyJWT (Autentificare), Bcrypt (Hashing parole)
* **Frontend:** HTML5, CSS3, Vanilla JavaScript (Fetch API, DOM manipulation) - *Zero external frameworks*
* **Infrastructură:** Docker & Docker Compose
* **Testare:** Pytest (teste de integrare pe o bază de date SQLite izolată)

## ⚙️ Rularea Proiectului (Local)

1. **Clonează repository-ul:**
   \`\`\`bash
   git clone <link-ul-tau-aici>
   cd pc-repair
   \`\`\`

2. **Setează variabilele de mediu:**
   Creează un fișier `.env` în rădăcina proiectului cu următoarele date:
   \`\`\`env
   POSTGRES_USER=utilizator
   POSTGRES_PASSWORD=parolasecreta
   POSTGRES_DB=pc_repair_db
   DATABASE_URL=postgresql://utilizator:parolasecreta@db:5432/pc_repair_db
   SECRET_KEY=o_cheie_foarte_secreta_pentru_jwt
   \`\`\`

3. **Pornește containerele Docker:**
   \`\`\`bash
   docker compose up --build -d
   \`\`\`

4. **Accesează Aplicația:**
   * Portal Client (Creare): [http://localhost:8002/static/index.html](http://localhost:8002/static/index.html)
   * Portal Client (Urmărire): [http://localhost:8002/static/urmarire_comanda.html](http://localhost:8002/static/urmarire_comanda.html)
   * Dashboard Tehnician: [http://localhost:8002/static/admin.html](http://localhost:8002/static/admin.html)
   * Documentație API (Swagger): [http://localhost:8002/docs](http://localhost:8002/docs)

## 🧪 Testare

Pentru a rula suita de teste automate:
\`\`\`bash
docker compose exec api pytest
\`\`\`