import tkinter as tk #grafik arayüzünü oluşturma
from tkinter import filedialog, messagebox #dosya seçimi
from reportlab.pdfgen import canvas #pdf'e çevirme
from PIL import Image #görüntüyü açma işleme
import os #dosya yolundan dosya adını alma

class ImageToPDFConverter:
    def __init__(self, root):
        self.root = root #pencere
        self.image_paths = [] #dosya yolunu saklama
        self.output_pdf_name = tk.StringVar() #dosyanın adını alma
        #seçilen görsellerin isimlerini göstermek için listbox kullanılır
        self.selected_images_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE)

        self.initialize_ui() #kullanıcı arayüzü başlatma

    def initialize_ui(self):#arayüzü ve pencereyi oluşturma
        title_label = tk.Label(self.root, text="Image to PDF Converter", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=10) #başlık

        select_images_button = tk.Button(self.root, text="Select Images", command=self.select_images)
        select_images_button.pack(pady=(0, 10)) #resim seç butonu

        self.selected_images_listbox.pack(pady=(0, 10), fill=tk.BOTH, expand=True) #görüntü listesi

        label = tk.Label(self.root, text="Enter output PDF name: ")
        label.pack()

        pdf_name_entry = tk.Entry(self.root, textvariable=self.output_pdf_name, width=40, justify='center')
        pdf_name_entry.pack()

        convert_button = tk.Button(self.root, text="Convert to PDF", command=self.convert_images_to_pdf)
        convert_button.pack(pady=(20, 40))

    def select_images(self):
        self.image_paths = filedialog.askopenfilenames(title="Select Images", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        self.update_selected_images_listbox() #dosya seçim penceresi açılır

    def update_selected_images_listbox(self): #seçim yapıldıktan sonra günceller
        self.selected_images_listbox.delete(0, tk.END) 

        for image_path in self.image_paths:
            _, image_name = os.path.split(image_path)
            self.selected_images_listbox.insert(tk.END, image_name)

    def convert_images_to_pdf(self): #pdf dosyasına dönüştürme
        if not self.image_paths:
            return
        #pdf adı belirlenir eğer pdf adı girilmezse output.pdf olarak varsayılır
        output_pdf_path = self.output_pdf_name.get() + ".pdf" if self.output_pdf_name.get() else "output.pdf"

        pdf = canvas.Canvas(output_pdf_path, pagesize=(612, 792)) #pdf boyutu ayarı

        for image_path in self.image_paths:#görüntü boyutunun sayfaya sığacak şekilde ayarlanması
            img = Image.open(image_path)
            available_width = 540
            available_height = 722
            scale_factor = min(available_width / img.width, available_height / img.height)
            new_width = img.width * scale_factor
            new_height = img.height * scale_factor
            x_centered = (612 - new_width) / 2
            y_centered = (794 - new_height) / 2

            pdf.setFillColorRGB(1, 1, 1)
            pdf.rect(0, 0, 612, 792, fill=True)
            pdf.drawInlineImage(img, x_centered, y_centered, width=new_width, height=new_height)
            pdf.showPage()

        pdf.save()

        messagebox.showinfo("Success", f"PDF successfully created: {output_pdf_path}")

def main():#uygulamayı başlatma
    root = tk.Tk()
    root.title("Image to PDF")
    converter = ImageToPDFConverter(root)
    root.geometry("400x600")
    root.mainloop()


if __name__ == "__main__":
    main()
