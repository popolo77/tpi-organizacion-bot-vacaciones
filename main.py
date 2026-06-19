"""
Trabajo Integrador Final - Organización Empresarial
Bot simulado para gestión de solicitudes de vacaciones.
Alumno: Mariano Popolo

Este programa acompaña el BPMN del trabajo: recibe una solicitud,
valida datos contra una base CSV, decide si corresponde aprobar o rechazar,
y registra el resultado. Se usa una máquina de estados simple para mostrar
en qué paso del proceso se encuentra el bot.
"""

import csv
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ARCHIVO_EMPLEADOS = BASE_DIR / "datos" / "empleados.csv"
ARCHIVO_SOLICITUDES = BASE_DIR / "datos" / "solicitudes.csv"

ESTADOS = {
    "INICIO": "inicio de la solicitud",
    "ESPERA_LEGAJO": "se espera el legajo del empleado",
    "VALIDA_EMPLEADO": "se valida el legajo contra empleados.csv",
    "ESPERA_FECHAS": "se esperan fecha de inicio y fecha de fin",
    "VALIDA_FECHAS": "se valida formato y orden cronológico",
    "DECIDE_SALDO": "se compara lo solicitado contra el saldo disponible",
    "REGISTRA": "se registra el resultado en solicitudes.csv",
    "FIN": "fin del proceso",
}


def cambiar_estado(nuevo_estado):
    print(f"\n[Estado] {nuevo_estado}: {ESTADOS[nuevo_estado]}")
    return nuevo_estado


def cargar_empleados():
    empleados = []
    try:
        with open(ARCHIVO_EMPLEADOS, "r", encoding="utf-8", newline="") as archivo:
            lector = csv.DictReader(archivo)
            columnas = {"legajo", "nombre", "sector", "dias_disponibles"}
            if not lector.fieldnames or not columnas.issubset(set(lector.fieldnames)):
                print("Error: empleados.csv no tiene las columnas esperadas.")
                return []
            for fila in lector:
                fila["dias_disponibles"] = int(fila["dias_disponibles"])
                empleados.append(fila)
    except FileNotFoundError:
        print("Error: no se encontró datos/empleados.csv.")
    except ValueError:
        print("Error: dias_disponibles debe ser numérico.")
    return empleados


def buscar_empleado(empleados, legajo):
    for empleado in empleados:
        if empleado["legajo"] == legajo:
            return empleado
    return None


def pedir_legajo():
    while True:
        legajo = input("Ingrese su número de legajo: ").strip()
        if legajo.isdigit():
            return legajo
        print("Entrada inválida: el legajo debe contener solo números.")


def pedir_fecha(mensaje):
    while True:
        texto = input(mensaje).strip()
        try:
            return datetime.strptime(texto, "%Y-%m-%d").date()
        except ValueError:
            print("Fecha inválida. Use el formato AAAA-MM-DD. Ejemplo: 2026-07-15")


def pedir_periodo():
    while True:
        fecha_inicio = pedir_fecha("Ingrese fecha de inicio (AAAA-MM-DD): ")
        fecha_fin = pedir_fecha("Ingrese fecha de fin (AAAA-MM-DD): ")
        if fecha_fin >= fecha_inicio:
            return fecha_inicio, fecha_fin
        print("Error: la fecha de fin no puede ser anterior a la fecha de inicio.")


def calcular_dias(fecha_inicio, fecha_fin):
    return (fecha_fin - fecha_inicio).days + 1


def obtener_proximo_id():
    if not ARCHIVO_SOLICITUDES.exists() or ARCHIVO_SOLICITUDES.stat().st_size == 0:
        return 1
    with open(ARCHIVO_SOLICITUDES, "r", encoding="utf-8", newline="") as archivo:
        filas = list(csv.DictReader(archivo))
    return max(int(f["id_solicitud"]) for f in filas) + 1 if filas else 1


def registrar_solicitud(empleado, fecha_inicio, fecha_fin, dias_solicitados, estado, observacion):
    campos = ["id_solicitud", "legajo", "nombre", "fecha_inicio", "fecha_fin", "dias_solicitados", "estado", "observacion"]
    archivo_existe = ARCHIVO_SOLICITUDES.exists() and ARCHIVO_SOLICITUDES.stat().st_size > 0
    with open(ARCHIVO_SOLICITUDES, "a", encoding="utf-8", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        if not archivo_existe:
            escritor.writeheader()
        escritor.writerow({
            "id_solicitud": obtener_proximo_id(),
            "legajo": empleado["legajo"],
            "nombre": empleado["nombre"],
            "fecha_inicio": fecha_inicio.isoformat(),
            "fecha_fin": fecha_fin.isoformat(),
            "dias_solicitados": dias_solicitados,
            "estado": estado,
            "observacion": observacion,
        })


def ejecutar_bot():
    print("============================================")
    print(" BOT RRHH - SOLICITUD DE VACACIONES")
    print("============================================")
    print("Bienvenido/a. Este asistente simula la gestión de vacaciones.")

    cambiar_estado("INICIO")
    empleados = cargar_empleados()
    if not empleados:
        cambiar_estado("FIN")
        return

    empleado = None
    intentos = 0
    max_intentos = 3

    while empleado is None and intentos < max_intentos:
        cambiar_estado("ESPERA_LEGAJO")
        legajo = pedir_legajo()
        cambiar_estado("VALIDA_EMPLEADO")
        empleado = buscar_empleado(empleados, legajo)
        if empleado is None:
            intentos += 1
            print("Legajo no encontrado.")
            if intentos < max_intentos:
                print(f"Puede intentar nuevamente. Intentos restantes: {max_intentos - intentos}")
            else:
                print("Se alcanzó el máximo de intentos. La solicitud finaliza sin registrarse.")
                cambiar_estado("FIN")
                return

    print(f"Empleado validado: {empleado['nombre']} - Sector: {empleado['sector']}")
    print(f"Días disponibles: {empleado['dias_disponibles']}")

    cambiar_estado("ESPERA_FECHAS")
    fecha_inicio, fecha_fin = pedir_periodo()
    cambiar_estado("VALIDA_FECHAS")
    dias_solicitados = calcular_dias(fecha_inicio, fecha_fin)
    print(f"Días solicitados: {dias_solicitados}")

    cambiar_estado("DECIDE_SALDO")
    if dias_solicitados <= empleado["dias_disponibles"]:
        resultado = "APROBADA"
        observacion = "Saldo suficiente de vacaciones."
        print("Solicitud aprobada. Se registra la solicitud.")
    else:
        resultado = "RECHAZADA"
        observacion = "Saldo insuficiente de vacaciones."
        print("Solicitud rechazada por saldo insuficiente.")

    cambiar_estado("REGISTRA")
    registrar_solicitud(empleado, fecha_inicio, fecha_fin, dias_solicitados, resultado, observacion)
    print("Resultado guardado en datos/solicitudes.csv")
    cambiar_estado("FIN")
    print("Proceso finalizado.")


if __name__ == "__main__":
    ejecutar_bot()
