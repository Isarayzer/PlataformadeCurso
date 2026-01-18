# CourseHub Frontend

Modern and beautiful course management platform built with React, Vite, and TailwindCSS.

## 🚀 Tech Stack

- **React 18** - UI library
- **Vite** - Build tool and dev server
- **TailwindCSS** - Utility-first CSS framework
- **React Router** - Client-side routing
- **Lucide React** - Beautiful icon set
- **Zustand** - State management (to be implemented)
- **Axios** - HTTP client (to be implemented)

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── ui/              # Reusable UI components
│   │   │   ├── Button.jsx
│   │   │   ├── Input.jsx
│   │   │   ├── Card.jsx
│   │   │   ├── Badge.jsx
│   │   │   ├── Modal.jsx
│   │   │   ├── Loading.jsx
│   │   │   └── index.js
│   │   └── layout/          # Layout components
│   │       ├── MainLayout.jsx
│   │       ├── Sidebar.jsx
│   │       └── Header.jsx
│   ├── pages/               # Page components
│   │   ├── Dashboard.jsx
│   │   ├── Login.jsx
│   │   └── Register.jsx
│   ├── store/               # State management (to be implemented)
│   ├── utils/               # Utility functions
│   ├── hooks/               # Custom React hooks
│   ├── assets/              # Static assets
│   ├── App.jsx              # Main app component
│   ├── main.jsx             # App entry point
│   └── index.css            # Global styles and Tailwind
├── public/                  # Public assets
├── index.html
├── package.json
├── vite.config.js
├── tailwind.config.js
└── postcss.config.js
```

## 🛠️ Installation

1. Install dependencies:
```bash
npm install
```

2. Start development server:
```bash
npm run dev
```

3. Build for production:
```bash
npm run build
```

## 📄 Available Scripts

- `npm run dev` - Start development server on http://localhost:5173
- `npm run build` - Build for production
- `npm run preview` - Preview production build locally

## 🎨 Design System

### Color Palette

- **Primary**: Blue (#0ea5e9)
- **Secondary**: Purple (#a855f7)
- **Success**: Green (#22c55e)
- **Warning**: Orange (#f59e0b)
- **Danger**: Red (#ef4444)
- **Neutral**: Gray scale

### Typography

- **Display**: Poppins
- **Body**: Inter
- **Mono**: Fira Code

## 🎯 Features Implemented

### ✅ Completed

- [x] Project setup with Vite and React
- [x] TailwindCSS configuration with custom theme
- [x] Design system with color palette and typography
- [x] UI Component library (Button, Input, Card, Badge, Modal, Loading)
- [x] Layout components (Sidebar, Header, MainLayout)
- [x] Authentication pages (Login, Register)
- [x] Dashboard page with statistics
- [x] Routing setup with React Router

### 🚧 To Be Implemented

- [ ] State management with Zustand
- [ ] API integration
- [ ] Video library page
- [ ] Course management
- [ ] Category management
- [ ] Learning paths
- [ ] Upload functionality
- [ ] Video player integration
- [ ] AI features

---

**Version**: 1.0.0
**Last Updated**: 2026-01-18
