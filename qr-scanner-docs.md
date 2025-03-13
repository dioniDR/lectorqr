# QRScannerLib - Documentación

QRScannerLib es una biblioteca extendida que proporciona una API amigable para el escaneo y procesamiento de códigos QR usando jsQR como base.

## Índice

1. [Requisitos](#requisitos)
2. [Instalación](#instalación)
3. [Uso Básico](#uso-básico)
4. [Opciones de Configuración](#opciones-de-configuración)
5. [Casos de Uso Específicos](#casos-de-uso-específicos)
   - [Escaneo con Cámara](#escaneo-con-cámara)
   - [Escaneo de Imágenes](#escaneo-de-imágenes)
   - [Escaneo de Archivos](#escaneo-de-archivos)
   - [Escáner Autónomo](#escáner-autónomo)
   - [Control del Flash](#control-del-flash)
   - [Cambio de Cámara](#cambio-de-cámara)
   - [Historial de Escaneos](#historial-de-escaneos)
   - [Procesamiento Manual](#procesamiento-manual)
6. [Gestión de Resultados](#gestión-de-resultados)
7. [API Completa](#api-completa)
8. [Ejemplos](#ejemplos)
9. [Solución de Problemas](#solución-de-problemas)

## Requisitos

- Navegador moderno con soporte para:
  - Canvas API
  - getUserMedia (acceso a la cámara)
  - ES6+
- Biblioteca [jsQR](https://github.com/cozmo/jsQR) incluida antes de QRScannerLib

## Instalación

1. Incluya jsQR en su proyecto:

```html
<script src="jsQR.js"></script>
```

2. Incluya QRScannerLib:

```html
<script src="QRScannerLib.js"></script>
```

## Uso Básico

```javascript
// Crear una instancia con opciones básicas
const scanner = new QRScannerLib({
    videoElementId: 'video-element', // ID del elemento <video> para mostrar la cámara
    outputElementId: 'result-element', // ID del elemento para mostrar resultados
    onFound: function(result) {
        console.log('Código QR encontrado:', result.data);
    }
});

// Iniciar el escaneo
scanner.start();

// Para detener el escaneo
// scanner.stop();
```

## Opciones de Configuración

```javascript
const scanner = new QRScannerLib({
    // Elementos DOM
    videoElementId: 'video-element', // ID del elemento video para la cámara
    canvasElementId: 'canvas-element', // ID del elemento canvas (opcional)
    outputElementId: 'result-element', // ID del elemento para resultados (opcional)
    
    // Configuración de comportamiento
    debug: false, // Habilitar modo de depuración
    scanRegion: 'full', // Región de escaneo: 'full', 'center', 'auto'
    scanInterval: 100, // Intervalo entre escaneos en ms
    successTolerance: 3, // Número de escaneos exitosos necesarios para confirmar
    autoStart: false, // Iniciar automáticamente al crear la instancia
    autoStop: false, // Detener automáticamente después de encontrar un código
    beepOnSuccess: false, // Reproducir sonido al encontrar un código
    vibrate: false, // Vibrar al encontrar un código
    timeout: 0, // Timeout en ms (0 = sin timeout)
    
    // Configuración de visualización
    highlightCode: true, // Resaltar código encontrado en el canvas
    highlightColor: '#FF5722', // Color para resaltar el código
    drawOutline: true, // Dibujar contorno alrededor del código
    
    // Configuración de la cámara
    facingMode: 'environment', // 'environment' (trasera) o 'user' (frontal)
    resolution: 'hd', // 'sd', 'hd', 'full-hd'
    
    // Configuración de jsQR
    inversionAttempts: 'attemptBoth', // 'attemptBoth', 'dontInvert', 'onlyInvert', 'invertFirst'
    
    // Callbacks
    onFound: function(result) {}, // Callback al encontrar un código
    onError: function(error) {} // Callback en caso de error
});
```

## Casos de Uso Específicos

### Escaneo con Cámara

```javascript
// HTML necesario
// <video id="camera"></video>
// <div id="result"></div>

const scanner = new QRScannerLib({
    videoElementId: 'camera',
    outputElementId: 'result',
    beepOnSuccess: true,
    highlightCode: true,
    onFound: (result) => {
        alert(`Código escaneado: ${result.data}`);
    }
});

// Iniciar cámara y escaneo
scanner.start().then(() => {
    console.log('Escaneo iniciado');
}).catch(error => {
    console.error('Error al iniciar el escaneo:', error);
});

// Para detener
document.getElementById('stop-button').addEventListener('click', () => {
    scanner.stop();
});
```

### Escaneo de Imágenes

```javascript
// HTML necesario
// <img id="qr-image" src="ruta/a/imagen-con-qr.png">

const scanner = new QRScannerLib();
const imgElement = document.getElementById('qr-image');

// Escanear una imagen desde un elemento <img>
imgElement.onload = () => {
    const result = scanner.scanImageElement(imgElement);
    if (result) {
        console.log('Código QR encontrado:', result.data);
    } else {
        console.log('No se encontró ningún código QR');
    }
};

// Escanear una imagen desde URL
scanner.scanImageFromUrl('https://ejemplo.com/imagen-qr.png')
    .then(result => {
        if (result) {
            console.log('Código QR encontrado:', result.data);
        } else {
            console.log('No se encontró ningún código QR');
        }
    })
    .catch(error => {
        console.error('Error al escanear la imagen:', error);
    });
```

### Escaneo de Archivos

```javascript
// HTML necesario
// <input type="file" id="file-input" accept="image/*">

const scanner = new QRScannerLib();
const fileInput = document.getElementById('file-input');

fileInput.addEventListener('change', (event) => {
    const file = event.target.files[0];
    
    if (file) {
        scanner.scanImageFile(file)
            .then(result => {
                if (result) {
                    console.log('Código QR encontrado:', result.data);
                } else {
                    console.log('No se encontró ningún código QR');
                }
            })
            .catch(error => {
                console.error('Error al escanear el archivo:', error);
            });
    }
});
```

### Escáner Autónomo

QRScannerLib proporciona un método estático para crear un escáner completo autónomo en un contenedor especificado:

```javascript
// HTML necesario
// <div id="qr-container"></div>

// Crear un escáner autónomo con controles
const scanner = QRScannerLib.createStandalone('#qr-container', {
    onFound: (result) => {
        alert(`Código escaneado: ${result.data}`);
    },
    highlightCode: true,
    beepOnSuccess: true
});

// El método crea todos los elementos necesarios dentro del contenedor
// y devuelve una instancia de QRScannerLib
```

### Control del Flash

```javascript
// Alternar el flash (torch) de la cámara
const toggleFlashButton = document.getElementById('toggle-flash');

toggleFlashButton.addEventListener('click', () => {
    scanner.toggleFlash()
        .then(isOn => {
            console.log('Flash ' + (isOn ? 'encendido' : 'apagado'));
            toggleFlashButton.textContent = isOn ? 'Apagar Flash' : 'Encender Flash';
        })
        .catch(error => {
            console.error('Error al alternar el flash:', error);
            alert('Este dispositivo no soporta control del flash');
        });
});
```

### Cambio de Cámara

```javascript
// Alternar entre cámara frontal y trasera
const switchCameraButton = document.getElementById('switch-camera');

switchCameraButton.addEventListener('click', () => {
    scanner.switchCamera()
        .then(() => {
            console.log('Cámara cambiada');
        })
        .catch(error => {
            console.error('Error al cambiar la cámara:', error);
            alert('No se puede cambiar la cámara. Es posible que solo haya una disponible.');
        });
});

// Verificar si el dispositivo admite cambio de cámara
if (scanner.getState().supportsCameraSwitch) {
    switchCameraButton.style.display = 'block';
} else {
    switchCameraButton.style.display = 'none';
}
```

### Historial de Escaneos

```javascript
// Obtener el historial de escaneos
const history = scanner.getHistory();
console.log('Historial de escaneos:', history);

// Cada elemento del historial contiene:
// {
//   data: string,         // Contenido del código QR
//   timestamp: number,    // Timestamp en milisegundos
//   contentType: string   // Tipo de contenido detectado
// }

// Limpiar el historial
scanner.clearHistory();

// Cambiar el tamaño máximo del historial (por defecto 20)
scanner.setHistoryMaxSize(50);

// Mostrar el historial en la interfaz
function showHistory() {
    const history = scanner.getHistory();
    const historyList = document.getElementById('history-list');
    
    historyList.innerHTML = '';
    
    history.forEach(item => {
        const li = document.createElement('li');
        const date = new Date(item.timestamp);
        li.innerHTML = `
            <strong>${item.contentType}</strong>: 
            ${item.data} 
            <small>(${date.toLocaleString()})</small>
        `;
        historyList.appendChild(li);
    });
}
```

### Procesamiento Manual

```javascript
// Procesar manualmente un texto como si fuera un código QR escaneado
const manualInput = document.getElementById('manual-input');
const processButton = document.getElementById('process-button');

processButton.addEventListener('click', () => {
    const text = manualInput.value.trim();
    
    if (text) {
        const result = scanner.processQRData(text);
        console.log('Procesado manualmente:', result);
    }
});
```

## Gestión de Resultados

El objeto `result` devuelto al encontrar un código QR contiene:

```javascript
{
    data: "Contenido del código QR",
    timestamp: 1678901234567,
    format: "QR_CODE",
    contentType: "URL", // Tipo detectado: URL, TEXT, EMAIL, WIFI, etc.
    location: {
        topLeftCorner: {x, y},
        topRightCorner: {x, y},
        bottomLeftCorner: {x, y},
        bottomRightCorner: {x, y}
    },
    // Campos originales de jsQR
    binaryData: Uint8ClampedArray,
    chunks: [...],
    version: number
}
```

La biblioteca detecta automáticamente el tipo de contenido, pudiendo ser:
- `URL`: Una dirección web
- `EMAIL`: Una dirección de correo o mailto:
- `PHONE`: Un número de teléfono o tel:
- `SMS`: Un enlace SMS
- `WIFI`: Configuración WiFi
- `CONTACT`: Tarjeta de contacto (vCard)
- `GEO`: Ubicación geográfica
- `CALENDAR`: Evento de calendario
- `JSON`: Contenido JSON
- `TEXT`: Texto plano u otro formato no específico

Ejemplo de procesamiento por tipo:

```javascript
scanner.setOptions({
    onFound: (result) => {
        switch (result.contentType) {
            case 'URL':
                window.open(result.data, '_blank');
                break;
            case 'EMAIL':
                window.location.href = result.data;
                break;
            case 'PHONE':
                if (confirm('¿Llamar al número ' + result.data.replace('tel:', '') + '?')) {
                    window.location.href = result.data;
                }
                break;
            case 'WIFI':
                displayWifiInfo(result.data);
                break;
            default:
                displayResult(result.data);
                break;
        }
    }
});

// Función para extraer información WiFi
function displayWifiInfo(data) {
    // Ejemplo: WIFI:S:NombreRed;T:WPA;P:Contraseña;;
    const ssid = data.match(/S:(.*?);/)[1];
    const pass = data.match(/P:(.*?);/)[1];
    const type = data.match(/T:(.*?);/)[1];
    
    alert(`Red WiFi: ${ssid}\nContraseña: ${pass}\nTipo: ${type}`);
}
```

## API Completa

### Constructor
```javascript
const scanner = new QRScannerLib(options);
```

### Métodos Principales
- `start()`: Inicia el escaneo con la cámara. Devuelve una Promise.
- `stop()`: Detiene el escaneo.
- `scanImageElement(element)`: Escanea una imagen desde un elemento HTML.
- `scanImageFromUrl(url)`: Escanea una imagen desde una URL. Devuelve una Promise.
- `scanImageFile(file)`: Escanea una imagen desde un archivo File. Devuelve una Promise.
- `switchCamera()`: Cambia entre cámara frontal y trasera. Devuelve una Promise.
- `toggleFlash()`: Activa/desactiva el flash. Devuelve una Promise con el estado (true/false).
- `getState()`: Devuelve el estado actual del escáner.
- `setOptions(options)`: Actualiza las opciones de configuración.

### Métodos para Historial
- `getHistory()`: Obtiene el historial de escaneos.
- `clearHistory()`: Limpia el historial de escaneos.
- `setHistoryMaxSize(size)`: Establece el tamaño máximo del historial.

### Método para Procesamiento Manual
- `processQRData(data)`: Procesa un texto como si fuera un código QR escaneado.

### Método Estático
- `QRScannerLib.createStandalone(container, options)`: Crea un escáner autónomo con interfaz incluida.

## Ejemplos

### Ejemplo Completo con Interfaz de Usuario

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Escáner QR Completo</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        .scanner-container {
            position: relative;
            width: 100%;
            max-width: 500px;
            margin: 0 auto;
        }
        #qr-video {
            width: 100%;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        #qr-result {
            margin-top: 20px;
            padding: 15px;
            background-color: #f5f5f5;
            border-radius: 4px;
            word-break: break-all;
        }
        .controls {
            margin-top: 15px;
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }
        button {
            padding: 8px 16px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:disabled {
            background-color: #cccccc;
        }
        #file-input {
            display: none;
        }
        .file-label {
            padding: 8px 16px;
            background-color: #2196F3;
            color: white;
            border-radius: 4px;
            cursor: pointer;
        }
        #history-container {
            margin-top: 30px;
        }
        #history-list {
            max-height: 200px;
            overflow-y: auto;
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 10px;
        }
    </style>
</head>
<body>
    <h1>Escáner de Códigos QR</h1>
    
    <div class="scanner-container">
        <video id="qr-video"></video>
        <canvas id="qr-canvas" style="display: none;"></canvas>
    </div>
    
    <div id="qr-result">El resultado aparecerá aquí</div>
    
    <div class="controls">
        <button id="start-button">Iniciar Cámara</button>
        <button id="stop-button" disabled>Detener Cámara</button>
        <button id="switch-camera" disabled>Cambiar Cámara</button>
        <button id="toggle-flash" disabled>Flash</button>
        <label for="file-input" class="file-label">Cargar Imagen</label>
        <input type="file" id="file-input" accept="image/*">
    </div>
    
    <div id="history-container">
        <h2>Historial de Escaneos</h2>
        <ul id="history-list"></ul>
        <button id="clear-history">Limpiar Historial</button>
    </div>

    <script src="jsQR.js"></script>
    <script src="QRScannerLib.js"></script>
    <script>
        // Elementos DOM
        const startButton = document.getElementById('start-button');
        const stopButton = document.getElementById('stop-button');
        const switchCameraButton = document.getElementById('switch-camera');
        const toggleFlashButton = document.getElementById('toggle-flash');
        const fileInput = document.getElementById('file-input');
        const resultElement = document.getElementById('qr-result');
        const historyList = document.getElementById('history-list');
        const clearHistoryButton = document.getElementById('clear-history');
        
        // Crear instancia del escáner
        const scanner = new QRScannerLib({
            videoElementId: 'qr-video',
            canvasElementId: 'qr-canvas',
            beepOnSuccess: true,
            highlightCode: true,
            vibrate: true,
            onFound: (result) => {
                resultElement.innerHTML = `
                    <strong>Contenido:</strong> ${result.data}<br>
                    <strong>Tipo:</strong> ${result.contentType}<br>
                    <strong>Tiempo:</strong> ${new Date(result.timestamp).toLocaleTimeString()}
                `;
                updateHistoryDisplay();
            },
            onError: (error) => {
                console.error('Error en el escáner:', error);
                resultElement.innerHTML = `<span style="color: red;">Error: ${error.message}</span>`;
            }
        });
        
        // Iniciar cámara
        startButton.addEventListener('click', () => {
            startButton.disabled = true;
            resultElement.innerHTML = 'Iniciando cámara...';
            
            scanner.start().then(() => {
                stopButton.disabled = false;
                toggleFlashButton.disabled = false;
                
                // Verificar si se soporta el cambio de cámara
                if (scanner.getState().supportsCameraSwitch) {
                    switchCameraButton.disabled = false;
                }
            }).catch(error => {
                startButton.disabled = false;
                resultElement.innerHTML = `<span style="color: red;">Error al iniciar la cámara: ${error.message}</span>`;
            });
        });
        
        // Detener cámara
        stopButton.addEventListener('click', () => {
            scanner.stop();
            startButton.disabled = false;
            stopButton.disabled = true;
            switchCameraButton.disabled = true;
            toggleFlashButton.disabled = true;
        });
        
        // Cambiar cámara
        switchCameraButton.addEventListener('click', () => {
            scanner.switchCamera()
                .catch(error => {
                    console.error('Error al cambiar la cámara:', error);
                });
        });
        
        // Alternar flash
        toggleFlashButton.addEventListener('click', () => {
            scanner.toggleFlash()
                .then(isOn => {
                    toggleFlashButton.textContent = isOn ? 'Flash On' : 'Flash Off';
                })
                .catch(error => {
                    console.error('Error con el flash:', error);
                    alert('Este dispositivo no soporta control del flash');
                });
        });
        
        // Escanear desde archivo
        fileInput.addEventListener('change', (event) => {
            const file = event.target.files[0];
            if (file) {
                resultElement.innerHTML = 'Procesando imagen...';
                
                scanner.scanImageFile(file)
                    .then(result => {
                        if (result) {
                            resultElement.innerHTML = `
                                <strong>Contenido:</strong> ${result.data}<br>
                                <strong>Tipo:</strong> ${result.contentType}<br>
                                <strong>Origen:</strong> Archivo
                            `;
                            
                            // Añadir al historial manualmente
                            scanner.processQRData(result.data);
                            updateHistoryDisplay();
                        } else {
                            resultElement.innerHTML = 'No se encontró ningún código QR en la imagen';
                        }
                    })
                    .catch(error => {
                        resultElement.innerHTML = `<span style="color: red;">Error al procesar la imagen: ${error.message}</span>`;
                    });
            }
        });
        
        // Limpiar historial
        clearHistoryButton.addEventListener('click', () => {
            scanner.clearHistory();
            updateHistoryDisplay();
        });
        
        // Actualizar visualización del historial
        function updateHistoryDisplay() {
            const history = scanner.getHistory();
            historyList.innerHTML = '';
            
            if (history.length === 0) {
                historyList.innerHTML = '<li>No hay escaneos en el historial</li>';
                return;
            }
            
            history.forEach(item => {
                const li = document.createElement('li');
                const date = new Date(item.timestamp);
                li.innerHTML = `
                    <strong>${item.contentType}</strong>: 
                    ${item.data.length > 50 ? item.data.substring(0, 50) + '...' : item.data} 
                    <small>(${date.toLocaleTimeString()})</small>
                `;
                historyList.appendChild(li);
            });
        }
        
        // Inicializar historial
        updateHistoryDisplay();
    </script>
</body>
</html>
```

### Ejemplo Sencillo para Integración en Formularios

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Escaneo QR para Formulario</title>
    <style>
        .form-group {
            margin-bottom: 15px;
        }
        .qr-container {
            max-width: 400px;
            margin: 20px 0;
            display: none;
        }
        video {
            width: 100%;
            border: 1px solid #ddd;
        }
    </style>
</head>
<body>
    <h1>Formulario con Escaneo QR</h1>
    
    <form id="data-form">
        <div class="form-group">
            <label for="code">Código de Producto:</label>
            <input type="text" id="code" name="code" required>
            <button type="button" id="scan-button">Escanear QR</button>
        </div>
        
        <div class="form-group">
            <label for="quantity">Cantidad:</label>
            <input type="number" id="quantity" name="quantity" min="1" value="1">
        </div>
        
        <button type="submit">Enviar</button>
    </form>
    
    <div id="qr-container" class="qr-container">
        <h3>Escanee el código QR</h3>
        <video id="qr-video"></video>
        <button type="button" id="close-scanner">Cerrar</button>
    </div>
    
    <script src="jsQR.js"></script>
    <script src="QRScannerLib.js"></script>
    <script>
        // Elementos
        const scanButton = document.getElementById('scan-button');
        const closeButton = document.getElementById('close-scanner');
        const qrContainer = document.getElementById('qr-container');
        const codeInput = document.getElementById('code');
        const form = document.getElementById('data-form');
        
        // Inicializar escáner
        const scanner = new QRScannerLib({
            videoElementId: 'qr-video',
            autoStop: true,
            highlightCode: true,
            beepOnSuccess: true,
            onFound: (result) => {
                codeInput.value = result.data;
                qrContainer.style.display = 'none';
            },
            onError: (error) => {
                alert('Error: ' + error.message);
            }
        });
        
        // Mostrar escáner
        scanButton.addEventListener('click', (e) => {
            e.preventDefault();
            qrContainer.style.display = 'block';
            
            scanner.start().catch(error => {
                alert('Error al iniciar la cámara: ' + error.message);
                qrContainer.style.display = 'none';
            });
        });
        
        // Cerrar escáner
        closeButton.addEventListener('click', () => {
            scanner.stop();
            qrContainer.style.display = 'none';
        });
        
        // Manejar envío del formulario
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            alert(`Formulario enviado con código: ${codeInput.value} y cantidad: ${document.getElementById('quantity').value}`);
            // Aquí iría la lógica para enviar el formulario
        });
    </script>
</body>
</html>
```

## Solución de Problemas

### La cámara no se inicia

- Asegúrese de que el sitio se esté ejecutando en un entorno seguro (HTTPS o localhost)
- El usuario debe conceder permiso para usar la cámara
- Algunos navegadores no soportan getUserMedia en pestañas inactivas o en segundo plano

### No se detectan códigos QR

- Asegúrese de que el código QR esté bien iluminado
- Intente ajustar la distancia entre la cámara y el código
- Verifique que la opción `inversionAttempts` esté configurada como "attemptBoth"
- Pruebe con diferentes valores para `scanRegion` y `successTolerance`

### Problemas de rendimiento

- Reduzca la resolución (options.resolution = 'sd')
- Aumente el intervalo de escaneo (options.scanInterval = 200)
- Configure scanRegion a 'center' para procesar menos área

### Error al cargar archivos grandes

- Las imágenes muy grandes pueden causar problemas de memoria
- Intente reducir el tamaño de la imagen antes de procesarla

### El flash no funciona

- La API de flash solo está disponible en dispositivos con cámara y flash físico
- No todos los navegadores admiten el control del flash

### Errores en dispositivos iOS

- iOS tiene restricciones adicionales para getUserMedia
- Asegúrese de que el elemento de video tenga el atributo `playsinline`
- En iOS, solo funciona en Safari o WebView de Safari
