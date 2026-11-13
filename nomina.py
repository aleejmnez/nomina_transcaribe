# ==============================================================
#  MODULO DE NOMINA - TransCaribeCol
#  Transportes del Gran Caribe Colombiano S.C.A.
#  Aplicacion en consola hecha en Python.
#  Los datos se guardan en una MATRIZ (lista de listas) y luego
#  se exportan a un archivo plano: nomina.txt
# ==============================================================

# ---------------- Constantes del negocio ----------------
VALOR_HORA_ADMIN = 20000      # pago por hora del administrativo
VALOR_HORA_EXTRA = 25000      # pago por hora extra del administrativo
VALOR_HORA_OPER = 40000       # pago por hora del operativo

NOMBRE_ARCHIVO = "nomina.txt"

# Matriz donde se guardan todos los empleados.
# Cada fila es una lista con 11 datos (las columnas del TXT).
nomina = []


# ---------------- Funciones de apoyo ----------------
def pedir_entero(mensaje):
    """Pide un numero entero y vuelve a preguntar si se escribe mal."""
    while True:
        dato = input(mensaje)
        if dato.isdigit():
            return int(dato)
        print("  Error: debe escribir un numero entero positivo.")


def pedir_texto(mensaje):
    """Pide un texto que no este vacio."""
    while True:
        dato = input(mensaje).strip()
        if dato != "":
            return dato
        print("  Error: este dato no puede quedar vacio.")


def pesos(valor):
    """Convierte un numero a formato de dinero. Ej: 800000 -> $800,000"""
    return "$" + format(valor, ",")


def mostrar_volante(fila):
    """Muestra en pantalla el volante de pago de un empleado."""
    nombre = fila[0]
    tipo = fila[1]
    cargo = fila[2]
    ht = fila[3]
    salario = fila[4]
    he = fila[5]
    tphe = fila[6]
    salud = fila[7]
    pension = fila[8]
    arl = fila[9]
    total = fila[10]
    total_descuentos = salud + pension + arl

    # Los porcentajes que se muestran cambian segun el tipo
    if tipo == "ADMINISTRATIVO":
        texto_salud = "Salud(4%)"
        texto_pension = "Pensión(4%)"
        texto_arl = "ARL(0,522%)"
    else:
        texto_salud = "Salud(12,5% del IBC)"
        texto_pension = "Pensión(16% del IBC)"
        if cargo == "Conductor":
            texto_arl = "ARL(1,044% del IBC)"
        elif cargo == "Vigilancia":
            texto_arl = "ARL(4,350% del IBC)"
        else:
            texto_arl = "ARL(0,522% del IBC)"

    print()
    print("*" * 67)
    print(" VOLANTE DE PAGO ".center(67, "*"))
    print("*" * 67)
    print("Nombre:", nombre)
    print("Cargo:", cargo)
    print("Horas Trabajadas(mes):", ht)
    print("Salario Bruto:", pesos(salario))
    print("Horas Extras:", he)
    print("Total pago Horas Extras:", pesos(tphe))
    print()
    print("*" * 67)
    print(" DESCUENTOS DE LEY ".center(67, "*"))
    print("*" * 67)
    print(texto_salud + ":", pesos(salud))
    print(texto_pension + ":", pesos(pension))
    print(texto_arl + ":", pesos(arl))
    print("Total Descuentos:", pesos(total_descuentos))
    print()
    print("Total a pagar:", pesos(total))
    print()
    print("*" * 67)
    print(" FIN DEL VOLANTE DE PAGO ".center(67, "*"))
    print("*" * 67)


# ---------------- Opcion 1: Administrativo ----------------
def registrar_administrativo():
    print("\n--- REGISTRO EMPLEADO ADMINISTRATIVO ---")
    nombre = pedir_texto("Nombre completo: ")
    cargo = pedir_texto("Cargo: ")
    ht = pedir_entero("Horas trabajadas en el mes: ")
    he = pedir_entero("Horas extras trabajadas: ")

    # Calculos
    salario = ht * VALOR_HORA_ADMIN
    tphe = he * VALOR_HORA_EXTRA
    devengado = salario + tphe              # base para descuentos
    salud = round(devengado * 0.04)         # 4 %
    pension = round(devengado * 0.04)       # 4 %
    arl = round(devengado * 0.00522)        # 0,522 % (Riesgo I)
    total = devengado - salud - pension - arl

    fila = [nombre, "ADMINISTRATIVO", cargo, ht, salario, he, tphe,
            salud, pension, arl, total]
    nomina.append(fila)
    mostrar_volante(fila)


# ---------------- Opcion 2: Operativo ----------------
def registrar_operativo():
    print("\n--- REGISTRO EMPLEADO OPERATIVO (Prestación de Servicios) ---")
    nombre = pedir_texto("Nombre completo: ")

    print("Seleccione el cargo:")
    print("  1. Conductor          (160 horas - Riesgo II)")
    print("  2. Oficios Generales  (100 horas - Riesgo I)")
    print("  3. Vigilancia         (336 horas - Riesgo IV)")
    opcion = pedir_entero("Opción: ")
    while opcion < 1 or opcion > 3:
        print("  Error: escoja 1, 2 o 3.")
        opcion = pedir_entero("Opción: ")

    # Horas fijas y porcentaje de ARL segun el cargo
    if opcion == 1:
        cargo = "Conductor"
        ht = 160
        porcentaje_arl = 0.01044
    elif opcion == 2:
        cargo = "Oficios Generales"
        ht = 100
        porcentaje_arl = 0.00522
    else:
        cargo = "Vigilancia"
        ht = 336
        porcentaje_arl = 0.0435

    # Calculos (no hay horas extras)
    salario = ht * VALOR_HORA_OPER
    he = 0
    tphe = 0
    ibc = salario * 0.40                    # IBC = 40 % del salario
    salud = round(ibc * 0.125)              # 12,5 % del IBC
    pension = round(ibc * 0.16)             # 16 % del IBC
    arl = round(ibc * porcentaje_arl)       # segun el riesgo
    total = salario - salud - pension - arl

    fila = [nombre, "OPERATIVO", cargo, ht, salario, he, tphe,
            salud, pension, arl, total]
    nomina.append(fila)
    mostrar_volante(fila)


# ---------------- Opcion 3: Listar ----------------
def listar_nomina():
    print("\n--- EMPLEADOS REGISTRADOS EN LA MATRIZ ---")
    if len(nomina) == 0:
        print("No hay empleados registrados.")
        return
    print(f"{'Nombre':<28}{'Tipo':<16}{'Cargo':<25}{'HT':>4}{'Total a pagar':>15}")
    print("-" * 88)
    for fila in nomina:
        print(f"{fila[0]:<28}{fila[1]:<16}{fila[2]:<25}{fila[3]:>4}{pesos(fila[10]):>15}")
    print("-" * 88)
    print("Total empleados:", len(nomina))


# ---------------- Opcion 4: Guardar TXT ----------------
def guardar_txt():
    if len(nomina) == 0:
        print("\nNo hay datos para guardar.")
        return
    archivo = open(NOMBRE_ARCHIVO, "w", encoding="utf-8")
    archivo.write("Nombre;Tipo;Cargo;HT;Salario;HE;TPHE;Salud;Pension;ARL;Total a pagar\n")
    for fila in nomina:
        linea = ""
        for i in range(len(fila)):
            linea = linea + str(fila[i])
            if i < len(fila) - 1:
                linea = linea + ";"
        archivo.write(linea + "\n")
    archivo.close()
    print("\nArchivo '" + NOMBRE_ARCHIVO + "' guardado con", len(nomina), "registro(s).")


# ---------------- Menu principal ----------------
def menu():
    opcion = 0
    while opcion != 5:
        print()
        print("=" * 50)
        print("   TRANSCARIBECOL - MÓDULO DE NÓMINA")
        print("=" * 50)
        print("1. Registrar Empleado Administrativo")
        print("2. Registrar Empleado Operativo")
        print("3. Ver empleados registrados")
        print("4. Guardar nómina en archivo TXT")
        print("5. Salir")
        opcion = pedir_entero("Seleccione una opción: ")

        if opcion == 1:
            registrar_administrativo()
        elif opcion == 2:
            registrar_operativo()
        elif opcion == 3:
            listar_nomina()
        elif opcion == 4:
            guardar_txt()
        elif opcion == 5:
            guardar_txt()
            print("Gracias por usar el sistema. ¡Hasta pronto!")
        else:
            print("Opción no válida. Intente de nuevo.")


menu()