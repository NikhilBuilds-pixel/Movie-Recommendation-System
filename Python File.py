import mysql.connector
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext, ttk

# ------------------ DATABASE CONNECTION ------------------ #
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="movie_recommendation"
    )

# ------------------ MOVIE LOGIC ------------------ #
def get_movie_suggestions(cursor, rating_range, language, genre):
    query = """
    SELECT title, genre, language, rating, description 
    FROM movies 
    WHERE rating BETWEEN %s AND %s AND language = %s AND genre = %s
    """
    cursor.execute(query, (rating_range[0], rating_range[1], language, genre))
    return cursor.fetchall()

def insert_movie(cursor, db, title, genre, language, rating, description):
    query = """
    INSERT INTO movies (title, genre, language, rating, description) 
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (title, genre, language, rating, description))
    db.commit()

# ------------------ GUI ACTIONS ------------------ #
def recommend_movies():
    try:
        min_rating = float(min_rating_var.get())
        max_rating = float(max_rating_var.get())
        language = language_var.get()
        genre = genre_var.get()

        if min_rating > max_rating:
            messagebox.showerror("Input Error", "Min rating can't be higher than max rating.")
            return

        movies = get_movie_suggestions(cursor, (min_rating, max_rating), language, genre)
        display_recommendations(movies)

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid rating numbers.")

def add_movie():
    try:
        title = simpledialog.askstring("Input", "Movie name:", parent=window)
        genre = genre_var.get()
        language = language_var.get()
        rating = float(simpledialog.askstring("Input", "Rating (0-10):", parent=window))
        description = simpledialog.askstring("Input", "Short Description:", parent=window)

        insert_movie(cursor, db, title, genre, language, rating, description)
        messagebox.showinfo("Success", f"'{title}' added successfully!")

    except Exception as e:
        messagebox.showerror("Input Error", f"Invalid movie details. Error: {e}")

def display_recommendations(movies):
    result_text.configure(state='normal')
    result_text.delete(1.0, tk.END)

    if not movies:
        result_text.insert(tk.END, "😕 Sorry, no movies match your preferences.")
    else:
        for movie in movies:
            title, genre, language, rating, description = movie
            result_text.insert(tk.END,
                f"🎬 {title} ({rating}/10)\nGenre: {genre} | Language: {language}\n📝 {description}\n\n")

    result_text.configure(state='disabled')

def exit_app():
    cursor.close()
    db.close()
    window.destroy()

# ------------------ GUI SETUP ------------------ #
window = tk.Tk()
window.title("🎥 Movie Recommendation System")
window.geometry("800x650")
window.configure(bg="#f0f4f7")

# Connect DB
db = connect_db()
cursor = db.cursor()

# Fonts and Colors
button_font = ("Helvetica", 12, "bold")
label_font = ("Helvetica", 16, "bold")
button_bg = "#4a90e2"
button_fg = "#ffffff"

# Genres & Languages (FIXED)
genres = ["Comedy", "Thriller", "Sports", "Sci-Fi"]
languages = ["English", "Hindi", "Korean", "Japanese"]

# ------------------ UI ELEMENTS ------------------ #
welcome_label = tk.Label(window, text="🎬 Welcome to Movie Recommender", font=label_font, bg="#f0f4f7", fg="#2c3e50")
welcome_label.pack(pady=15)

input_frame = tk.Frame(window, bg="#f0f4f7")
input_frame.pack(pady=10)

# Variables
genre_var = tk.StringVar(value=genres[0])
language_var = tk.StringVar(value=languages[0])
min_rating_var = tk.StringVar(value="0")
max_rating_var = tk.StringVar(value="10")

# Dropdowns
tk.Label(input_frame, text="Genre:", bg="#f0f4f7", font=("Helvetica", 12)).grid(row=0, column=0, padx=10, pady=5)
ttk.OptionMenu(input_frame, genre_var, genres[0], *genres).grid(row=0, column=1, padx=10)

tk.Label(input_frame, text="Language:", bg="#f0f4f7", font=("Helvetica", 12)).grid(row=0, column=2, padx=10, pady=5)
ttk.OptionMenu(input_frame, language_var, languages[0], *languages).grid(row=0, column=3, padx=10)

tk.Label(input_frame, text="Min Rating:", bg="#f0f4f7", font=("Helvetica", 12)).grid(row=1, column=0, padx=10)
tk.Entry(input_frame, textvariable=min_rating_var, width=5).grid(row=1, column=1)

tk.Label(input_frame, text="Max Rating:", bg="#f0f4f7", font=("Helvetica", 12)).grid(row=1, column=2, padx=10)
tk.Entry(input_frame, textvariable=max_rating_var, width=5).grid(row=1, column=3)

# Buttons
button_frame = tk.Frame(window, bg="#f0f4f7")
button_frame.pack(pady=10)

tk.Button(button_frame, text="🎯 Recommend Movies", font=button_font, bg=button_bg, fg=button_fg,
          width=20, command=recommend_movies).grid(row=0, column=0, padx=10, pady=10)

tk.Button(button_frame, text="➕ Add Movie", font=button_font, bg=button_bg, fg=button_fg,
          width=20, command=add_movie).grid(row=0, column=1, padx=10, pady=10)

tk.Button(button_frame, text="❌ Exit", font=button_font, bg="#e74c3c", fg=button_fg,
          width=20, command=exit_app).grid(row=0, column=2, padx=10, pady=10)

# Result Box
result_text = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=90, height=20, font=("Consolas", 11))
result_text.pack(padx=20, pady=20)
result_text.configure(state='disabled')

# Run App
window.mainloop()