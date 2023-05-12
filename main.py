import nltk
from nltk.stem.snowball import SnowballStemmer


# nltk.download('punkt')

def found_root(palabras):
    stemmer = SnowballStemmer('spanish')
    just_root = []
    for w in palabras:
        if stemmer.stem(w) not in just_root:
            just_root.append(stemmer.stem(w))
    return just_root


def tokenizar(text):
    return nltk.word_tokenize(text.lower())


def clean_text(palabras):
    # Leer StopList
    fileStopList = open('keys/stoplist.txt', 'r')
    StopListTXT = fileStopList.read()
    fileStopList.close()

    stop_list = tokenizar(StopListTXT)
    stop_list += ['.', '?', '¿', '-', '!', '\'', ',', ':', '«', '(', ')',
                  '``', 'con', ';']
    palabras_limpias = []
    for token in palabras:
        if token.lower() not in stop_list:
            palabras_limpias.append(token)
    return palabras_limpias


def load_file(name_file):
    file = open('libros/' + name_file, 'r')
    tokenFile = tokenizar(file.read())
    filtrado = clean_text(tokenFile)
    filtrado = found_root(filtrado)
    file.close()
    return filtrado


def matriz_incidencia(palabras_1, palabras_2, palabras_3, palabras_4, palabras_5, palabras_6):
    archivo = open("matriz_incidencia.txt", "w")
    palabras_interes = list(set(palabras_1 + palabras_2 + palabras_3
                                + palabras_4 + palabras_5 + palabras_6))

    # Tenerlo guardado en un diccionario
    matriz = {}
    for palabra in palabras_interes:
        temp = []
        temp.append(int(palabra in palabras_1))
        temp.append(int(palabra in palabras_2))
        temp.append(int(palabra in palabras_3))
        temp.append(int(palabra in palabras_4))
        temp.append(int(palabra in palabras_5))
        temp.append(int(palabra in palabras_6))
        matriz[palabra] = temp
        archivo.write(palabra + ": " + str(matriz[palabra]) + '\n')
    return matriz


palabras_1 = load_file('libro1.txt')
palabras_2 = load_file('libro2.txt')
palabras_3 = load_file('libro3.txt')
palabras_4 = load_file('libro4.txt')
palabras_5 = load_file('libro5.txt')
palabras_6 = load_file('libro6.txt')

matrix = matriz_incidencia(palabras_1, palabras_2, palabras_3, palabras_4, palabras_5, palabras_6)
print(matrix)


# ======================================================================================================

# Implementacion de la funcion booleana
def recuperacion_booleana(consulta, matriz_incidencia):
    terminos = consulta.split()

    # Aplicar la consulta booleana a la matriz de incidencia
    resultado = None
    operador = None

    for termino in terminos:
        if termino == 'AND':
            operador = 'AND'
        elif termino == 'OR':
            operador = 'OR'
        elif termino == 'NOT':
            operador = 'NOT'
        else:
            if resultado is None:
                resultado = set([i for i, valor in enumerate(matriz_incidencia[termino]) if valor == 1])
            elif operador == 'AND':
                resultado &= set([i for i, valor in enumerate(matriz_incidencia[termino]) if valor == 1])
            elif operador == 'OR':
                resultado |= set([i for i, valor in enumerate(matriz_incidencia[termino]) if valor == 1])
            elif operador == 'NOT':
                resultado -= set([i for i, valor in enumerate(matriz_incidencia[termino]) if valor == 1])

    # Obtener los índices de los documentos que satisfacen la consulta
    if resultado is None:
        return []
    else:
        libros = ["Libro 1", "Libro 2", "Libro 3", "Libro 4", "Libro 5", "Libro 6"]
        result = []
        for r in resultado:
            result.append(libros[r])
        return result


# Querys a realizar
print("consulta 1:")
consulta = 'graci OR llev AND uruk-hai'
resultado = recuperacion_booleana(consulta, matrix)
print(resultado)
# resultado: ['Libro 3']

print('\n')

print("consulta 2:")
consulta = 'vuelv AND rey'
resultado = recuperacion_booleana(consulta, matrix)
print(resultado)
# resultado: ['Libro 4', 'Libro 5']

print('\n')

print("consulta 3:")
consulta = 'estall AND funeral OR caradhr'
resultado = recuperacion_booleana(consulta, matrix)
print(resultado)
# resultado: ['Libro 2', 'Libro 6']

print('\n')

print("consulta 4:")
consulta = 'evit OR capitan OR orodruin'
resultado = recuperacion_booleana(consulta, matrix)
print(resultado)
# resultado: ['Libro 1', 'Libro 2', 'Libro 4', 'Libro 5', 'Libro 6']

print('\n')

print("consulta 5:")
consulta = 'min AND bruj AND tirith'
resultado = recuperacion_booleana(consulta, matrix)
print(resultado)
# resultado: ['Libro 4', 'Libro 5']

print('\n')

print("La validación de los resultados se hizo a partir de la matriz de incidencia ")
