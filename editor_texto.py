class Pila:
    def __init__(self):
        # Inicializa el historial con capacidad máxima de 20 operaciones.
        self.elementos = []
        self.limite = 20

    def apilar(self, operacion):
        # Descarta la operación más antigua cuando se alcanza el límite.
        if len(self.elementos) >= self.limite:
            self.elementos.pop(0)
        self.elementos.append(operacion)

    def desapilar(self):
        # Retira la operación más reciente según el principio LIFO.
        return None if self.esta_vacia() else self.elementos.pop()

    def esta_vacia(self):
        # Comprueba si existen operaciones pendientes.
        return len(self.elementos) == 0

    def mostrar(self):
        # Recorre el historial desde la operación más reciente.
        if self.esta_vacia():
            print('No hay operaciones en el historial.')
        for i, (tipo, contenido) in enumerate(reversed(self.elementos), 1):
            print(f'{i}. {tipo}: {contenido!r}')


class EditorTexto:
    def __init__(self):
        # Almacena los fragmentos del documento y una única pila de historial.
        self.documento = []
        self.historial = Pila()

    def agregar_texto(self, texto):
        # Agrega un fragmento y registra la acción para poder revertirla.
        if not texto:
            print('No se puede agregar texto vacío.')
            return
        self.documento.append(texto)
        self.historial.apilar(('agregar', texto))
        print('Texto agregado correctamente.')

    def eliminar_texto(self):
        # Elimina el último fragmento y conserva su contenido en el historial.
        if not self.documento:
            print('No hay texto para eliminar.')
            return
        texto = self.documento.pop()
        self.historial.apilar(('eliminar', [texto]))
        print(f'Texto eliminado: {texto}')

    def mostrar_documento(self):
        # Une los fragmentos respetando los espacios originales.
        print(''.join(self.documento) if self.documento else 'El documento está vacío.')

    def limpiar_documento(self):
        # Conserva todos los fragmentos para permitir deshacer la limpieza.
        if not self.documento:
            print('El documento ya está vacío.')
            return
        self.historial.apilar(('eliminar', self.documento.copy()))
        self.documento.clear()
        print('Documento limpiado correctamente.')

    def deshacer(self):
        # Invierte la última operación sin generar una nueva entrada.
        operacion = self.historial.desapilar()
        if operacion is None:
            print('No hay operaciones para deshacer.')
            return
        tipo, contenido = operacion
        if tipo == 'agregar':
            self.documento.pop()
            print('Se deshizo la última inserción.')
        else:
            self.documento.extend(contenido)
            print('Se recuperó el texto eliminado.')

    def mostrar_historial(self):
        # Delega la visualización a la pila.
        self.historial.mostrar()


def main():
    editor = EditorTexto()
    while True:
        print('\n=== EDITOR DE TEXTO ===\n1. Agregar texto\n2. Eliminar último texto\n3. Mostrar documento\n4. Limpiar documento\n5. Deshacer\n6. Mostrar historial\n0. Salir')
        opcion = input('Seleccione una opción: ')
        if opcion == '1':
            editor.agregar_texto(input('Ingrese el texto: '))
        elif opcion == '2':
            editor.eliminar_texto()
        elif opcion == '3':
            editor.mostrar_documento()
        elif opcion == '4':
            editor.limpiar_documento()
        elif opcion == '5':
            editor.deshacer()
        elif opcion == '6':
            editor.mostrar_historial()
        elif opcion == '0':
            break
        else:
            print('Opción inválida.')


# Bloque de pruebas: verifica las operaciones y el límite del historial.
def pruebas():
    e = EditorTexto()
    e.deshacer()
    e.agregar_texto('Hola')
    e.agregar_texto(' mundo')
    assert ''.join(e.documento) == 'Hola mundo'
    e.eliminar_texto()
    assert e.documento == ['Hola']
    e.deshacer()
    assert e.documento == ['Hola', ' mundo']
    e.deshacer()
    assert e.documento == ['Hola']
    e.limpiar_documento()
    assert not e.documento
    e.deshacer()
    assert e.documento == ['Hola']
    e = EditorTexto()
    for i in range(21):
        e.agregar_texto(str(i))
    assert len(e.historial.elementos) == 20
    for i in range(20):
        e.deshacer()
    assert e.documento == ['0'] and e.historial.esta_vacia()
    print('Todas las pruebas superadas.')

if __name__ == '__main__':
    if input('¿Ejecutar pruebas? (s/n): ').lower() == 's':
        pruebas()
    else:
        main()

