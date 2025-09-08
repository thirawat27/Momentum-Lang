# file: momentum.py
# The main entry point for the executable application.

import sys
import os
from intp import run_momentum, MomentumError, GFX_GLOBALS, gfx_wait

def main():
    """
    Main function to handle program execution, file reading,
    and graceful exit.
    """
    # ตรวจสอบว่ามีการส่งชื่อไฟล์มาเป็น argument หรือไม่
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        
        # ตรวจสอบว่าไฟล์มีอยู่จริงหรือไม่
        if not os.path.exists(filename):
            print(f"ข้อผิดพลาด: ไม่พบไฟล์ '{filename}'", file=sys.stderr)
            input("\nกด Enter เพื่อปิดหน้าต่าง...") # ป้องกันหน้าต่างปิดทันที
            sys.exit(1)
            
        try:
            # อ่าน Source Code จากไฟล์
            with open(filename, 'r', encoding="utf-8-sig") as f:
                source_code = f.read()
            
            # รันโค้ด Momentum
            print(f"--- กำลังรันไฟล์: {os.path.basename(filename)} ---")
            run_momentum(source_code)
            print("---------------------------------")

        except MomentumError as e:
            # ข้อผิดพลาดจาก Interpreter จะถูกพิมพ์ภายใน run_momentum แล้ว
            # เราแค่รอให้ผู้ใช้กด Enter ก่อนปิด
            input("\nโปรแกรมจบการทำงานเนื่องจากข้อผิดพลาด กด Enter เพื่อปิด...")
            sys.exit(1)
        except Exception as e:
            print(f"ข้อผิดพลาดที่ไม่คาดคิด: {e}", file=sys.stderr)
            input("\nกด Enter เพื่อปิดหน้าต่าง...")
            sys.exit(1)
            
        # ถ้ามีการใช้กราฟิก ให้รอจนกว่าหน้าต่างจะถูกปิด
        if GFX_GLOBALS["window"]:
            print("หน้าต่างกราฟิกทำงานอยู่ ปิดหน้าต่างเพื่อจบการทำงาน...")
            gfx_wait()
        else:
            # ถ้าไม่มีกราฟิก ให้รอผู้ใช้กด Enter (เพื่อให้ผลลัพธ์ไม่หายไปทันที)
            input("\nโปรแกรมทำงานเสร็จสิ้น กด Enter เพื่อปิด...")

    else:
        # ถ้าไม่ได้รับชื่อไฟล์ ให้แสดงวิธีใช้งาน
        print("--- Momentum Language Interpreter v1.0 ---")
        print("การใช้งาน: ลากไฟล์ .mn ของคุณมาวางบนไฟล์ momentum.exe")
        print("หรือรันผ่าน command line: momentum your_program.mn")
        input("\nกด Enter เพื่อปิด...")

if __name__ == "__main__":
    main()