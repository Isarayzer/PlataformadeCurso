# Checklist de Desenvolvimento - Plataforma de Cursos em Vídeo

## 📋 Legenda
- ⬜ Não iniciado
- 🟨 Em progresso
- ✅ Concluído
- ⏸️ Pausado/Bloqueado

---

## 🎯 FASE 1 - MVP (Mínimo Produto Viável)

### 1.1 Setup Inicial do Projeto
- ⬜ Criar estrutura de pastas do projeto
- ⬜ Configurar Git e repositório
- ⬜ Setup do ambiente de desenvolvimento
- ⬜ Instalar dependências principais (React, Node.js, etc.)
- ⬜ Configurar ESLint e Prettier
- ⬜ Configurar variáveis de ambiente (.env)

### 1.2 Configuração do Backend

#### 1.2.1 Servidor Base
- ⬜ Configurar servidor Express/FastAPI
- ⬜ Configurar CORS e middlewares básicos
- ⬜ Setup de estrutura de pastas (routes, controllers, models)
- ⬜ Configurar porta e ambiente de execução

#### 1.2.2 Banco de Dados
- ⬜ Escolher banco de dados (PostgreSQL ou SQLite)
- ⬜ Configurar conexão com banco de dados
- ⬜ Criar esquema inicial do banco
- ⬜ Configurar migrations
- ⬜ Setup de seeds (dados iniciais para testes)

#### 1.2.3 Sistema de Arquivos
- ⬜ Criar estrutura de pastas para armazenamento de vídeos
  - ⬜ `/uploads/videos/`
  - ⬜ `/uploads/thumbnails/`
  - ⬜ `/temp/` (arquivos temporários)
- ⬜ Implementar sistema de nomenclatura de arquivos
- ⬜ Configurar permissões de pasta

### 1.3 Sistema de Autenticação

- ⬜ Criar modelo de usuário (User)
- ⬜ Implementar registro de usuário
  - ⬜ Validação de email
  - ⬜ Hash de senha com bcrypt
  - ⬜ Endpoint POST /api/auth/register
- ⬜ Implementar login
  - ⬜ Validação de credenciais
  - ⬜ Geração de token JWT
  - ⬜ Endpoint POST /api/auth/login
- ⬜ Implementar logout
  - ⬜ Invalidação de token
  - ⬜ Endpoint POST /api/auth/logout
- ⬜ Middleware de autenticação (verificar JWT)
- ⬜ Rota protegida de teste
- ⬜ Recuperação de senha (opcional para MVP)

### 1.4 Gerenciamento de Vídeos

#### 1.4.1 Upload de Vídeos
- ⬜ Configurar Multer ou biblioteca similar
- ⬜ Implementar validação de formato (MP4, AVI, MOV, WebM)
- ⬜ Implementar validação de tamanho (máx 200MB)
- ⬜ Criar endpoint POST /api/videos/upload
- ⬜ Salvar vídeo no file system
- ⬜ Gerar thumbnail automático (FFmpeg)
- ⬜ Salvar metadados no banco de dados
- ⬜ Retornar informações do vídeo após upload
- ⬜ Tratamento de erros de upload

#### 1.4.2 Listagem e Visualização
- ⬜ Endpoint GET /api/videos (listar todos)
- ⬜ Endpoint GET /api/videos/:id (buscar por ID)
- ⬜ Endpoint para servir arquivo de vídeo (streaming)
- ⬜ Endpoint para servir thumbnail
- ⬜ Implementar paginação na listagem

#### 1.4.3 Edição de Metadados
- ⬜ Endpoint PUT /api/videos/:id
- ⬜ Atualizar título
- ⬜ Atualizar descrição
- ⬜ Atualizar tags
- ⬜ Upload de thumbnail customizado

#### 1.4.4 Exclusão de Vídeos
- ⬜ Endpoint DELETE /api/videos/:id
- ⬜ Remover arquivo do file system
- ⬜ Remover thumbnail
- ⬜ Remover registro do banco de dados
- ⬜ Validar que vídeo não está em uso em cursos

#### 1.4.5 Upload em Lote
- ⬜ Suporte para múltiplos arquivos simultâneos
- ⬜ Processamento assíncrono de lote
- ⬜ Retornar status de cada upload

### 1.5 Gerenciamento de Cursos

#### 1.5.1 Modelo de Dados
- ⬜ Criar modelo Course (Curso)
- ⬜ Criar modelo Module (Módulo/Seção)
- ⬜ Criar modelo Lesson (Aula)
- ⬜ Definir relacionamentos entre modelos
- ⬜ Criar migrations para tabelas

#### 1.5.2 CRUD de Cursos
- ⬜ Endpoint POST /api/courses (criar curso)
- ⬜ Endpoint GET /api/courses (listar cursos)
- ⬜ Endpoint GET /api/courses/:id (buscar curso específico)
- ⬜ Endpoint PUT /api/courses/:id (atualizar curso)
- ⬜ Endpoint DELETE /api/courses/:id (deletar curso)

#### 1.5.3 Estrutura Hierárquica
- ⬜ Adicionar módulos a um curso
  - ⬜ Endpoint POST /api/courses/:id/modules
- ⬜ Adicionar aulas a um módulo
  - ⬜ Endpoint POST /api/modules/:id/lessons
- ⬜ Vincular vídeos a aulas
- ⬜ Definir ordem de módulos e aulas
- ⬜ Implementar drag & drop para reordenação (backend)

#### 1.5.4 Gerenciamento de Módulos
- ⬜ Endpoint GET /api/modules/:id
- ⬜ Endpoint PUT /api/modules/:id (atualizar módulo)
- ⬜ Endpoint DELETE /api/modules/:id (deletar módulo)
- ⬜ Reordenar módulos dentro do curso

#### 1.5.5 Gerenciamento de Aulas
- ⬜ Endpoint GET /api/lessons/:id
- ⬜ Endpoint PUT /api/lessons/:id (atualizar aula)
- ⬜ Endpoint DELETE /api/lessons/:id (deletar aula)
- ⬜ Reordenar aulas dentro do módulo
- ⬜ Adicionar descrição e objetivos de aprendizado
- ⬜ Marcar aula como obrigatória/opcional

### 1.6 Sistema de Categorias

- ⬜ Criar modelo Category
- ⬜ Endpoint POST /api/categories (criar categoria)
- ⬜ Endpoint GET /api/categories (listar categorias)
- ⬜ Endpoint PUT /api/categories/:id (atualizar)
- ⬜ Endpoint DELETE /api/categories/:id (deletar)
- ⬜ Associar cursos a categorias
- ⬜ Filtrar cursos por categoria
- ⬜ Implementar subcategorias (opcional)
- ⬜ Sistema de tags para cursos

### 1.7 Frontend - Setup Inicial

#### 1.7.1 Configuração Base
- ✅ Criar projeto React/Next.js
- ✅ Configurar roteamento (React Router ou Next Router)
- ✅ Escolher e configurar UI library (Material-UI/Ant Design/TailwindCSS)
- ⬜ Configurar state management (Redux/Zustand)
- ⬜ Configurar axios ou fetch para API calls
- ⬜ Setup de autenticação no frontend (interceptors)

#### 1.7.2 Design System
- ✅ Definir paleta de cores
- ✅ Definir tipografia
- ✅ Criar componentes base (Button, Input, Card, etc.)
- ⬜ Configurar tema (modo claro/escuro - opcional)
- ✅ Criar layout principal

### 1.8 Frontend - Autenticação

- ✅ Página de Login
  - ✅ Formulário de login
  - ✅ Validação de campos
  - ⬜ Integração com API
  - ⬜ Armazenar token (localStorage/cookie)
- ✅ Página de Registro
  - ✅ Formulário de cadastro
  - ✅ Validação de email e senha
  - ⬜ Integração com API
- ⬜ Página de Logout
- ⬜ Rotas protegidas (redirect se não autenticado)
- ⬜ Exibir informações do usuário logado
- ⬜ Refresh automático de token

### 1.9 Frontend - Dashboard Principal

- ✅ Criar layout do dashboard
- ✅ Sidebar com navegação
- ✅ Header com informações do usuário
- ✅ Cards de estatísticas
  - ✅ Total de cursos
  - ✅ Total de vídeos
  - ✅ Total de categorias
- ✅ Lista de cursos recentes
- ✅ Ações rápidas (Criar Curso, Upload Vídeo)

### 1.10 Frontend - Biblioteca de Vídeos

#### 1.10.1 Listagem de Vídeos
- ⬜ Página de biblioteca de vídeos
- ⬜ Visualização em grid
- ⬜ Visualização em lista (alternativa)
- ⬜ Card de vídeo com thumbnail e informações
- ⬜ Paginação
- ⬜ Loading states
- ⬜ Empty states (quando não há vídeos)

#### 1.10.2 Upload de Vídeos
- ⬜ Modal/Página de upload
- ⬜ Drag & drop zone
- ⬜ Seleção de arquivos (input file)
- ⬜ Preview de arquivos selecionados
- ⬜ Barra de progresso de upload
- ⬜ Validação de formato e tamanho no frontend
- ⬜ Upload múltiplo (batch)
- ⬜ Feedback de sucesso/erro
- ⬜ Atualizar lista após upload

#### 1.10.3 Detalhes e Edição de Vídeo
- ⬜ Página/Modal de detalhes do vídeo
- ⬜ Player de vídeo integrado (Video.js/Plyr)
- ⬜ Formulário de edição de metadados
  - ⬜ Editar título
  - ⬜ Editar descrição
  - ⬜ Editar tags
- ⬜ Upload de thumbnail customizado
- ⬜ Exibir informações técnicas (duração, tamanho, resolução)
- ⬜ Botão de deletar vídeo (com confirmação)

#### 1.10.4 Busca e Filtros
- ⬜ Campo de busca por título
- ⬜ Filtro por tags
- ⬜ Ordenação (data, nome, duração)

### 1.11 Frontend - Gerenciamento de Cursos

#### 1.11.1 Listagem de Cursos
- ⬜ Página de cursos
- ⬜ Cards de curso com informações básicas
- ⬜ Filtro por categoria
- ⬜ Busca por nome
- ⬜ Botão "Criar Novo Curso"
- ⬜ Indicadores de status (rascunho, publicado)

#### 1.11.2 Criar/Editar Curso
- ⬜ Página de criação de curso
- ⬜ Formulário de informações básicas
  - ⬜ Título do curso
  - ⬜ Descrição
  - ⬜ Categoria
  - ⬜ Thumbnail do curso
- ⬜ Adicionar módulos
  - ⬜ Nome do módulo
  - ⬜ Descrição do módulo
- ⬜ Adicionar aulas aos módulos
  - ⬜ Selecionar vídeo da biblioteca
  - ⬜ Nome da aula
  - ⬜ Descrição da aula
  - ⬜ Objetivos de aprendizado
  - ⬜ Marcar como obrigatória/opcional
- ⬜ Drag & drop para reordenar módulos
- ⬜ Drag & drop para reordenar aulas
- ⬜ Preview da estrutura do curso
- ⬜ Salvar como rascunho
- ⬜ Publicar curso
- ⬜ Validações de formulário

#### 1.11.3 Visualização de Curso
- ⬜ Página de detalhes do curso
- ⬜ Exibir informações do curso
- ⬜ Exibir estrutura (módulos e aulas)
- ⬜ Navegação entre aulas
- ⬜ Player de vídeo da aula selecionada
- ⬜ Botões de editar/deletar curso

### 1.12 Frontend - Categorias

- ⬜ Página de gerenciamento de categorias
- ⬜ Listar todas as categorias
- ⬜ Criar nova categoria
- ⬜ Editar categoria
- ⬜ Deletar categoria (com validação)
- ⬜ Contagem de cursos por categoria

### 1.13 Player de Vídeo

- ⬜ Integrar biblioteca de player (Video.js ou Plyr)
- ⬜ Controles de reprodução (play, pause, volume)
- ⬜ Barra de progresso
- ⬜ Controle de velocidade (0.5x, 1x, 1.25x, 1.5x, 2x)
- ⬜ Fullscreen
- ⬜ Picture-in-picture (opcional)
- ⬜ Atalhos de teclado (espaço, setas)

### 1.14 Testes e Qualidade

- ⬜ Testes unitários do backend (principais endpoints)
- ⬜ Testes de integração (fluxos principais)
- ⬜ Testes do frontend (componentes críticos)
- ⬜ Testes de upload de vídeo
- ⬜ Validação de segurança básica
- ⬜ Tratamento de erros abrangente

### 1.15 Deploy e Documentação

- ⬜ Configurar ambiente de produção
- ⬜ Documentar API (Swagger/Postman)
- ⬜ README com instruções de instalação
- ⬜ Variáveis de ambiente documentadas
- ⬜ Scripts de build e deploy
- ⬜ Backup básico do banco de dados

---

## 🎯 FASE 2 - Recursos Avançados

### 2.1 Trilhas de Aprendizado

#### 2.1.1 Backend
- ⬜ Criar modelo LearningPath
- ⬜ Relacionar cursos a trilhas
- ⬜ Endpoint POST /api/learning-paths (criar trilha)
- ⬜ Endpoint GET /api/learning-paths (listar trilhas)
- ⬜ Endpoint GET /api/learning-paths/:id
- ⬜ Endpoint PUT /api/learning-paths/:id
- ⬜ Endpoint DELETE /api/learning-paths/:id
- ⬜ Definir ordem dos cursos na trilha
- ⬜ Estabelecer dependências entre cursos

#### 2.1.2 Frontend
- ⬜ Página de trilhas de aprendizado
- ⬜ Criar nova trilha
- ⬜ Adicionar cursos à trilha
- ⬜ Visualização em roadmap/timeline
- ⬜ Drag & drop para reordenar cursos
- ⬜ Definir pré-requisitos visualmente
- ⬜ Estimativa de tempo total da trilha
- ⬜ Editar/Deletar trilha

### 2.2 Marcadores Temporais em Vídeos

#### 2.2.1 Backend
- ⬜ Criar modelo Timestamp/Marker
- ⬜ Endpoint POST /api/videos/:id/markers (adicionar marcador)
- ⬜ Endpoint GET /api/videos/:id/markers (listar marcadores)
- ⬜ Endpoint PUT /api/markers/:id (atualizar marcador)
- ⬜ Endpoint DELETE /api/markers/:id (deletar marcador)

#### 2.2.2 Frontend
- ⬜ Interface para adicionar marcadores no player
- ⬜ Exibir marcadores na linha do tempo
- ⬜ Clicar em marcador para navegar
- ⬜ Editar nome e descrição do marcador
- ⬜ Deletar marcador

### 2.3 Sistema de Busca Avançado

- ⬜ Busca global (cursos, vídeos, categorias)
- ⬜ Autocomplete/sugestões
- ⬜ Filtros combinados
- ⬜ Ordenação por relevância
- ⬜ Histórico de buscas
- ⬜ Busca por conteúdo (integrar com transcrições - Fase 3)

### 2.4 Interface Melhorada

- ⬜ Animações e transições suaves
- ⬜ Feedback visual aprimorado
- ⬜ Tooltips e ajuda contextual
- ⬜ Responsividade tablet
- ⬜ Atalhos de teclado
- ⬜ Modo escuro (se não implementado na Fase 1)

### 2.5 Recursos Adicionais

- ⬜ Exportar estrutura de curso (JSON/PDF)
- ⬜ Importar estrutura de curso
- ⬜ Duplicar curso
- ⬜ Templates de curso
- ⬜ Estatísticas de uso (cursos mais acessados, vídeos, etc.)

---

## 🎯 FASE 3 - Integração de IA

### 3.1 Setup de IA

- ⬜ Criar conta OpenAI e obter API key
- ⬜ Configurar OpenAI SDK no backend
- ⬜ Criar serviço/módulo de IA
- ⬜ Implementar rate limiting para chamadas de IA
- ⬜ Sistema de filas para processamento assíncrono
- ⬜ Configurar Redis para gerenciar filas

### 3.2 Transcrição de Vídeos (Whisper)

#### 3.2.1 Backend
- ⬜ Extrair áudio do vídeo (FFmpeg)
- ⬜ Integrar Whisper API
- ⬜ Endpoint POST /api/videos/:id/transcribe
- ⬜ Armazenar transcrição no banco de dados
- ⬜ Processar em background (job queue)
- ⬜ Webhooks/polling para status de transcrição
- ⬜ Tratamento de erros da API
- ⬜ Retry logic

#### 3.2.2 Frontend
- ⬜ Botão para solicitar transcrição
- ⬜ Indicador de progresso de transcrição
- ⬜ Exibir transcrição completa
- ⬜ Editar transcrição manualmente
- ⬜ Buscar dentro da transcrição
- ⬜ Clicar em trecho para ir ao momento do vídeo

### 3.3 Geração de Resumos (GPT-4)

#### 3.3.1 Backend
- ⬜ Endpoint POST /api/videos/:id/generate-summary
- ⬜ Enviar transcrição para GPT-4
- ⬜ Prompt engineering para resumos de qualidade
- ⬜ Configurar parâmetros (temperatura, max_tokens)
- ⬜ Extrair tópicos principais
- ⬜ Identificar palavras-chave
- ⬜ Gerar timestamps dos tópicos
- ⬜ Armazenar resumo no banco de dados
- ⬜ Processar em background

#### 3.3.2 Frontend
- ⬜ Botão "Gerar Resumo com IA"
- ⬜ Modal de configuração (tamanho do resumo, foco)
- ⬜ Indicador de processamento
- ⬜ Exibir resumo gerado
  - ⬜ Resumo executivo
  - ⬜ Lista de tópicos
  - ⬜ Palavras-chave
  - ⬜ Timestamps clicáveis
- ⬜ Editar resumo manualmente
- ⬜ Salvar/Descartar resumo
- ⬜ Re-gerar resumo

### 3.4 Geração de Questionários (GPT-4)

#### 3.4.1 Backend
- ⬜ Endpoint POST /api/videos/:id/generate-quiz
- ⬜ Prompt engineering para geração de questões
- ⬜ Suporte a múltiplos tipos de questões
  - ⬜ Múltipla escolha
  - ⬜ Verdadeiro/Falso
  - ⬜ Questões discursivas
- ⬜ Configurar número de questões
- ⬜ Configurar nível de dificuldade
- ⬜ Gerar explicações para respostas
- ⬜ Armazenar questionário no banco de dados
- ⬜ Processar em background

#### 3.4.2 Frontend
- ⬜ Botão "Gerar Questionário com IA"
- ⬜ Modal de configuração
  - ⬜ Número de questões (slider)
  - ⬜ Tipo de questões (checkboxes)
  - ⬜ Nível de dificuldade (select)
- ⬜ Indicador de processamento
- ⬜ Exibir questionário gerado
  - ⬜ Lista de questões
  - ⬜ Alternativas (para múltipla escolha)
  - ⬜ Resposta correta
  - ⬜ Explicação
- ⬜ Editar questões manualmente
  - ⬜ Editar enunciado
  - ⬜ Editar alternativas
  - ⬜ Editar resposta correta
  - ⬜ Editar explicação
- ⬜ Adicionar/Remover questões
- ⬜ Reordenar questões (drag & drop)
- ⬜ Salvar questionário
- ⬜ Re-gerar questionário

### 3.5 Associação de Conteúdo IA às Aulas

- ⬜ Vincular resumos a aulas
- ⬜ Vincular questionários a aulas
- ⬜ Exibir resumo na página da aula
- ⬜ Disponibilizar questionário para alunos (se houver área de aluno)
- ⬜ Download de resumos (PDF/TXT)
- ⬜ Histórico de versões de resumos/questionários

### 3.6 Otimizações e Melhorias de IA

- ⬜ Cache de transcrições
- ⬜ Cache de resumos
- ⬜ Processamento em lote (múltiplos vídeos)
- ⬜ Estimativa de custo de IA antes de processar
- ⬜ Limite de uso de IA por usuário (opcional)
- ⬜ Feedback loop (avaliar qualidade dos resultados)
- ⬜ Melhorar prompts baseado em feedback

---

## 🎯 FASE 4 - Otimização e Polimento

### 4.1 Performance

- ⬜ Otimizar queries do banco de dados
- ⬜ Implementar índices apropriados
- ⬜ Lazy loading de vídeos
- ⬜ Paginação server-side
- ⬜ Compressão de respostas (gzip)
- ⬜ Otimização de imagens (thumbnails)
- ⬜ Code splitting no frontend
- ⬜ Bundle size optimization

### 4.2 Analytics e Monitoramento

- ⬜ Sistema de logs estruturado
- ⬜ Monitoramento de erros (Sentry ou similar)
- ⬜ Métricas de uso
  - ⬜ Cursos criados
  - ⬜ Vídeos uploadados
  - ⬜ Uso de IA (transcrições, resumos, questionários)
- ⬜ Dashboard de analytics
- ⬜ Alertas para erros críticos

### 4.3 Backup e Segurança

- ⬜ Sistema de backup automático do banco de dados
- ⬜ Backup de vídeos (opcional, devido ao tamanho)
- ⬜ Restauração de backup (procedimento documentado)
- ⬜ Auditoria de segurança
- ⬜ Testes de penetração básicos
- ⬜ HTTPS obrigatório em produção
- ⬜ Headers de segurança (CSP, HSTS, etc.)

### 4.4 Documentação

- ⬜ Documentação de API completa (Swagger)
- ⬜ Guia de usuário (como usar a plataforma)
- ⬜ Documentação técnica (arquitetura)
- ⬜ Troubleshooting guide
- ⬜ FAQ
- ⬜ Vídeos tutoriais (opcional)

### 4.5 Testes Finais

- ⬜ Testes de carga (stress testing)
- ⬜ Testes de usabilidade
- ⬜ Testes cross-browser
- ⬜ Testes de acessibilidade (WCAG básico)
- ⬜ QA completo de todos os fluxos

### 4.6 Preparação para Produção

- ⬜ Configurar ambiente de produção
- ⬜ SSL/TLS configurado
- ⬜ Domínio configurado
- ⬜ Email transacional configurado (reset senha, etc.)
- ⬜ Backups automáticos configurados
- ⬜ Monitoramento configurado
- ⬜ Plano de rollback
- ⬜ Runbook de deploy

---

## 🔮 Funcionalidades Futuras (Backlog)

### Recursos de Usuário Avançados
- ⬜ Sistema de permissões (admin, editor, viewer)
- ⬜ Múltiplos usuários/organizações
- ⬜ Colaboração em cursos
- ⬜ Comentários e anotações

### Recursos para Alunos
- ⬜ Portal do aluno
- ⬜ Matrícula em cursos
- ⬜ Progresso de aulas
- ⬜ Certificados de conclusão
- ⬜ Realizar questionários
- ⬜ Nota e avaliação

### Recursos de Conteúdo
- ⬜ Suporte a outros tipos de mídia (PDFs, slides, áudio)
- ⬜ Aulas ao vivo (live streaming)
- ⬜ Exercícios práticos
- ⬜ Projetos finais

### IA Avançada
- ⬜ Detecção de slides importantes
- ⬜ Geração de flashcards
- ⬜ Sugestões de material complementar
- ⬜ Análise de engajamento
- ⬜ Legendas automáticas multilíngue

### Integrações
- ⬜ Integração com Zoom/Google Meet
- ⬜ Integração com LMS (Moodle, Canvas)
- ⬜ Integração com sistemas de pagamento
- ⬜ API pública para integrações

### Migração para Cloud
- ⬜ Migrar armazenamento para AWS S3/Google Cloud
- ⬜ Implementar CDN
- ⬜ Transcodificação de vídeo (múltiplas resoluções)
- ⬜ Streaming adaptativo (HLS/DASH)

---

## 📊 Progresso Geral

### Fase 1 - MVP: ⬜ 0% concluído (0/115 tarefas)
### Fase 2 - Recursos Avançados: ⬜ 0% concluído (0/31 tarefas)
### Fase 3 - IA: ⬜ 0% concluído (0/49 tarefas)
### Fase 4 - Otimização: ⬜ 0% concluído (0/30 tarefas)

**TOTAL GERAL: ⬜ 0% concluído (0/225 tarefas)**

---

*Última atualização: 2026-01-18*
