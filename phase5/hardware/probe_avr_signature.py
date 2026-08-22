import serial, time

port = "COM6"

def probe_stk500():
    results = {}
    for baud in [115200, 57600]:
        print(f"\n--- Testing STK500 on {port} @ {baud} baud ---")
        try:
            ser = serial.Serial(port, baudrate=baud, timeout=1.0)
            
            # Pulse DTR to trigger hardware reset into bootloader
            ser.dtr = False
            time.sleep(0.05)
            ser.dtr = True
            time.sleep(0.05)
            ser.dtr = False
            time.sleep(0.1)
            ser.reset_input_buffer()
            
            # 1. Send STK_GET_SYNC (0x30 0x20)
            ser.write(b'\x30\x20')
            sync_resp = ser.read(2)
            print(f"  Sent STK_GET_SYNC (0x30 0x20) -> Received: {sync_resp.hex()} ({sync_resp})")
            
            if sync_resp == b'\x14\x10':
                print("  ==> STK500v1 SYNC SUCCESS (0x14 0x10 = STK_INSYNC + STK_OK)")
                
                # 2. Read Device Signature (STK_READ_SIGN: 0x75 0x20)
                ser.write(b'\x75\x20')
                sign_resp = ser.read(5)
                print(f"  Sent STK_READ_SIGN (0x75 0x20) -> Received: {sign_resp.hex()}")
                
                if len(sign_resp) == 5 and sign_resp[0:1] == b'\x14' and sign_resp[4:5] == b'\x10':
                    sig_bytes = sign_resp[1:4]
                    sig_hex = sig_bytes.hex().upper()
                    print(f"  ==> RAW DEVICE SIGNATURE BYTES: {sig_hex}")
                    
                    # Signature Decode
                    sig_map = {
                        "1E950F": {"mcu": "ATmega328P", "flash": "32 KB", "manufacturer": "Atmel / Microchip"},
                        "1E9801": {"mcu": "ATmega2560", "flash": "256 KB", "manufacturer": "Atmel / Microchip"},
                        "1E9514": {"mcu": "ATmega328",  "flash": "32 KB", "manufacturer": "Atmel / Microchip"},
                        "1E9406": {"mcu": "ATmega168P", "flash": "16 KB", "manufacturer": "Atmel / Microchip"},
                    }
                    
                    decoded = sig_map.get(sig_hex, {"mcu": "Unknown AVR", "flash": "Unknown", "manufacturer": "Atmel / Microchip"})
                    print(f"  ==> DECODED MCU: {decoded['mcu']}")
                    print(f"  ==> FLASH SIZE: {decoded['flash']}")
                    print(f"  ==> MANUFACTURER: {decoded['manufacturer']}")
                    
                    results[baud] = {
                        "sync": True,
                        "raw_signature": sig_hex,
                        "decoded": decoded
                    }
            else:
                results[baud] = {"sync": False, "raw_signature": None}
            ser.close()
        except Exception as e:
            print(f"  Error at {baud} baud: {e}")
            results[baud] = {"error": str(e)}
    return results

if __name__ == "__main__":
    probe_stk500()
