# 💊 Dashboard de Medicamentos Dispensados — EPS (2020-2021)

Tablero interactivo desarrollado con **Python + Dash + SQLite** para el análisis de medicamentos dispensados por una Entidad Promotora de Salud (EPS) durante los años 2020 y 2021.

---

## 📋 Descripción

Este proyecto fue desarrollado como parte de un taller de análisis de datos en el sector salud. El tablero permite a analistas y tomadores de decisiones explorar el comportamiento de la dispensación de medicamentos, identificar patrones de costo, analizar la cobertura del Plan de Beneficios en Salud (PBS) y evaluar grupos farmacológicos de interés como los **antidiabéticos**.

La fuente de datos es una base de datos **SQLite** (`medicamentos.db`) consultada en tiempo real mediante **SQL**, y la visualización se construye con **Plotly Dash**.

---

## 📊 Funcionalidades del Tablero

### Indicadores Clave (KPIs)
- 👥 **Número de personas** con al menos una dispensación (variable `id`)
- 📄 **Número de fórmulas distintas** dispensadas (variable `formula`)
- 💰 **Costo promedio** por fórmula dispensada

### Visualizaciones
- 📈 **Serie de tiempo** — Evolución del costo de dispensación mensual (2020-2021)
- 🏆 **Top 10 medicamentos** con mayor costo total acumulado
- 🟦 **PBS vs No-PBS** — Distribución de costos según cobertura del plan de beneficios
- 🗺️ **Por departamento** — Costo de medicamentos por municipio/regional CAF
- 🚚 **Por tipo de entrega** — Comparación de costos según modalidad de dispensación

### Filtros Interactivos
- 💊 Grupo farmacológico (`grupo_fco_economico`)
- 📅 Año y mes de dispensación
- 📍 Regional CAF

---

## 🔬 Análisis Especial: Antidiabéticos

El tablero incluye un análisis focalizado en el grupo farmacológico **ANTIDIABÉTICOS**, respondiendo:
- ¿Ha aumentado el costo de este grupo entre 2020 y 2021?
- ¿Cuál es el medicamento antidiabético más costoso?
- ¿Cuál es el costo promedio de una fórmula de este grupo?

---

## 🛠️ Stack Tecnológico

| Tecnología | Uso |
|---|---|
| `Python 3.10+` | Lenguaje principal |
| `Dash 2.x` | Framework del tablero web |
| `Plotly` | Visualizaciones interactivas |
| `Dash Bootstrap Components` | Diseño y layout responsivo |
| `Pandas` | Manipulación de datos |
| `SQLite3` | Motor de base de datos |
| `Gunicorn` | Servidor WSGI para despliegue |

---

## 📁 Estructura del Proyecto

```
├── app.py                  # Aplicación principal Dash
├── queries.py              # Consultas SQL organizadas por métrica
├── components/
│   ├── kpis.py             # Tarjetas de indicadores clave
│   ├── charts.py           # Componentes de gráficas
│   └── filters.py          # Controles de filtros interactivos
├── assets/
│   └── style.css           # Estilos personalizados
├── medicamentos.db         # Base de datos SQLite (no incluida en repo)
├── requirements.txt        # Dependencias del proyecto
└── README.md
```

> ⚠️ El archivo `medicamentos.db` no se incluye en el repositorio por tamaño y confidencialidad. Debe colocarse en la raíz del proyecto antes de ejecutar la aplicación.

---

## ⚙️ Instalación y Ejecución Local

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/dashboard-medicamentos-eps.git
cd dashboard-medicamentos-eps
```

### 2. Crear entorno virtual e instalar dependencias
```bash
python -m venv venv
source venv/bin/activate        # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Colocar la base de datos
Copia el archivo `medicamentos.db` en la raíz del proyecto.

### 4. Ejecutar la aplicación
```bash
python app.py
```

Abre tu navegador en `http://localhost:8050`

---

## 🚀 Despliegue

El tablero está desplegado en **Render.com** y es accesible públicamente en:

🔗 **[https://dashboard-medicamentos-eps.onrender.com](https://dashboard-medicamentos-eps.onrender.com)**

### Pasos para redesplegar
1. Hacer push a la rama `main` del repositorio
2. Render detecta los cambios automáticamente y redespliega
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn app:server`

---

## 📄 Documentación

El documento PDF con la explicación detallada de la lógica del tablero, descripción de los datos, análisis de antidiabéticos y el código completo como anexo se encuentra en:

📎 `docs/informe_tablero_medicamentos.pdf`

---

## 👤 Autor

Desarrollado como parte del taller de análisis de datos en salud — **Aseguradora EPS**.

---

## 📜 Licencia

Este proyecto es de uso académico. Los datos utilizados son confidenciales y no se distribuyen en este repositorio.
