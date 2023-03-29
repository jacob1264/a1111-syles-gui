import pandas as pd
import tkinter as tk
from tkinter import messagebox

class StyleEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("A1111 Styles Editor by Ok-Lobster-919")

        # Initialize the DataFrame and other state variables
        self.styles_df = None
        self.current_style = None
        self.unsaved_changes = False
        self.root.grid_columnconfigure(0, weight=1)

        self.unsaved_changes_label = tk.Label(self.root, text="Unsaved changes", fg="red")

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.load_button = tk.Button(self.root, text="Reload Styles", command=self.load_csv)
        self.load_button.grid(row=0, column=0, padx=5, sticky="w")

        self.save_button = tk.Button(self.root, text="Save Styles", command=self.save_changes_and_csv)
        self.save_button.grid(row=0, column=0, padx=88, sticky="w")

        self.style_listbox = tk.Listbox(self.root, exportselection=False)
        self.style_listbox.grid(row=1, column=0, padx=5, pady=(5, 0), sticky="nsew")
        self.style_listbox.bind("<<ListboxSelect>>", self.show_style)

        self.button_frame = tk.Frame(self.root)
        self.button_frame.grid(row=1, column=1, rowspan=2, padx=5, pady=(5, 0), sticky="nse")

        button_width = 15

        self.new_style_button = tk.Button(self.button_frame, text="New Style", command=self.create_new_style, width=button_width)
        self.new_style_button.pack(side="top", pady=2, fill="x", anchor="w")

        self.delete_style_button = tk.Button(self.button_frame, text="Delete Style", command=self.delete_style, width=button_width)
        self.delete_style_button.pack(side="top", pady=2, fill="x", anchor="w")

        self.copy_style_button = tk.Button(self.button_frame, text="Copy Style", command=self.copy_style, width=button_width)
        self.copy_style_button.pack(side="left", pady=2, fill="x", anchor="w")

        self.labels = ["name", "prompt", "negative_prompt"]
        self.entries = []

        labels_frame = tk.Frame(self.root)
        labels_frame.grid(row=2, column=0, columnspan=3, sticky="ew")

        for i, field in enumerate(self.labels):
            label = tk.Label(labels_frame, text=f"{field.capitalize()}")
            entry_row = i * 2

            label.grid(row=entry_row, column=0, padx=5, sticky="w")

            if field in ["prompt", "negative_prompt"]:
                entry = tk.Text(labels_frame, height=8, wrap=tk.WORD)
                entry.bind("<KeyRelease>", lambda event: (self.set_unsaved_changes(True), self.save_changes()))
            else:
                entry = tk.Entry(labels_frame)
                entry.bind("<KeyRelease>", lambda event: (self.set_unsaved_changes(True), self.save_changes()))

            entry.grid(row=entry_row + 1, column=0, padx=5, sticky="ew")

            labels_frame.grid_columnconfigure(0, weight=1)

            self.entries.append(entry)
            self.load_csv()

    # Load the CSV file containing the styles
    def load_csv(self):
        if self.check_unsaved_file():
            return

        file_path = './styles.csv'
        if file_path:
            try:
                self.styles_df = pd.read_csv(file_path, na_filter=False)
                self.update_style_listbox()
                self.style_listbox.selection_clear(0, tk.END)
                self.style_listbox.selection_set(0)
            except pd.errors.ParserError as e:
                messagebox.showerror("Error", f"Error reading csv file: {e}")
            self.show_style(None)

    # Create a new empty style in the DataFrame
    def create_new_style(self):
        new_style = {'name': '', 'prompt': '', 'negative_prompt': ''}
        self.styles_df = self.styles_df.append(new_style, ignore_index=True)
        self.update_style_listbox()
        self.style_listbox.selection_clear(0, tk.END)
        self.style_listbox.selection_set(tk.END)
        self.style_listbox.activate(tk.END)
        self.show_style(None)
        self.set_unsaved_changes(True)

    # Delete the selected style from the DataFrame
    def delete_style(self):
        selected = self.style_listbox.curselection()
        if not selected:
            return

        index = selected[0]
        style_name = self.styles_df.at[index, "name"]

        confirm = messagebox.askyesno("Delete Style", f"Are you sure you want to delete the '{style_name}' style?")
        if confirm:
            self.styles_df.drop(index, inplace=True)
            self.styles_df.reset_index(drop=True, inplace=True)
            self.update_style_listbox()
            self.style_listbox.selection_clear(0, tk.END)
            self.current_style = None
            for entry in self.entries:
                entry.delete('1.0', tk.END) if isinstance(entry, tk.Text) else entry.delete(0, tk.END)
            self.set_unsaved_changes(True)

    # Copy selected style and add the copy to the DataFrame
    def copy_style(self):
        selected = self.style_listbox.curselection()
        if not selected:
            return

        index = selected[0]
        copied_style = self.styles_df.iloc[index].copy()
        copied_style['name'] = f"{copied_style['name']} (Copy)"
        self.styles_df = self.styles_df.append(copied_style, ignore_index=True)
        self.update_style_listbox()
        self.style_listbox.selection_clear(0, tk.END)
        self.style_listbox.selection_set(tk.END)
        self.style_listbox.activate(tk.END)
        self.show_style(None)
        self.set_unsaved_changes(True)

    # Update the styles listbox with the current DataFrame contents
    def update_style_listbox(self):

        self.style_listbox.delete(0, tk.END)
        for _, row in self.styles_df.iterrows():
            self.style_listbox.insert(tk.END, row['name'])

    # Display the selected style in the form fields
    def show_style(self, event=None):
        try:
            index = self.style_listbox.curselection()[0]
            style = self.styles_df.iloc[index]
            self.current_style = style

            for i, field in enumerate(self.labels):
                self.entries[i].delete('1.0', tk.END) if isinstance(self.entries[i], tk.Text) else self.entries[i].delete(0, tk.END)
                self.entries[i].insert('1.0', str(style[field])) if isinstance(self.entries[i], tk.Text) else self.entries[i].insert(0, str(style[field]))

        except IndexError:
            pass

    # Set the unsaved_changes flag and update the "Unsaved changes" label
    def set_unsaved_changes(self, value):
        self.unsaved_changes = value
        if value:
            self.unsaved_changes_label.place(x=160, y=12, anchor="nw")
        else:
            self.unsaved_changes_label.place_forget()

    # Handle the window close event
    def on_close(self):
        if self.check_unsaved_file():
            return
        self.root.destroy()

    # Check if there are unsaved changes and prompt the user accordingly
    def check_unsaved_file(self):
        if self.unsaved_changes:
            response = messagebox.askyesnocancel("Save changes?", "Styles have been modified, do you want to save changes?")
            if response is False:
                self.set_unsaved_changes(False)
            if response is None:
                return True
            if response:
                self.save_changes_and_csv()

        return False

    # Save the changes to the DataFrame and the CSV file
    def save_changes_and_csv(self):
        self.save_changes()
        self.save_csv()

    # Save the changes to the DataFrame
    def save_changes(self):
        if self.current_style is None or self.current_style.empty:
            return

        selected = self.style_listbox.curselection()
        if not selected:
            return

        index = selected[0]

        for i, field in enumerate(self.labels):
            value = self.entries[i].get('1.0', tk.END).strip() if isinstance(self.entries[i], tk.Text) else self.entries[i].get().strip()
            self.styles_df.at[index, field] = value

    # Save the DataFrame to a CSV file
    def save_csv(self):
        if self.styles_df is None:
            return

        #file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        file_path = './styles.csv'
        if file_path:
            try:
                self.styles_df.to_csv(file_path, index=True)
            except Exception as e:
                messagebox.showerror("Error", f"Error saving csv file: {e}")
        self.set_unsaved_changes(False)
        if (len(self.style_listbox.curselection()) > 0):
            index = self.style_listbox.curselection()[0]
            self.update_style_listbox()
            self.style_listbox.selection_set(index)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x550")
    root.resizable(True,False)
    app = StyleEditor(root)
    root.mainloop()
