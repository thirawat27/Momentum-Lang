
# Momentum Language (`.mn`)



**Momentum** คือภาษาโปรแกรมสมัยใหม่ที่ได้รับการออกแบบมาเพื่อความเรียบง่าย, อ่านง่าย, และมีประสิทธิภาพสูง โดยได้รับแรงบันดาลใจจากจิตวิญญาณที่เข้าถึงง่ายของภาษา BASIC ในยุค 8-bit ผสมผสานกับพลังและความสามารถของภาษาโปรแกรมยุคใหม่อย่าง Python และ Rust

> **เป้าหมาย:** สร้างภาษาที่เรียนรู้ได้ง่ายเหมือน BASIC, มีพลังเหมือน Python, และมีความเร็วของภาษาที่คอมไพล์เป็นโค้ดเนทีฟ

---

## ที่มาและปรัชญา

ภาษา Momentum ถือกำเนิดขึ้นจากโปรเจกต์ที่ต้องการ "อัปเกรด" ซอร์สโค้ดระดับตำนานของ **Microsoft 6502 BASIC** ให้เข้ากับยุคสมัยใหม่ โดยยังคงรักษาปรัชญาดั้งเดิมไว้ แต่แก้ไขจุดอ่อนที่สำคัญ:

1.  **จาก Spaghetti Code สู่ Structured Code:** เราได้ยกเลิก `GOTO` และแทนที่ด้วยโครงสร้างควบคุมที่ทันสมัย เช่น ฟังก์ชัน, Loop, และ `if/else` ที่ชัดเจน
2.  **ความเรียบง่ายต้องมาก่อน (Readability is King):** ไวยากรณ์ถูกออกแบบมาให้อ่านเหมือนภาษาอังกฤษ ไม่สนใจตัวพิมพ์เล็ก-ใหญ่ (Case-Insensitive) และลดสัญลักษณ์ที่ไม่จำเป็น
3.  **ปลอดภัยและชัดเจน (Safety and Clarity):** ใช้ระบบชนิดข้อมูลที่แข็งแกร่ง (Strongly Typed) แต่ยืดหยุ่น (Type Inference) และบังคับให้มีการแปลงชนิดข้อมูลอย่างชัดเจน (Explicit Casting) เพื่อป้องกันข้อผิดพลาดที่คาดไม่ถึง
4.  **เริ่มต้นง่ายและรวดเร็ว:** เพียงแค่เขียนโค้ดในไฟล์ `.mn` แล้วรันผ่านอินเทอร์พรีเตอร์ ก็สามารถเห็นผลลัพธ์ได้ทันที

## คุณสมบัติหลัก (Features)

*   **ไวยากรณ์ที่สะอาดตา:** ไม่มี `{}` หรือ `;`
*   **Case-Insensitive:** `print`, `Print`, `PRINT` ถือเป็นคำสั่งเดียวกัน
*   **ชนิดข้อมูลพื้นฐาน:** Integer, Float, String
*   **ตัวแปร:** ประกาศด้วย `let`
*   **โครงสร้างควบคุม:** `if/then/else/endif`, `while/wend`, `for/to/step/next`
*   **ฟังก์ชัน:** รองรับฟังก์ชันที่ผู้ใช้สร้างเอง, พารามิเตอร์, และ `return` ค่า
*   **ขอบเขตตัวแปร (Scoping):** ฟังก์ชันมี Local Scope ของตัวเอง
*   **ฟังก์ชันในตัว (Built-in Functions):** `str()`, `int()`, `float()`, `time()`
*   **คอมเมนต์:** ใช้ `//` สำหรับคอมเมนต์บรรทัดเดียว

## คู่มือการใช้งาน (Quick Start)

### 1. การติดตั้ง

คุณต้องมี **Python 3.12** หรือสูงกว่าติดตั้งในเครื่องของคุณ

### 2. การรันโปรแกรม

1.  **สร้างไฟล์โปรแกรม:** สร้างไฟล์ใหม่และตั้งชื่อให้ลงท้ายด้วย `.mn` เช่น `hello.mn`
2.  **เขียนโค้ด:** เขียนโค้ด Momentum ของคุณลงในไฟล์นั้น

    ```momentum
    // file: hello.mn
    print("Hello from Momentum!")
    
    input name, "What is your name? "
    print("Nice to meet you, " + name)
    ```

3.  **รันผ่านอินเทอร์พรีเตอร์:**
    เปิด Terminal หรือ Command Prompt แล้วรันคำสั่ง:
    ```bash
    python intp.py hello.mn
    ```

## ไวยากรณ์และตัวอย่างโค้ด (Syntax & Examples)

### 1. ตัวแปรและการกำหนดค่า

ใช้ `let` เพื่อประกาศและกำหนดค่าตัวแปร

```momentum
let message = "This is a string"
let score = 100
let pi = 3.14
```

### 2. การแสดงผล (Printing)

ใช้ `print` เพื่อแสดงผลค่าต่างๆ ออกทางหน้าจอ

```momentum
let name = "Momentum"
print("Hello, " + name)
print("Score: " + str(100)) // ต้องใช้ str() เพื่อแปลงตัวเลขเป็นสตริง
```

### 3. การรับค่า (Input)

ใช้ `input` เพื่อรับค่าจากผู้ใช้และเก็บไว้ในตัวแปร

```momentum
input user_age, "Please enter your age: "
let age_in_dog_years = int(user_age) * 7
print("You are " + str(age_in_dog_years) + " in dog years!")
```

### 4. โครงสร้างเงื่อนไข (If/Then/Else)

```momentum
let temperature = 25

if temperature > 30 then
  print("It's a hot day!")
else if temperature < 15 then
  print("It's a cold day!")
else
  print("The weather is nice.")
end if
```

### 5. Loop

#### While Loop
```momentum
let countdown = 3
while countdown > 0
  print(countdown)
  let countdown = countdown - 1
wend
print("Blast off!")
```

#### For Loop
```momentum
// นับขึ้น
for i = 1 to 5
  print("Counting up: " + str(i))
next i

// นับถอยหลัง
for j = 3 to 1 step -1
  print("Counting down: " + str(j))
next j
```

### 6. ฟังก์ชัน (Functions)

ฟังก์ชันช่วยให้คุณจัดระเบียบโค้ดและนำกลับมาใช้ใหม่ได้

```momentum
// การประกาศฟังก์ชัน
function add(a, b)
  return a + b
end function

// การเรียกใช้ฟังก์ชัน
let sum = add(10, 20)
print("10 + 20 = " + str(sum)) // ผลลัพธ์: 30

// ตัวอย่างฟังก์ชันที่ซับซ้อนขึ้น
function greet(name, enthusiastic)
  let message = "Hello, " + name
  if enthusiastic == 1 then
    return message + "!!!"
  else
    return message + "."
  end if
end function

print(greet("World", 1)) // ผลลัพธ์: Hello, World!!!
```

## การมีส่วนร่วม (Contributing)

เรายินดีต้อนรับผู้ที่มีส่วนร่วมทุกคน! หากคุณมีไอเดีย, ต้องการแก้ไขบั๊ก, หรือเพิ่มฟีเจอร์ใหม่ๆ กรุณาเปิด Issue หรือส่ง Pull Request เข้ามาใน Repository นี้

## ใบอนุญาต (License)

โปรเจกต์นี้อยู่ภายใต้ใบอนุญาตแบบ MIT - ดูรายละเอียดเพิ่มเติมได้ในไฟล์ `LICENSE`