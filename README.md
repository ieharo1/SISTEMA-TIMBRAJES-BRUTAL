# 🚨 Sistema de Timbrajes Brutal

<p align="center">
  <img src="https://img.icons8.com/color/200/000000/time-machine.png" alt="Timbrajes Logo" width="200"/>
</p>

---

## 📱 Descripción

**Sistema de Timbrajes Brutal** es una plataforma empresarial desarrollada con **Django + PostgreSQL + Docker** para controlar asistencia de personal en múltiples oficinas y ubicaciones.

Incluye:
- timbraje de entrada y salida,
- cálculo automático de horas trabajadas,
- cálculo de horas extras,
- cálculo de pago regular y pago extra,
- panel de reportería con filtros,
- exportación CSV.

> Diseñado para ser escalable, responsive y reutilizable en cualquier oficina o sede.

---

## ✨ Características

### Funcionalidades Implementadas ✅

- ✅ **Autenticación** con login/logout de Django
- ✅ **Multi-oficina** para operar en diferentes ciudades/países
- ✅ **Gestión de personal** (código, cargo, tarifa por hora, estado)
- ✅ **Gestión de turnos** con break configurable
- ✅ **Timbraje de entrada/salida** por empleado
- ✅ **Control de timbraje abierto** (evita doble entrada simultánea)
- ✅ **Cálculo de horas trabajadas** por registro
- ✅ **Cálculo de horas extras** por umbral de turno
- ✅ **Cálculo de pago regular + extra (1.5x)**
- ✅ **Dashboard ejecutivo** con KPIs rápidos
- ✅ **Reportería por fecha y oficina**
- ✅ **Exportación CSV** de reportes
- ✅ **UI 100% Bootstrap 5** (sin CSS personalizado)
- ✅ **Docker + Docker Compose** para despliegue rápido
- ✅ **Datos semilla automáticos** para demo inmediata

### Próximamente 🔄

- 🔄 API REST con DRF
- 🔄 Geolocalización / geocercas por oficina
- 🔄 App móvil para timbraje remoto
- 🔄 Módulo de aprobaciones de horas extras
- 🔄 Integración con biométrico y QR

---

## 🛠️ Stack Tecnológico

| Componente | Tecnología | Versión |
|------------|------------|---------|
| Backend | Python | 3.12 |
| Framework | Django | 5.1.7 |
| Base de Datos | PostgreSQL | 16 |
| Servidor WSGI | Gunicorn | 23.0.0 |
| Frontend | Bootstrap | 5.3.3 (CDN) |
| Contenedores | Docker / Compose | latest |

---

## 📁 Estructura del Proyecto

```bash
telegram-bot-test-python/
├── attendance/
│   ├── management/commands/seed_data.py
│   ├── migrations/0001_initial.py
│   ├── templates/
│   │   ├── registration/login.html
│   │   └── attendance/
│   │       ├── dashboard.html
│   │       ├── employee_form.html
│   │       ├── employee_list.html
│   │       └── reports.html
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh
├── requirements.txt
├── manage.py
└── README.md
```

---

## 🚀 Cómo Ejecutar el Proyecto

### 1. Clonar el Repositorio
```bash
git clone <tu-repo>
cd telegram-bot-test-python
```

### 2. Ejecutar con Docker
```bash
# Construir y levantar servicios
docker compose up --build
```

La app quedará disponible en:
- **http://localhost:8000**

### 3. Credenciales Demo

- **Admin:**
  - usuario: `admin`
  - contraseña: `admin123`

- **Empleado demo:**
  - usuario: `empleado.demo`
  - contraseña: `demo12345`

---

## 📊 Módulos del Sistema

### 1) Dashboard
- Estado de timbraje actual
- Botón para entrada/salida
- Últimos registros
- Totales rápidos de horas y horas extra

### 2) Personal
- Listado de empleados
- Alta de nuevos empleados
- Asociación con oficina y tarifa/hora

### 3) Reportería
- Filtro por rango de fechas
- Filtro por oficina
- KPIs: horas, extras, pago regular y extra
- Exportación CSV para auditoría/contabilidad

---

## 🎯 Cálculo de Horas y Horas Extras

```text
worked_minutes = (clock_out - clock_in) - break_minutes
overtime_minutes = max(worked_minutes - overtime_threshold_minutes, 0)

regular_pay = horas_regulares * tarifa_hora
overtime_pay = horas_extra * tarifa_hora * 1.5
```

---

## 🔐 Escalabilidad

- Estructura por entidades (`Office`, `Employee`, `Shift`, `AttendanceRecord`)
- Multi sede/país habilitado
- Fácil integración con API y módulos enterprise
- Lista para desplegar en VPS, cloud o Kubernetes

---

## 📦 Generar ZIP del Proyecto

> Nota: el archivo `.zip` no se incluye en el repositorio para mantener compatibilidad con revisores de texto/diff.

Ejecuta este comando desde la raíz:

```bash
zip -r sistema-timbrajes-brutal.zip . -x ".git/*" "__pycache__/*" "*.pyc" ".venv/*"
```

---

## 👨‍💻 Desarrollado por Isaac Esteban Haro Torres

**Ingeniero en Sistemas · Full Stack Developer · Automatización · Data**

### 📞 Contacto

- 📧 **Email:** zackharo1@gmail.com
- 📱 **WhatsApp:** [+593 988055517](https://wa.me/593988055517)
- 💻 **GitHub:** [ieharo1](https://github.com/ieharo1)
- 🌐 **Portafolio:** [ieharo1.github.io](https://ieharo1.github.io/portafolio-isaac.haro/)

---

## 📄 Licencia

© 2026 Isaac Esteban Haro Torres - Todos los derechos reservados.

---

⭐ Si te gustó el proyecto, ¡dale una estrella en GitHub!
