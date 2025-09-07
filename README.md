# Momentum Language (`.mn`)

**Momentum** คือภาษาโปรแกรมสมัยใหม่ที่ได้รับการออกแบบมาเพื่อความเรียบง่าย, อ่านง่าย, และมีประสิทธิภาพสูง โดยได้รับแรงบันดาลใจจากจิตวิญญาณที่เข้าถึงง่ายของภาษา BASIC ในยุค 8-bit ผสมผสานกับพลังและความสามารถของภาษาโปรแกรมยุคใหม่อย่าง Python

> **เป้าหมาย:** สร้างภาษาที่เรียนรู้ได้ง่ายเหมือน BASIC และมีพลังเหมือน Python

---

## ที่มาและปรัชญา

ภาษา Momentum ถือกำเนิดขึ้นจากโปรเจกต์ที่ต้องการ "อัปเกรด" ซอร์สโค้ดระดับตำนานของ **Microsoft 6502 BASIC** ให้เข้ากับยุคสมัยใหม่ โดยยังคงรักษาปรัชญาดั้งเดิมไว้ แต่แก้ไขจุดอ่อนที่สำคัญ:

1.  **จาก Spaghetti Code สู่ Structured Code:** เราได้ยกเลิก `GOTO` และแทนที่ด้วยโครงสร้างควบคุมที่ทันสมัย เช่น ฟังก์ชัน, Loop, และ `if/else` ที่ชัดเจน
2.  **ความเรียบง่ายต้องมาก่อน (Readability is King):** ไวยากรณ์ถูกออกแบบมาให้อ่านเหมือนภาษาอังกฤษ ไม่สนใจตัวพิมพ์เล็ก-ใหญ่ (Case-Insensitive) และลดสัญลักษณ์ที่ไม่จำเป็น
3.  **ปลอดภัยและชัดเจน (Safety and Clarity):** ใช้ระบบชนิดข้อมูลที่แข็งแกร่ง (Strongly Typed) แต่ยืดหยุ่น และบังคับให้มีการแปลงชนิดข้อมูลอย่างชัดเจน (Explicit Casting) เพื่อป้องกันข้อผิดพลาด
4.  **เริ่มต้นง่ายและรวดเร็ว:** เพียงแค่เขียนโค้ดในไฟล์ `.mn` แล้วรันผ่านอินเทอร์พรีเตอร์ ก็สามารถเห็นผลลัพธ์ได้ทันที

## คุณสมบัติหลัก (Features)

*   **ไวยากรณ์ที่สะอาดตา:** ไม่มี `{}` หรือ `;`
*   **Case-Insensitive:** `print`, `Print`, `PRINT` ถือเป็นคำสั่งเดียวกัน
*   **ชนิดข้อมูลพื้นฐาน:** Integer, Float, String
*   **ตัวแปร:** กำหนดค่าด้วย `let` (หรือสร้างอัตโนมัติเมื่อใช้ `read`)
*   **โครงสร้างควบคุม:** `if/then/else/endif`, `while/wend`, `for/to/step/next`
*   **ฟังก์ชัน:** รองรับฟังก์ชันที่ผู้ใช้สร้างเอง, พารามิเตอร์, และ `return` ค่า (แม้จะซ้อนใน `if`)
*   **อาร์เรย์ (Arrays):** รองรับอาร์เรย์หนึ่งมิติผ่านคำสั่ง `DIM`
*   **การจัดการข้อมูลในตัว (Built-in Data):** รองรับ `DATA`, `READ`, และ `RESTORE` เพื่อการจัดการชุดข้อมูลอย่างง่าย
*   **ขอบเขตตัวแปร (Scoping):** ฟังก์ชันมี Local Scope ของตัวเอง
*   **ฟังก์ชันในตัว (Built-in Functions):** `str()`, `int()`, `float()`, `time()`
*   **คอมเมนต์:** ใช้ `//` สำหรับคอมเมนต์บรรทัดเดียว

## คู่มือการใช้งาน (Quick Start)

### 1. การติดตั้ง

คุณต้องมี **Python 3.10** หรือสูงกว่าติดตั้งในเครื่องของคุณ

### 2. การรันโปรแกรม

1.  **สร้างไฟล์โปรแกรม:** สร้างไฟล์ใหม่และตั้งชื่อให้ลงท้ายด้วย `.mn` เช่น `demo.mn`
2.  **เขียนโค้ด:** เขียนโค้ด Momentum ของคุณลงในไฟล์นั้น

    ```momentum
    // file: demo.mn
    print("Hello from Momentum!")
    
    input name, "What is your name? "
    print("Nice to meet you, " + name)
    ```

3.  **รันผ่านอินเทอร์พรีเตอร์:**
    เปิด Terminal หรือ Command Prompt แล้วรันคำสั่ง:
    ```bash
    python intp.py demo.mn
    ```

## ไวยากรณ์และตัวอย่างโค้ด (Syntax & Examples)

### 1. ตัวแปรและการกำหนดค่า

ใช้ `let` เพื่อกำหนดค่าตัวแปร

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

ใช้ `input` เพื่อรับค่าจากผู้ใช้และเก็บไว้ในตัวแปรธรรมดา หรือสมาชิกของอาร์เรย์

```momentum
// รับค่าใส่ตัวแปรธรรมดา
input user_age, "Please enter your age: "
let age_in_dog_years = int(user_age) * 7
print("You are " + str(age_in_dog_years) + " in dog years!")

// รับค่าใส่อาร์เรย์
dim values(1)
input values(0), "Enter a value for the array: "
print("You entered: " + str(values(0)))
```

### 4. ตัวดำเนินการทางคณิตศาสตร์

Momentum รองรับตัวดำเนินการพื้นฐาน รวมถึงเครื่องหมายลบนำหน้าตัวเลข (Unary Minus)

```momentum
let x = 10
let y = -5
print("x + y = " + str(x + y)) // ผลลัพธ์: 5
```

### 5. โครงสร้างเงื่อนไข (If/Then/Else)

```momentum
let temperature = 25

if temperature > 30 then
  print("It's a hot day!")
else
  print("The weather is nice.")
end if
```

### 6. Loop

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
for j = 10 to 0 step -2
  print("Counting down: " + str(j))
next j
```

### 7. อาร์เรย์ (Arrays)

ใช้ `dim` เพื่อประกาศอาร์เรย์หนึ่งมิติ (one-dimensional array)

```momentum
// ประกาศอาร์เรย์ชื่อ scores ขนาด 5 ช่อง (index 0-4)
dim scores(5)

// กำหนดค่าให้อาร์เรย์
let scores(0) = 98
let scores(1) = 87
let scores(2) = 92
let scores(3) = 79
let scores(4) = 85

// วนลูปเพื่อแสดงผล
let total_score = 0
for i = 0 to 4
    let total_score = total_score + scores(i)
next i

print("Average score: " + str(total_score / 5))
```

### 8. การจัดการข้อมูล (DATA / READ / RESTORE)

ฝังชุดข้อมูลไว้ในโปรแกรมและอ่านมาใช้งานได้อย่างง่ายดาย

```momentum
data "Alice", 95, "Bob", 88, -1 // ข้อมูลสามารถเป็นชนิดต่างๆ และติดลบได้

// อ่านข้อมูลมาใส่ในตัวแปร (ตัวแปรจะถูกสร้างอัตโนมัติ)
read student_name, student_score
print(student_name + " got a score of " + str(student_score)) // Alice got a score of 95

// อ่านข้อมูลชุดถัดไป
read student_name, student_score
print(student_name + " got a score of " + str(student_score)) // Bob got a score of 88

restore // ย้ายตัวชี้กลับไปที่ข้อมูลตัวแรก
read student_name, student_score
print("After restore, first student is: " + student_name) // Alice
```

### 9. ฟังก์ชัน (Functions)

ฟังก์ชันช่วยให้คุณจัดระเบียบโค้ดและนำกลับมาใช้ใหม่ได้ สามารถใช้ `return` จากในเงื่อนไขที่ซ้อนกันได้

```momentum
// การประกาศฟังก์ชัน
function add(a, b)
  return a + b
end function

let sum = add(10, -5)
print("10 + (-5) = " + str(sum)) // ผลลัพธ์: 5

// ตัวอย่างฟังก์ชันที่ซับซ้อนขึ้น พร้อม return ที่ซ้อนกัน
function get_sign(n)
  if n > 0 then
    return "Positive"
  else if n < 0 then
    return "Negative"
  else
    return "Zero"
  end if
end function

print("The sign of -100 is: " + get_sign(-100)) // ผลลัพธ์: Negative
```

## การมีส่วนร่วม (Contributing)

เรายินดีต้อนรับผู้ที่มีส่วนร่วมทุกคน! หากคุณมีไอเดีย, ต้องการแก้ไขบั๊ก, หรือเพิ่มฟีเจอร์ใหม่ๆ กรุณาเปิด Issue หรือส่ง Pull Request เข้ามาใน Repository นี้

## ใบอนุญาต (License)

โปรเจกต์นี้อยู่ภายใต้ใบอนุญาตแบบ MIT - ดูรายละเอียดเพิ่มเติมได้ในไฟล์ `LICENSE`