# Discord Message Monitor Client

Client Discord sederhana yang dapat memantau aktivitas pesan dan pengguna secara real-time dari thread/sub-channel dalam sebuah channel menggunakan akun user.

## Persyaratan
- Python 3.8 atau lebih baru
- Package yang diperlukan ada di `requirements.txt`

## Cara Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Konfigurasi client:
- Dapatkan User Token Discord Anda (Lihat panduan di bawah)
- Masukkan token ke file `.env` pada variabel `DISCORD_USER_TOKEN`
- Dapatkan ID channel utama yang ingin dipantau (Aktifkan mode developer di Discord, klik kanan pada channel, dan pilih "Copy ID")
- Dapatkan ID thread/sub-channel yang ingin dipantau dengan cara yang sama
- Masukkan kedua ID tersebut ke file `.env`:
  - `CHANNEL_ID`: ID channel utama
  - `SUB_CHANNEL_ID`: ID thread/sub-channel yang ingin dipantau

3. Pilih mode yang ingin digunakan:
- Untuk monitoring lengkap (pesan, edit, hapus, user join/leave):
  ```bash
  python monitor.py
  ```
- Untuk memantau pesan secara real-time saja:
  ```bash
  python client.py
  ```
- Untuk mengambil history pesan dan memantau pesan baru:
  ```bash
  python thread_reader.py
  ```

## Cara Mendapatkan User Token
1. Buka Discord di browser web
2. Tekan F12 untuk membuka Developer Tools
3. Pilih tab "Network"
4. Refresh halaman
5. Cari request yang mengandung "api/v9"
6. Lihat header "Authorization" - ini adalah user token Anda

## Fitur

### Monitor.py (Full Monitoring)
- Memantau semua aktivitas secara real-time:
  - Pesan baru yang dikirim
  - Pesan yang diedit
  - Pesan yang dihapus
  - User yang bergabung ke server
  - User yang meninggalkan server
- Mencatat detail pengguna (nama dan ID)
- Mencatat attachment yang dikirim
- Membuat file log baru untuk setiap sesi dengan timestamp
- Menampilkan log secara real-time di console

### Client.py (Simple Monitor)
- Memantau pesan yang dikirim ke thread/sub-channel tertentu secara real-time
- Menampilkan pesan beserta informasi pengirimnya di console
- Mencatat attachment yang dikirim dalam pesan

### Thread_reader.py (History + Monitor)
- Mengambil seluruh history pesan dari thread/sub-channel
- Menampilkan waktu pengiriman setiap pesan
- Memantau pesan baru yang masuk setelah client berjalan
- Mencatat attachment yang dikirim dalam pesan

### Format Log
- Semua log disimpan di folder `logs`
- Format nama file:
  - Monitor: `discord_monitor_YYYYMMDD_HHMMSS.log`
  - Client: `discord_messages_YYYYMMDD.log`
  - Thread Reader: `discord_thread_messages_YYYYMMDD.log`
- Log berisi:
  - Timestamp kejadian
  - Jenis aktivitas
  - Detail pengguna (nama dan ID)
  - Isi pesan atau deskripsi aktivitas

## Catatan Keamanan
- **PENTING**: Jangan pernah membagikan User Token Anda dengan siapapun
- User Token memberikan akses penuh ke akun Discord Anda
- Selalu simpan token dan informasi sensitif di file `.env`
- Tambahkan `.env` ke dalam `.gitignore`
- Pertimbangkan untuk menambahkan folder `logs` ke dalam `.gitignore` jika berisi informasi sensitif

## Peringatan
- Menggunakan user token untuk automasi dapat melanggar Ketentuan Layanan Discord
- Gunakan dengan bijak dan pada risiko Anda sendiri