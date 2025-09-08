<div align="center">

![Momentum Logo](./momentum_logo.ico)  

# ภาษา Momentum (`.mn`)

</div>
**Momentum** คือภาษาโปรแกรมสมัยใหม่ที่ได้รับการออกแบบมาเพื่อความเรียบง่าย, อ่านง่าย, และมีประสิทธิภาพสูง โดยได้รับแรงบันดาลใจจากจิตวิญญาณที่เข้าถึงง่ายของภาษา BASIC ในยุค 8-bit ผสมผสานกับพลังและความสามารถของภาษาโปรแกรมยุคใหม่อย่าง Python

> **เป้าหมาย:** สร้างภาษาที่เรียนรู้ได้ง่ายเหมือน BASIC และมีพลังเหมือน Python

---

## ที่มาและปรัชญา

ภาษา Momentum ถือกำเนิดขึ้นจากโปรเจกต์ที่ต้องการ "อัปเกรด" ซอร์สโค้ดระดับตำนานของ **Microsoft 6502 BASIC** ให้เข้ากับยุคสมัยใหม่ โดยยังคงรักษาปรัชญาดั้งเดิมไว้ แต่แก้ไขจุดอ่อนที่สำคัญ:

1. **จาก Spaghetti Code สู่ Structured Code:** เราได้ยกเลิก `GOTO` และแทนที่ด้วยโครงสร้างควบคุมที่ทันสมัย เช่น ฟังก์ชัน, Loop, และ `if/elseif/else` ที่ชัดเจน
2. **ความเรียบง่ายต้องมาก่อน (Readability is King):** ไวยากรณ์ถูกออกแบบมาให้อ่านเหมือนภาษาอังกฤษ ไม่สนใจตัวพิมพ์เล็ก-ใหญ่ (Case-Insensitive) และลดสัญลักษณ์ที่ไม่จำเป็น
3. **ปลอดภัยและชัดเจน (Safety and Clarity):** ใช้ระบบชนิดข้อมูลที่แข็งแกร่ง (Strongly Typed) แต่ยืดหยุ่น และบังคับให้มีการแปลงชนิดข้อมูลอย่างชัดเจน (Explicit Casting) เพื่อป้องกันข้อผิดพลาด
4. **เริ่มต้นง่ายและรวดเร็ว:** เพียงแค่เขียนโค้ดในไฟล์ `.mn` แล้วรันผ่านอินเทอร์พรีเตอร์ ก็สามารถเห็นผลลัพธ์ได้ทันที พร้อมระบบแจ้งข้อผิดพลาดที่ระบุหมายเลขบรรทัดชัดเจน

## คุณสมบัติหลัก (Features)

- **ไวยากรณ์ที่สะอาดตา:** ไม่มี `{}` หรือ `;`
- **Case-Insensitive:** `print`, `Print`, `PRINT` ถือเป็นคำสั่งเดียวกัน
- **ชนิดข้อมูลพื้นฐาน:** Integer, Float, String, Array
- **ตัวแปร:** กำหนดค่าด้วย `let`
- **โครงสร้างควบคุม:** `if/then/elseif/else/endif`, `while/wend`, `for/to/step/next`
- **ตัวดำเนินการตรรกะ:** รองรับ `AND`, `OR`, `NOT`
- **ฟังก์ชันและโปรซีเยอร์:** รองรับฟังก์ชันที่คืนค่า (`return`) และโปรซีเยอร์ที่ไม่คืนค่า
- **อาร์เรย์หลายมิติ (Multi-dimensional Arrays):** รองรับผ่านคำสั่ง `DIM a(rows, cols, ...)`
- **การจัดการข้อมูลในตัว:** รองรับ `DATA`, `READ`, และ `RESTORE`
- **ขอบเขตตัวแปร (Scoping):** ฟังก์ชันมี Local Scope ของตัวเอง
- **ฟังก์ชันในตัว (Built-in Functions):** `str()`, `int()`, `float()`, `time()`, `len()`, `abs()`, `round()`, `type()`, `sqrt()` และอื่นๆ
- **คอมเมนต์:** ใช้ `//` สำหรับคอมเมนต์บรรทัดเดียว
- **Escape Characters:** รองรับ `\n`, `\t`, `\"`, `\\` ใน String
- **ระบบกราฟิกเบื้องต้น:** สามารถวาดรูปทรงเรขาคณิต, กำหนดสี, และสร้างหน้าต่างกราฟิกได้
- **คุณสมบัติขั้นสูง:**
  - **JIT Compilation:** เพิ่มความเร็วในการคำนวณที่ซับซ้อนด้วย `jit_function` 
  - **Asynchronous Programming:** รองรับการทำงานแบบไม่รอ (Non-blocking) ด้วย `async function`, `await`, และ `run async`

## การติดตั้งและการรัน

### 1. การติดตั้งสำหรับผู้ใช้งานทั่วไป (แนะนำ)

วิธีที่ง่ายที่สุดในการเริ่มต้นใช้งาน Momentum คือการใช้ตัวติดตั้งของเรา

1. ไปที่หน้า **Releases** ของโปรเจกต์บน GitHub
2. ดาวน์โหลดไฟล์ `Momentum_Setup_vX.X.exe` เวอร์ชันล่าสุด
3. รันตัวติดตั้งและทำตามขั้นตอนบนหน้าจอ
   - คุณสามารถเลือกสร้าง Shortcut บน Desktop และเชื่อมโยงไฟล์ `.mn` กับโปรแกรมได้

เมื่อติดตั้งเสร็จแล้ว คุณสามารถรันโปรแกรม Momentum ได้โดยการ **ดับเบิลคลิกที่ไฟล์ `.mn` ของคุณได้โดยตรง**

### 2. การรันสำหรับนักพัฒนา (ทางเลือก)

หากคุณต้องการรันจากซอร์สโค้ดโดยตรง:
- คุณต้องมี **Python 3.11** หรือสูงกว่าติดตั้งในเครื่องของคุณ

จากนั้นเปิด Terminal หรือ Command Prompt แล้วรันคำสั่ง:

```bash
python intp.py your_program.mn
```

---

## คู่มือไวยากรณ์ฉบับสมบูรณ์ (Comprehensive Syntax Guide)

### 1. ตัวแปรและการกำหนดค่า (Variables & Assignment)

ใช้ `let` เพื่อกำหนดค่าให้กับตัวแปร ชื่อตัวแปรไม่สนใจตัวพิมพ์เล็ก-ใหญ่ (`myVar` และ `myvar` คือตัวเดียวกัน)

```mn
// ตัวเลข
let age = 30
let price = 199.95

// ข้อความ
let name = "Momentum"

// กำหนดค่าจากตัวแปรอื่น
let new_price = price + 50.0
print(new_price) // 249.95
```

### 2. ชนิดข้อมูล และการแปลงชนิด (Data Types & Casting)

Momentum รองรับ `INTEGER`, `FLOAT`, `STRING` และ `ARRAY` ใช้ฟังก์ชันในตัวเพื่อแปลงชนิดข้อมูล

```mn
let num_str = "123"
let num_int = int(num_str) // แปลงเป็น Integer
let num_float = float("99.5") // แปลงเป็น Float

print(type(num_int))   // แสดงผล: INTEGER
print(type(num_float)) // แสดงผล: FLOAT

let message = "Version " + str(3.0) // แปลงเลขเป็น String เพื่อต่อข้อความ
print(message) // Version 3.0
```

### 3. การแสดงผลและการรับข้อมูล (Output & Input)

- `print` สำหรับแสดงผล
- `input` สำหรับรับค่าจากผู้ใช้

```mn
// แสดงผล
print("Hello, World!")

// รับค่า
input user_name, "Please enter your name: "
print("Welcome, " + user_name)

// รับค่าโดยไม่มีข้อความแจ้ง
input age
print("You are " + str(age) + " years old.")
```

### 4. ตัวดำเนินการ (Operators)

#### ตัวดำเนินการทางคณิตศาสตร์

| ตัวดำเนินการ | ความหมาย |
| :---: | :--- |
| `+` | บวก |
| `-` | ลบ |
| `*` | คูณ |
| `/` | หาร |

#### ตัวดำเนินการเปรียบเทียบ

| ตัวดำเนินการ | ความหมาย |
| :---: | :--- |
| `==` | เท่ากับ |
| `!=` | ไม่เท่ากับ |
| `>` | มากกว่า |
| `<` | น้อยกว่า |
| `>=` | มากกว่าหรือเท่ากับ |
| `<=` | น้อยกว่าหรือเท่ากับ |

#### ตัวดำเนินการตรรกะ

| ตัวดำเนินการ | ความหมาย |
| :---: | :--- |
| `AND` | และ |
| `OR` | หรือ |
| `NOT` | ไม่ |

### 5. โครงสร้างควบคุม (Control Structures)

#### IF / ELSEIF / ELSE

```mn
let score = 75

if score >= 80 then
    print("Grade A")
else if score >= 70 then
    print("Grade is B")
else
    print("Grade C or lower")
end if
```

#### WHILE Loop

```mn
let count = 3
while count > 0
  print("Countdown: " + str(count))
  let count = count - 1
wend
print("Blast off!")
```

#### FOR Loop

```mn
// นับขึ้นทีละ 1 (default step)
for i = 1 to 3
  print("Up: " + str(i))
next i

// นับถอยหลังทีละ 2
for j = 10 to 0 step -2
  print("Down: " + str(j))
next j
```

### 6. ฟังก์ชันและโปรซีเยอร์ (Functions & Procedures)

ฟังก์ชันสามารถคืนค่าด้วย `return` หรือไม่คืนค่าก็ได้ (เรียกว่า "โปรซีเยอร์")

```mn
// ฟังก์ชันคืนค่า
function add(a, b)
  return a + b
end function

let sum = add(10, 5)
print("Sum is: " + str(sum))

// โปรซีเยอร์ (ไม่คืนค่า)
function greet(name)
    print("Hello, " + name)
end function

greet("World") // เรียกใช้ได้โดยตรง
```

### 7. อาร์เรย์ (Arrays)

ใช้ `dim` เพื่อประกาศอาร์เรย์ ดัชนีเริ่มต้นที่ 0

```mn
// อาร์เรย์ 1 มิติ
dim names(3) // สร้างอาร์เรย์ขนาด 3 (index 0, 1, 2)
let names(0) = "Alice"
let names(1) = "Bob"
let names(2) = 123 // หมายเหตุ: อาร์เรย์สามารถเก็บข้อมูลคละประเภทได้
print(names(1)) // Bob

// อาร์เรย์ 2 มิติ (Matrix 2x3)
dim matrix(2, 3)
let matrix(1, 2) = 99
print("Matrix value: " + str(matrix(1, 2))) // 99
```

### 8. การจัดการข้อมูลแบบฝัง (Embedded Data)

ใช้ `DATA` เพื่อฝังข้อมูลไว้ในโค้ด, `READ` เพื่ออ่าน, และ `RESTORE` เพื่อรีเซ็ตตัวชี้กลับไปที่ข้อมูลตัวแรก

```mn
data 10, 20, "Hello", 30.5

dim my_vals(4)

read my_vals(0) // 10
read my_vals(1) // 20
read my_vals(2) // "Hello"
read my_vals(3) // 30.5

print("Third item: " + my_vals(2)) // Hello

restore // รีเซ็ตกลับไปที่ 10
read first_item
print("First item again: " + str(first_item)) // 10
```

### 9. คุณสมบัติขั้นสูง (Advanced Features)

#### Asynchronous Programming

ใช้สำหรับงานที่ต้องรอ เช่น การดาวน์โหลดข้อมูล หรือ I/O เพื่อไม่ให้โปรแกรมหยุดชะงัก

**รูปแบบที่ 1: `run async` - รันงานพร้อมกันโดยไม่ต้องรอ**  
ใช้เมื่อต้องการสั่งให้งานหลายๆ อย่างเริ่มทำงานพร้อมกันในเบื้องหลัง และให้โปรแกรมหลักทำงานต่อไปทันที

```mn
async function long_task(name, delay)
    print("Task " + name + " started.")
    await sleep(delay) // sleep() เป็นฟังก์ชัน async ในตัว
    print("Task " + name + " finished.")
end async function

print("Starting concurrent tasks...")
run async long_task("A", 2), long_task("B", 1)
print("Main program continues immediately.") // บรรทัดนี้จะแสดงผลทันที
```

**รูปแบบที่ 2: `await` - หยุดรอเพื่อรับผลลัพธ์**  
ใช้เมื่อต้องการเรียกฟังก์ชัน async และต้องรอจนกว่าจะได้ค่า `return` กลับมาเพื่อนำไปใช้งานต่อ

```mn
async function fetch_data(source)
    await sleep(1.5) // จำลองการรอข้อมูลจาก network
    return "Data from " + source
end function

print("Fetching user data...")
let user_data = await fetch_data("API Server") // โปรแกรมจะหยุดรอ 1.5 วินาที
print("Result received: " + user_data) // ...จากนั้นจึงทำงานต่อ
```

#### JIT Compilation

ใช้ `jit_function` เพื่อคอมไพล์โค้ดส่วนที่คำนวณหนักๆ ให้เป็นภาษาเครื่อง ณ เวลาที่รัน ทำให้ทำงานได้เร็วขึ้นมาก (เหมาะกับ Loop และคณิตศาสตร์)

```mn
// ฟังก์ชันนี้จะถูกคอมไพล์ด้วย Numba
jit_function fast_calc(iterations)
    let result = 0.0
    for i = 1 to iterations
        let result = result + i
    next i
    return result
end function

let start_time = time()
let total = fast_calc(10000000)
let end_time = time()

print("JIT result: " + str(total))
print("JIT execution time: " + str(end_time - start_time) + "s")
```

### 10. ฟังก์ชันในตัว (Built-in Functions)

- **ทั่วไป:** `str()`, `int()`, `float()`, `time()`, `len()`, `abs()`, `round()`, `type()`, `sqrt()`
- **Async:** `sleep(seconds)` (ต้องใช้กับ `await`)
- **กราฟิก:**
  - `gfx_init(width, height, title)`: สร้างหน้าต่าง
  - `gfx_set_color(r, g, b)`: กำหนดสี (0-255)
  - `gfx_draw_line(x1, y1, x2, y2)`: วาดเส้น
  - `gfx_draw_rect(x, y, w, h, fill)`: วาดสี่เหลี่ยม (fill=1 คือทึบ)
  - `gfx_draw_circle(cx, cy, r, fill)`: วาดวงกลม (fill=1 คือทึบ)
  - `gfx_update()`: อัปเดตการวาดบนหน้าจอ
  - `gfx_wait()`: รอจนกว่าผู้ใช้จะปิดหน้าต่าง

## การมีส่วนร่วม (Contributing)

เรายินดีต้อนรับผู้ที่มีส่วนร่วมทุกคน! หากคุณมีไอเดีย, ต้องการแก้ไขบั๊ก, หรือเพิ่มฟีเจอร์ใหม่ๆ กรุณาเปิด Issue หรือส่ง Pull Request เข้ามาใน Repository นี้

## ใบอนุญาต (License)

โปรเจกต์นี้อยู่ภายใต้ใบอนุญาต Apache-2.0 license - ดูรายละเอียดเพิ่มเติมได้ในไฟล์ `LICENSE`