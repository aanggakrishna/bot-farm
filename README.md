# Discord Message Reader Bot

Bot Discord sederhana yang dapat membaca pesan dari sub-channel tertentu dalam sebuah channel dan menyimpannya ke dalam file log.

## Persyaratan
- Python 3.8 atau lebih baru
- Package yang diperlukan ada di `requirements.txt`

## Cara Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Konfigurasi bot:
- Buat aplikasi bot baru di [Discord Developer Portal](https://discord.com/developers/applications)
- Dapatkan token bot dan salin ke file `.env`
- Dapatkan ID channel utama yang ingin dipantau (Aktifkan mode developer di Discord, klik kanan pada channel, dan pilih "Copy ID")
- Dapatkan ID sub-channel yang ingin dipantau dengan cara yang sama
- Masukkan kedua ID tersebut ke file `.env`:
  - `CHANNEL_ID`: ID channel utama
  - `SUB_CHANNEL_ID`: ID sub-channel yang ingin dipantau

3. Jalankan bot:
```bash
python bot.py
```

## Fitur
- Membaca pesan yang dikirim ke sub-channel tertentu dalam channel yang ditentukan
- Menampilkan pesan beserta informasi pengirimnya di console
- Menyimpan log pesan ke dalam file di folder `logs` dengan format nama file `discord_messages_YYYYMMDD.log`
- Log berisi timestamp, level log, dan isi pesan

## Catatan Keamanan
- Jangan pernah membagikan token bot Anda
- Selalu simpan token dan informasi sensitif di file `.env`
- Tambahkan `.env` ke dalam `.gitignore` jika menggunakan git
- Pertimbangkan untuk menambahkan folder `logs` ke dalam `.gitignore` jika berisi informasi sensitif