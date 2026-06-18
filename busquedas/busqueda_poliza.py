from busquedas.estrategia_base import BusquedaEstrategia

class BusquedaPoliza(BusquedaEstrategia):
    def __init__(self, page):
        super().__init__(page)
        self.selector_input_sucursal = "input[formcontrolname='p_sucursal']"
        self.selector_input_poliza = "input[formcontrolname='p_poliza_central']"
        self.selector_input_inciso = "input[formcontrolname='p_inciso']"
        self.selector_btn_buscar = "//button[contains(., 'Buscar')]"
        
    def ejecutar(self):
        print("--- Formulario de Búsqueda de Póliza ---")
        
        # INGRESO DE DATOS POR CONSOLA
        sucursal = input("Ingrese la Sucursal: ")
        poliza = input("Ingrese el número de Póliza: ")
        inciso = input("Ingrese el Inciso: ")
        
        print(f"\n>> [Estrategia] Iniciando búsqueda con: Sucursal {sucursal}, Póliza {poliza}, Inciso {inciso}...")
        
        # LLENADO DE DATOS 
        self.page.locator(self.selector_input_sucursal).fill(sucursal)
        self.page.locator(self.selector_input_poliza).fill(poliza)
        self.page.locator(self.selector_input_inciso).fill(inciso)
        
        print("Clic en botón Buscar...")
        self.page.locator(self.selector_btn_buscar).click(force=True)