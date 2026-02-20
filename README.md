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

Bu repo, projenin tüm yazılım altyapısını, analiz araçlarını ve dokümantasyonunu barındırır.

### 🎯 Temel Hedefler | Core Objectives
- **Hassas İletişim:** Uzun mesafeli veri aktarımı ve telemetri takibi.
- **Otonom Kontrol:** Uydu terminalinin otonom yönelimi ve stabilizasyonu.
- **Gerçek Zamanlı Analiz:** Uçuş verilerinin anlık işlenmesi ve görselleştirilmesi.

---

## 🛠️ Özellikler | Features

- **📡 Güçlü İletişim Altyapısı**
  - Uzun menzilli LoRa/RF modülleri ile kesintisiz veri akışı.
  - Özel geliştirilmiş *Link Budget* hesaplayıcıları.

- **🪂 Uçuş Mekaniği ve Analiz**
  - Paraşüt boyutlandırma algoritmaları.
  - İniş hızı simülasyonları.

- **💻 Modüler Yazılım Mimarisi**
  - Kolay genişletilebilir Python tabanlı analiz araçları.
  - Temiz ve dokümante edilmiş kod yapısı.

---

## 📂 Dizin Yapısı | Directory Structure

```bash
teknofest_hareketli_uydu_terminali/
├── analysis/           # Analiz ve hesaplama araçları
│   └── calculators/    # Link budget, paraşüt vb. hesaplayıcılar
├── src/                # Kaynak kodlar (Gömülü yazılım, arayüz vb.)
├── docs/               # Proje dokümantasyonu ve raporlar
├── assets/             # Görseller ve şemalar
└── README.md           # Proje ana dokümanı
```

---

## 🧮 Analiz Araçları | Analysis Tools

Bu proje, mühendislik hesaplamalarını otomatize etmek için özel Python scriptleri içerir.

### 1. Paraşüt Boyutlandırma (`parachute_sizing.py`)
Model uydunun istenen iniş hızına ulaşması için gereken paraşüt çapını hesaplar.
```bash
python analysis/calculators/parachute_sizing.py
```

### 2. Link Bütçesi Hesaplama (`link_budget.py`)
Haberleşme sisteminin güvenilirliğini test etmek için RF link bütçesi hesabı yapar.
```bash
python analysis/calculators/link_budget.py
```

---

## 🚀 Kurulum | Installation

Projeyi yerel ortamınızda çalıştırmak için aşağıdaki adımları izleyin:

1. **Repoyu Klonlayın:**
   ```bash
   git clone https://github.com/bahattinyunus/teknofest_hareketli_uydu_terminali.git
   cd teknofest_hareketli_uydu_terminali
   ```

2. **Gereksinimleri Yükleyin:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🤝 Katkıda Bulunma | Contributing

1. Bu repoyu forklayın.
2. Yeni bir özellik dalı (feature branch) oluşturun (`git checkout -b ozellik/YeniOzellik`).
3. Değişikliklerinizi commit edin (`git commit -m 'Yeni özellik eklendi'`).
4. Dalınızı pushlayın (`git push origin ozellik/YeniOzellik`).
5. Bir Pull Request oluşturun.

---

<div align="center">

**[Takım İsmi]** tarafından ❤️ ile geliştirilmiştir.

</div>
