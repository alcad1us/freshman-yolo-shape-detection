import cv2
import math
import cvzone
from ultralytics import YOLO

confidence = 0.5
model = YOLO("best.pt")
classNames = ['altigen', 'besgen', 'daire', 'dikdortgen', 'elips', 'kare', 'trombus', 'ucgen', 'yildiz', 'yonca']

video_path = "video11.mp4"  # Kullanılacak video
output_path = "output_video.mp4"  # İşlenmiş video
snapshot_paths = {name: f"{name}.png" for name in classNames}  # Şekil isimlerine göre fotoğraf yolları

cap = cv2.VideoCapture(video_path)

# Video özellikleri
fps = cap.get(cv2.CAP_PROP_FPS)
width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Çıktı video dosyasını oluştur
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # .mp4 formatı için dört karakter kodu
out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

screen_center = (width // 2, height // 2)
tolerance = 20  # Orta nokta ekranın ortasına ne kadar yakın olmalı (piksel cinsinden)

# Fotoğraf çekme kontrolü için set oluştur
captured_classes = set()

while cap.isOpened():
    ret, img = cap.read()
    if not ret:
        break

    # Orta noktayı görsele çiz
    cv2.circle(img, screen_center, 5, (255, 0, 0), -1)
    cv2.putText(img, "0", (screen_center[0] + 10, screen_center[1] + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    results = model(img, stream=True, verbose=False)
    for r in results:  # r bulunan nesne
        boxes = r.boxes  # kutu çiz
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            contour = [[x1, y1], [x2, y1], [x2, y2], [x1, y2]]
            print(f'Kontur: {contour}')

            alan = (x2 - x1) * (y2 - y1)
            print("Alan = " + str(alan))

            ortaNoktaX = x1 + (x2 - x1) // 2
            ortaNoktaY = y1 + (y2 - y1) // 2
            ortaNokta = (ortaNoktaX, ortaNoktaY)
            print(f"OrtaNokta = {ortaNokta}")

            cv2.circle(img, ortaNokta, 5, (0, 255, 0), -1)
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

            w, h = x2 - x1, y2 - y1
            print("W kenari = " + str(w) + " " + "H Kenarı = " + str(h))

            uzaklikX = screen_center[0] - ortaNoktaX
            uzaklikY = screen_center[1] - ortaNoktaY
            print(f"Uzaklık X = {uzaklikX}, Uzaklık Y = {uzaklikY}")

            # Orta noktanın ekran ortasına olan uzaklığının tolerans içinde olup olmadığını kontrol et
            if abs(uzaklikX) < tolerance and abs(uzaklikY) < tolerance:
                conf = math.ceil((box.conf[0] * 100)) / 100
                cls = int(box.cls[0])
                if conf > confidence:
                    print(classNames[cls])
                    if classNames[cls] == 'acik':
                        color = (0, 255, 0)
                    else:
                        color = (0, 0, 255)
                    cvzone.cornerRect(img, (x1, y1, w, h), colorC=color, colorR=color)
                    cvzone.putTextRect(img, f'{classNames[cls].upper()} {int(conf * 100)}%',
                                       (max(0, x1), max(35, y1)), scale=1, thickness=1, colorR=color,
                                       colorB=color)

                    # Şekil orta noktasının ekran ortasına yakın olup olmadığını kontrol et ve fotoğraf çek
                    if classNames[cls] not in captured_classes:
                        cv2.imwrite(snapshot_paths[classNames[cls]], img)
                        captured_classes.add(classNames[cls])
                        print(f"Snapshot taken for {classNames[cls]} at confidence {conf}")

    fps_text = "FPS: {:.2f}".format(fps)
    cv2.putText(img, fps_text, (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    out.write(img)

    # Ekranda görseli göster
    cv2.imshow("Video", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()
