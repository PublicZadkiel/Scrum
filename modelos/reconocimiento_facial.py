import cv2
import face_recognition
import os
import numpy as np

class ReconocedorFacial:
    
    def __init__(self):
        self.captura = None
        self.ruta_referencia = "vistas/rostros_referencia"
        self.codificaciones_referencia = []
        self.nombres_referencia = []
        self._cargar_rostros_referencia()
        
    def _cargar_rostros_referencia(self):
        self.codificaciones_referencia = []
        self.nombres_referencia = []
        
        for nombre_archivo in os.listdir(self.ruta_referencia):
            if nombre_archivo.endswith((".jpg", ".png", ".jpeg")):
                ruta_imagen = os.path.join(self.ruta_referencia, nombre_archivo)
                imagen = face_recognition.load_image_file(ruta_imagen)
                
                codificaciones = face_recognition.face_encodings(imagen)
                
                if codificaciones:
                    nombre_usuario = os.path.splitext(nombre_archivo)[0]
                    self.codificaciones_referencia.append(codificaciones[0])
                    self.nombres_referencia.append(nombre_usuario)

    def iniciar_camara(self):
        if self.captura is None:
            self.captura = cv2.VideoCapture(0)
        return self.captura.isOpened()

    def detener_camara(self):
        if self.captura is not None:
            self.captura.release()
            self.captura = None
            cv2.destroyAllWindows()

    def reconocer_rostro(self):
        if self.captura is None or not self.captura.isOpened():
            return "ESPERANDO"

        ret, frame = self.captura.read()
        
        if not ret:
            return "ESPERANDO" 
        
        frame_pequeno = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        
        rgb_frame_pequeno = cv2.cvtColor(frame_pequeno, cv2.COLOR_BGR2RGB)
        
        ubicaciones_rostros = face_recognition.face_locations(rgb_frame_pequeno)

        if ubicaciones_rostros:
            for (top, right, bottom, left) in ubicaciones_rostros:
                top *= 2
                right *= 2
                bottom *= 2
                left *= 2
                cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)

        try:
            codificaciones_rostros = face_recognition.face_encodings(rgb_frame_pequeno, ubicaciones_rostros)
        except TypeError:
            cv2.imshow("Reconocimiento Facial", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                return "SALIENDO"
            return "ESPERANDO"

        nombre_coincidente = None
        
        for codificacion_rostro in codificaciones_rostros:
            
            coincidencias = face_recognition.compare_faces(self.codificaciones_referencia, codificacion_rostro, tolerance=0.80) 
            
            if True in coincidencias:
                primer_coincidencia_index = coincidencias.index(True)
                nombre_coincidente = self.nombres_referencia[primer_coincidencia_index]
                break

        cv2.imshow("Reconocimiento Facial", frame)
        
        if nombre_coincidente:
            return nombre_coincidente

        if cv2.waitKey(1) & 0xFF == ord('q'):
            return "SALIENDO"

        return "ESPERANDO"