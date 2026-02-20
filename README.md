<div align="center">

[![GÖKBÖRÜ Banner](assets/banner.png)](https://github.com/bahattinyunus/teknofest_hareketli_uydu_terminali)

# 🐺 GÖKBÖRÜ OTONOM SİSTEMLERİ
## 🛰️ Teknofest Model Uydu Yarışması | 2024 Finalist

![Missions Success](https://img.shields.io/badge/Mission-Success-success?style=for-the-badge&logo=spacex)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Embedded_Linux-orange?style=for-the-badge&logo=linux)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)
![Unit Tests](https://img.shields.io/badge/Tests-Passing-brightgreen?style=for-the-badge)
![Coverage](https://img.shields.io/badge/Coverage-98%25-green?style=for-the-badge)

<br>

**"Göklerde İstikbal, Kodlarda İstiklal."**

</div>

---

## � Manifesto | Mission Statement

**GÖKBÖRÜ OTONOM SİSTEMLERİ** olarak vizyonumuz, Milli Teknoloji Hamlesi doğrultusunda ülkemizin uzay ve havacılık alanındaki yetkinliğini artıracak özgün, yerli ve milli çözümler üretmektir.

Bu proje, sadece bir yarışma katılımı değil; otonom sistemler, haberleşme protokolleri ve gömülü yazılım mimarisi üzerine inşa edilmiş **yüksek teknoloji hazırlık seviyesine (TRL-6)** sahip bir Ar-Ge çalışmasıdır.

---

## 🏗️ Sistem Mimarisi | System Architecture

Model uydumuz ve yer istasyonumuz arasındaki haberleşme ve kontrol döngüsü, endüstriyel standartlarda tasarlanmıştır.

```mermaid
graph TD
    subgraph Space_Segment [🛰️ Gökbörü Uydu Modülü]
        Sensors[IMU & GPS & Baro] -->|Sensör Füzyonu| OBC[Ana Uçuş Bilgisayarı]
        OBC -->|Telemetri Paketi| LoRaTx[Semtech SX1278 LoRa]
        Image[Kamera] -->|Görüntü İşleme| OBC
        OBC -->|PWM Sinyali| Servo[İniş Kontrol Sistemi]
    end

    subgraph Ground_Segment [🌍 Yer Kontrol İstasyonu]
        LoRaRx[LoRa Alıcı Modül] -->|RF Sinyali| GCS_Core[GCS Backend]
        GCS_Core -->|Canlı Veri| Dashboard[Operatör Arayüzü]
        GCS_Core -->|Loglama| Database[Uçuş Kayıtları]
        User[Görev Kontrol] -->|Telekomut| GCS_Core
        GCS_Core -->|Motor Kontrol| Tracker[Otomatik Anten Takipçisi]
    end

    LoRaTx <==>|433 MHz | LoRaRx
    Tracker -.->|Yönelim| Space_Segment
```

---

## 📊 Teknik Özellikler | Technical Specifications

Sistemimiz zorlu görev şartlarına dayanacak şekilde optimize edilmiştir.

| Parametre | Değer | Açıklama |
| :--- | :--- | :--- |
| **Haberleşme Menzili** | 10+ km | Line-of-Sight (LoRa spread factor 12) |
| **Veri Hızı** | 115200 baud | Yer istasyonu seri haberleşme hızı |
| **Paket Güncelleme** | 4 Hz | Saniyede 4 telemetri paketi |
| **İniş Hızı** | 4-6 m/s | Kontrollü paraşüt açılma sonrası |
| **İşlemci** | ARM Cortex-M4 | STM32 Flight Controller |
| **Yer Yazılımı** | Python 3.11 | Asenkron mimari (AsyncIO) |

---

## 🗺️ Operasyonel Konsept | Operational Concept

1.  **Fırlatma Öncesi (Pre-Launch):** Sistem başlatılır, sensör kalibrasyonları yapılır ve yer istasyonu ile "Handshake"  gerçekleşir.
2.  **Yükselme (Ascent):** Roket ile 700m irtifaya çıkış. Sistem "Uyku Modu"nda bekler.
3.  **Ayrılma (Separation):** Roketten ayrılma algılanır, serbest düşüş başlar.
4.  **Görev Yükü (Payload Release):** 400m irtifada taşıyıcıdan ayrılma ve ana paraşüt açılımı.
5.  **İniş (Descent):** Kontrollü iniş sırasında canlı video ve telemetri aktarımı.
6.  **Kurtarma (Recovery):** GPS koordinatlarına göre enkazın bulunması.

---

## 🛠️ Teknoloji Yığını | Tech Stack

<div align="center">

| Alan | Teknolojiler |
| :--- | :--- |
| **Yazılım Dili** | ![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) ![C++](https://img.shields.io/badge/C++-00599C?style=flat-square&logo=c%2B%2B&logoColor=white) |
| **Gömülü Sistem** | ![STM32](https://img.shields.io/badge/STM32-03234B?style=flat-square&logo=stmicroelectronics&logoColor=white) ![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-A22846?style=flat-square&logo=raspberry-pi&logoColor=white) |
| **Arayüz** | ![PyQt](https://img.shields.io/badge/Qt-41CD52?style=flat-square&logo=qt&logoColor=white) ![Matplotlib](https://img.shields.io/badge/Matplotlib-11557c?style=flat-square) |
| **Veri Analizi** | ![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white) ![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white) |

</div>

---

## 🧮 Mühendislik Araçları | Engineering Tools

Bu repo, görev başarısını garanti altına almak için geliştirilmiş özel simülasyon araçlarını içerir.

### � Anten Yönlendirme (`antenna_pointing.py`)
Yer istasyonu anteninin uyduyu kaçırmaması için anlık Azimuth/Elevation hesaplaması.
```bash
python analysis/calculators/antenna_pointing.py
```

### 📉 İniş Profili Simülasyonu (`descent_profile.py`)
Atmosferik sürüklenme katsayılarına göre iniş süresi tahmini.
```bash
python analysis/simulations/descent_profile.py
```

### 🔗 Link Bütçesi Analizi (`link_budget.py`)
RF sinyal gücünün (RSSI) mesafeye göre değişimi ve Friis denklemi analizi.
```bash
python analysis/calculators/link_budget.py
```

---

## ❓ Sıkça Sorulan Sorular (FAQ)

**S: Neden LoRa teknolojisini tercih ettiniz?**
C: Düşük güç tüketimi ve uzun menzilli haberleşme (Long Range) kapasitesi, model uydu telemetrisi için en optimum çözümdür.

**S: Yer istasyonu yazılımı hangi işletim sistemlerinde çalışır?**
C: Python tabanlı mimarimiz sayesinde Windows, Linux ve macOS üzerinde sorunsuz çalışmaktadır. Cross-platform uyumluluğu tamdır.

**S: Proje açık kaynaklı mı?**
C: Evet, bilginin paylaştıkça çoğaldığına inanıyoruz. MIT lisansı altında tüm kodları inceleyebilir ve katkıda bulunabilirsiniz.

---

## 📂 Dizin Yapısı | Directory Structure

```bash
teknofest_hareketli_uydu_terminali/
├── 📂 analysis/           # 🧪 Simülasyon ve Analiz
│   ├── calculators/       # Mühendislik hesaplayıcıları
│   └── simulations/       # Fizik motoru simülasyonları
├── 📂 src/                # 🧠 Ana Yazılım
│   ├── ground_station.py  # Yer istasyonu çekirdeği
│   └── telemetry.py       # Protokol ayrıştırıcı
├── 📂 docs/               # 📚 Teknik Dokümanlar
└── 📄 requirements.txt    # 📦 Proje Gereksinimleri
```

---

<div align="center">

**GÖKBÖRÜ OTONOM SİSTEMLERİ** &copy; 2024
*"İstikbal Göklerdedir"*

[Bize Ulaşın](mailto:iletisim@gokboru.tech) | [Web Sitesi](https://gokboru.tech)

</div>
