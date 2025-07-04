# Workflow: SELECT en Base de Datos con Validación y Auditoría

## Descripción

Workflow para ejecutar SELECT en base de datos, con validación previa y recuperación de credenciales via st2kv.

Este workflow automatiza la ejecución de consultas SQL `SELECT` en una base de datos, incluyendo validación previa de la consulta, recuperación de credenciales desde `st2kv`, y registro de auditoría en una tabla específica.

---

## Entradas

- `environment`: Entorno de ejecución (por ejemplo, `dev`, `prod`)
- `database`: Nombre de la base de datos
- `query`: Consulta SQL a ejecutar

## Variables Internas

- `kv_key_name`: Nombre de la clave en st2kv
- `credentials`: Credenciales recuperadas
- `conn_info`: Información de conexión parseada
- `query_result`: Resultado de la consulta
- `estado`: Estado final del workflow
- `mensaje`: Mensaje de salida

## Tareas Principales

1. **build_kv_key**: Construye el nombre de la clave para recuperar credenciales.
2. **get_credentials**: Recupera las credenciales desde st2kv.
3. **parse_conn_info**: Parsea las credenciales a formato JSON.
4. **validate_query**: Valida que la consulta SQL sea un `SELECT`.
5. **execute_query**: Ejecuta la consulta SQL.
6. **verificar_tabla**: Verifica si existe la tabla de auditoría.
7. **crear_tabla**: Crea la tabla `auditoria_ejecuciones` si no existe.
8. **insertar_auditoria**: Registra la ejecución en la tabla de auditoría.

## Salidas

- `estado`: Estado final (`succeeded` o `failed`)
- `resultado`: Resultado o mensaje de error

---

## Requisitos

- StackStorm con acciones personalizadas (`sql.query`, `utils.parse_json`, etc.)
- Acceso a base de datos con credenciales almacenadas en `st2kv`
- Tabla `auditoria_ejecuciones` en la base de datos o permisos para crearla

## Auditoría

El workflow registra automáticamente cada ejecución en la tabla `auditoria_ejecuciones` con:

- Usuario que ejecutó
- Fecha y hora
- Descripción de la acción

---

## Versión

`1.0`
