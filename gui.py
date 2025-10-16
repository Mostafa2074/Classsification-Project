import customtkinter
import tkinter
import joblib
import pandas as pd


class NicotineApp(customtkinter.CTk):

    def __init__(self):
        super().__init__()
        self.title("Nicotine Consumption")
        self.geometry("1000x800")
        self.configure(fg_color="white")

        self.encodings = self.setup_encodings()
        self.values = {
            'Nscore': [0],
            'Escore': [0],
            'Oscore': [0],
            'Ascore': [0],
            'Cscore': [0],
            'Gender': [0],
            'Education': [0],
            'Country': [0],
            'Age': [0],
            'Ethnicity': [0],
            'Impulsive': [0],
            'SS': [0]
        }

        self.create_widgets()

    # ------------------- Encoding setup -------------------
    @staticmethod
    def setup_encodings():
        return {
            'Age': {
                '18-24': -0.95197,
                '25-34': -0.07854,
                '35-44': 0.49788,
                '45-54': 1.09449,
                '55-64': 1.82213,
                '65+': 2.59171
            },
            'Gender': {
                'Female': 0.48246,
                'Male': -0.48246
            },
            'Education': {
                'Left School Before 16 years': -2.43591,
                'Left School at 16 years': -1.73790,
                'Left School at 17 years': -1.43719,
                'Left School at 18 years': -1.22751,
                'Some College, No Certificate Or Degree': -0.61113,
                'Professional Certificate/ Diploma': -0.05921,
                'University Degree': 0.45468,
                'Masters Degree': 1.16365,
                'Doctorate Degree': 1.98437
            },
            'Country': {
                'Australia': -0.09765,
                'Canada': 0.24923,
                'New Zealand': -0.46841,
                'Other': -0.28519,
                'Republic of Ireland': 0.21128,
                'UK': 0.96082,
                'USA': -0.57009
            },
            'Ethnicity': {
                'Asian': -0.50212,
                'Black': -1.10702,
                'Mixed-Black/Asian': 1.90725,
                'Mixed-White/Asian': 0.12600,
                'Mixed-White/Black': -0.22166,
                'Other': 0.11440,
                'White': -0.31685
            }
        }

    # ------------------- GUI setup -------------------
    def create_widgets(self):
        title = customtkinter.CTkLabel(
            self, text='Model for Nicotine Addiction Detection',
            text_color='#144870', font=("Arial", 38)
        )
        title.pack(padx=5, pady=(40, 0))

        self.frame = customtkinter.CTkFrame(self, width=700, height=400, fg_color="#1E1E2E")
        self.frame.pack(pady=20)

        self.up_frame = customtkinter.CTkFrame(self.frame, width=700, height=400, fg_color="#1E1E2E")
        self.up_frame.pack(pady=20)

        self.make_slider(3, 0, "Nscore", 12, 60, 48, self.values['Nscore'])
        self.make_slider(3, 1, "Escore", 16, 59, 43, self.values['Escore'])
        self.make_slider(3, 2, "Oscore", 24, 60, 36, self.values['Oscore'])
        self.make_slider(4, 0, "Ascore", 12, 60, 48, self.values['Ascore'])
        self.make_slider(4, 1, "Cscore", 17, 59, 42, self.values['Cscore'])

        self.create_option_menus()

        low_frame = customtkinter.CTkFrame(self.frame, fg_color="#144870")
        low_frame.pack(expand=True, fill="both", pady=(10, 0), anchor="center")

        submit = customtkinter.CTkButton(
            low_frame, width=150, height=40, text='Predict',
            font=('Arial', 20), fg_color="#02B2B2",
            hover_color='#009393', command=self.predict_button
        )
        submit.pack(side='left', padx=(90, 0), pady=10)

        self.result = customtkinter.CTkLabel(low_frame, text='', font=('Arial', 30))
        self.result.pack(side='right', padx=(0, 90), pady=10)

    # ------------------- Sliders -------------------
    def make_slider(self, row, column, text, minv, maxv, steps, val_list):
        def update_val(_):
            val_list[0] = slider.get()
            label.configure(text=f"{text}: {int(val_list[0])}")

        frame_ = customtkinter.CTkFrame(self.up_frame, fg_color="#1E1E2E")
        frame_.grid(row=row, column=column, padx=40, pady=(0, 10))
        label = customtkinter.CTkLabel(frame_, text=f"{text}: ", font=("Arial", 16))
        label.pack(pady=(20, 10))
        slider = customtkinter.CTkSlider(frame_, from_=minv, to=maxv, number_of_steps=steps, command=update_val)
        slider.set(minv)
        slider.pack(padx=40, pady=(0, 10))
        return slider

    # ------------------- Dropdown Menus -------------------
    def create_option_menus(self):
        def make_dropdown(row, column, label, values, key):
            bar = customtkinter.CTkOptionMenu(self.up_frame, values=values,
                                              command=lambda choice: self.values[key].__setitem__(0, choice))
            bar.set(label)
            bar.grid(row=row, column=column, pady=(20, 0))
            return bar

        make_dropdown(0, 0, "Gender", ["Male", "Female"], 'Gender')
        make_dropdown(0, 1, "Education", [
            'Professional Certificate/ Diploma', 'Doctorate Degree', 'Masters Degree',
            'Left School at 18 years', 'Left School at 16 years', 'University Degree',
            'Some College, No Certificate Or Degree', 'Left School Before 16 years', 'Left School at 17 years'
        ], 'Education')
        make_dropdown(2, 0, "Country", [
            'UK', 'Canada', 'USA', 'Other', 'Australia', 'Republic of Ireland', 'New Zealand'
        ], 'Country')
        make_dropdown(1, 0, "Age Range", [
            '18-24', '25-34', '35-44', '45-54', '55-64', '65+'
        ], 'Age')
        make_dropdown(1, 1, "Ethnicity", [
            'Mixed-White/Asian', 'White', 'Mixed-White/Black', 'Asian', 'Black',
            'Mixed-Black/Asian', 'Other'
        ], 'Ethnicity')
        make_dropdown(1, 2, "Impulsive", [str(x) for x in [
            -2.55524, -1.37983, -0.71126, -0.21712, 0.19268, 0.52975,
            0.88113, 1.29221, 1.86203, 2.90161
        ]], 'Impulsive')
        make_dropdown(0, 2, "SS", [str(x) for x in [
            -2.07848, -1.54858, -1.18084, -0.84637, -0.52593, -0.21575,
            0.07987, 0.40148, 0.7654, 1.2247, 1.92173
        ]], 'SS')

    # ------------------- Prediction -------------------
    def predict_button(self):
        try:
            values = {k: float(v[0]) if isinstance(v[0], (int, float)) else v[0] for k, v in self.values.items()}

            for col in ['Age', 'Gender', 'Education', 'Country', 'Ethnicity']:
                if values[col] in self.encodings[col]:
                    values[col] = self.encodings[col][values[col]]

            df = pd.DataFrame([values])
            model = joblib.load(r"D:\DEPI ASSIGN 11\archive (4)\project\drug_model.pkl")
            pred = model.predict(df)[0]

            if pred == 1:
                self.result.configure(text="Addictor", text_color="white")
            else:
                self.result.configure(text="Not Addictor", text_color="white")

            print("✅ Predicted:", pred)

        except Exception as e:
            self.result.configure(text=f"Error: {e}", text_color="red")
            print("❌ Error:", e)


if __name__ == "__main__":
    app = NicotineApp()
    app.mainloop()
