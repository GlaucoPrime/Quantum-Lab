"""
Acesso por QR Code na rede local.
Obtém o IP ativo da máquina e gera um QR apontando para http://IP:8501.
"""
import socket
import qrcode
from qrcode.image.pil import PilImage
from io import BytesIO


def get_local_ip() -> str:
    """
    Retorna o IPv4 da interface de rede ativa.
    O truque do socket UDP não envia pacotes de fato;
    apenas força o SO a escolher a interface de saída.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except OSError:
        # fallback: resolução do hostname
        try:
            return socket.gethostbyname(socket.gethostname())
        except OSError:
            return "127.0.0.1"


def build_access_url(port: int = 8501) -> str:
    """Monta a URL de acesso para a rede local."""
    ip = get_local_ip()
    return f"http://{ip}:{port}"


def generate_qr_image(url: str) -> BytesIO:
    """Gera um QR Code PNG em memória."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=8,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white", image_factory=PilImage)
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer