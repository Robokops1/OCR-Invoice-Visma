import customtkinter
import os
from PIL import Image, ImageTk, ImageDraw
from Main_Test import process_image, clean_extracted_text, extract_correct_total
from tkinter import filedialog
from API_TEST import create_xml, send_invoice_to_api, clean_date
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("OCR Interface.py")
        self.geometry("1100x900")

        #Summai
        self.total_amounts = [] # satur sarakstu ar total summam no katra izvēlētā rēķina.
        # Additional attributes for logging
        self.invoice_logs = []  # List to store log entries

        #Uzmetums
        self.processed_image_path = None
        self.extracted_texts = {}
        self.display_photo = None

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_paths = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Image Example")
        self.large_test_image = customtkinter.CTkImage(Image.open(os.path.join(image_paths, "3_png_jpg.rf.e51c6f26998bb3fbcb684ff9e3752d27.jpg")), size=(640, 600))

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        # Frame for Image Display
        self.image_frame = customtkinter.CTkFrame(self)
        self.image_frame.grid(row=0, column=0, padx=20, pady=20)

        # Image Display Label
        self.image_label = customtkinter.CTkLabel(self.image_frame, text= "")
        self.image_label.grid(row=0, column=0)


        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text=" OCR",
                                                             compound="left", font= ("Helvetica", 14, "bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="OCR",
                                                   font= ("Helvetica", 14, "bold"),
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"))

        #LOad image
        self.load_image_button = customtkinter.CTkButton(self.navigation_frame, text="Load Image", command=self.load_image, font= ("Helvetica", 14, "bold"))
        self.load_image_button.grid(row=2, column=0, padx=20, pady=10)


        #LOad image 2
        self.load_image_button_1 = customtkinter.CTkButton(self.navigation_frame, text="Load Image SUM", command=self.load_image_SUM, font= ("Helvetica", 14, "bold"))
        self.load_image_button_1.grid(row=5, column=0, padx=20, pady=10)
        self.load_image_button_1.place(x = 100, y = 270)

        # Text area for logging
        self.log_text_area = customtkinter.CTkTextbox(self.navigation_frame, width=300, height=150, state="disabled")
        self.log_text_area.grid(row=4, column=0, padx=20, pady=20)

        #CLEAR SUM BUTTon
        self.button_1 = customtkinter.CTkButton(self.navigation_frame, text="Clear", command=self.clear_logs_and_totals, font= ("Helvetica", 14, "bold"))
        self.button_1.grid(row=4, column=0, padx=20, pady=10)
        self.button_1.place(x = 100, y = 620)

        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.home_frame_large_image_label = customtkinter.CTkLabel(self.home_frame, text="", image=self.large_test_image)
        self.home_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)

        # Text Display Label
        self.text_label = customtkinter.CTkLabel(self.home_frame, text=" ", font= ("Helvetica", 14, "bold"))
        self.text_label.grid(row=1, column=0, padx=20, pady=10)
        self.text_label.place(x = 30, y = 610)

        #text summ
        self.text_label_3 = customtkinter.CTkLabel(self.navigation_frame, text="Total SUM = 0.00", font= ("Helvetica", 14, "bold"))
        self.text_label_3.grid(row=4, column=0, padx=20, pady=10)
        self.text_label_3.place(x = 110, y = 410)
        #text slider
        self.threshold_value = customtkinter.DoubleVar()  
        self.text_label_1 = customtkinter.CTkLabel(self.navigation_frame, text="Threshold", 
                                                                    font= ("Helvetica", 14, "bold"))
        self.text_label_1.grid(row=3, column=0, padx=20, pady=20)
        self.text_label_1.place(x = 110, y = 140)
       
        #Slider result
        self.text_label_2 = customtkinter.CTkLabel(self.navigation_frame, text="0.50", 
                                                                    font= ("Helvetica", 14, "bold"))
        self.text_label_2.grid(row=3, column=0, padx=20, pady=10)
        self.text_label_2.place(x = 190, y = 140)
       
        # Slider
        self.threshold_value = customtkinter.DoubleVar(value=0.5)  

        # Slier 
        self.home_frame_slider = customtkinter.CTkSlider(self.navigation_frame, from_=0, to=1, number_of_steps=10, variable=self.threshold_value, command=self.on_threshold_change)
        self.home_frame_slider.grid(row=3, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")

        # Text area for data
        self.log_text_area_1 = customtkinter.CTkTextbox(self.home_frame, width=300, height=150, state="disabled")
        self.log_text_area_1.place(x = 400, y = 640)
        
        #Button for API
        self.home_frame_button_1 = customtkinter.CTkButton(self.home_frame, text="Send data to Horizon", command=self.send_data_to_api, font= ("Helvetica", 14, "bold"))
        self.home_frame_button_1.place(x = 470, y = 800)

        self.home_frame_button_1 = customtkinter.CTkButton(self.home_frame, text="Invoice Number", command=self.show_invoice_number, font= ("Helvetica", 14, "bold"))
        self.home_frame_button_1.place(x = 50, y = 650)
        self.home_frame_button_2 = customtkinter.CTkButton(self.home_frame, text="Total", command=self.show_total, font= ("Helvetica", 14, "bold"))
        self.home_frame_button_2.place(x = 50, y = 690)
        self.home_frame_button_3 = customtkinter.CTkButton(self.home_frame, text="Supplier", command=self.show_supplier, font= ("Helvetica", 14, "bold"))
        self.home_frame_button_3.place(x = 50, y = 730)
        self.home_frame_button_4 = customtkinter.CTkButton(self.home_frame, text="Date", command=self.show_date, font= ("Helvetica", 14, "bold"))
        self.home_frame_button_4.place(x = 50, y = 770)
        self.home_frame_button_5 = customtkinter.CTkButton(self.home_frame, text="Due Date", command=self.show_due_date, font= ("Helvetica", 14, "bold"))
        self.home_frame_button_5.place(x = 50, y = 810)

        # create second frame
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # create third frame
        self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # select default frame
        self.select_frame_by_name("home")


    def on_threshold_change(self, value):
        # Update the label to show the current value
        self.text_label_2.configure(text=f"{float(value):.2f}")

        # If an image is currently loaded, reprocess it with the new threshold
        if hasattr(self, 'current_image_path') and self.current_image_path:
            self.load_image(file_path=self.current_image_path, use_existing_threshold=True)



    def clear_logs_and_totals(self):
        # Clear log disp
        self.log_text_area.configure(state="normal")  # Enable editing
        self.log_text_area.delete("1.0", "end")  # Clear all content
        self.log_text_area.configure(state="disabled")  # Disable editing 

        # Reset the total amounts list and update the display
        self.total_amounts = []
        self.update_total_sum_label()  # refresh the total sum label


    def load_image_SUM(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png ")], multiple=True)  # multiple file selection
        for path in file_path:
            if path:
                self.process_image_and_extract_total(path)


    def process_image_and_extract_total(self, file_path):
        threshold = 0.5
        extracted_texts, processed_image_path = process_image(file_path, threshold)

        # Try to find 'total' first, if not found, then fall back to 'sub_total'
        total_key = next((key for key in extracted_texts if 'total' in key.lower() and 'sub' not in key.lower()), None)
        if not total_key:  # If 'total' not found, check for 'sub_total'
            total_key = next((key for key in extracted_texts if 'sub_total' in key.lower()), None)

        if total_key:
            total_amount, _ = extracted_texts[total_key]
            cleaned_total = clean_extracted_text(total_amount, 'TOTAL')  # Initial cleaning of the total amount
            corrected_total = extract_correct_total({total_key: cleaned_total})  # Correct the formatting 

            try:
                clean_total = float(corrected_total) if corrected_total is not None else None
                if clean_total is not None:
                    self.total_amounts.append(clean_total)
                    invoice_name = os.path.basename(file_path)
                    log_entry = f"{invoice_name}: {clean_total:.2f}"
                    self.invoice_logs.append(log_entry)
                    self.update_log_display(log_entry)
                else:
                    raise ValueError("Failed to extract a valid total")
            except ValueError as e:
                print(f"Error converting '{cleaned_total}' to float: {e}")
                log_entry = f"{invoice_name}: Error in total value"
                self.invoice_logs.append(log_entry)
                self.update_log_display(log_entry)

        self.update_total_sum_label()
    
    def update_log_display(self, entry):
        self.log_text_area.configure(state="normal")  # Enable editing of the text area
        self.log_text_area.insert("end", entry + "\n")  # Insert new log entry
        self.log_text_area.configure(state="disabled")  # Disable editing again
        self.log_text_area.see("end")  # Scroll to the end of the text area

    def update_total_sum_label(self):
        total_sum = sum(self.total_amounts)
        self.text_label_3.configure(text=f"Total Sum: {total_sum:.2f}")  # Display formatted sum


    def send_data_to_api(self):
        # Izgūstam nepieciešamos datus no `self.extracted_texts`
        invoice_number = self.extracted_texts.get('INVOICE NUMBER', ('', ''))[0]
        due_date = self.extracted_texts.get('DUE_DATE', ('', ''))[0]
        total = self.extracted_texts.get('TOTAL', ('', ''))[0]
        date = self.extracted_texts.get('INVOICE DATE', ('', ''))[0]

        # Clean date
        cleaned_date = clean_date(date)
        cleaned_due_date = clean_date(due_date)

        # Create XML
        xml_data = create_xml(invoice_number, cleaned_date, cleaned_due_date, total)
        
        # Send to API
        send_invoice_to_api(xml_data)




    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif")])
        if file_path:
            self.original_image = Image.open(file_path)
            self.original_photo = ImageTk.PhotoImage(self.original_image.resize((640, 600), Image.Resampling.LANCZOS))
            self.home_frame_large_image_label.configure(image=self.original_photo)
            self.home_frame_large_image_label.image = self.original_photo  # reference!

            current_threshold = self.threshold_value.get()
            
            # Perform OCR with current threshold
            self.extracted_texts, self.processed_image_path = process_image(file_path, threshold=current_threshold)
            print("OCR Results:", self.extracted_texts)

            # Clear the text area before displaying new data
            self.log_text_area_1.configure(state="normal")
            self.log_text_area_1.delete("1.0", "end")

            # Iterate through the dictionary and format the extracted data
            for key, value in self.extracted_texts.items():
                if isinstance(value, tuple):
                    data, bbox = value
                    formatted_data = f"{key}: {data}\n"
                    self.log_text_area_1.insert("end", formatted_data)

            self.log_text_area_1.configure(state="disabled")

    def update_display(self, image, box=None):
        if image:
            image_copy = image.copy()
            if box:
                # Draw the bounding box on the image
                draw = ImageDraw.Draw(image_copy)
                draw.rectangle(box, outline='red', width=2)
            # Resize the image for display purposes
            image_copy = image_copy.resize((640, 600), Image.Resampling.LANCZOS)
            self.display_photo = ImageTk.PhotoImage(image_copy)
            self.home_frame_large_image_label.configure(image=self.display_photo)
            self.home_frame_large_image_label.image = self.display_photo
        else:
            print("No image loaded")

    def show_invoice_number(self):

        invoice_number_key = next((key for key in self.extracted_texts if 'invoice number' in key.lower()), None)
        if invoice_number_key:
            invoice_data = self.extracted_texts[invoice_number_key]
            # Ensure the data includes both text and a bounding box
            if isinstance(invoice_data, tuple) and len(invoice_data) == 2:
                invoice_number, box = invoice_data
                display_text = f"Invoice Number: {invoice_number}"
                # Ensure the box is a tuple and correctly formatted
                if isinstance(box, tuple) and len(box) == 4:
                    self.update_display(self.original_image, box)
                else:
                    display_text = "Invoice number not found"
                    self.update_display(self.original_image)  

        self.text_label.configure(text=display_text)

    def show_total(self):

    # Find 'total' while excluding 'sub_total'
        total_key = next((key for key in self.extracted_texts if 'total' in key.lower() and 'sub' not in key.lower()), None)
        if total_key:
            total_data = self.extracted_texts[total_key]
            if isinstance(total_data, tuple) and len(total_data) == 2:
                total_amount, box = total_data
                display_text = f"Total: {total_amount}"
                if isinstance(box, tuple) and len(box) == 4:
                    self.update_display(self.original_image, box)
                else:
                    display_text = "Total not found"
                    self.update_display(self.original_image)

        self.text_label.configure(text=display_text)

    def show_supplier(self):

        supplier_key = next((key for key in self.extracted_texts if 'name_client' in key.lower()), None)
        if supplier_key:
            supplier_data = self.extracted_texts[supplier_key]
            if isinstance(supplier_data, tuple) and len(supplier_data) == 2:
                supplier_name, box = supplier_data
                display_text = f"Supplier: {supplier_name}"
                if isinstance(box, tuple) and len(box) == 4:
                    self.update_display(self.original_image, box)
                else:
                    display_text = "Supplier not found"
                    self.update_display(self.original_image)

        self.text_label.configure(text=display_text)

    def show_date(self):

        date_key = next((key for key in self.extracted_texts if 'date' in key.lower()), None)
        if date_key:
            date_data = self.extracted_texts[date_key]
            if isinstance(date_data, tuple) and len(date_data) == 2:
                date, box = date_data
                display_text = f"Date: {date}"
                if isinstance(box, tuple) and len(box) == 4:
                    self.update_display(self.original_image, box)
                else:
                    display_text = "Date not found"
                    self.update_display(self.original_image)

        self.text_label.configure(text=display_text)

    def show_due_date(self):

        due_date_key = next((key for key in self.extracted_texts if 'due_date' in key.lower()), None)
        if due_date_key:
            due_date_data = self.extracted_texts[due_date_key]
            if isinstance(due_date_data, tuple) and len(due_date_data) == 2:
                due_date, box = due_date_data
                display_text = f"Due Date: {due_date}"
                if isinstance(box, tuple) and len(box) == 4:
                    self.update_display(self.original_image, box)
                else:
                    display_text = "Due Date not found"
                    self.update_display(self.original_image)

        self.text_label.configure(text=display_text)


    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")


    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

        
if __name__ == "__main__":
    app = App()
    app.mainloop()