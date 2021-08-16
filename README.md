
# Durable K-NN Query Using Grid Index
Tugas Akhir Durable K Nearest Neighbor Query Using Grid Index

## Requirement

 - Python 3

## Instalasi Python

 - Windows [Here](https://realpython.com/installing-python/#how-to-install-python-on-windows)
 - MacOS [Here](https://realpython.com/installing-python/#how-to-install-python-on-macos)
 - Linux [Here](https://realpython.com/installing-python/#how-to-install-python-on-linux)

## Cara Running

 1. Tempatkan berkas `Grid.py`, `Precompute_Main.py`, dan `Compute.py` di direktori yang sama dengan dataset yang akan digunakan.
 2. Jalankan proses ***Data Precomputing*** terlebih dahulu dengan mengeksekusi program `Precompute_Main.py` menggunakan command`python Precompute_Main.py`.
 3. Masukkan besar grid yang akan dibangun.
 4. Pilih dataset yang tersedia (IND, ANT, FC).
 ![Dataset yang tersedia](https://raw.githubusercontent.com/Armunz/TA_Durable_KNN_Query/main/images/dataset%20yang%20tersedia.PNG)
 5. Pilih berkas dataset yang tersedia.
 ![enter image description here](https://raw.githubusercontent.com/Armunz/TA_Durable_KNN_Query/main/images/berkas%20yang%20tersedia.PNG)
 6. Proses ***Data Precomputing*** selesai.
 7. Jalankan proses ***Query Processing*** dengan mengeksekusi program `Compute.py` menggunakan command `python Compute.py`.
 8. Terdapat beberapa parameter masukan, yaitu:
		 - Objek referensi (*sref*)
		 - Jumlah objek yang dicari (*k*)
		 - Timestamp awal (*tb*)
		 - Timestamp akhir (*tc*)
		 - *Durability Threshold*
Disini saya menggunakan dataset `random_50000_2d_ind.csv` dan berikut adalah contoh kueri masukannya.
![Contoh kueri masukan](https://raw.githubusercontent.com/Armunz/TA_Durable_KNN_Query/main/images/contoh%20masukan%20query%20processing.PNG)
 9. Hasil kueri adalah sebagai berikut. ![Contoh hasil kueri](https://raw.githubusercontent.com/Armunz/TA_Durable_KNN_Query/main/images/contoh%20hasil%20query%20processing.PNG)
 10. Selesai.

