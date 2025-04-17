#FinOps Tags – Repositorio de gestión de etiquetas en la nube

Este repositorio contiene herramientas, scripts, documentación y automatizaciones para la **gestión de tags (etiquetas)** en entornos **multinube (AWS y Azure)**, alineados con prácticas de FinOps y gobernanza corporativa.

---

## 🎯 Objetivo

Facilitar la estandarización, validación y aplicación de etiquetas que permiten:

- Imputar correctamente los costos por centro de costo, aplicación y entorno.
- Automatizar controles de cumplimiento.
- Mejorar la visibilidad financiera de los recursos cloud.
- Empoderar a los equipos de desarrollo con herramientas fáciles de usar.

---

## 📁 Contenido del repositorio

| Carpeta | Descripción |
|--------|-------------|
| `scripts/` | Scripts en PowerShell, Bash y Python para aplicar, validar o migrar tags |
| `documentacion/` | Guías y estándares internos de etiquetado, políticas y formatos recomendados |
| `dashboards/` | Plantillas de reportes de tags, dashboards de cumplimiento y visualizaciones |
| `azure-function-tags/` | Azure Function en Python que expone un diccionario de tags válidos vía HTTP API |
| `README.md` | Este archivo ✍️ |

---

## 🧩 Componentes destacados

### 🔹 Azure Function – Diccionario de Tags

Función HTTP desplegable en Azure para que cualquier usuario o automatización consulte los tags válidos y sus valores permitidos.

➡️ [Ver función](./azure-function-tags/README.md)

---

## ✅ Tags estándar utilizados

Algunos de los tags corporativos definidos incluyen:

- `owner`: Sector responsable
- `app`: Aplicación o producto
- `costcenter`: Código de centro de costo
- `environment`: dev / test / prod
- `referente`: Responsable técnico o funcional
- `project`: Proyecto asociado (opcional)

> Para el listado completo consultá el diccionario en el Azure Function o el archivo `tags.json`.

---

## 🧠 Buenas prácticas

- Validar tags antes del despliegue (con scripts o políticas)
- Usar tags consistentes en todas las cuentas y suscripciones
- Automatizar la aplicación de tags por entorno, grupo de recursos o pipeline

---

## 🛠️ Requisitos

- Git
- VS Code o CLI
- Azure Functions Core Tools (para ejecutar localmente)
- Acceso a suscripción en Azure / cuenta en AWS

---

## 🤝 Contribuciones

¿Querés proponer una mejora? ¿Agregar nuevos tags?  
Abrí un **Issue** o **Pull Request**, ¡toda contribución es bienvenida!

---

## 🛡️ Licencia

Este proyecto se encuentra bajo licencia MIT.

