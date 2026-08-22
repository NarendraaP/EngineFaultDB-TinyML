# Phase 5.1 — Fresh Hardware Discovery & Identity Verification Report

**Project:** QoS-Aware TinyML Runtime Research  
**Dataset:** EngineFaultDB (`EngineFaultDB_Final.csv`, 55,998 rows)  
**Authoritative Input Model Profile:** [`results/tinyml_model_profile_verified.csv`](file:///d:/WiDe/EngineFaultDB-main/results/tinyml_model_profile_verified.csv)  
**Discovery Output JSON:** [`phase5/measurements/fresh_hardware_discovery.json`](file:///d:/WiDe/EngineFaultDB-main/phase5/measurements/fresh_hardware_discovery.json)  
**Date:** August 20, 2026  

---

## 1. Fresh Serial Port & USB Device Discovery

A complete hardware discovery sweep was performed across host serial ports and USB subsystems:

```bash
python -m serial.tools.list_ports -v
```
**Output:**
```
COM1
    desc: Communications Port (COM1)
    hwid: ACPI\PNP0501\0
COM6
    desc: USB-SERIAL CH340 (COM6)
    hwid: USB VID:PID=1A86:7523 SER= LOCATION=1-3
```

- **Serial Ports Detected:** 2 ports (`COM1` = ACPI Internal, `COM6` = USB-to-UART Bridge).
- **USB Device Instance ID:** `USB\VID_1A86&PID_7523\5&2DD792E3&0&3`
- **PnP Status:** `Status: OK`, `Problem: CM_PROB_NONE`, `Present: True`.

---

## 2. USB-to-UART Bridge vs. MCU Silicon Separation

To maintain strict scientific accuracy, the interface bridge is explicitly separated from the MCU silicon:

- **USB-to-UART Bridge:** **WCH CH340** (`USB\VID_1A86&PID_7523`)
  - *Function:* Hardware interface IC translating USB packets to TTL UART serial signals.
- **Microcontroller (MCU) Silicon:** **Microchip / Atmel ATmega328P**
  - *Function:* Target computing processor executing the application code.

---

## 3. Protocol Probes & Identification Evidence

### A. ESP32 Bootloader Protocol Interrogation
```bash
python -m esptool --port COM6 chip-id
```
- **Result:** `Failed to connect to Espressif device: Invalid head of packet (0x00)`.
- **Verdict:** The microcontroller does **not** implement or respond to the Espressif ROM bootloader protocol.

### B. Non-Destructive AVR Bootloader Interrogation (`phase5/hardware/probe_avr_signature.py`)
- **Protocol:** STK500v1 (Optiboot Bootloader @ 115200 baud).
- **Command Sequence:**
  1. `STK_GET_SYNC (0x30 0x20)` $\rightarrow$ Returned `0x14 0x10` (`STK_INSYNC` + `STK_OK`).
  2. `STK_READ_SIGN (0x75 0x20)` $\rightarrow$ Returned **`0x1E 0x95 0x0F`**.
- **Silicon Signature Decode:**
  - `0x1E`: Atmel / Microchip Vendor ID
  - `0x95`: 32 KB Flash Density Code
  - `0x0F`: **ATmega328P Silicon Identifier**

---

## 4. Hardware Identity & Specification Record

| Attribute | Verified Empirical Value | Verification Evidence / Source |
| :--- | :--- | :--- |
| **CURRENT_BOARD** | Arduino Nano / Uno (with CH340 bridge) | Device Signature `0x1E 0x95 0x0F` |
| **COM_PORT** | `COM6` | Windows Serial Enumeration |
| **USB_VID** | `0x1A86` | Windows PnP Hardware ID |
| **USB_PID** | `0x7523` | Windows PnP Hardware ID |
| **USB_BRIDGE** | WCH CH340 USB-to-UART Bridge | Windows PnP Hardware Descriptor |
| **MCU** | **Microchip / Atmel ATmega328P** | Direct STK500v1 Device Signature Query |
| **ARCHITECTURE** | 8-bit AVR RISC | ATmega328P Silicon Architecture |
| **CORES** | 1 Core | ATmega328P Hardware Spec |
| **CLOCK** | 16.0 MHz | External Crystal Oscillator |
| **FLASH** | 32 KB Flash (0.5 KB bootloader) | ATmega328P Hardware Spec |
| **SRAM** | 2 KB Internal SRAM | ATmega328P Hardware Spec |
| **PSRAM** | 0 KB (None) | Not supported on AVR |
| **IDENTIFICATION_METHOD** | STK500v1 Device Signature Interrogation | `phase5/hardware/probe_avr_signature.py` |
| **IDENTIFICATION_EVIDENCE** | Raw Signature Bytes: `0x1E 0x95 0x0F` | Direct UART STK500 response |
| **TOOLCHAIN_STATUS** | `esptool 5.3.1`, `pyserial 3.5` installed | Host Python Environment |

---

## 5. Board Classification & Final Status

- **Board Classification:** **`ATmega328P`**
- **ESP32 Detection Result:** **`ESP32_NOT_PRESENT`**

---

### **FINAL STATUS: `ESP32_NOT_PRESENT`**
*(Reason: The connected board on COM6 was empirically identified via device signature 0x1E 0x95 0x0F as an ATmega328P with a CH340 USB bridge. No ESP32 silicon is present on any connected port).*
