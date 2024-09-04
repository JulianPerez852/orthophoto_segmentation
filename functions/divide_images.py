from PIL import Image, ImageOps, ImageDraw, ImageFont

def divide_images(image_name):
    # Ruta de la imagen original
    imagen_ruta = f"data/input/{image_name}"

    # Cargar la imagen original
    imagen = Image.open(imagen_ruta)
    ancho_original, alto_original = imagen.size

    # Configuración
    tamano_subimagen = 640
    # Calcular el número de sub-imágenes necesarias en cada dimensión
    num_subimagens_ancho = (ancho_original + tamano_subimagen - 1) // tamano_subimagen
    num_subimagens_alto = (alto_original + tamano_subimagen - 1) // tamano_subimagen

    # Calcular el tamaño necesario para que las divisiones sean exactas
    ancho_necesario = num_subimagens_ancho * tamano_subimagen
    alto_necesario = num_subimagens_alto * tamano_subimagen

    # Añadir franjas negras para ajustar el tamaño sin cambiar las proporciones de los píxeles
    imagen_ajustada = ImageOps.pad(imagen, (ancho_necesario, alto_necesario), color=(0, 0, 0))

    # Crear una copia de la imagen ajustada para dibujar las líneas y textos
    imagen_con_lineas = imagen_ajustada.copy()
    draw = ImageDraw.Draw(imagen_con_lineas)

    # Dibujar las líneas de división
    for i in range(1, num_subimagens_ancho):
        x = i * tamano_subimagen
        draw.line([(x, 0), (x, imagen_con_lineas.height)], fill="red", width=5)

    for j in range(1, num_subimagens_alto):
        y = j * tamano_subimagen
        draw.line([(0, y), (imagen_con_lineas.width, y)], fill="red", width=5)

    # Usar una fuente más grande para asegurar que el texto sea visible
    font = ImageFont.truetype("arial.ttf", 24)  # Puedes ajustar el tamaño según sea necesario

    # Dibujar textos en la imagen con líneas para indicar la posición de cada sub-imagen
    for i in range(num_subimagens_alto):
        for j in range(num_subimagens_ancho):
            texto = f"{i+1}x{j+1}"
            x_texto = j * tamano_subimagen + 10  # Pequeño desplazamiento para no pegar el texto al borde
            y_texto = i * tamano_subimagen + 10
            draw.text((x_texto, y_texto), texto, fill="yellow", font=font)

    # Guardar la imagen actualizada con las líneas y textos
    imagen_con_lineas.save(f"data/references/{image_name}_.png")

    # Recortar y guardar las sub-imágenes limpias desde la imagen ajustada original
    subimagenes = []
    nombre_base = image_name
    for i in range(num_subimagens_alto):
        for j in range(num_subimagens_ancho):
            izquierda = j * tamano_subimagen
            superior = i * tamano_subimagen
            derecha = izquierda + tamano_subimagen
            inferior = superior + tamano_subimagen
            
            # Recortar la sub-imagen limpia
            subimagen = imagen_ajustada.crop((izquierda, superior, derecha, inferior))
            
            nombre_subimagen = f"{nombre_base}_{i+1}x{j+1}.png"
            subimagen.save(f"data/output/{nombre_subimagen}")
            subimagenes.append(subimagen)
