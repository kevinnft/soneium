# 🔄 Auto Token Sender (Soneium Chain)

Script Python untuk **mengirim token ERC20 secara bergantian** (USD0, USDT, USDC) dari daftar wallet ke daftar address tujuan, dengan jumlah **acak** dan interval **5 menit sekali**.

## ✨ Fitur
- ✅ Bergantian token: USD0 → USDT → USDC → ulang lagi
- ✅ Jumlah random: antara `0.000001` – `0.00001`
- ✅ Interval otomatis: tiap **5 menit sekali**
- ✅ Cek saldo & decimals otomatis (skip kalau saldo kurang)
- ✅ Output berwarna dengan info **nonce** dan **sisa saldo**
- ✅ Bisa dijalankan di VPS maupun laptop

## ⚙️ Persiapan

### 1. Install Python & Pip
Pastikan sudah terinstall **Python 3.9+**
```bash
python3 --version
pip3 --version
```

### 2. Install Library
```bash
pip install -r requirements.txt
```

### 3. Buat File Input
- **wallets.txt** → daftar private key (satu per baris)
- **addres.txt** → daftar alamat tujuan (satu per baris)

## 🚀 Cara Menjalankan
```bash
python3 autosend.py
```

## 🖥️ Contoh Output
```text
[0xAbc...] Sent 0.00000750 USDT -> 0x123...
   Nonce: 42 | Tx: 0xabc123...
   Sisa saldo: 12.345678 USDT

[0xDef...] SKIP USD0 | saldo: 0.000000
```

## 📌 Catatan
- Gunakan **RPC Soneium**: `https://rpc.soneium.org`
- Chain ID: **1868**
- Token Address:
  - USD0: `0x102d758f688a4c1c5a80b116bd945d4455460282`
  - USDT: `0xba9986d2381edf1da03b0b9c1f8b00dc4aacc369`
  - USDC: `0x3a337a6ada9d885b6ad95ec48f9b75f197b5ae35`
