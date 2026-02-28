#!/bin/bash
# 🚀 GÖKBÖRÜ SOTM: Over-The-Air (OTA) Edge Deployment Script
# Deploys the Python ecosystem to a target Edge Computer (Raspberry Pi 4 / Nvidia Jetson Nano)

TARGET_IP="192.168.1.100"
TARGET_USER="gokboru"
TARGET_DIR="/opt/gokboru_sotm"

echo "======================================================"
echo "🐺 GÖKBÖRÜ EDGE DEPLOYMENT INITIATED"
echo "Target: ${TARGET_USER}@${TARGET_IP}:${TARGET_DIR}"
echo "======================================================"

# 1. Sync Files
echo "[1/3] Syncing repository to edge device via RSYNC..."
rsync -avz --exclude '.git' --exclude 'venv' --exclude '__pycache__' --exclude '.pytest_cache' ./ ${TARGET_USER}@${TARGET_IP}:${TARGET_DIR}

if [ $? -eq 0 ]; then
    echo "✅ Sync successful."
else
    echo "❌ Sync failed! Check SSH keys and network connection."
    exit 1
fi

# 2. Remote Install
echo "[2/3] Installing/Updating dependencies on edge device..."
ssh ${TARGET_USER}@${TARGET_IP} "cd ${TARGET_DIR} && pip3 install -r requirements.txt --break-system-packages"

# 3. Service Restart
echo "[3/3] Restarting Gökbörü Telemetry Service..."
ssh ${TARGET_USER}@${TARGET_IP} "sudo systemctl restart gokboru_sotm.service"

echo "======================================================"
echo "🎯 OTA DEPLOYMENT COMPLETE. İSTİKBAL GÖKLERDEDİR!"
echo "======================================================"
