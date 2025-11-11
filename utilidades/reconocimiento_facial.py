import cv2
import face_recognition
import os

class ReconocedorFacial:
    
    def __init__(self, ruta_referencia='rostros_referencia'):
        self.ruta_referencia = ruta_referencia
        self.rostros_codificados = {}
        self.cap = None
        self._cargar_rostros_referencia()

    def _cargar_rostros_referencia(self):
        for nombre_archivo in os.listdir(self.ruta_referencia):
            if nombre_archivo.endswith(('.jpg', '.png')):
                nombre_usuario = os.path.splitext(nombre_archivo)[0]
                ruta_imagen = os.path.join(self.ruta_referencia, nombre_archivo)
                
                imagen = face_recognition.load_image_file(ruta_imagen)
                codificaciones = face_recognition.face_encodings(imagen)
                
                if codificaciones:
                    self.rostros_codificados[nombre_usuario] = codificaciones[0]
                
    def iniciar_camara(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            return False
        return True

    def detener_camara(self):
        if self.cap:
            self.cap.release()
            self.cap = None
            cv2.destroyAllWindows()

    def reconocer_rostro(self):
        if not self.cap:
            return None

        success, frame = self.cap.read()
        if not success:
            return None

        frame_pequeno = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_frame_pequeno = frame_pequeno[:, :, ::-1]

        ubicaciones_rostros = face_recognition.face_locations(rgb_frame_pequeno)
        codificaciones_rostros = face_recognition.face_encodings(rgb_frame_pequeno, ubicaciones_rostros)

        rol_detectado = None

        for codificacion_rostro in codificaciones_rostros:
            nombres_rostros = list(self.rostros_codificados.keys())
            codificaciones_conocidas = list(self.rostros_codificados.values())
            
            coincidencias = face_recognition.compare_faces(codificaciones_conocidas, codificacion_rostro)
            
            if True in coincidencias:
                primer_indice_coincidencia = coincidencias.index(True)
                rol_detectado = nombres_rostros[primer_indice_coincidencia]
                
                top, right, bottom, left = ubicaciones_rostros[0]
                top *= 4; right *= 4; bottom *= 4; left *= 4
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, rol_detectado, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)

        cv2.imshow('Reconocimiento Facial', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.detener_camara()
            return "SALIENDO"

        return rol_detectado