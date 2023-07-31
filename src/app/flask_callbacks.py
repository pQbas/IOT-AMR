import cv2

def obtener_imagen_camara(video, ZED_IMG, SIMULATOR):
    # global video, ZED_IMG
    # Captura el fotograma actual de la cámara
    if SIMULATOR == False:
        # print(ZED_IMG.shape)
        if ZED_IMG is not None:
            ret, jpeg = cv2.imencode('.jpg', ZED_IMG)
            frame_bytes = jpeg.tobytes()
            # Devuelve el fotograma como respuesta al cliente
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')
    else:
        ret, frame = video.read()
        if ret:
            # Convierte el fotograma a formato JPEG
            ret, jpeg = cv2.imencode('.jpg', frame)
            # Genera el fotograma codificado en bytes
            frame_bytes = jpeg.tobytes()
            # Devuelve el fotograma como respuesta al cliente
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')
