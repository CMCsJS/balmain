import tkinter as tk
from tkinter import messagebox
import pyperclip

# Fibonacci dizisini üretme
def generate_fibonacci_upto(limit):
    fib_sequence = [1, 2]
    while True:
        next_fib = fib_sequence[-1] + fib_sequence[-2]
        if next_fib > limit:
            break
        fib_sequence.append(next_fib)
    return fib_sequence

# Onluk sayıyı Fibonacci sistemine çevirme
def decimal_to_fibonacci(number, fib_sequence):
    fib_representation = []
    for fib in reversed(fib_sequence):
        if fib <= number:
            fib_representation.append('1')
            number -= fib
        else:
            if fib_representation:
                fib_representation.append('0')
    return ''.join(fib_representation)

# Fibonacci sisteminden onluk sayıya çevirme
def fibonacci_to_decimal(fib_number, fib_sequence):
    decimal_value = 0
    for i, digit in enumerate(reversed(fib_number)):
        if digit == '1':
            decimal_value += fib_sequence[i]
    return decimal_value

# Metni şifreleme
def encrypt_text(text, k_value, n_value, fib_sequence):
    text = text.replace("\n", " ").strip()

    # Metindeki karakterlerin sayıya dönüştürülmesi (alfabe üzerinden sayıya çevirme)
    char_values = [(ALPHABET.index(char) + k_value) for char in text]
    number_representation = ''.join([str(value).zfill(4) for value in char_values])  # Sayıları 4 basamağa sıfırla

    # İlk Fibonacci dönüşümü
    fib_representation = decimal_to_fibonacci(int(number_representation), fib_sequence)

    # Fibonacci dönüşümünü n defa uygula
    for _ in range(n_value):
        fib_representation = decimal_to_fibonacci(int(fib_representation, 2), fib_sequence)

    return fib_representation

# Şifreyi çözme
def decrypt_fibonacci(fib_text, k_value, n_value, fib_sequence):
    current_text = fib_text

    # n defa Fibonacci çözümleme yap (şifreleme işlemini geri almak için tersine çözümleme)
    for _ in range(n_value):
        current_text = bin(fibonacci_to_decimal(current_text, fib_sequence))[2:]

    # Son olarak, sayılardan karakterlere dönüştür
    decimal_value = fibonacci_to_decimal(current_text, fib_sequence)
    decimal_str = str(decimal_value)
    while len(decimal_str) % 4 != 0:
        decimal_str = '0' + decimal_str

    char_indices = [int(decimal_str[i:i+4]) for i in range(0, len(decimal_str), 4)]
    decrypted_text = ''.join(ALPHABET[idx - k_value] for idx in char_indices)

    return decrypted_text

# Panoya kopyalama
def copy_to_clipboard(text):
    pyperclip.copy(text)
    messagebox.showinfo("Başarılı", "Sonuç panoya kopyalandı!")

# Şifreleme işlemi
def encrypt_action():
    text = text_entry.get("1.0", tk.END).strip()
    try:
        k_value = int(k_entry.get())
        n_value = int(n_entry.get())
        if n_value < 0:
            raise ValueError("N değeri negatif olamaz.")
    except ValueError as ve:
        messagebox.showerror("Hata", f"Geçersiz giriş: {ve}")
        return

    if not text:
        messagebox.showerror("Hata", "Metin boş olamaz!")
        return

    try:
        fib_representation = encrypt_text(text, k_value, n_value, fib_sequence)
        result_entry.delete("1.0", tk.END)
        result_entry.insert(tk.END, fib_representation)
    except Exception as e:
        messagebox.showerror("Hata", f"Şifreleme sırasında bir hata oluştu: {e}")

# Şifre çözme işlemi
def decrypt_action():
    fib_text = text_entry.get("1.0", tk.END).strip()
    try:
        k_value = int(k_entry.get())
        n_value = int(n_entry.get())
        if n_value < 0:
            raise ValueError("N değeri negatif olamaz.")
    except ValueError as ve:
        messagebox.showerror("Hata", f"Geçersiz giriş: {ve}")
        return

    if not fib_text:
        messagebox.showerror("Hata", "Şifre çözmek için bir metin girin!")
        return

    try:
        decrypted_text = decrypt_fibonacci(fib_text, k_value, n_value, fib_sequence)
        result_entry.delete("1.0", tk.END)
        result_entry.insert(tk.END, decrypted_text)
    except Exception as e:
        messagebox.showerror("Hata", f"Şifre çözme sırasında bir hata oluştu: {e}")

# Fibonacci dizisini oluştur
max_value = 10**100  # Üst sınır
fib_sequence = generate_fibonacci_upto(max_value)

# Alfabe
ALPHABET = (
    " ABCÇDEFGĞHIİJKLMNOPOÖQRSŞTUÜVWXYZ"
    "abcçdefgğhıijklmnopoöqrsştuüvwxyz"
    "ÄÖÜäöüß"
    ".,!?;:'\"()[]{}<>-_/\\@#&%*$+=^|~`"
)

# Tkinter arayüzü
root = tk.Tk()
root.title("Fibonacci Şifreleme ve Çözme")

# Kullanıcı arayüzü bileşenleri
tk.Label(root, text="Metin veya Şifre Girdisi").pack()
text_entry = tk.Text(root, height=5, width=50)
text_entry.pack()

tk.Label(root, text="K Değeri").pack()
k_entry = tk.Entry(root)
k_entry.pack()

tk.Label(root, text="N Değeri").pack()
n_entry = tk.Entry(root)
n_entry.pack()

tk.Button(root, text="Şifrele", command=encrypt_action).pack()
tk.Button(root, text="Şifre Çöz", command=decrypt_action).pack()

result_label = tk.Label(root, text="Çıktı")
result_label.pack()

result_entry = tk.Text(root, height=5, width=50)
result_entry.pack()

tk.Button(root, text="Sonucu Kopyala", command=lambda: copy_to_clipboard(result_entry.get("1.0", tk.END).strip())).pack()

root.mainloop()
