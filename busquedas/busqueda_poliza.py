from busquedas.estrategia_base import BusquedaEstrategia

class BusquedaPoliza(BusquedaEstrategia):
    def __init__(self, page):
        super().__init__(page)
        self.selector_input_sucursal = "input[formcontrolname='p_sucursal']"
        self.selector_input_poliza = "input[formcontrolname='p_poliza_central']"
        # 1. Definimos el selector del input de producto
        self.selector_input_producto = "input[formcontrolname='p_producto']"
        self.selector_input_inciso = "input[formcontrolname='p_inciso']"
        self.selector_btn_buscar = "//button[contains(., 'Buscar')]"
        
    def ejecutar(self):
        print(">> [Estrategia] Iniciando búsqueda por Póliza (Tradicional)...")
        self.page.locator(self.selector_input_sucursal).fill("EA9")
        self.page.locator(self.selector_input_poliza).fill("5612")
        # 2. Llenamos el campo producto con "1" justo después de la póliza central
        self.page.locator(self.selector_input_producto).fill("1")
        self.page.locator(self.selector_input_inciso).fill("1")
        
        print("Clic en botón Buscar...")
        self.page.locator(self.selector_btn_buscar).click(force=True)