import customtkinter
import tkinter
import joblib
import pandas as pd


# =============== Encoding setup ===============
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


# =============== GUI Window ===============
window = customtkinter.CTk(fg_color="white")
window.title("Nicotine Consumption")
window.geometry("1000x800")

title = customtkinter.CTkLabel(window, text='Model for Nicotine addiction detection',
                               text_color='#144870', font=("Arial", 38))
title.pack(padx=5, pady=(40, 0))

frame = customtkinter.CTkFrame(window, width=700, height=400, fg_color="#1E1E2E")
frame.pack(pady=20)

up_frame = customtkinter.CTkFrame(frame, width=700, height=400, fg_color="#1E1E2E")
up_frame.pack(pady=20)

# ================= Variables =================
val_nscore = [0]
val_oscore = [0]
val_escore = [0]
val_ascore = [0]
val_cscore = [0]
val_gender = [0]
val_education = [0]
val_country = [0]
val_age = [0]
val_ethnicity = [0]
val_impulsive = [0]
val_ss = [0]


# =============== Slider Functions ===============
def make_slider(row, column, text, minv, maxv, steps, val_list):
    def update_val(_):
        val_list[0] = slider.get()
        label.configure(text=f"{text}: {int(val_list[0])}")
    frame_ = customtkinter.CTkFrame(up_frame, fg_color="#1E1E2E")
    frame_.grid(row=row, column=column, padx=40, pady=(0, 10))
    label = customtkinter.CTkLabel(frame_, text=f"{text}: ", font=("Arial", 16))
    label.pack(pady=(20, 10))
    slider = customtkinter.CTkSlider(frame_, from_=minv, to=maxv, number_of_steps=steps, command=update_val)
    slider.set(minv)
    slider.pack(padx=40, pady=(0, 10))
    return slider


make_slider(3, 0, "Nscore", 12, 60, 48, val_nscore)
make_slider(3, 1, "Escore", 16, 59, 43, val_escore)
make_slider(3, 2, "Oscore", 24, 60, 36, val_oscore)
make_slider(4, 0, "Ascore", 12, 60, 48, val_ascore)
make_slider(4, 1, "Cscore", 17, 59, 42, val_cscore)

# =============== Dropdowns ===============
def option_changed_gender(choice): val_gender[0] = choice
def option_changed_education(choice): val_education[0] = choice
def option_changed_country(choice): val_country[0] = choice
def option_changed_age(choice): val_age[0] = choice
def option_changed_ethnicity(choice): val_ethnicity[0] = choice
def option_changed_impulsive(choice): val_impulsive[0] = choice
def option_changed_ss(choice): val_ss[0] = choice

gender_bar = customtkinter.CTkOptionMenu(up_frame, values=["Male", "Female"], command=option_changed_gender)
gender_bar.set("Gender")
gender_bar.grid(row=0, column=0, pady=(20, 0))

education_bar = customtkinter.CTkOptionMenu(
    up_frame,
    values=[
        'Professional Certificate/ Diploma', 'Doctorate Degree', 'Masters Degree',
        'Left School at 18 years', 'Left School at 16 years', 'University Degree',
        'Some College, No Certificate Or Degree', 'Left School Before 16 years', 'Left School at 17 years'
    ],
    command=option_changed_education)
education_bar.set("Education")
education_bar.grid(row=0, column=1, pady=(20, 0))

country_bar = customtkinter.CTkOptionMenu(
    up_frame,
    values=['UK', 'Canada', 'USA', 'Other', 'Australia', 'Republic of Ireland', 'New Zealand'],
    command=option_changed_country)
country_bar.set("Country")
country_bar.grid(row=2, column=0, pady=(20, 0))

age_bar = customtkinter.CTkOptionMenu(up_frame,
    values=['18-24', '25-34', '35-44', '45-54', '55-64', '65+'], command=option_changed_age)
age_bar.set("Age Range")
age_bar.grid(row=1, column=0, pady=(20, 0))

ethnicity_bar = customtkinter.CTkOptionMenu(
    up_frame,
    values=['Mixed-White/Asian', 'White', 'Mixed-White/Black', 'Asian', 'Black', 'Mixed-Black/Asian', 'Other'],
    command=option_changed_ethnicity)
ethnicity_bar.set("Ethnicity")
ethnicity_bar.grid(row=1, column=1, pady=(20, 0))

impulsive_bar = customtkinter.CTkOptionMenu(
    up_frame, values=[str(x) for x in [-2.55524, -1.37983, -0.71126, -0.21712,
                                       0.19268, 0.52975, 0.88113, 1.29221, 1.86203, 2.90161]],
    command=option_changed_impulsive)
impulsive_bar.set("Impulsive")
impulsive_bar.grid(row=1, column=2, pady=(20, 0))

ss_bar = customtkinter.CTkOptionMenu(
    up_frame, values=[str(x) for x in [-2.07848, -1.54858, -1.18084, -0.84637,
                                       -0.52593, -0.21575, 0.07987, 0.40148, 0.7654, 1.2247, 1.92173]],
    command=option_changed_ss)
ss_bar.set("SS")
ss_bar.grid(row=0, column=2, pady=(20, 0))

# =============== Predict Button ===============
def predict_button():
    enc = setup_encodings()

    values = {
        'Age': val_age[0],
        'Gender': val_gender[0],
        'Education': val_education[0],
        'Country': val_country[0],
        'Ethnicity': val_ethnicity[0],
        'Nscore': float(val_nscore[0]),
        'Escore': float(val_escore[0]),
        'Oscore': float(val_oscore[0]),
        'Ascore': float(val_ascore[0]),
        'Cscore': float(val_cscore[0]),
        'Impulsive': float(val_impulsive[0]),
        'SS': float(val_ss[0])
    }

    # Apply encoding
    for col in ['Age', 'Gender', 'Education', 'Country', 'Ethnicity']:
        if values[col] in enc[col]:
            values[col] = enc[col][values[col]]
        else:
            print(f"⚠ Missing encoding for {col}: {values[col]}")

    df = pd.DataFrame([values])

    try:
        model = joblib.load(r"D:\DEPI ASSIGN 11\archive (4)\project\drug_model.pkl")
        pred = model.predict(df)[0]
        if pred ==1:
            result.configure(text="Addictor", text_color="white")
        else:
            result.configure(text="Not Addictor", text_color="white")
        print("✅ Predicted:", pred)
    except Exception as e:
        result.configure(text=f"Error: {e}", text_color="red")
        print("❌ Error:", e)


low_frame = customtkinter.CTkFrame(frame, fg_color="#144870")
low_frame.pack(expand=True, fill="both", pady=(10, 0), anchor="center")

submit = customtkinter.CTkButton(low_frame, width=150, height=40, text='Predict',
                                 font=('Ariel', 20), fg_color="#02B2B2",
                                 hover_color='#009393', command=predict_button)
submit.pack(side='left', padx=(90, 0), pady=10)

result = customtkinter.CTkLabel(low_frame, text='', font=('Ariel', 30))
result.pack(side='right', padx=(0, 90), pady=10)

window.mainloop()