# Trabajo Integrador Final - Organización Empresarial

## Proyecto
Bot simulado para la gestión de solicitudes de vacaciones en una empresa ficticia llamada **TecnoGestión SRL**.

El objetivo es demostrar la coherencia entre:

- el proceso administrativo elegido,
- el modelado BPMN AS-IS y TO-BE,
- la lógica implementada en Python,
- la base de datos simulada en CSV,
- la máquina de estados y el manejo del camino infeliz.

## Cómo ejecutar

Desde la carpeta raíz del proyecto:

```bash
python main.py
```

## Datos de prueba

Legajos disponibles:

- 1001 - Mariano Popolo - 14 días
- 1002 - Ana Gomez - 5 días
- 1003 - Carlos Ruiz - 0 días
- 1004 - Lucia Perez - 10 días

Ejemplo aprobado:

```text
Legajo: 1001
Inicio: 2026-07-01
Fin: 2026-07-05
Resultado: APROBADA
```

Ejemplo rechazado por saldo:

```text
Legajo: 1002
Inicio: 2026-07-01
Fin: 2026-07-10
Resultado: RECHAZADA
```

## Relación BPMN - Código

- El evento de inicio se representa con el mensaje inicial del bot.
- La tarea de ingresar legajo se implementa con `pedir_legajo()`.
- El gateway "¿Legajo existe?" se implementa con `buscar_empleado()`.
- La validación de fechas se implementa con `pedir_periodo()`.
- El gateway "¿Saldo suficiente?" se implementa con `dias_solicitados <= dias_disponibles`.
- El registro final se implementa con `registrar_solicitud()` y `datos/solicitudes.csv`.

## Seguridad

No se incluye ningún Personal Access Token (PAT), contraseña ni credencial en el repositorio. Si se usa un PAT para subir a GitHub, debe ingresarse solo como contraseña de autenticación y nunca guardarse en archivos o capturas.
