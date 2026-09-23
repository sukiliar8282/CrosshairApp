# CrosshairApp

Aplikasi crosshair overlay ringan untuk Windows yang dibuat menggunakan Python dan PyQt6.

## Fitur

- 4 model crosshair
- Mengubah warna crosshair
- Mengatur ukuran crosshair
- Memindahkan posisi crosshair dengan mouse
- Edit Mode
- Shortcut keyboard global
- Shortcut Guide
- Crosshair otomatis kembali ke tengah saat aplikasi dibuka
- Pengaturan tersimpan otomatis
- Ringan dan sederhana

## Shortcut

| Shortcut | Fungsi |
|---|---|
| F6 | Tampilkan / sembunyikan Shortcut Guide |
| F7 | Membuka pengaturan warna crosshair |
| F8 | Mengaktifkan / menonaktifkan Edit Mode |
| Shift + Alt + 1 | Model Crosshair 1 |
| Shift + Alt + 2 | Model Crosshair 2 |
| Shift + Alt + 3 | Model Crosshair 3 |
| Shift + Alt + 4 | Model Crosshair 4 |
| + / - | Mengubah ukuran crosshair |

## Persyaratan

- Windows
- Python 3.14+
- PyQt6

Install PyQt6:

```bash
pip install PyQt6
Menjalankan Aplikasi

Jalankan:

python main.py
Membuat File EXE

Gunakan PyInstaller:

pyinstaller --onefile --noconsole --name CrosshairApp main.py

File EXE akan berada di folder:

dist/
Konfigurasi

Pengaturan aplikasi akan disimpan otomatis dalam file:

config.json

Pengaturan yang disimpan meliputi:

Ukuran crosshair
Model crosshair
Warna crosshair
Posisi crosshair
