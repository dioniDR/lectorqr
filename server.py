import http.server
import ssl
import os
import socket
import subprocess
import sys
from pathlib import Path

# Configuración
PORT = 8002
HOST = '0.0.0.0'  # Escucha en todas las interfaces

# Nombres de los archivos de certificados
CERT_FILE = 'certificado.pem'
KEY_FILE = 'llave.pem'

def get_ip():
    """Obtiene la dirección IP local del equipo"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # No importa si esta dirección es alcanzable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def generar_certificados():
    """Genera certificados SSL autofirmados si no existen"""
    if os.path.exists(CERT_FILE) and os.path.exists(KEY_FILE):
        print(f"Los certificados ya existen: {CERT_FILE} y {KEY_FILE}")
        return
    
    print("Generando certificados SSL autofirmados...")
    
    # Crear un certificado autofirmado con OpenSSL
    comando = f'openssl req -x509 -newkey rsa:4096 -keyout {KEY_FILE} -out {CERT_FILE} -days 365 -nodes -subj "/CN=localhost"'
    
    try:
        subprocess.run(comando, shell=True, check=True)
        print(f"Certificados generados exitosamente: {CERT_FILE} y {KEY_FILE}")
    except subprocess.CalledProcessError as e:
        print(f"Error al generar certificados: {e}")
        print("\nIntentando método alternativo...")
        
        try:
            # Método alternativo utilizando Python directamente
            from cryptography import x509
            from cryptography.x509.oid import NameOID
            from cryptography.hazmat.primitives import hashes
            from cryptography.hazmat.primitives.asymmetric import rsa
            from cryptography.hazmat.primitives import serialization
            import datetime
            
            # Generar clave privada
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
            )
            
            # Escribir clave privada al archivo
            with open(KEY_FILE, "wb") as f:
                f.write(private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption(),
                ))
            
            # Crear certificado autofirmado
            subject = issuer = x509.Name([
                x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
            ])
            
            cert = x509.CertificateBuilder().subject_name(
                subject
            ).issuer_name(
                issuer
            ).public_key(
                private_key.public_key()
            ).serial_number(
                x509.random_serial_number()
            ).not_valid_before(
                datetime.datetime.utcnow()
            ).not_valid_after(
                datetime.datetime.utcnow() + datetime.timedelta(days=365)
            ).add_extension(
                x509.SubjectAlternativeName([x509.DNSName("localhost")]),
                critical=False,
            ).sign(private_key, hashes.SHA256())
            
            # Escribir certificado al archivo
            with open(CERT_FILE, "wb") as f:
                f.write(cert.public_bytes(serialization.Encoding.PEM))
                
            print(f"Certificados generados exitosamente mediante Python: {CERT_FILE} y {KEY_FILE}")
            
        except Exception as e2:
            print(f"Error en el método alternativo: {e2}")
            print("\nPor favor, instala el paquete 'cryptography' de Python:")
            print("pip install cryptography")
            sys.exit(1)

def verificar_archivos():
    """Verifica que los archivos necesarios existan"""
    # Verificar jsQR.js
    if not os.path.exists('jsQR.js'):
        print("⚠️ ADVERTENCIA: No se encontró el archivo jsQR.js")
        print("Debes tener el archivo jsQR.js en la misma carpeta.")
        print("Verifica que el archivo exista y esté correctamente nombrado.")
        return False
    
    return True

def iniciar_servidor():
    """Inicia el servidor HTTPS"""
    try:
        # Crear el manejador de archivos
        handler = http.server.SimpleHTTPRequestHandler
        
        # Crear el servidor
        httpd = http.server.HTTPServer((HOST, PORT), handler)
        
        # Configurar SSL
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)
        httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
        
        # Mostrar información
        local_ip = get_ip()
        print(f"\n✅ Servidor HTTPS iniciado en:")
        print(f"- Local: https://localhost:{PORT}")
        print(f"- Red:   https://{local_ip}:{PORT}")
        print("\n⚠️ ADVERTENCIA: Como el certificado es autofirmado, verás advertencias de seguridad.")
        print("Para proceder, haz clic en 'Configuración avanzada' y luego 'Proceder a (sitio) de todos modos'")
        print("\nPresiona Ctrl+C para detener el servidor.")
        
        # Iniciar el servidor
        httpd.serve_forever()
        
    except KeyboardInterrupt:
        print("\nServidor detenido.")
    except Exception as e:
        print(f"Error al iniciar el servidor: {e}")

def main():
    """Función principal"""
    print("=== Servidor HTTPS para Lector QR ===")
    
    # Asegurar que estamos en el directorio correcto
    script_dir = Path(__file__).parent.absolute()
    os.chdir(script_dir)
    
    # Si hay un archivo paste.txt pero no index.html, usar paste.txt
    if not os.path.exists('index.html'):
        if os.path.exists('paste.txt'):
            print("Encontrado paste.txt - usándolo como index.html...")
            with open('paste.txt', 'r', encoding='utf-8') as f:
                content = f.read()
            with open('index.html', 'w', encoding='utf-8') as f:
                f.write(content)
            print("Archivo index.html creado a partir de paste.txt.")
    
    # Verificar que los archivos necesarios existan
    if not verificar_archivos():
        sys.exit(1)
    
    # Generar certificados si no existen
    generar_certificados()
    
    # Iniciar el servidor
    iniciar_servidor()

if __name__ == "__main__":
    main()