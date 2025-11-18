import cv2
import mediapipe as mp
import time

class ReconocedorGestos:
    def __init__(self, cam_index_or_url=0):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
        self.mp_draw = mp.solutions.drawing_utils
        self.cap = None
        self.cam_index_or_url = cam_index_or_url
        self.ultima_deteccion = 0

    def iniciar_camara(self):
        try:
            self.cap = cv2.VideoCapture(self.cam_index_or_url)
            if not self.cap.isOpened():
                raise IOError(f"No se puede abrir la cámara: {self.cam_index_or_url}")
            return True
        except Exception as e:
            print(f"Error al iniciar cámara: {e}")
            self.cap = None
            return False

    def detener_camara(self):
        if self.cap:
            self.cap.release()
            self.cap = None
            cv2.destroyAllWindows()

    def detectar_gesto_pulgar_arriba(self):
        if not self.cap or not self.cap.isOpened():
            return "CÁMARA_NO_DISPONIBLE"
        
        success, img = self.cap.read()
        if not success:
            return None

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(img_rgb)
        
        cv2.putText(img, "Presiona Q para salir", (10, 30), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
        
        gesto_detectado = False
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                
                punto_4_y = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP].y
                punto_3_y = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_IP].y

                if punto_4_y < punto_3_y - 0.08:
                    gesto_detectado = True
                    cv2.putText(img, "PULGAR ARRIBA!", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    
                self.mp_draw.draw_landmarks(img, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

        cv2.imshow("Ventana de Gesto", img)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.detener_camara()
            return "SALIENDO"
            
        return "PULGAR_ARRIBA" if gesto_detectado else "ESPERANDO_GESTO"