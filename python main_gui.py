# Initial UI screen
root = Tk()
w, h = 750, 550
ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()
x, y = (ws - w) // 2, (hs - h) // 2
root.geometry(f'{w}x{h}+{x}+{y}')
root.title(sample_data.student.title)
root.configure(background=sample_data.student.background)
root.resizable(False, False)

Label(root, text=sample_data.student.titlec, fg=sample_data.student.text_color,
      bg=sample_data.student.background, width=35, height=3,
      font=('times', 30, 'italic bold')).place(x=0, y=20)

Label(root, justify=CENTER, text="PATH", width=20, bg=sample_data.student.background,
      height=2, fg=sample_data.student.text_color, font=('times', 15, 'bold')).place(x=100, y=150)

Label(root, justify=RIGHT, text="FILE", width=20, bg=sample_data.student.background,
      height=2, fg=sample_data.student.text_color, font=('times', 15, 'bold')).place(x=100, y=225)

txt = Entry(root, validate="key", width=20, font=('times', 25, 'bold'))
txt.place(x=300, y=150)
txt2 = Entry(root, width=20, font=('times', 25, 'bold'))
txt2.place(x=300, y=225)

Button(root, text="Select Image", width=15, command=read_first_data, height=1,
       fg="#FFF", bg="#004080", activebackground="#ff8000", activeforeground="white",
       font=('times', 15, 'bold')).place(x=250, y=400)

Button(root, text="Next", width=15, height=1, command=feature_extraction_page,
       fg="#FFF", bg="#004080", activebackground="#ff8000", activeforeground="white",
       font=('times', 15, 'bold')).place(x=450, y=400)

root.mainloop()
