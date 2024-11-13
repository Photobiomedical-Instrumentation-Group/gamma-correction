import cv2

def extrair_frame(video_path, frame_number, output_image_path):
    # Carrega o vídeo
    video = cv2.VideoCapture(video_path)

    # Verifica se o vídeo foi carregado corretamente
    if not video.isOpened():
        print("Erro ao abrir o vídeo.")
        return

    # Define o frame a ser extraído
    video.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

    # Lê o frame
    ret, frame = video.read()

    # Verifica se o frame foi lido com sucesso
    if ret:
        # Salva o frame como imagem
        cv2.imwrite(output_image_path, frame)
        print(f"Frame {frame_number} salvo como {output_image_path}")
    else:
        print(f"Não foi possível ler o frame {frame_number}")

    # Libera o vídeo
    video.release()

# Exemplo de uso
video_path = 'Desp.mp4'  # Caminho para o vídeo
frame_number = 10 # Número do frame desejado
output_image_path = 'frame_extraido.jpg'  # Caminho para salvar o frame

extrair_frame(video_path, frame_number, output_image_path)
