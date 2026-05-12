from pages.base_page import BasePage

class SiniestroPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

        
        # --- SELECTORES: LOADER ---
        self.loader = ".contenedorBlock"
        
        # --- SELECTORES: DATOS DEL REPORTANTE ---
        self.input_nombre = "input[formcontrolname='nombre']"
        self.input_paterno = "input[formcontrolname='apellido_paterno']"
        self.input_materno = "input[formcontrolname='apellido_materno']"
        self.btn_desplegable = ".mat-mdc-select-value"
        self.opcion_celular = "//span[contains(text(), 'Celular')]"
        self.inputs_telefono = "input[formcontrolname='telefono']"
        
        # Como hay varios elementos iguales, en Playwright podemos seguir usando XPATH o nth
        self.btn_desplegable_confirm = "(//div[contains(@class, 'mat-mdc-select-value')])[2]"
        self.opcion_celular_confirm = "(//span[contains(text(), 'Celular')])[2]"
        self.input_confirm_tel = "(//input[@formcontrolname='telefono'])[2]"
        #boton de causa
        self.btn_causa = "//span[contains(text(), 'Causa')]"
       # self.opcion_colision = "//span[contains(text(), 'COLISION')]"
       # --- SELECTORES: ROBO TOTAL 
        self.chk_acta = "label:has-text('¿Cuenta con Acta de levantada?')"
        self.input_averiguacion = "input[formcontrolname='numeroAveriguacion']"
       #SELECTORES DE ROBO AUN NO TOMAN LOS DATOS
        self.sel_tipo_robo = "mat-select[formcontrolname='tipo_robo']"
        self.sel_pais = "mat-select[formcontrolname='id_pais']"
        self.sel_estado = "mat-select[formcontrolname='id_estado']"
        self.sel_municipio = "mat-select[formcontrolname='id_municipio']"
        

        # --- SELECTORES: DATOS DEL CONDUCTOR ---
        # En Playwright podemos usar CSS con el #ID directamente
        self.checkbox_conductor = "#mat-mdc-checkbox-2-input"
        self.checkbox_1 = "#mat-mdc-checkbox-1-input"

        # --- SELECTORES: UBICACIÓN DEL SINIESTRO ---
        self.btn_lupa = "button[aria-label='Btn búsqueda']"
        self.input_mapa = "input.pac-target-input"
        self.btn_crear_folio = "//button[contains(text(), 'Crear folio')]"

        # --- SELECTORES: DATOS DEL SINIESTRO ---
        self.btn_calendario = "mat-datepicker-toggle button"
        self.btn_dia_hoy = "button[aria-current='date']"
        self.btn_reloj = "//mat-icon[contains(text(), 'schedule')]/ancestor::button"
        self.textarea_hechos = "textarea[formcontrolname='que_ocurrio']"
        self.input_placas = "input[formcontrolname='placas_cabina']"
        self.btn_color = "//span[contains(text(), 'Color')]"
        self.opcion_color_amarillo = "//span[contains(text(), 'AMARILLO')]"

        # --- SELECTORES: AJUSTE REMOTO ---
        self.radio_no = "//input[@name='mat-radio-group-4' and @value='false']"
        self.radio_group_5_no = "//input[@name='mat-radio-group-5' and @value='false']"
        self.radio_group_6_no = "//input[@name='mat-radio-group-6' and @value='false']"
        self.radio_group_7_no = "//input[@name='mat-radio-group-7' and @value='false']"

    def seleccionar_opcion_mat(self, selector_trigger, texto_opcion):
        """Maneja cualquier mat-select de Angular Material de forma segura."""
        print(f"Buscando: {texto_opcion}...")
        
        # 2. ESPERA CRÍTICA: Esperamos a que el panel de opciones sea visible
        ## 1. Clic al trigger
        trigger = self.page.locator(selector_trigger)
        trigger.scroll_into_view_if_needed()
        trigger.click(force=True)
        
        # 3. Buscar la opción por su texto interno (usamos el span que vimos en tu inspección)
        opcion = self.page.locator(f"//mat-option//span[contains(text(), '{texto_opcion}')]").first
        opcion.wait_for(state="visible", timeout=5000)
        opcion.click()
        print(f"✅ Seleccionado: {texto_opcion}")


    def esperar_carga(self):
        """Espera a que el loader de Angular desaparezca."""
        print("Esperando que desaparezca la pantalla de carga...")
        # Playwright espera a que el elemento cumpla el estado 'hidden'
        self.page.locator(self.loader).wait_for(state="hidden")

    def llenar_datos_reportante(self, nombre="Juan", paterno="Galindo", materno="Peres", telefono="5555555555", causa="COLISION", tiene_acta=True):
        self.esperar_carga()
        print("Llenando datos del reportante...")
        
        # Agregamos .first para decirle a Playwright que tome el primero que encuentre (como hacía Selenium)
        self.page.locator(self.input_nombre).first.fill(nombre)
        self.page.locator(self.input_paterno).first.fill(paterno)
        self.page.locator(self.input_materno).first.fill(materno)

        print("Llenando primer teléfono...")
        self.page.locator(self.btn_desplegable).first.click()
        self.page.locator(self.opcion_celular).first.click()
        self.page.locator(self.inputs_telefono).first.fill(telefono)
        
        print("Llenando segundo teléfono...")
        # Nota: Aquí ya estabas usando [2] en el XPATH desde tu versión anterior, 
        # así que este no debería chocar, pero igual es seguro dejarlo normal.
        self.page.locator(self.btn_desplegable_confirm).click()
        self.page.locator(self.opcion_celular_confirm).click()
        self.page.locator(self.input_confirm_tel).fill(telefono)

        #Aqui se epieza a conectar causa NUEVOS
        self.seleccionar_causa_siniestro(causa,tiene_acta_usuario=tiene_acta)
        
    def seleccionar_causa_siniestro(self, causa="COLISION", tiene_acta_usuario=True):
        print(f"--- Seleccionando criterio en menú: {causa} ---")
        
        # Opciones válidas
        opciones_causa = {
            "COLISION": "COLISION",
            "ROTURA_DE_CRISTAL": "ROTURA DE CRISTAL",
            "ROBO_TOTAL": "ROBO TOTAL"
        }
        texto_opcion2 = opciones_causa.get(causa.upper())

        if not texto_opcion2:
            print(f"Causa '{causa}' no válida.")
            return

        try:
            # 1. Desplegar y seleccionar la causa
            print("Desplegando menú 'Causa'...")
            self.page.locator(self.btn_causa).first.click(force=True)
            self.page.wait_for_timeout(1000) 
            
            print(f"Eligiendo opción '{texto_opcion2}'...")
            self.page.locator(f"//mat-option//span[contains(text(), '{texto_opcion2}')]").first.click(force=True)
            
            # ESPERA CRÍTICA: Esperamos a que la UI se actualice según la causa
            self.page.wait_for_timeout(1500) 

            # 2. Lógica condicional según la causa elegida
            if causa.upper() == "ROTURA_DE_CRISTAL":
                self.manejar_aviso_cristales(requiere_ajustador=True)
                self.esperar_carga()
            
            elif causa.upper() == "ROBO_TOTAL":
                # Integramos aquí la llamada al nuevo método
                self.manejar_detalles_robo(tiene_acta=tiene_acta_usuario)
            
            self.page.wait_for_timeout(1000)
            
        except Exception as e:
            print(f"Error seleccionando el criterio: {e}")

    def manejar_detalles_robo(self, tiene_acta=True, num_averiguacion="123456"):
        print(f"🕵️ Configurando detalles de Robo (Acta: {tiene_acta})")
        try:
            # Espera a que el formulario cargue tras elegir la causa
            self.page.wait_for_timeout(2000) 
            
            label_acta = self.page.locator(self.chk_acta)
            input_ave = self.page.locator(self.input_averiguacion)

            if tiene_acta:
                # Lógica del check de acta
                if not input_ave.is_visible():
                    label_acta.click(force=True)
                    input_ave.wait_for(state="visible", timeout=5000)
                input_ave.fill(num_averiguacion)
            else:
                if input_ave.is_visible():
                    label_acta.click(force=True)

            # --- SECCIÓN DE SELECTORES ESTOS CAMPOS AUN NO LOS TOMA ---
            # Tipo de Robo REVISION
            print("⏳ Esperando campos de robo...")
            
            self.seleccionar_opcion_mat(self.sel_tipo_robo, "ESTACIONADO")
            
            self.page.locator(self.sel_pais).wait_for(state="visible") 

            # País
            self.seleccionar_opcion_mat(self.sel_pais, "MEXICO")
            self.page.locator(self.sel_estado).wait_for(state="visible")
            
            # Estado
            self.seleccionar_opcion_mat(self.sel_estado, "ESTADO DE MEXICO")
            self.page.locator(self.sel_municipio).wait_for(state="visible")
            
            # Municipio (Pequeña espera porque esta lista depende de la elección del Estado)
            self.page.wait_for_timeout(1000) 
            self.seleccionar_opcion_mat(self.sel_municipio, "CHALCO")

            print("✅ Todos los campos de Robo y Ubicación completados.")

        except Exception as e:
            print(f"⚠️ Error en Robo: {e}")
            
    def llenar_datos_conductor(self):
        print("Llenando datos del conductor...")
        # force=True reemplaza tu viejo self._click_js() de Selenium para checkboxes rebeldes
        self.page.locator(self.checkbox_conductor).click(force=True)
        self.page.locator(self.checkbox_1).click(force=True)

    def llenar_ubicacion_siniestro(self, direccion="Metrobús Nápoles, Avenida Insurgentes Sur, Colonia Nápoles, Mexico City, CDMX, Mexico"):
        print("Iniciando ubicación del siniestro...")
        self.page.locator(self.btn_lupa).click(force=True)
        
        # En Playwright es recomendable escribir pausado si es un mapa predictivo
        self.page.locator(self.input_mapa).press_sequentially(direccion, delay=50)
        self.page.locator(self.input_mapa).press("Enter")
        print(f">> Dirección '{direccion}' ingresada con éxito.")

    def finalizar_registro(self):
        print("Finalizando registro (Crear Folio)...")
        # Playwright hace el scroll de forma automática antes de dar clic
        self.page.locator(self.btn_crear_folio).click()
        print(">> Clic exitoso en Crear Folio.")

    def llenar_datos_siniestro(self, hechos="El conductor perdió el control del vehículo y chocó contra un poste.", placas="TX11111"):
        print("Llenando datos del siniestro...")
        
        # 1. Esperamos si aparece algún loader de Angular después de "Crear Folio"
        self.esperar_carga()
        
        # 2. Le damos un pequeño respiro a la UI de Angular (equivalente a tu time.sleep(2) original)
        self.page.wait_for_timeout(1000) 

        print("Dando clic en el calendario...")
        # Quitamos el force=True para que Playwright valide que el botón realmente está listo para recibir el clic
        self.page.locator(self.btn_calendario).click()

        # 3. Esperamos explícitamente a que la animación del calendario termine y el botón sea visible
        print("Seleccionando el día de hoy...")
        self.page.locator(self.btn_color).scroll_into_view_if_needed() # Como este bajamos para que cargue el calendario
        btn_hoy = self.page.locator(self.btn_dia_hoy)
        btn_hoy.wait_for(state="visible") 
        btn_hoy.click() # Aquí ya no necesitamos force=True

        self.page.locator(self.btn_reloj).click()

        print("Escribiendo hechos...")
        self.page.locator(self.textarea_hechos).fill(hechos)

        self.page.locator(self.input_placas).fill(placas)
        print("Seleccionando color del vehículo...")
        self.page.locator(self.btn_color).click(force=True)
        self.page.locator(self.opcion_color_amarillo).click()

    def seleccionar_ajuste_remoto(self):
        print("Seleccionando opción 'No' para ajuste remoto...")
        self.page.locator(self.radio_no).click(force=True)
        self.page.locator(self.radio_group_5_no).click(force=True)
        self.page.locator(self.radio_group_6_no).click(force=True)
        self.page.locator(self.radio_group_7_no).click(force=True)
        
        #se agrego la causa y el acta
    def completar_flujo_siniestro(self,causa_test="COLISION", tiene_acta=True):
        """Método de conveniencia para ejecutar todo el flujo de esta página de una vez"""
        self.llenar_datos_reportante(causa=causa_test, tiene_acta=tiene_acta)
        self.llenar_datos_conductor()
        self.llenar_ubicacion_siniestro()
        self.finalizar_registro()
        self.llenar_datos_siniestro()
        self.seleccionar_ajuste_remoto()
    
    def seleccionar_criterio_busqueda(self, criterio="PLACAS"):
        print(f"--- Seleccionando criterio en menú: {criterio} ---")
        
        # Selectores del menú de búsqueda
        dropdown_criterio = "//mat-label[contains(text(), 'Buscar por')]/ancestor::mat-form-field//mat-select"
        
        # Opciones válidas
        opciones = {
            "POLIZA": "Póliza",
            "SERIE": "Serie",
            "PLACAS": "Placas",
            "SANTANDER": "Santander",
            "INCISO": "Inciso"
        }
        texto_opcion = opciones.get(criterio)

        if not texto_opcion:
            print(f"Criterio '{criterio}' no válido.")
            return

        try:
            print("Desplegando menú 'Buscar por'...")
            self.page.locator(dropdown_criterio).click(force=True)
            self.page.wait_for_timeout(1000) # Pausa para animación de Angular
            
            print(f"Eligiendo opción '{texto_opcion}'...")
            self.page.locator(f"//mat-option//span[contains(text(), '{texto_opcion}')]").click(force=True)
            self.page.wait_for_timeout(1000)
            
        except Exception as e:
            print(f"Error seleccionando el criterio: {e}")

            #se agregaran los campos de rotura de cristal --->

    def manejar_aviso_cristales(self, requiere_ajustador=True, correo="ana.test@ejemplo.com"):
        print("📢 Procesando ventana emergente de AVISO...")
        try:
            # 1. Esperar el texto del aviso para confirmar que el modal cargó
            self.page.wait_for_selector("text=¿Se requiere envío de Ajustador?", timeout=7000)

            # 2. Hacer clic en Si o No (el correo aparecerá de todos modos)
            if requiere_ajustador:
                self.page.get_by_role("button", name="Si").click()
            else:
                self.page.get_by_role("button", name="No").click()
            
            # 3. Llenar el correo usando el formcontrolname de tu imagen
            campo_email = self.page.locator("input[formcontrolname='cveCorreoCausa']")
            campo_email.wait_for(state="visible")
            campo_email.fill(correo)
            print(f"✅ Correo '{correo}' ingresado correctamente.")
            self.page.keyboard.press("Enter")
            
            # 4. Cerrar el aviso (puedes usar Enter o buscar el botón 'Aceptar')
            self.page.locator(".swal2-container").wait_for(state="hidden")
            print("✅ Modal de cristales cerrado y pantalla liberada.")
            self.page.locator(".swal2-container").wait_for(state="hidden")

            self.page.wait_for_timeout(1500) 
            print("✅ Pantalla de póliza liberada.")
            
        except Exception as e:
            print(f"⚠️ No se pudo completar el aviso de cristales: {e}")