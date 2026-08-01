import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, scrolledtext


# ---------------- DATABASE CONNECTION ---------------- #

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="movie_recommendation"
    )


db = connect_db()
cursor = db.cursor()


# ---------------- DATABASE FUNCTIONS ---------------- #

def get_movie_suggestions(min_rating, max_rating, language, genre):
    query = """
    SELECT title, genre, language, rating, description
    FROM movies
    WHERE rating BETWEEN %s AND %s
    AND language=%s
    AND genre=%s
    """

    cursor.execute(query, (min_rating, max_rating, language, genre))
    return cursor.fetchall()


def insert_movie(title, genre, language, rating, description):
    query = """
    INSERT INTO movies(title,genre,language,rating,description)
    VALUES(%s,%s,%s,%s,%s)
    """

    cursor.execute(
        query,
        (
            title,
            genre,
            language,
            rating,
            description
        )
    )

    db.commit()
    # ---------------- DISPLAY FUNCTIONS ---------------- #

def display_recommendations(movies):

    result_text.config(state="normal")
    result_text.delete(1.0, tk.END)

    if len(movies) == 0:
        result_text.insert(tk.END, "\nNo Movies Found.\n")

    else:
        result_text.insert(
            tk.END,
            f"\nFound {len(movies)} Movie(s)\n"
        )

        result_text.insert(
            tk.END,
            "=" * 70 + "\n\n"
        )

        for movie in movies:

            result_text.insert(
                tk.END,
                f"🎬 Title      : {movie[0]}\n"
            )

            result_text.insert(
                tk.END,
                f"🎭 Genre      : {movie[1]}\n"
            )

            result_text.insert(
                tk.END,
                f"🌐 Language   : {movie[2]}\n"
            )

            result_text.insert(
                tk.END,
                f"⭐ Rating     : {movie[3]}\n"
            )

            result_text.insert(
                tk.END,
                f"📝 Description:\n{movie[4]}\n"
            )

            result_text.insert(
                tk.END,
                "-" * 70 + "\n\n"
            )

    result_text.config(state="disabled")


# ---------------- BUTTON FUNCTIONS ---------------- #

def add_movie():

    try:

        title = simpledialog.askstring(
            "Movie Title",
            "Enter Movie Title"
        )

        if not title:
            return

        genre = simpledialog.askstring(
            "Genre",
            "Enter Genre"
        )

        if not genre:
            return

        language = simpledialog.askstring(
            "Language",
            "Enter Language"
        )

        if not language:
            return

        rating = simpledialog.askfloat(
            "Rating",
            "Enter Rating (0-10)"
        )

        if rating is None:
            return

        description = simpledialog.askstring(
            "Description",
            "Enter Description"
        )

        if not description:
            return

        insert_movie(
            title,
            genre,
            language,
            rating,
            description
        )

        messagebox.showinfo(
            "Success",
            "Movie Added Successfully."
        )

    except Exception as e:

        messagebox.showerror(
            "Error",
            str(e)
        )
        # ---------------- RECOMMEND MOVIES ---------------- #

def recommend_movies():

    try:

        min_rating = float(min_rating_var.get())
        max_rating = float(max_rating_var.get())

        if min_rating > max_rating:
            messagebox.showerror(
                "Error",
                "Min Rating cannot be greater than Max Rating."
            )
            return

        language = language_var.get()
        genre = genre_var.get()

        movies = get_movie_suggestions(
            min_rating,
            max_rating,
            language,
            genre
        )

        display_recommendations(movies)

    except ValueError:

        messagebox.showerror(
            "Error",
            "Please enter valid ratings."
        )

    except Exception as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )


# ---------------- EXIT ---------------- #

def exit_app():

    if messagebox.askyesno(
        "Exit",
        "Do you want to Exit?"
    ):

        cursor.close()
        db.close()
        window.destroy()


# ---------------- GUI ---------------- #

window = tk.Tk()

window.title("🎬 Movie Recommendation System")

window.geometry("850x700")

window.configure(bg="#f0f4f8")


button_bg = "#1976D2"
button_fg = "white"

title_font = ("Arial", 20, "bold")

label_font = ("Arial", 12)


genres = [
    "Comedy",
    "Thriller",
    "Sports",
    "Sci-Fi"
]

languages = [
    "English",
    "Hindi",
    "Korean",
    "Japanese"
]


genre_var = tk.StringVar(value=genres[0])

language_var = tk.StringVar(value=languages[0])

min_rating_var = tk.StringVar(value="0")

max_rating_var = tk.StringVar(value="10")


tk.Label(
    window,
    text="🎥 Movie Recommendation System",
    font=title_font,
    bg="#f0f4f8"
).pack(pady=15)


frame = tk.Frame(window, bg="#f0f4f8")

frame.pack()
# ---------------- INPUT FIELDS ---------------- #

tk.Label(
    frame,
    text="Genre",
    font=label_font,
    bg="#f0f4f8"
).grid(row=0, column=0, padx=10, pady=10)

ttk.Combobox(
    frame,
    textvariable=genre_var,
    values=genres,
    state="readonly",
    width=15
).grid(row=0, column=1, padx=10)


tk.Label(
    frame,
    text="Language",
    font=label_font,
    bg="#f0f4f8"
).grid(row=0, column=2, padx=10)

ttk.Combobox(
    frame,
    textvariable=language_var,
    values=languages,
    state="readonly",
    width=15
).grid(row=0, column=3, padx=10)


tk.Label(
    frame,
    text="Min Rating",
    font=label_font,
    bg="#f0f4f8"
).grid(row=1, column=0, pady=15)

tk.Entry(
    frame,
    textvariable=min_rating_var,
    width=10
).grid(row=1, column=1)


tk.Label(
    frame,
    text="Max Rating",
    font=label_font,
    bg="#f0f4f8"
).grid(row=1, column=2)

tk.Entry(
    frame,
    textvariable=max_rating_var,
    width=10
).grid(row=1, column=3)


# ---------------- BUTTONS ---------------- #

button_frame = tk.Frame(
    window,
    bg="#f0f4f8"
)

button_frame.pack(pady=20)


tk.Button(
    button_frame,
    text="🎯 Recommend Movies",
    command=recommend_movies,
    bg=button_bg,
    fg=button_fg,
    width=20,
    font=("Arial", 11, "bold")
).grid(row=0, column=0, padx=10)


tk.Button(
    button_frame,
    text="➕ Add Movie",
    command=add_movie,
    bg="green",
    fg="white",
    width=15,
    font=("Arial", 11, "bold")
).grid(row=0, column=1, padx=10)


tk.Button(
    button_frame,
    text="❌ Exit",
    command=exit_app,
    bg="red",
    fg="white",
    width=12,
    font=("Arial", 11, "bold")
).grid(row=0, column=2, padx=10)


# ---------------- RESULT BOX ---------------- #

result_text = scrolledtext.ScrolledText(
    window,
    width=95,
    height=22,
    font=("Consolas", 10)
)

result_text.pack(padx=15, pady=15)

result_text.config(state="disabled")


# ---------------- START ---------------- #

window.mainloop()