from playwright.sync_api import sync_playwright
from utils.config import Config
from pages.login_page import LoginPage
from pages.siniestro_page import SiniestroPage
from pages.tabla_resultados_page import TablaResultadosPage
from pages.asignacion_page import AsignacionPage
from busquedas.busqueda_poliza import BusquedaPoliza
from busquedas.busqueda_serie import BusquedaSerie
from busquedas.busqueda_santander import BusquedaSantander
from busquedas.busqueda_inciso import BusquedaInciso
from busquedas.busqueda_placas import BusquedaPlacas 

def probar_flujo(criterio, tipo_asignacion, causa_seleccionada):
    print("\n--- INICIANDO AUTOMATIZACIÓN E2E (PLAYWRIGHT) ---")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=Config.HEADLESS, args=["--start-maximized"])
        context = browser.new_context(no_viewport=True)
        page = context.new_page()

        try:
            # 1. Instanciar todas las páginas
            login_page = LoginPage(page)
            siniestro_page = SiniestroPage(page)
            tabla_page = TablaResultadosPage(page)
            asignacion_page = AsignacionPage(page)
            
            # 2. Login
            login_page.iniciar_sesion()

            # 3. Completar el flujo de siniestro usando la causa seleccionada
            siniestro_page.completar_flujo_siniestro(causa_test=causa_seleccionada)
            
            # 4. Seleccionar el menú en la UI
            siniestro_page.seleccionar_criterio_busqueda(criterio)
            
            # 5. Ejecutar la estrategia correspondiente
            estrategias = {
                "PLACAS": BusquedaPlacas,
                "POLIZA": BusquedaPoliza,
                "SERIE": BusquedaSerie,
                "SANTANDER": BusquedaSantander,
                "INCISO": BusquedaInciso
            }
            
            if criterio in estrategias:
                estrategia = estrategias[criterio](page)
                estrategia.ejecutar()
            
            # 6. Tabla y Popups
            tabla_page.procesar_seleccion()
            
            # 7. Asignación de Ajustador
            if tipo_asignacion == "2":
                asignacion_page.seguimiento_ajustadores()
            else:
                asignacion_page.asignacion_manual()
            
            print("\n✅ ¡Flujo E2E completado con éxito!")
            page.wait_for_timeout(5000)
            
        except Exception as e:
            print(f"❌ ERROR: {e}")
            page.screenshot(path="error_prueba.png")
            print("Captura de error guardada.")
        finally:
            browser.close()

if __name__ == "__main__":
    print("\n--- CONFIGURACIÓN INICIAL ---")
    criterio_usuario = input("Ingrese el criterio de búsqueda (Ej. PLACAS, POLIZA, SERIE, SANTANDER, INCISO): ").strip().upper()
    if not criterio_usuario:
        criterio_usuario = "PLACAS"

    print("\n--- TIPO DE CAUSA ---")
    print("Opciones: COLISION, ROTURA_DE_CRISTAL, ROBO_TOTAL")
    causa_usuario = input("Ingrese la causa del siniestro: ").strip().upper()
    if not causa_usuario:
        causa_usuario = "COLISION" 
    acta_input = "N"
    if causa_usuario == "ROBO_TOTAL":
        acta_input = input("¿Cuenta con Acta de levantada? (S/N): ").strip().upper()
    
    tiene_acta = True if acta_input == "S" else False

    print("\n--- TIPO DE ASIGNACIÓN ---")
    print("1. Asignación Manual (Directa desde la tabla)")
    print("2. Asignación por Menú de Seguimiento")
    opcion_asignacion = input("Seleccione una opción (1 o 2): ").strip()

    # Llamada a la función con los 3 argumentos en orden correcto
    probar_flujo(criterio_usuario, opcion_asignacion, causa_usuario)