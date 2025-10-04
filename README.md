<div align="center">

![Momentum Logo](./momentum_logo.ico)  

# คู่มือภาษา Momentum หรือ Momentumlang (`.mn`)

</div>

**Momentum** คือภาษาโปรแกรมสมัยใหม่ที่ได้รับการออกแบบมาเพื่อการคำนวณทางวิทยาศาสตร์, การจัดการข้อมูล, และการเขียนโปรแกรมทั่วไป โดยเน้นความเรียบง่าย, อ่านง่าย, และมีประสิทธิภาพสูง ได้รับแรงบันดาลใจจากจิตวิญญาณที่เข้าถึงง่ายของภาษา BASIC ผสมผสานกับพลังการคำนวณของ Python

เอกสารนี้เป็นคู่มือฉบับสมบูรณ์สำหรับภาษา Momentum หรือ Momentumlang ครอบคลุมตั้งแต่แนวคิดพื้นฐานไปจนถึงคุณสมบัติขั้นสูง เหมาะสำหรับผู้เริ่มต้นและนักพัฒนาที่มีประสบการณ์

---

## สารบัญ

- [คู่มือภาษา Momentum หรือ Momentumlang (`.mn`)](#คู่มือภาษา-momentum-หรือ-momentumlang-mn)
  - [สารบัญ](#สารบัญ)
  - [1. ปรัชญาและหลักการออกแบบ](#1-ปรัชญาและหลักการออกแบบ)
  - [2. เริ่มต้นใช้งาน (Getting Started)](#2-เริ่มต้นใช้งาน-getting-started)
    - [การติดตั้ง](#การติดตั้ง)
    - [การรันโปรแกรม](#การรันโปรแกรม)
    - [โปรแกรมแรกของคุณ Hello, World!](#โปรแกรมแรกของคุณ-hello-world)
  - [3. พื้นฐานภาษา (Language Fundamentals)](#3-พื้นฐานภาษา-language-fundamentals)
    - [โครงสร้างและไวยากรณ์ (Syntax and Structure)](#โครงสร้างและไวยากรณ์-syntax-and-structure)
    - [ตัวแปรและการกำหนดค่า (Variables \& Assignment)](#ตัวแปรและการกำหนดค่า-variables--assignment)
    - [ชนิดข้อมูล (Data Types)](#ชนิดข้อมูล-data-types)
    - [ตัวดำเนินการ (Operators)](#ตัวดำเนินการ-operators)
      - [ตารางตัวดำเนินการ (เรียงตามลำดับความสำคัญจากสูงไปต่ำ)](#ตารางตัวดำเนินการ-เรียงตามลำดับความสำคัญจากสูงไปต่ำ)
  - [4. โครงสร้างควบคุม (Control Flow)](#4-โครงสร้างควบคุม-control-flow)
    - [เงื่อนไข `IF...THEN...ENDIF`](#เงื่อนไข-ifthenendif)
    - [เลือกเงื่อนไข `SWITCH...CASE...ENDSWITCH`](#เลือกเงื่อนไข-switchcaseendswitch)
    - [การวนซ้ำ `WHILE...WEND`](#การวนซ้ำ-whilewend)
    - [การวนซ้ำ `FOR` Loops (`FOR...TO` and `FOR EACH`)](#การวนซ้ำ-for-loops-forto-and-for-each)
    - [การควบคุม Loop `BREAK` และ `CONTINUE`](#การควบคุม-loop-break-และ-continue)
  - [5. ฟังก์ชัน (Functions)](#5-ฟังก์ชัน-functions)
    - [การนิยามและการเรียกใช้](#การนิยามและการเรียกใช้)
    - [ขอบเขตของตัวแปร (Variable Scope)](#ขอบเขตของตัวแปร-variable-scope)
  - [6. การจัดการข้อผิดพลาด (Error Handling)](#6-การจัดการข้อผิดพลาด-error-handling)
  - [7. โมดูลและการจัดการโค้ด](#7-โมดูลและการจัดการโค้ด)
  - [8. คุณสมบัติขั้นสูง (Advanced Features)](#8-คุณสมบัติขั้นสูง-advanced-features)
    - [Pipe Operator (`|>`)](#pipe-operator-)
    - [Asynchronous Programming](#asynchronous-programming)
    - [JIT Compilation](#jit-compilation)
    - [การดีบักด้วย `DEBUG`](#การดีบักด้วย-debug)
  - [9. ระบบข้อมูลในตัว `DATA`, `READ`, `RESTORE`](#9-ระบบข้อมูลในตัว-data-read-restore)
  - [10. การมีส่วนร่วม (Contributing)](#10-การมีส่วนร่วม-contributing)
  - [11. ใบอนุญาต (License)](#11-ใบอนุญาต-license)

---

## 1. ปรัชญาและหลักการออกแบบ

-   **ความเรียบง่ายต้องมาก่อน (Simplicity First)** ไวยากรณ์ถูกออกแบบมาให้อ่านง่ายเหมือนภาษาอังกฤษ ลดสัญลักษณ์ที่ไม่จำเป็น เพื่อให้โค้ดสามารถสื่อสารเจตนาของผู้เขียนได้อย่างชัดเจน
-   **ทรงพลังแต่เข้าถึงง่าย (Powerful yet Approachable)** ผสมผสานความง่ายของ BASIC เข้ากับความสามารถในการคำนวณทางวิทยาศาสตร์ของ Python ทำให้ผู้เริ่มต้นสามารถสร้างโปรแกรมที่มีประโยชน์ได้รวดเร็ว
-   **โครงสร้างที่ชัดเจน (Structured and Explicit)** บังคับใช้การประกาศตัวแปรด้วย `LET` และใช้บล็อกคำสั่งที่ชัดเจน (`IF...ENDIF`, `FUNCTION...ENDFUNCTION`) เพื่อส่งเสริมการเขียนโค้ดที่เป็นระเบียบและลดข้อผิดพลาด
-   **ครบเครื่องในตัว (Batteries Included)** มาพร้อมกับฟังก์ชันทางคณิตศาสตร์, สถิติ, และพีชคณิตเชิงเส้นที่จำเป็น ทำให้ไม่ต้องพึ่งพาไลบรารีภายนอกสำหรับงานคำนวณส่วนใหญ่

---

## 2. เริ่มต้นใช้งาน (Getting Started)

### การติดตั้ง
1.  ไปที่หน้า **Releases** ของโปรเจกต์บน GitHub
2.  ดาวน์โหลดไฟล์ `Momentum_Setup_vX.X.exe` เวอร์ชันล่าสุด
3.  รันตัวติดตั้งและทำตามขั้นตอนบนหน้าจอ

### การรันโปรแกรม
-   **รันไฟล์ `.mn`**
    ```bash
    python intp.py your_program.mn
    ```
-   **รันโหมดโต้ตอบ (REPL)**
    ```bash
    python intp.py
    ```

### โปรแกรมแรกของคุณ Hello, World!
สร้างไฟล์ชื่อ `hello.mn` และใส่โค้ดต่อไปนี้
```momentum
// my first program in Momentum
print("Hello, World!")
```
รันโปรแกรมจาก Terminal
```bash
python intp.py hello.mn
```
คุณจะเห็นข้อความ `Hello, World!` แสดงผลออกมา

---

## 3. พื้นฐานภาษา (Language Fundamentals)

### โครงสร้างและไวยากรณ์ (Syntax and Structure)
-   **Comments** ใช้ `//` เพื่อเขียนคอมเมนต์ ทุกอย่างที่อยู่หลัง `//` ในบรรทัดนั้นจะถูกข้ามไป
-   **Case-Insensitivity** คีย์เวิร์ดของภาษา (`PRINT`, `LET`, `IF`, etc.) ไม่สนใจตัวพิมพ์เล็ก-ใหญ่ อย่างไรก็ตาม ชื่อตัวแปรจะถูกจัดการเป็นตัวพิมพ์เล็กทั้งหมดเป็นการภายในเพื่อความเป็นเอกภาพ (`MyVar` และ `myvar` คือตัวแปรเดียวกัน)
-   **Blocks** โค้ดถูกจัดกลุ่มเป็นบล็อกด้วยคีย์เวิร์ดเปิดและปิดที่ชัดเจน เช่น `IF...ENDIF`, `WHILE...WEND`, `FUNCTION...ENDFUNCTION`
-   **Multiple Statements** สามารถเขียนหลายคำสั่งในบรรทัดเดียวได้โดยใช้เครื่องหมายเซมิโคลอน (`;`) คั่น
    ```momentum
    let x = 10; let y = 20; print(x + y)
    ```

### ตัวแปรและการกำหนดค่า (Variables & Assignment)
กฎสำคัญที่สุดคือ **"ประกาศด้วย `LET`, กำหนดค่าใหม่โดยไม่มี `LET`"**

-   **การประกาศ (Declaration)**
    -   `LET var = value` ประกาศตัวแปรพร้อมกำหนดค่าเริ่มต้น
    -   `LET var` ประกาศตัวแปรโดยไม่กำหนดค่าเริ่มต้น ตัวแปรนั้นจะมีค่าเป็น `None` ซึ่งมีประโยชน์สำหรับการจองชื่อตัวแปรไว้ก่อน
-   **การกำหนดค่าใหม่ (Re-assignment)** เมื่อตัวแปรถูกประกาศแล้ว สามารถเปลี่ยนค่าได้โดยใช้ `=`
    ```momentum
    // ประกาศ
    let score = 0
    let player_name

    // กำหนดค่าใหม่
    score = 100
    player_name = "Alex"
    ```

### ชนิดข้อมูล (Data Types)

-   **`INTEGER` & `FLOAT`** ตัวเลขจำนวนเต็มและทศนิยม
    ```momentum
    let count = 10
    let pi = 3.14159
    ```
-   **`STRING`** ข้อความที่อยู่ภายใน `"` หรือ `'` รองรับ Escape Characters เช่น `\n` (ขึ้นบรรทัดใหม่) และ `\t` (แท็บ)
    -   **F-Strings** วิธีที่ทรงพลังในการแทรกนิพจน์ลงในข้อความ
    ```momentum
    let name = "Momentum"
    let version = 1.1
    print(f"Welcome to {name} v{version}. Two plus two is {2 + 2}.")
    ```
-   **`ARRAY` / `MATRIX`** ชุดข้อมูลหลายมิติที่จัดเก็บตามลำดับ (0-based index) มีประสิทธิภาพสูงเพราะใช้ NumPy เป็นเบื้องหลัง
    -   **การสร้าง**
        ```momentum
        dim empty_array(10)      // สร้าง Array 1 มิติ 10 ช่อง (ค่าเริ่มต้นเป็น 0)
        dim matrix = mat_zeros(3, 4) // สร้างเมทริกซ์ 3x4 ที่มีค่าเป็น 0 ทั้งหมด
        let literal_array = [10, 20, "thirty"] // สร้าง Array จากค่า Literal
        ```    -   **การเข้าถึงและกำหนดค่า**
        ```momentum
        literal_array(0) = 15
        print(literal_array(2)) // "thirty"
        matrix(1, 2) = 99
        ```
-   **`DICTIONARY`** ชุดข้อมูลแบบ Key-Value ที่ไม่มีลำดับ Key ต้องเป็น `STRING` เสมอ
    ```momentum
    let config = {"host" "localhost", "port" 8080, "is_active" 1}
    print(f"Connecting to {config["host"]}{config["port"]}")
    config["is_active"] = 0 // เปลี่ยนค่า
    ```
-   **`NONE`** ชนิดข้อมูลพิเศษที่หมายถึง "ไม่มีค่า" เป็นค่าเริ่มต้นของตัวแปรที่ประกาศโดยไม่มีการกำหนดค่า

### ตัวดำเนินการ (Operators)
-   **Truthiness and Falsiness** ในเงื่อนไข (`IF`, `WHILE`), ค่า `0` และ `None` ถือเป็นเท็จ (false) ส่วนค่าอื่นๆ ทั้งหมด (รวมถึง String ที่ไม่ว่างเปล่า) ถือเป็นจริง (true)

#### ตารางตัวดำเนินการ (เรียงตามลำดับความสำคัญจากสูงไปต่ำ)
| ลำดับ | ประเภท | ตัวดำเนินการ | ตัวอย่าง |
|--- |--- |--- |--- |
| 1 | Grouping & Access | `()`, `[]` | `(a + b) * c`, `my_array[0]` |
| 2 | Unary | `NOT` | `NOT is_ready` |
| 3 | Multiplicative | `*`, `/` | `price * quantity` |
| 4 | Additive | `+`, `-` | `subtotal + tax` |
| 5 | Relational | `>`, `<`, `>=`, `<=` | `score >= 90` |
| 6 | Equality | `==`, `!=` | `name == "admin"` |
| 7 | Logical AND | `AND` | `is_logged_in AND has_permission` |
| 8 | Logical OR | `OR` | `is_admin OR is_owner` |
| 9 | Chaining | `|>` (Pipe) | `data |> trim |> upper` |
| 10 | Assignment | `=` | `x = 10` |

---

## 4. โครงสร้างควบคุม (Control Flow)

### เงื่อนไข `IF...THEN...ENDIF`
**Syntax**```momentum
IF condition THEN
    ...
ELSE IF another_condition THEN
    ...
ELSE
    ...
END IF
```
**Example**
```momentum
let temperature = 32
if temperature > 30 then
    print("It's hot.")
else if temperature < 15 then
    print("It's cold.")
else
    print("It's pleasant.")
end if
```

### เลือกเงื่อนไข `SWITCH...CASE...ENDSWITCH`
**Syntax**
```momentum
SWITCH expression
    CASE value1, value2
        ...
    CASE value3
        ...
    DEFAULT
        ...
END SWITCH
```
**Note** `SWITCH` ใน Momentum ไม่มีการ "fall-through" เมื่อเจอ `CASE` ที่ตรงกันแล้ว จะทำงานในบล็อกนั้นและออกจาก `SWITCH` ทันที
```momentum
let http_status = 404
switch http_status
    case 200
        print("OK")
    case 403, 404
        print("Client Error Not Found or Forbidden")
    case 500
        print("Server Error")
    default
        print("Unknown status")
end switch
```

### การวนซ้ำ `WHILE...WEND`
**Syntax** `WHILE condition ... WEND`
```momentum
let buffer = ""
while len(buffer) < 10
    // สมมติว่า get_char() เป็นฟังก์ชันที่อ่านตัวอักษรทีละตัว
    // buffer = buffer + get_char() 
wend
```

### การวนซ้ำ `FOR` Loops (`FOR...TO` and `FOR EACH`)
1.  **`FOR...TO...STEP`** สำหรับการวนซ้ำตามจำนวนรอบที่แน่นอน
    ```momentum
    // พิมพ์เลขคู่จาก 10 ถึง 2
    for i = 10 to 2 step -2
        print(i)
    next i
    ```
2.  **`FOR EACH...IN`** สำหรับวนซ้ำสมาชิกทุกตัวใน Collection (เช่น Array)
    ```momentum
    let file_list = os_list_dir(".")
    print("Files in current directory")
    for each filename in file_list
        if os_is_file(filename) then
            print(f"- {filename}")
        end if
    next filename
    ```

### การควบคุม Loop `BREAK` และ `CONTINUE`
-   `BREAK` ออกจาก Loop ทันที (ใช้ได้กับ `FOR` และ `WHILE`)
-   `CONTINUE` ข้ามรอบปัจจุบันและไปเริ่มรอบถัดไปทันที

---

## 5. ฟังก์ชัน (Functions)

### การนิยามและการเรียกใช้
ฟังก์ชันช่วยให้คุณสามารถจัดกลุ่มโค้ดที่ทำงานเฉพาะอย่างไว้ด้วยกันและเรียกใช้ซ้ำได้
```momentum
function is_valid_email(email)
    // การตรวจสอบแบบง่าย
    if len(email) > 5 and len(split(email, "@")) == 2 then
        return 1 // True
    else
        return 0 // False
    end if
end function

let email = "test@example.com"
if is_valid_email(email) then
    print("Email format is valid.")
end if
```

### ขอบเขตของตัวแปร (Variable Scope)
-   **Global Scope** ตัวแปรที่ประกาศนอกฟังก์ชันใดๆ สามารถเข้าถึงได้จากทุกที่
-   **Local Scope** พารามิเตอร์และตัวแปรที่ประกาศด้วย `LET` ภายในฟังก์ชัน จะมีอยู่แค่ในฟังก์ชันนั้นๆ
```momentum
let app_name = "My App" // Global

function print_header()
    let version = "1.0" // Local to print_header
    print(f"{app_name} - Version {version}")
end function

print_header()
// print(version) // <-- จะเกิด Error เพราะ version เป็น Local
```

---

## 6. การจัดการข้อผิดพลาด (Error Handling)
ใช้ `TRY...CATCH` เพื่อจัดการกับข้อผิดพลาดที่อาจเกิดขึ้นขณะโปรแกรมทำงาน (Runtime Errors) เช่น การหารด้วยศูนย์ หรือการเข้าถึงไฟล์ที่ไม่มีอยู่จริง
```momentum
function get_config(filename)
    try
        let content = file_read(filename)
        return json_parse(content)
    catch err
        print(f"Could not load config '{filename}' {err}")
        // คืนค่า config เริ่มต้นถ้าไฟล์มีปัญหา
        return {"default" 1} 
    end try
end function
```

---

## 7. โมดูลและการจัดการโค้ด
ใช้ `IMPORT "filename.mn"` เพื่อนำเข้าฟังก์ชันและตัวแปรทั้งหมดจากไฟล์อื่น ซึ่งเป็นหัวใจของการสร้างโปรแกรมขนาดใหญ่ที่มีการจัดระเบียบที่ดี

**ไฟล์ `string_helpers.mn`**
```momentum
function is_empty(text)
    return len(trim(text)) == 0
end function
```

**ไฟล์ `main.mn`**
```momentum
import "string_helpers.mn"

let user_input = ""
if is_empty(user_input) then
    print("Input cannot be empty.")
end if
```

---

## 8. คุณสมบัติขั้นสูง (Advanced Features)

### Pipe Operator (`|>`)
ทำให้การเรียกฟังก์ชันซ้อนกัน (nested function calls) อ่านง่ายขึ้นโดยเปลี่ยนลำดับการเขียนให้เป็นเหมือนลำดับการทำงาน
```momentum
let raw_data = "   apple, BANANA, Cherry   "

// แบบดั้งเดิม (อ่านจากในไปนอก)
// let processed = split(upper(trim(raw_data)), ",")

// แบบใช้ Pipe (อ่านจากซ้ายไปขวา)
let processed = raw_data |> trim |> upper |> split(",")

debug processed // [DEBUG] processed (ARRAY) ['APPLE' 'BANANA' 'CHERRY']
```

### Asynchronous Programming
**แนวคิด** ใช้สำหรับงานที่ต้อง "รอ" (เช่น รอการตอบกลับจากเครือข่าย, รอการอ่านไฟล์ขนาดใหญ่) โดยไม่หยุดการทำงานของโปรแกรมส่วนอื่น
```momentum
async function fetch_data(url)
    print(f"Fetching from {url}...")
    await sleep(1.5) // จำลองการรอ Network
    return f"Data from {url}"
end function

// รันสอง task พร้อมกันโดยไม่รอให้อันแรกเสร็จก่อน
run async fetch_data("API 1"), fetch_data("API 2")

print("Main program continues while tasks are running...")
await sleep(2) // รอให้ task ทั้งหมดทำงานเสร็จ
print("All fetching complete.")
```

### JIT Compilation
**แนวคิด** แปลงโค้ด Momentum เป็น Machine Code ประสิทธิภาพสูงขณะรัน (Just-In-Time) เหมาะสำหรับฟังก์ชันที่มีการคำนวณทางคณิตศาสตร์ใน Loop จำนวนมาก
-   **ข้อจำกัด** `jit_function` รองรับเฉพาะการทำงานกับตัวเลขและฟังก์ชันคณิตศาสตร์พื้นฐาน ไม่สามารถเรียกใช้ฟังก์ชันจัดการ String หรือ I/O ได้
```momentum
jit_function mandelbrot_iterations(cx, cy, max_iter)
    let x = 0.0; let y = 0.0
    let iter = 0
    while x*x + y*y <= 4 and iter < max_iter
        let xtemp = x*x - y*y + cx
        y = 2*x*y + cy
        x = xtemp
        iter = iter + 1
    next
    return iter
end function
```

### การดีบักด้วย `DEBUG`
เป็นเครื่องมือที่ง่ายและรวดเร็วสำหรับตรวจสอบค่าของนิพจน์ใดๆ ขณะที่โปรแกรมทำงาน
```momentum
let config = {"user" "admin", "retries" 3}
debug config["user"] == "admin"
debug config["retries"] * 2
```

---

## 9. ระบบข้อมูลในตัว `DATA`, `READ`, `RESTORE`
เป็นวิธีที่เรียบง่ายในการฝังชุดข้อมูลไว้ในซอร์สโค้ดโดยตรง เหมาะสำหรับสคริปต์ขนาดเล็กหรือโปรแกรมเพื่อการศึกษา
```momentum
data "apple", 1.50, "banana", 0.75, "cherry", 3.00

print("Fruit Prices")
for i = 1 to 3
    let fruit_name, price
    read fruit_name, price
    print(f"- {fruit_name} ${price}")
next i
```

---

## 10. การมีส่วนร่วม (Contributing)

เรายินดีต้อนรับผู้ที่มีส่วนร่วมทุกคน! หากคุณมีไอเดีย, ต้องการแก้ไขบั๊ก, หรือเพิ่มฟีเจอร์ใหม่ๆ กรุณาเปิด Issue หรือส่ง Pull Request เข้ามาใน Repository นี้

## 11. ใบอนุญาต (License)

โปรเจกต์นี้อยู่ภายใต้ใบอนุญาต Apache-2.0 license - ดูรายละเอียดเพิ่มเติมได้ในไฟล์ `LICENSE`
