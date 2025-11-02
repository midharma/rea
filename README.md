# Setup AIO Bots

Panduan lengkap untuk setup dan menjalankan **AIO Bots** di Linux menggunakan **virtual environment (venv)**.

---

## Mengapa Virtual Environment?
Virtual environment berfungsi untuk **mengisolasi library Python**.  
Artinya, library yang diinstall di satu proyek tidak akan mengganggu proyek lain.

---

## Langkah-langkah Setup

1. **Update paket sistem**  
```bash
sudo apt-get update
```
> Update `package`

2. **Upgrade semua paket** 
```bash
sudo apt-get upgrade -y
```
> Upgrade `package`.

3. **Install Python dan FFMPEG** 
```bash
sudo apt-get install python3-pip ffmpeg -y
```
> Install paket `PYTHON` dan `FFMPEG`.

4. **Install virtualenv**
```bash
sudo apt-get install python3-virtualenv -y
```
> Install paket `venv`. 

5. **Clone repository bot** 
```bash
git clone <url_repo>
```
> Memasukan repository ke VPS.

6. **Buat screen session baru**
```bash
screen -S nama_screen
```
> Membuat screen.

7. **Masuk ke screen session**
```bash
screen -x nama_screen
```
> Masuk ke screen.

8. **Masuk ke folder repository**
```bash
cd nama_repo
```
> Masuk ke folder bot.

9. **Buat virtual environment**
```bash
virtualenv venv
```
> Membuat folder `venv` untuk semua library proyek ini.

10. **Aktifkan virtual environment** 
```bash
. venv/bin/activate 
``` 
> Semua `pip install` selanjutnya hanya berlaku di environment ini.

11. **Install semua dependensi**
```bash
pip3 install -U -r bahan.txt
```
> Install semua `library` kebutuhan bot ini.

12. **Jalankan bot**
```bash
bash start.sh
```
> Langkah akhir menjalankan bot.

## Catatan
- Untuk keluar dari virtual environment:  
deactivate

- Gunakan **screen** agar bot tetap berjalan meski terminal ditutup.  
- Setiap buka terminal baru, aktifkan dulu `venv` sebelum menjalankan bot.

Bot sekarang siap dijalankan!

