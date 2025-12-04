
# HouseMusic Platform

HouseMusic is a multi-channel marketing automation platform designed to manage advertising campaigns, synchronize social media publications, and centralize customer communication. It includes an API backend built with FastAPI, a frontend application built with Next.js, and a background worker system for task scheduling and message processing.

This repository contains the full project architecture, including backend, frontend, and infrastructure configuration.

---

## Overview

HouseMusic provides a unified solution for:

- Creating and scheduling marketing campaigns.
- Publishing content across multiple social accounts (Instagram, Facebook, Gmail, etc.).
- Managing social media and messaging webhooks.
- Processing automated replies through a state-based or AI-enhanced bot engine.
- Executing background jobs for scheduled tasks, message handling, and email delivery.

The system is structured to support future growth, modular development, and scalable deployment.

---

## Project Structure

```
HouseMusic/
├─ backend/
│  ├─ app/
│  │  ├─ main.py
│  │  ├─ core/                # Configuration and application settings
│  │  ├─ db/                  # Database session and base classes
│  │  ├─ models/              # SQLAlchemy ORM models
│  │  ├─ schemas/             # Pydantic validation schemas
│  │  ├─ api/v1/              # Versioned API routes
│  │  ├─ services/            # Business logic and integrations
│  │  ├─ workers/             # Celery tasks and background processing
│  │  └─ utils/               # Utility functions
│  ├─ alembic/                # Database migrations
│  └─ pyproject.toml
│
├─ frontend/
│  └─ src/
│     ├─ app/                 # Next.js app directory
│     ├─ components/          # UI components
│     ├─ lib/                 # API client utilities
│     └─ styles/              # Global styles
│
└─ infra/
   └─ docker-compose.yml       # Service orchestration (API, DB, workers, etc.)
```

---

## Key Components

### Backend (FastAPI)

The backend provides:

- REST API for authentication, campaign management, social account integration, and message handling.
- Webhook endpoints for social media platforms.
- A conversation engine for automated responses using state tracking.
- Celery background workers for scheduling, publishing, and email processing.
- PostgreSQL persistence with SQLAlchemy ORM and Alembic migrations.

### Frontend (Next.js)

The frontend includes:

- Dashboard for campaign creation and monitoring.
- Social account connection interface.
- Views for managing publications, schedules, and message history.
- TypeScript-based architecture with reusable components.

### Workers (Celery)

Celery workers are used for:

- Executing scheduled campaign publications.
- Handling message replies and webhook events.
- Processing email deliveries and error recovery.

---

## Technologies Used

- Python 3.x
- FastAPI
- SQLAlchemy
- Alembic
- Celery
- Redis or RabbitMQ (as Celery broker)
- PostgreSQL
- Next.js (React + TypeScript)
- Docker / Docker Compose

---

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.10+
- Node.js 18+

### Initial Setup

1. Clone the repository:
   ```
   git clone <repository-url>
   cd HouseMusic
   ```

2. Set up environment variables using the template in `infra/env.example`.

3. Start the stack:
   ```
   docker-compose up -d
   ```

4. Apply migrations:
   ```
   alembic upgrade head
   ```

5. Start the frontend development server:
   ```
   cd frontend
   npm install
   npm run dev
   ```

---

## Development Workflow

HouseMusic follows a GitFlow-based branching model:

- main – stable production-ready code.
- develop – integration branch for ongoing development.
- feature/* – feature-specific branches.
- hotfix/* – urgent fixes based on main.

All features should be developed in isolated branches and merged into develop through pull requests.

---

## Future Extensions

The architecture is designed to support:

- Additional messaging platforms (WhatsApp, Telegram, SMS).
- AI-based conversation routing and intent detection.
- Advanced analytics dashboards for advertising performance.
- Integration with CRMs and third-party marketing tools.
- Multi-tenant expanded support for SaaS deployments.

---

## License

This project is proprietary and confidential. Unauthorized copying or distribution of any part of this repository is prohibited.
