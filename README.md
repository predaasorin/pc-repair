# 🛠️ PC Repair Shop - Full Stack Management System

Acest proiect reprezintă o soluție completă (Full-Stack) construită pe o arhitectură decuplată. Folosește un backend robust și rapid dezvoltat în **Python (FastAPI)**, susținut de o bază de date relațională **PostgreSQL** (gestionată prin ORM-ul **SQLAlchemy**) și rulat integral în containere **Docker**. 

Sistemul rezolvă probleme reale de business acoperind întreg fluxul operațional al unui service IT: validarea inteligentă a programărilor (limitare de capacitate și zile nelucrătoare), trasabilitatea reparațiilor (tracking timeline), ofertarea clienților și o gestiune securizată a angajaților folosind un sistem de permisiuni (RBAC) bazat pe **JWT** (JSON Web Tokens).

Pentru interfața cu utilizatorul, aplicația dispune de un frontend modern dezvoltat în **Next.js (React) și Tailwind CSS**, oferind o experiență fluidă de tip Single Page Application (SPA). Totodată, proiectul include și o implementare inițială de bază în **Vanilla HTML/CSS/JS** pentru a demonstra fundamentele dezvoltării web.

## 🚀 Funcționalități Principale

### Pentru Clienți:
* **Programare Inteligentă:** Formular de trimitere a dispozitivului în service. Calendarul validează datele în timp real, blocând zilele din trecut, duminicile și datele în care capacitatea maximă (3 reparații/zi) a fost atinsă.
* **Urmărire Live (Tracking):** Pe baza unui cod unic (ex: `RPR-ABCD-12`), clienții pot verifica statusul reparației și istoricul notițelor publice.
* **Gestionare Oferte:** Clienții primesc oferte de preț detaliate (manoperă + piese) pe care le pot accepta sau refuza direct din interfață.

### Pentru Echipa Tehnică (Tehnicieni & Admini):
* **Dashboard Securizat:** Interfață web dedicată, protejată prin autentificare JWT.
* **Managementul Comenzilor (SPA UX):** Modal interactiv pentru schimbarea rapidă a statusurilor, adăugarea de notițe (publice sau interne) și emiterea ofertelor de preț.
* **Role-Based Access Control (RBAC):** Administratorii au panouri dedicate pentru a crea conturi noi de tehnicieni, în timp ce tehnicienii au acces strict la fluxul operațional.

## 💻 Tehnologii Utilizate

**Backend (API Server):**
* Python 3.13 & FastAPI
* PostgreSQL (Producție) / SQLite (Teste de integrare)
* SQLAlchemy (ORM) & Alembic (Migrații baze de date)
* PyJWT (Autentificare JWT) & Bcrypt (Hashing parole)
* Docker & Docker Compose

**Frontend (Next.js - Varianta Principală):**
* React 18 & Next.js (App Router)
* Tailwind CSS pentru un design modern și responsive
* TypeScript
* Fetch API cu suport CORS pentru comunicarea cu backend-ul

*Notă: Versiunea inițială Vanilla (HTML5, CSS3, JS) este disponibilă în folderul `frontend/`.*

## ⚙️ Cum să rulezi proiectul local

Ai nevoie de **Docker** și **Node.js** instalate pe sistemul tău.

### Pasul 1: Pornirea Backend-ului (FastAPI + PostgreSQL)

1. **Clonează repository-ul:**
```bash
git clone https://github.com/predaasorin/pc-repair.git
cd pc-repair
```
### 2. Configurarea Variabilelor de Mediu
Proiectul conține un fișier de referință numit `.env.example`. Creează un fișier nou cu numele `.env` în rădăcina proiectului și adaugă variabilele necesare
### 3. Pornirea Backend-ului (Docker)
Construiește și pornește containerele pentru baza de date PostgreSQL și serverul FastAPI. Din folderul rădăcină (`pc-repair`), rulează:
```bash
docker compose up --build -d
```
*Backend-ul va rula pe portul 8002. Baza de date și migrațiile se vor inițializa automat. Documentația Swagger o găsești la `http://localhost:8002/docs`.*

### 4. Pornirea Frontend-ului (Next.js)
Deschide un terminal nou, navighează în folderul interfeței moderne, instalează pachetele necesare și pornește serverul de dezvoltare:
```bash
cd frontend-next
npm install
npm run dev
```
*Aplicația web va deveni accesibilă la adresa `http://localhost:3000`.*

## 📍 Rute Navigare (Frontend)
* **Preluare Cerere Nouă:** `http://localhost:3000`
* **Urmărire Comandă Client:** `http://localhost:3000/urmarire`
* **Dashboard Tehnician/Admin:** `http://localhost:3000/dashboard`

## 🧪 Testare

Pentru a rula suita de teste automate: 
```bash 
docker compose exec api pytest 
```

