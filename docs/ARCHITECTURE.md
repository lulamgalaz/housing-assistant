# Scout Friend – Architecture

Version: 1.0

---

# Filosofía

Scout Friend NO es un scraper.

Scout Friend es un motor de búsqueda inmobiliaria.

Los scrapers son únicamente conectores hacia distintas fuentes de información.

Toda la aplicación debe poder cambiar de ciudad, país o portal sin modificar la interfaz.

---

# Flujo general

Usuario

↓

Perfil de búsqueda

↓

Search Service

↓

Scraper Manager

↓

Scrapers

↓

Normalizer

↓

Database

↓

Matcher

↓

Ranking

↓

Streamlit

---

# Capas

## app/

Únicamente interfaz.

Nunca:

- scrapea
- calcula score
- guarda datos

Solo muestra información y recibe acciones del usuario.

---

## scrapers/

Responsabilidad:

Obtener anuncios.

Todos los scrapers deben devolver exactamente el mismo formato.

Nunca escriben en la base.

Nunca calculan score.

Nunca conocen Streamlit.

---

## services/

Contiene toda la lógica del negocio.

Ejemplos:

- search_service
- listing_service
- matcher
- score
- preference_service

Toda decisión inteligente vive aquí.

---

## database/

Persistencia.

No contiene lógica de negocio.

---

## config/

Configuración del sistema.

No contiene lógica.

---

# Modelo de datos

Listing

↓

Propiedad individual.

SearchProfile

↓

Conjunto de preferencias de un usuario.

SearchPlan

↓

Una estrategia concreta de búsqueda.

Ejemplo:

2 habitaciones
1200 €
11 meses

Recommendation

↓

Resultado del análisis entre un Listing y un SearchProfile.

---

# Responsabilidades

Streamlit

↓

Mostrar

Search Service

↓

Coordinar búsquedas

Scraper Manager

↓

Ejecutar scrapers

Scraper

↓

Extraer datos

Normalizer

↓

Unificar datos

Listing Service

↓

Guardar anuncios

Matcher

↓

Comparar anuncio vs perfil

Score

↓

Calcular puntuación

---

# Regla principal

Cada archivo debe tener una única responsabilidad.
