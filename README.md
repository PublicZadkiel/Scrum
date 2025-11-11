Las librerías que le dan vida son Tkinter, OpenCV, y MediaPipe. Siendo Tkinter la biblioteca estandar para la creacion del GUI, incluyendo la pantalla de login y el panel de administración. 
Con la combinación de OpenCV, el cuál gestiona la comunicación con la cámara web o DroidCam y procesa el video, y MediaPipe, que es utilizada para la detección en tiempo real de puntos clave en la mano.
El flujo se activa cuando el usuario selecciona la opción de "Login con Gesto", el Controlador intercepta esta acción y llama a la clase ReconocedorGestos ubicada de la carpeta utilidades. 
Esta, iniciara la cámara a través de OpenCV y comenzara a procesar cada frame del video. MediaPipe detecta las coordenadas de los dedos en el frame. 
El código comprueba si la coordenada Y de la punta del dedo está significativamente por encima de la coordenada Y de su base. 
si la condición se cumple, el método devuelve un estado de "PULGAR_ARRIBA" al Controlador. el cual, al recibir este éxito, completa la autenticación y redirige al usuario a su Vista de Perfil o Administración, dependiendo del rol asignado.

Además, esta también la opción estándar de autenticación mediante contraseña. al elegirla, la Vista de Login envía el nombre de usuario y la contraseña introducidos directamente al Controlador. 
El cuál delegará la tarea de verificación al Modelo.
Utilizando el conector oficial mysql-connector-python, se establece la conexión con el servidor de bases de datos MySQL y ejecuta consultas SQL para verificar las credenciales contra la tabla usuarios. 
si coinciden, el Modelo devuelve el rol del usuario al Controlador, que cargará la vista correspondiente.
Cuando el usuario accede a la Vista de Perfil y cambia sus datos, al guardarlos, la Vista envía la información nueva al Controlador. 
este llama al método de actualización del Modelo, transmitiendo los nuevos valores. el Modelo, luego ejecuta la consulta UPDATE de SQL, interactuando directamente con el servidor para mantener los cambios de manera definitiva en la tabla usuarios. 
Finalmente, el Controlador envia una notificacion a la Vista, que se refresca para mostrar los datos recién guardados.
