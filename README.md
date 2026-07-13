# 🔧 NexoPro Platform

ERP multi-sector con núcleo de facturación común y módulos sectoriales especializados.

## 🏗️ Arquitectura

```
nexopro-platform/
├── 📁 core/              # NÚCLEO COMÚN (facturación, contactos, artículos, auth)
│   ├── backend/          # FastAPI + MongoDB
│   └── frontend/         # React + Tailwind + shadcn/ui
├── 📁 sectors/           # MÓDULOS SECTORIALES
│   └── taller/           # Taller mecánico (Fase 1-4)
│   └── hosteleria/       # Restaurantes/bares (futuro)
│   └── retail/           # Tiendas/comercio (futuro)
│   └── servicios/        # Servicios profesionales (futuro)
└── 📁 shared/            # Utilidades compartidas
```

## 🚀 Quick Start

### Backend

```bash
# 1. Clonar
git clone https://github.com/filatecnicasl-sketch/NEXOPRO-KIMI.git
cd NEXOPRO-KIMI

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o: venv\Scripts\activate  # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus valores (MONGO_URL, JWT_SECRET, etc.)

# 5. Iniciar servidor
uvicorn core.backend.main:app --reload --port 8000
```

### Frontend

```bash
cd core/frontend
npm install
npm start
```

## 📋 Features del Core

- ✅ CRUD Clientes/Proveedores
- ✅ Autenticación JWT (admin)
- ✅ Sistema de licencias multi-tenant
- ✅ Verifactu (huella encadenada + QR)
- ✅ Facturae 3.2.2 (FACe)
- ✅ Extracción IA de PDFs
- ✅ Notificaciones Email/WhatsApp

## 📋 Features del Sector Taller

- ✅ Vehículos + Órdenes de trabajo
- ✅ Peritajes + Compañías de seguros
- ✅ Citas + Recordatorios automáticos
- ✅ Vehículos de cortesía
- ✅ Hoja de entrada PDF (ASORECA)
- ✅ Parte de trabajo PDF
- ✅ Fotos por QR + Firma digital

## 🛡️ Seguridad

- JWT con bcrypt
- Rate limiting (pendiente)
- Validación de licencias por tenant
- Secretos enmascarados en API

## 📄 Licencia

MIT
