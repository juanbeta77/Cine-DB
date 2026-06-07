# Documentación Técnica - Cine-DB

## Tabla de Contenidos

- [Descripción General](#descripción-general)
- [Diseño de la Base de Datos](#diseño-de-la-base-de-datos)
- [Colecciones](#colecciones)
- [Funcionalidades del Sistema](#funcionalidades-del-sistema)
- [Interfaz Gráfica (Tkinter)](#interfaz-gráfica-tkinter)
- [Flujo de Trabajo del Sistema](#flujo-de-trabajo-del-sistema)
- [Dependencias del Sistema](#dependencias-del-sistema)
- [Archivos del Proyecto](#archivos-del-proyecto)
- [Notas Importantes](#notas-importantes)

## Descripción General
<details>
<summary> Ver Descripción General</summary>

Cine-DB es un sistema de gestión de cine desarrollado en Python con interfaz gráfica Tkinter y base de datos MongoDB. El sistema permite la gestión de películas, funciones, usuarios y ventas de entradas.

### Tecnología
- **Motor de Base de Datos**: MongoDB
- **Conexión**: mongodb://localhost:27017/
- **Nombre de la Base de Datos**: Cine-DB
- **Lenguaje del backend**: Python

</details>

---

## Diseño de la Base de Datos
<details>
<summary> Ver Diseño de la Base de Datos</summary>

### Colecciones
<details>
<summary> Ver Colecciones</summary>

#### 1. Colección: `usuarios`
Almacena la información de los usuarios del sistema.

**Estructura del documento:**
```json
{
  "_id": ObjectId,
  "documento": String,
  "nombre": String,
  "correo": String,
  "telefono": String,
  "password": String,
  "preferencias": Array,
  "historial_compras": Array
}
```

**Campos:**
- `_id`: Identificador único del usuario (autogenerado por MongoDB)
- `documento`: Documento de identidad del usuario (único)
- `nombre`: Nombre completo del usuario
- `correo`: Correo electrónico del usuario (único, case-insensitive)
- `telefono`: Número de teléfono
- `password`: Contraseña del usuario
- `preferencias`: Array de preferencias del usuario
- `historial_compras`: Array con el historial de compras del usuario


**Estructura de historial_compras:**
```json
{
  "entrada_id": String,
  "pelicula": String,
  "cantidad": Integer,
  "total": Float,
  "fecha": DateTime
}
```


**Campos:**
- `entrada_id`: Identificador único de la entrada (autogenerado)
- `pelicula`: Título de la película comprada
- `cantidad`: Cantidad de entradas compradas
- `total`: Total a pagar por las entradas
- `fecha`: Fecha y hora de la compra

---

#### 2. Colección: `Peliculas`
Almacena el catálogo de películas disponibles en el cine.

**Estructura del documento:**
```json
{
  "_id": ObjectId,
  "titulo": String,
  "genero": String,
  "duracion": Integer,
  "clasificacion": String,
  "disponible": Boolean
}
```

**Campos:**
- `_id`: Identificador único de la película (autogenerado)
- `titulo`: Título de la película (único, case-insensitive)
- `genero`: Género de la película
- `duracion`: Duración en minutos (entero)
- `clasificacion`: Clasificación de la película
- `disponible`: Estado de disponibilidad (true/false)

---

#### 3. Colección: `Funciones`
Almacena las funciones programadas para cada película.

**Estructura del documento:**
```json
{
  "_id": ObjectId,
  "pelicula_id": String,
  "sala": Integer,
  "horario": String,
  "asientos_disponibles": Integer,
  "precio": Float
}
```

**Campos:**
- `_id`: Identificador único de la función (autogenerado)
- `pelicula_id`: Referencia al ID de la película en la colección Peliculas
- `sala`: Número de sala (entero)
- `horario`: Horario de la función (formato string)
- `asientos_disponibles`: Cantidad de asientos disponibles
- `precio`: Precio de la entrada (float)

**Restricciones:**
- No puede existir una función duplicada para la misma película, sala y horario

---

#### 4. Colección: `Entradas`
Almacena las entradas vendidas a los usuarios.

**Estructura del documento:**
```json
{
  "_id": ObjectId,
  "usuario_id": String,
  "usuario_nombre": String,
  "funcion_id": String,
  "pelicula_titulo": String,
  "horario": String,
  "sala": Integer,
  "cantidad": Integer,
  "total": Float,
  "fecha_compra": DateTime
}
```

**Campos:**
- `_id`: Identificador único de la entrada (autogenerado)
- `usuario_id`: Referencia al ID del usuario
- `usuario_nombre`: Nombre del usuario (denormalizado para consulta)
- `funcion_id`: Referencia al ID de la función
- `pelicula_titulo`: Título de la película (denormalizado)
- `horario`: Horario de la función
- `sala`: Número de sala
- `cantidad`: Cantidad de entradas compradas
- `total`: Precio total de la compra
- `fecha_compra`: Fecha y hora de la compra

---
</details>
</details>

## Funcionalidades del Sistema
<details>
<summary> Ver Funcionalidades del Sistema</summary>

### Módulo de Usuarios (Usuarios.py)

#### 1. Crear Usuario
- **Función**: `crear_usuario(documento, nombre, correo, telefono, password)`
- **Descripción**: Registra un nuevo usuario en el sistema
- **Validaciones**:
  - Verifica que no exista un usuario con el mismo documento
  - Verifica que no exista un usuario con el mismo correo (case-insensitive)
- **Retorno**: Mensaje de éxito o error

**Ejemplo de la interfaz - Crear Usuario:**

<img src="capturas/admin/Crear Usuario a-.png" width="600">

#### 2. Mostrar Usuarios
- **Función**: `mostrar_usuarios(return_list=False)`
- **Descripción**: Lista todos los usuarios del sistema
- **Parámetro opcional**: `return_list` - Si es True, retorna la lista en lugar de imprimirla
- **Nota**: Excluye el campo password de la visualización

<img src="capturas/admin/Mostrar Usuario a-.png" width="800">

#### 3. Actualizar Usuario
- **Función**: `actualizar_usuario_por_documento(documento, nuevo_telefono, nuevo_correo)`
- **Descripción**: Actualiza teléfono y/o correo de un usuario
- **Parámetros**: Documento de identidad y nuevos valores (opcionales)
- **Retorno**: Mensaje de éxito o error

#### 4. Eliminar Usuario
- **Función**: `eliminar_usuario_por_documento(documento)`
- **Descripción**: Elimina un usuario por su documento de identidad
- **Retorno**: Mensaje de éxito o error

#### 5. Obtener Historial de Usuario
- **Función**: `obtener_historial_usuario(user_id)`
- **Descripción**: Obtiene el historial de compras de un usuario
- **Parámetro**: ID del usuario
- **Retorno**: Array con el historial de compras

**Ejemplo - Historial de Usuario:**

<img src="capturas/usuarios/Obtener Historial de Usuario u-.png" width="800">

#### 6. Login de Usuario
- **Función**: `login_usuario(correo, password)`
- **Descripción**: Autentica un usuario en el sistema
- **Parámetros**: Correo y contraseña
- **Retorno**: Objeto de usuario si las credenciales son correctas, None en caso contrario

---

### Módulo de Películas (Peliculas.py)

#### 1. Agregar Película
- **Función**: `agregar_pelicula(titulo, genero, duracion, clasificacion)`
- **Descripción**: Registra una nueva película en el catálogo
- **Validaciones**:
  - Verifica que no exista una película con el mismo título (case-insensitive)
  - Valida que la duración sea un número entero
- **Retorno**: Mensaje de éxito o error

**Ejemplo de la interfaz - Agregar Película:**

<img src="capturas/admin/Agregar pelicula a-.png" width="500">

#### 2. Mostrar Películas
- **Función**: `mostrar_peliculas(return_list=False)`
- **Descripción**: Lista todas las películas del catálogo
- **Parámetro opcional**: `return_list` - Si es True, retorna la lista en lugar de imprimirla

#### 3. Actualizar Película
- **Función**: `actualizar_pelicula_por_id(id_o_titulo, nuevo_genero, nuevo_titulo=None)`
- **Descripción**: Actualiza género y/o título de una película
- **Parámetros**: ID o título de la película, nuevo género, nuevo título (opcional)
- **Retorno**: Mensaje de éxito o error

#### 4. Eliminar Película
- **Función**: `eliminar_pelicula_por_id(id_o_titulo)`
- **Descripción**: Elimina una película por ID o título
- **Parámetros**: ID (24 caracteres) o título de la película
- **Retorno**: Mensaje de éxito o error

#### 5. Obtener Película por ID
- **Función**: `get_pelicula_by_id(pelicula_id)`
- **Descripción**: Obtiene una película específica por su ID
- **Retorno**: Objeto de película o None

---

### Módulo de Funciones (Funciones.py)

#### 1. Agregar Función
- **Función**: `agregar_funcion(titulo_pelicula, sala, horario, asientos, precio)`
- **Descripción**: Programa una nueva función de una película
- **Validaciones**:
  - Verifica que la película exista en la base de datos
  - Valida que sala, asientos y precio sean números válidos
  - Verifica que no exista una función duplicada (misma película, sala y horario)
- **Retorno**: Mensaje de éxito o error

**Ejemplo de la interfaz - Agregar Función:**

<img src="capturas/admin/Agregar funcion a-.png" width="500">

#### 2. Mostrar Funciones
- **Función**: `mostrar_funciones(return_list=False)`
- **Descripción**: Lista todas las funciones programadas
- **Característica**: Incluye el título de la película (join con colección Peliculas)
- **Parámetro opcional**: `return_list` - Si es True, retorna la lista en lugar de imprimirla

<img src="capturas/admin/mostrar funcones a-.png" width="800">

#### 3. Obtener Funciones Disponibles
- **Función**: `get_funciones_disponibles()`
- **Descripción**: Obtiene todas las funciones con asientos disponibles
- **Retorno**: Lista de funciones con asientos_disponibles > 0

**Ejemplo - Funciones disponibles en la vista de usuario:**

<img src="capturas/usuarios/Obtener Funciones Disponibles u-.png" width="700">

#### 4. Obtener Función por ID
- **Función**: `get_funcion_by_id(funcion_id)`
- **Descripción**: Obtiene una función específica por su ID
- **Retorno**: Objeto de función o None

---

### Módulo de Entradas (Entradas.py)

#### 1. Comprar Entrada
- **Función**: `comprar_entrada(user_id, funcion_id, cantidad, precio_total)`
- **Descripción**: Procesa la compra de entradas para una función
- **Validaciones**:
  - Valida formato de IDs
  - Verifica que la función exista
  - Verifica disponibilidad de asientos
- **Proceso**:
  1. Crea el documento de entrada
  2. Agrega la compra al historial del usuario
  3. Actualiza los asientos disponibles de la función
- **Retorno**: "exito" o mensaje de error

#### 2. Mostrar Entradas
- **Función**: `mostrar_entradas(return_list=False)`
- **Descripción**: Lista todas las entradas vendidas
- **Parámetro opcional**: `return_list` - Si es True, retorna la lista en lugar de imprimirla

#### 3. Obtener Historial de Usuario (Entradas)
- **Función**: `obtener_historial_usuario(user_id)`
- **Descripción**: Obtiene el historial de compras formateado de un usuario
- **Características**:
  - Formatea las fechas a DD/MM/YYYY HH:MM
  - Ordena las compras de más reciente a más antigua
  - Incluye campos: id_compra, película, sala, horario, cantidad, total, fecha_compra
- **Retorno**: Array con el historial formateado

---
</details>

## Interfaz Gráfica (Tkinter)
<details>
<summary>Ver Interfaz Gráfica (Tkinter)</summary>

### Estructura de Vistas

#### 1. Ventana Principal (main_window.py)
- **Clase**: `App`
- **Descripción**: Ventana principal de la aplicación
- **Dimensiones**: 800x600
- **Funcionalidad**: Gestiona el cambio entre diferentes vistas/frames

#### 2. Página de Login (login_view.py)

##### LoginPage
- **Descripción**: Página de selección de tipo de acceso
- **Opciones**:
  - Módulo Administrador
  - Módulo Usuario

<img src="capturas/general/LoginPage g-.png" width="700">

##### AdminLoginPage
- **Descripción**: Login para administradores
- **Credenciales por defecto**:
  - Usuario: admin
  - Contraseña: 1234
- **Redirección**: AdminDashboard al login exitoso

<img src="capturas/general/AdminLoginPage g-.png" width="600">

#### 3. Vistas de Administrador (views/admin/)

##### Admin Dashboard (admin_dashboard_view.py)
- **Descripción**: Panel principal del administrador
- **Funcionalidades**: Acceso a los módulos de gestión

<img src="capturas/general/Admin Dashboard g-.png" width="700">

##### Gestión de Usuarios (user_management_view.py)
- **Funcionalidades**:
  - Crear usuarios
  - Listar usuarios
  - Actualizar usuarios
  - Eliminar usuarios

<img src="capturas/admin/Gestión de Usuarios a-.png" width="800">

##### Gestión de Películas (movie_management_view.py)
- **Funcionalidades**:
  - Agregar películas
  - Listar películas
  - Actualizar películas
  - Eliminar películas

<img src="capturas/admin/Gestión de Películas a-.png" width="800">

##### Gestión de Funciones (function_management_view.py)
- **Funcionalidades**:
  - Agregar funciones
  - Listar funciones
  - Ver funciones disponibles

<img src="capturas/admin/Gestión de Funciones a-.png" width="800">

#### 4. Vistas de Usuario (views/user/)

##### User Login Page (user_login_view.py)
- **Descripción**: Login para usuarios registrados
- **Autenticación**: Usa función `login_usuario` de Usuarios.py
- **Redirección**: UserDashboard al login exitoso

<img src="capturas/general/User Login Page g-.png" width="700">

##### User Dashboard (user_dashboard_view.py)
- **Descripción**: Panel principal del usuario
- **Funcionalidades**: Acceso a las opciones del usuario

<img src="capturas/general/User Dashboard g-.png" width="700">

##### Ver Películas (view_movies_view.py)
- **Funcionalidades**:
  - Listar todas las películas disponibles
  - Ver detalles de películas

<img src="capturas/admin/Mostrar pelicula a-.png" width="600">

##### Comprar Entradas (buy_tickets_view.py)
- **Funcionalidades**:
  - Ver funciones disponibles
  - Seleccionar función
  - Especificar cantidad de entradas
  - Procesar compra
  - Validar disponibilidad de asientos

<img src="capturas/usuarios/comprar entrada u-.png" width="600">

##### Historial de Compras (purchase_history_view.py)
- **Funcionalidades**:
  - Ver historial de compras del usuario
  - Mostrar detalles de cada compra
  - Formateo de fechas

<img src="capturas/usuarios/Obtener Historial de Usuario u-.png" width="800">

##### Preferencias (preferences_view.py)
- **Funcionalidades**:
  - Gestionar preferencias del usuario
  - Actualizar información personal

<img src="capturas/usuarios/Preferencias u-.png" width="500">

</details>

## Flujo de Trabajo del Sistema
<details>
<summary>Ver Flujo de Trabajo del Sistema</summary>

### Flujo de Administrador
1. Login con credenciales de administrador (admin/1234)
2. Acceso al Dashboard de Administrador
3. Gestión de películas:
   - Agregar nuevas películas al catálogo
   - Actualizar información de películas existentes
   - Eliminar películas
4. Gestión de funciones:
   - Programar funciones para películas
   - Especificar sala, horario, asientos y precio
   - Ver funciones disponibles
5. Gestión de usuarios:
   - Crear usuarios
   - Ver lista de usuarios
   - Actualizar información de usuarios
   - Eliminar usuarios

### Flujo de Usuario
1. Login con correo y contraseña
2. Acceso al Dashboard de Usuario
3. Ver catálogo de películas
4. Ver funciones disponibles
5. Comprar entradas:
   - Seleccionar función
   - Especificar cantidad
   - Procesar pago
6. Ver historial de compras
7. Gestionar preferencias personales

---
</details>

## Dependencias del Sistema
<details>
<summary>Ver Dependencias y Requisitos</summary>

### Python Packages
- `pymongo`: Driver de MongoDB para Python
- `tkinter`: Interfaz gráfica (incluido en Python estándar)

### Requisitos del Sistema
- MongoDB instalado y ejecutándose en localhost:27017
- Python 3.x
- Sistema operativo compatible con Tkinter

---
</details>

## Archivos del Proyecto
<details>
<summary>Ver Estructura de Directorios</summary>

```
Cine-DB/
├── main.py                    # Punto de entrada de la aplicación
├── conexion.py                # Configuración de conexión a MongoDB
├── Usuarios.py                # Lógica de gestión de usuarios
├── Peliculas.py               # Lógica de gestión de películas
├── Funciones.py               # Lógica de gestión de funciones
├── Entradas.py                # Lógica de gestión de entradas
├── views/                     # Directorio de vistas GUI
│   ├── main_window.py         # Ventana principal
│   ├── login_view.py          # Páginas de login
│   ├── admin/                 # Vistas de administrador
│   │   ├── admin_dashboard_view.py
│   │   ├── user_management_view.py
│   │   ├── movie_management_view.py
│   │   └── function_management_view.py
│   └── user/                  # Vistas de usuario
│       ├── user_login_view.py
│       ├── user_dashboard_view.py
│       ├── view_movies_view.py
│       ├── buy_tickets_view.py
│       ├── purchase_history_view.py
│       └── preferences_view.py
└── DOCUMENTACION_TECNICA.md  # Este documento
```

---
</details>


## Notas Importantes
<details>
<summary>Ver Notas de Seguridad, Validaciones y Errores</summary>

### Seguridad
- Las contraseñas se almacenan en texto plano (no recomendado para producción)
- El login de administrador usa credenciales hardcoded (admin/1234)
- No hay encriptación de datos sensibles

### Validaciones
- Los correos electrónicos se validan como case-insensitive
- Los títulos de películas se validan como case-insensitive
- La duración de películas debe ser un entero
- Los IDs de MongoDB se validan antes de su uso

### Consistencia de Datos
- Al comprar una entrada, se actualizan tres colecciones: Entradas, usuarios, Funciones
- El historial de compras se mantiene en la colección usuarios
- Los datos se denormalizan en algunas colecciones para optimizar consultas (ej: usuario_nombre en Entradas)

### Manejo de Errores
- Las funciones retornan mensajes de error descriptivos
- Se manejan excepciones para operaciones de base de datos
- Se validan formatos de IDs antes de operaciones CRUD

---
</details>

## Fecha de Documentación
Junio 2026
