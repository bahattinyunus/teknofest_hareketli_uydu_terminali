<div align="center">

# 🛰️ Teknofest Hareketli Uydu Terminali
### Model Uydu Yarışması | Team [Takım İsmi]

![Missions Success](https://img.shields.io/badge/Mission-Success-success?style=for-the-badge&logo=spacex)
![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Build Status](https://img.shields.io/badge/Build-Passing-success?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)

</div>

---

## 🚀 Proje Hakkında | Project Overview

**Teknofest Hareketli Uydu Terminali** projesi, model uydu yarışması kapsamında geliştirilen, yüksek hareket kabiliyetine ve hassas veri iletişimine sahip bir yer istasyonu ve uydu sistemidir.

> "Gökyüzü sadece bir başlangıç, sınır değil." 🌌

Bu repo, projenin tüm yazılım altyapısını, analiz araçlarını ve dokümantasyonunu barındırır.

---

## 🏗️ Sistem Mimarisi | System Architecture

Aşağıdaki diyagram, yer istasyonu ve uydu arasındaki veri akışını ve kontrol döngüsünü göstermektedir.

```mermaid
graph TD
    subgraph Space Segment [🛰️ Uydu Segmenti]
        Sensors[Sensör Verisi] -->|Okuma| OBC[On-Board Computer]
        OBC -->|Paketleme| LoRaTx[LoRa Verici]
    end

    subgraph Ground Segment [🌍 Yer İstasyonu]
        LoRaRx[LoRa Alıcı] -->|Sinyal| GCS[Yer Kontrol Yazılımı]
        GCS -->|Parse| Dashboard[Telemetri Arayüzü]
        GCS -->|Analiz| Analytics[Uçuş Analizi]
        User[Operatör] -->|Komut| GCS
        GCS -->|Kontrol| Antenna[Anten Takip Sistemi]
    end

    LoRaTx -.->|433 MHz RF Link| LoRaRx
    Antenna -.->|Yönelim| Space Segment
```

---

## 🛠️ Teknoloji Yığını | Tech Stack

<div align="center">

| Kategori | Teknolojiler |
| :--- | :--- |
| **Diller** | ![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) ![C++](https://img.shields.io/badge/C++-00599C?style=flat-square&logo=c%2B%2B&logoColor=white) |
| **Donanım** | ![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-A22846?style=flat-square&logo=raspberry-pi&logoColor=white) ![Arduino](https://img.shields.io/badge/Arduino-00979D?style=flat-square&logo=arduino&logoColor=white) |
| **İletişim** | ![LoRa](https://img.shields.io/badge/LoRa-Communication-orange?style=flat-square) |
| **Veri** | ![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white) ![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white) |

</div>

---

## 🗺️ Yol Haritası | Roadmap

- [x] **Faz 1: Hazırlık**
  - [x] Repo kurulumu ve dizin yapısı
  - [x] Temel analiz araçları (`parachute_sizing`, `link_budget`)
- [ ] **Faz 2: Çekirdek Geliştirme**
  - [x] Yer istasyonu iskelet yapısı
  - [x] Telemetri protokol tasarımı
  - [ ] RF iletişim modülü entegrasyonu
- [ ] **Faz 3: Arayüz ve Test**
  - [ ] GUI Tasarımı (PyQt/Tkinter)
  - [ ] Saha testleri ve optimizasyon

---

## 📂 Dizin Yapısı | Directory Structure

```bash
teknofest_hareketli_uydu_terminali/
├── 📂 analysis/           # 🧮 Mühendislik analizleri
│   └── calculators/       # Hesaplama scriptleri
├── 📂 src/                # 💻 Kaynak kodlar
│   ├── ground_station.py  # Ana kontrol yazılımı
│   └── telemetry.py       # Veri paketleme modülü
├── 📂 docs/               # 📚 Dokümantasyon
└── 📄 requirements.txt    # 📦 Bağımlılıklar
```

---

## 🧮 Analiz Araçları | Analysis Tools

### 1. Paraşüt Boyutlandırma
Model uydunun güvenli inişi için gerekli hesaplamalar.
```bash
python analysis/calculators/parachute_sizing.py
```

### 2. Link Bütçesi
İletişim menzili ve güvenilirliği analizi.
```bash
python analysis/calculators/link_budget.py
```

---

## 🚀 Kurulum | Installation

1. **Repoyu Klonlayın:**
   ```bash
   git clone https://github.com/bahattinyunus/teknofest_hareketli_uydu_terminali.git
   ```

2. **Bağımlılıkları Yükleyin:**
   ```bash
   pip install -r requirements.txt
   ```

---

<div align="center">

**[Takım İsmi]** &copy; 2024
*"Geleceğe Uçuyoruz" by Bahattin Yunus*

</div>
