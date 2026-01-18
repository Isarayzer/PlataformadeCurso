# CourseHub - Plataforma de Gerenciamento de Cursos em Vídeo

Uma plataforma moderna e avançada para criação, organização e gerenciamento de cursos baseados em vídeo, com funcionalidades de IA para geração automática de resumos e questionários.

## 🎯 Visão Geral

CourseHub é uma solução completa para educadores, criadores de conteúdo e instituições que desejam estruturar e gerenciar cursos em vídeo de forma profissional e intuitiva.

### Principais Funcionalidades

- 📹 **Upload e gerenciamento de vídeos** - Suporte para múltiplos formatos (MP4, AVI, MOV, WebM)
- 📚 **Estruturação de cursos** - Organize em módulos e aulas com drag & drop
- 🏷️ **Categorias e tags** - Sistema flexível de organização
- 🛤️ **Trilhas de aprendizado** - Agrupe cursos em jornadas de conhecimento
- 🤖 **IA integrada** - Geração automática de resumos e questionários via OpenAI
- 🎨 **Interface moderna** - Design bonito, responsivo e fácil de usar

## 🚀 Tech Stack

### Frontend
- **React 18** - Biblioteca de UI
- **Vite** - Build tool e dev server
- **TailwindCSS** - Framework CSS utility-first
- **React Router** - Roteamento client-side
- **Lucide React** - Biblioteca de ícones
- **Zustand** - Gerenciamento de estado (em implementação)

### Backend (em desenvolvimento)
- **Node.js/Express** ou **Python/FastAPI**
- **PostgreSQL** ou **SQLite** - Banco de dados
- **JWT** - Autenticação
- **OpenAI API** - Transcrição (Whisper) e geração de conteúdo (GPT-4)

## 📁 Estrutura do Projeto

```
Plataforma de Curso/
├── frontend/                 # Aplicação React
│   ├── src/
│   │   ├── components/
│   │   │   ├── ui/          # Componentes reutilizáveis
│   │   │   └── layout/      # Layout (Sidebar, Header)
│   │   ├── pages/           # Páginas da aplicação
│   │   ├── store/           # Estado global (Zustand)
│   │   ├── hooks/           # Custom hooks
│   │   └── utils/           # Funções utilitárias
│   └── ...
├── backend/                  # API (em desenvolvimento)
├── PRD.md                    # Documento de requisitos
├── CHECKLIST.md              # Lista de tarefas detalhada
├── PROGRESS.md               # Relatório de progresso
└── VISUAL_GUIDE.md           # Guia visual do design system
```

## 🛠️ Instalação e Execução

### Pré-requisitos
- Node.js 18+
- npm ou yarn

### Frontend

```bash
# Entrar na pasta do frontend
cd frontend

# Instalar dependências
npm install

# Rodar em modo de desenvolvimento
npm run dev

# Build para produção
npm run build
```

O servidor de desenvolvimento estará disponível em `http://localhost:5173`

## 🎨 Design System

O projeto utiliza um design system consistente com:

### Cores
- **Primary**: Azul (#0ea5e9) - Ações principais
- **Secondary**: Roxo (#a855f7) - Elementos de destaque
- **Success**: Verde (#22c55e) - Estados de sucesso
- **Warning**: Laranja (#f59e0b) - Alertas
- **Danger**: Vermelho (#ef4444) - Erros e ações destrutivas

### Tipografia
- **Display**: Poppins - Títulos e destaques
- **Body**: Inter - Texto geral
- **Mono**: Fira Code - Código

### Componentes UI
- Button (5 variantes)
- Input (com ícones e validação)
- Card (com hover effects)
- Badge (indicadores de status)
- Modal (diálogos)
- Loading (spinners)

## 📱 Screenshots

### Dashboard
- Cards de estatísticas (cursos, vídeos, alunos)
- Ações rápidas (criar curso, upload de vídeo)
- Lista de cursos recentes

### Autenticação
- Login com validação
- Registro de novos usuários

## 🗺️ Roadmap

### ✅ Fase 1 - MVP (Em progresso)
- [x] Setup do projeto frontend
- [x] Design system e componentes UI
- [x] Layout responsivo (Sidebar, Header)
- [x] Páginas de autenticação
- [x] Dashboard principal
- [ ] Biblioteca de vídeos
- [ ] Gerenciamento de cursos
- [ ] Backend API
- [ ] Sistema de autenticação

### 🔜 Fase 2 - Recursos Avançados
- [ ] Trilhas de aprendizado
- [ ] Marcadores temporais em vídeos
- [ ] Sistema de busca avançado
- [ ] Drag & drop para reorganização

### 🔮 Fase 3 - Integração de IA
- [ ] Transcrição automática (Whisper)
- [ ] Geração de resumos (GPT-4)
- [ ] Geração de questionários (GPT-4)

### 📈 Fase 4 - Otimização
- [ ] Performance e caching
- [ ] Analytics e monitoramento
- [ ] Documentação completa

## 📄 Documentação

- [PRD.md](./PRD.md) - Documento completo de requisitos do produto
- [CHECKLIST.md](./CHECKLIST.md) - Lista detalhada de tarefas por fase
- [PROGRESS.md](./PROGRESS.md) - Relatório de progresso atual
- [VISUAL_GUIDE.md](./VISUAL_GUIDE.md) - Guia visual do design system

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'feat: Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

### Convenções de Commit
- `feat:` Nova funcionalidade
- `fix:` Correção de bug
- `docs:` Documentação
- `style:` Formatação
- `refactor:` Refatoração de código
- `test:` Testes
- `chore:` Manutenção

## 📝 Licença

Este projeto está sob licença privada.

---

**Desenvolvido com ❤️ usando React, TailwindCSS e muito café ☕**
