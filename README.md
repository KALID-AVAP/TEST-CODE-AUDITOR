# Test-Repository
Este es un repositorio dedicado a pruebas de PR.

## Auditoría recomendada
Aquí se indica qué archivos deben revisarse según cada categoría de auditoría.

### Lógica
- `procesador_pedidos.py` — orquestador principal y flujo de compra.
- `logic/calculadora_impuestos.py` — cálculos de IVA y descuentos.
- `logic/validador_negocio.py` — validación de transacciones, cupones y límites.
- `utils/formatter.py` — reglas de prioridad y tarifas internacionales.
- `database_mock.py` — lógica de acceso a datos y estado compartido.

### Reglas de Negocio
- `reglas_negocio.txt` — especificación de reglas del sistema.
- `procesador_pedidos.py` — aplicación de reglas de negocio en el flujo.
- `logic/calculadora_impuestos.py` — reglas de descuentos e impuestos.
- `logic/validador_negocio.py` — restricciones de compra y validaciones.
- `utils/formatter.py` — prioridades de envío e impuestos internacionales.

### Buenas Prácticas
- `procesador_pedidos.py` — modularidad, orden de validaciones y uso de constantes.
- `database_mock.py` — acceso a datos, estado global y concurrencia.
- `logic/calculadora_impuestos.py` — claridad de funciones y separación de responsabilidades.
- `logic/validador_negocio.py` — consistencia de datos y manejo de errores.
- `utils/config_loader.py` — carga de configuración externa.
- `config.py` — uso de variables de entorno y configuración sensible.

### Seguridad
- `auth.py` — autenticación y acceso.
- `database_mock.py` — manejo de estado global y bloqueo de stock.
- `procesador_pedidos.py` — validación de entradas, saldo y control de límites.
- `logic/validador_negocio.py` — validación de transacciones seguras y cupones.
- `utils/config_loader.py` — uso de claves de API y configuración segura.
- `config.py` — variables sensibles y configuración de entorno.
