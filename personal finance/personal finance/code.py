import datetime as dt
import pandas as pd
import sqlite3
from tkinter import *
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from database import Database
from tkinter.filedialog import asksaveasfilename



class PersonalFinanceManager:
    def __init__(self, root):
        self.root = root
        self.root.title("PersonalFinanceManager")
        self.root.geometry('1000x600')

        self.data = Database(db='myclean.db')

        self.setup_variables()
        self.setup_ui()

    def setup_variables(self):
        self.amptvar = IntVar()
        self.dopvar = StringVar()
        self.namevar = StringVar()
        self.category_var = StringVar()
        self.search_var = StringVar()
        self.filter_var = StringVar()
        self.income_var = StringVar()
        self.expense_var = StringVar()
        self.balance_var = StringVar()

    def setup_ui(self):
        font_settings = ('Times new roman', 16)
        main_frame = Frame(self.root, padx=10, pady=10)
        main_frame.pack(expand=True, fill=BOTH)

        self.create_form(main_frame, font_settings)
        self.create_buttons(main_frame, font_settings)
        self.create_summary_labels(main_frame, font_settings)
        self.create_treeview(main_frame)

        self.fetch_records()

    def create_form(self, frame, font):
        Label(frame, text='ΚΑΤΗΓΟΡΙΑ', font=font).grid(row=0, column=0, sticky=W)
        Label(frame, text='ΠΟΣΟ', font=font).grid(row=1, column=0, sticky=W)
        Label(frame, text='ΗΜΕΡΟΜΗΝΙΑ', font=font).grid(row=2, column=0, sticky=W)
        Label(frame, text='ΤΥΠΟΣ', font=font).grid(row=3, column=0, sticky=W)

        self.item_name_entry = Entry(frame, font=font, textvariable=self.namevar)
        self.item_amt_entry = Entry(frame, font=font, textvariable=self.amptvar)
        self.transaction_date_entry = Entry(frame, font=font, textvariable=self.dopvar)
        self.category_entry = ttk.Combobox(frame, font=font, textvariable=self.category_var,
                                           values=['έσοδο', 'έξοδο'], state='readonly')

        self.item_name_entry.grid(row=0, column=1, sticky=EW, padx=(10, 0))
        self.item_amt_entry.grid(row=1, column=1, sticky=EW, padx=(10, 0))
        self.transaction_date_entry.grid(row=2, column=1, sticky=EW, padx=(10, 0))
        self.category_entry.grid(row=3, column=1, sticky=EW, padx=(10, 0))

    def create_buttons(self, frame, font):
        Button(frame, text='ΤΩΡΙΝΗ ΗΜΕΡΟΜΗΝΙΑ', font=font, bg='#8B7D6B', command=self.set_date, width=15).grid(
            row=4, column=1, sticky=EW, padx=(10, 0))
        Button(frame, text='ΑΠΟΘΗΚΕΥΣΗ', font=font, bg='#D2691E', command=self.save_record, fg='white').grid(
            row=0, column=2, sticky=EW, padx=(10, 0))
        Button(frame, text='ΚΑΘΑΡΙΣΜΟΣ', font=font, bg='#DC143C', command=self.clear_entries, fg='white').grid(
            row=1, column=2, sticky=EW, padx=(10, 0))
        Button(frame, text='ΕΞΟΔΟΣ', font=font, bg='#6495ED', command=self.root.destroy, fg='white').grid(
            row=2, column=2, sticky=EW, padx=(10, 0))
        Button(frame, text="ΧΡΗΜΑΤΙΚΟ ΥΠΟΛΟΙΠΟ", font=font, bg='#486966', command=self.total_balance, fg='white').grid(
            row=0, column=3, sticky=EW, padx=(10, 0))
        Button(frame, text='ΤΡΟΠΟΠΟΙΗΣΗ', font=font, bg='#BD2A2E', command=self.update_record, fg='white').grid(
            row=1, column=3, sticky=EW, padx=(10, 0))
        Button(frame, text='ΔΙΑΓΡΑΦΗ', font=font, bg='#C2BB00', command=self.delete_row, fg='white').grid(
            row=2, column=3, sticky=EW, padx=(10, 0))
        Button(frame, text='Export to Excel', font=font, bg='#F7F7F7', command=self.export_to_excel).grid(
            row=3, column=3, sticky=EW, padx=(10, 0))
        Button(frame, text='Show to Graph', font=font, bg='#8DB6CD', command=self.show_graph).grid(
            row=4, column=2, sticky=EW, padx=(10, 0))

        self.create_search_and_filter(frame, font)

    def create_search_and_filter(self, frame, font):
        Label(frame, text='ΑΝΑΖΗΤΗΣΗ', font=font).grid(row=5, column=0, sticky=W)
        search_entry = Entry(frame, font=font, textvariable=self.search_var)
        search_entry.grid(row=5, column=1, sticky=EW, padx=(10, 0))
        Button(frame, text='ΑΝΑΖΗΤΗΣΗ', font=font, bg='#D2691E', command=self.search_records, fg='white').grid(
            row=5, column=2, sticky=EW, padx=(10, 0))

        Label(frame, text='ΦΙΛΤΡΟ ΚΑΤΗΓΟΡΙΑΣ', font=font).grid(row=6, column=0, sticky=W)
        filter_entry = ttk.Combobox(frame, font=font, textvariable=self.filter_var, values=['', 'έσοδο', 'έξοδο'],
                                    state='readonly')
        filter_entry.grid(row=6, column=1, sticky=EW, padx=(10, 0))
        Button(frame, text='ΦΙΛΤΡΟ', font=font, bg='#D2691E', command=self.filter_records, fg='white').grid(
            row=6, column=2, sticky=EW, padx=(10, 0))

    def create_summary_labels(self, frame, font):
        Label(frame, textvariable=self.income_var, font=font, fg='green').grid(row=7, column=0, columnspan=2, sticky=W)
        Label(frame, textvariable=self.expense_var, font=font, fg='red').grid(row=8, column=0, columnspan=2, sticky=W)
        Label(frame, textvariable=self.balance_var, font=font, fg='blue').grid(row=9, column=0, columnspan=2, sticky=W)

    def create_treeview(self, frame):
        treeview_frame = Frame(self.root)
        treeview_frame.pack()

        self.tv = ttk.Treeview(treeview_frame, columns=(1, 2, 3, 4, 5), show='headings', height=8)
        self.tv.pack(side='left')

        self.tv.column(1, anchor=CENTER, stretch=NO, width=60)
        self.tv.column(2, anchor=CENTER)
        self.tv.column(3, anchor=CENTER)
        self.tv.column(4, anchor=CENTER)
        self.tv.column(5, anchor=CENTER)
        self.tv.heading(1, text="No.")
        self.tv.heading(2, text="ΚΑΤΗΓΟΡΙΑ")
        self.tv.heading(3, text='ΠΟΣΟ')
        self.tv.heading(4, text="ΗΜΕΡΟΜΗΝΙΑ")
        self.tv.heading(5, text="ΤΥΠΟΣ")

        self.tv.bind("<ButtonRelease-1>", self.select_record)

        scrollbar = Scrollbar(treeview_frame, orient='vertical')
        scrollbar.configure(command=self.tv.yview)
        scrollbar.pack(side="right", fill="y")
        self.tv.config(yscrollcommand=scrollbar.set)

    def save_record(self):
        if not self.namevar.get() or self.amptvar.get() == 0 or not self.dopvar.get() or not self.category_var.get():
            messagebox.showerror('ΛΑΘΟΣ', 'Όλα τα πεδία πρέπει να συμπληρωθούν')
            return
        try:
            self.data.insert_record(
                item_name=self.namevar.get(),
                item_price=self.amptvar.get(),
                purchase_date=self.dopvar.get(),
                category=self.category_var.get()
            )
            self.refresh_data()
            self.clear_entries()
        except Exception as ep:
            messagebox.showerror('ΛΑΘΟΣ', ep)

    def set_date(self):
        date = dt.datetime.now()
        self.dopvar.set(f'{date:%d %B %Y}')

    def clear_entries(self):
        self.item_name_entry.delete(0, 'end')
        self.item_amt_entry.delete(0, 'end')
        self.transaction_date_entry.delete(0, 'end')
        self.category_var.set('')

    def fetch_records(self, query='select rowid, * from καθαρα'):
        for item in self.tv.get_children():
            self.tv.delete(item)
        records = self.data.fetch_record(query)
        for count, rec in enumerate(records):
            self.tv.insert(parent='', index='end', iid=count, values=(rec[0], rec[1], rec[2], rec[3], rec[4]))
        self.update_summary()

    def select_record(self, event):
        selected = self.tv.focus()
        val = self.tv.item(selected, 'values')

        try:
            self.selected_rowid = val[0]
            self.namevar.set(val[1])
            self.amptvar.set(val[2])
            self.dopvar.set(val[3])
            self.category_var.set(val[4])
        except Exception:
            pass

    def update_record(self):
        if not self.namevar.get() or self.amptvar.get() == 0 or not self.dopvar.get() or not self.category_var.get():
            messagebox.showerror('ΛΑΘΟΣ', 'Όλα τα πεδία πρέπει να συμπληρωθούν')
            return
        try:
            self.data.update_record(
                item_name=self.namevar.get(),
                item_price=self.amptvar.get(),
                purchase_date=self.dopvar.get(),
                category=self.category_var.get(),
                rowid=self.selected_rowid
            )
            self.refresh_data()
        except Exception as ep:
            messagebox.showerror('ΛΑΘΟΣ', ep)

    def total_balance(self):
        try:
            total_income = self._sum_by_category('έσοδο')
            total_expenses = self._sum_by_category('έξοδο')
            balance = total_income - total_expenses
            messagebox.showinfo('ΤΩΡΙΝΗ ΚΑΤΑΣΤΑΣΗ: ',
                                f"ΣΥΝΟΛΙΚΑ ΕΣΟΔΑ: {total_income} \nΣΥΝΟΛΙΚΑ ΕΞΟΔΑ: {total_expenses} \nΥΠΟΛΟΙΠΟ ΛΟΓΑΡΙΑΣΜΟΥ: {balance}")
        except Exception as ep:
            messagebox.showerror('ΛΑΘΟΣ', ep)

    def _sum_by_category(self, category):
        query = f"Select sum(item_price) from καθαρα where category='{category}'"
        records = self.data.fetch_record(query)
        total = 0
        for record in records:
            if record[0] is not None:
                total += record[0]
        return total

    def delete_row(self):
        try:
            if messagebox.askyesno("Επιβεβαίωση Διαγραφής", "Είστε σίγουροι ότι θέλετε να διαγράψετε αυτή την εγγραφή;"):
                self.data.remove_record(self.selected_rowid)
                self.refresh_data()
        except Exception as ep:
            messagebox.showerror('ΛΑΘΟΣ', ep)

    def refresh_data(self):
        self.fetch_records()

    def export_to_excel(self):
        try:
            file_path = asksaveasfilename(defaultextension=".xlsx",
                                          filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                                          title="Save as")
            if not file_path:
                return  # User cancelled the save dialog
            conn = sqlite3.connect('myclean.db')
            df = pd.read_sql_query('SELECT * FROM καθαρα', conn)
            df.to_excel(file_path, index=False)
            conn.close()
            messagebox.showinfo('Επιτυχία', f'Το αρχείο αποθηκεύτηκε επιτυχώς στο {file_path}')
        except Exception as ep:
            messagebox.showerror('ΛΑΘΟΣ', ep)

    def show_graph(self):
        try:
            conn = sqlite3.connect('myclean.db')
            df = pd.read_sql_query('SELECT * FROM καθαρα', conn)
            df['purchase_date'] = pd.to_datetime(df['purchase_date'])
            df['month'] = df['purchase_date'].dt.to_period('M')

            income_df = df[df['category'] == 'έσοδο']
            expense_df = df[df['category'] == 'έξοδο']

            income_by_month = income_df.groupby('month')['item_price'].sum()
            expense_by_month = expense_df.groupby('month')['item_price'].sum()

            fig, ax = plt.subplots()

            income_by_month.plot(kind='bar', color='green', ax=ax, width=0.4, position=1, label='Έσοδα')
            expense_by_month.plot(kind='bar', color='red', ax=ax, width=0.4, position=0, label='Έξοδα')

            ax.set_title('Μηνιαία Έσοδα και Έξοδα')
            ax.set_xlabel('Μήνας')
            ax.set_ylabel('Ποσό')
            ax.legend()
            plt.grid(True)

            plt.show()
            conn.close()
        except Exception as ep:
            messagebox.showerror('ΛΑΘΟΣ', ep)

    def search_records(self):
        query = self.search_var.get()
        sql_query = f"SELECT rowid, * FROM καθαρα WHERE item_name LIKE '%{query}%' OR item_price LIKE '%{query}%' OR purchase_date LIKE '%{query}%' OR category LIKE '%{query}%'"
        self.fetch_records(sql_query)

    def filter_records(self):
        category = self.filter_var.get()
        if category:
            sql_query = f"SELECT rowid, * FROM καθαρα WHERE category='{category}'"
            self.fetch_records(sql_query)
        else:
            self.refresh_data()

    def update_summary(self):
        try:
            total_income = self._sum_by_category('έσοδο')
            total_expenses = self._sum_by_category('έξοδο')
            balance = total_income - total_expenses
            self.income_var.set(f"ΣΥΝΟΛΙΚΑ ΕΣΟΔΑ: {total_income}")
            self.expense_var.set(f"ΣΥΝΟΛΙΚΑ ΕΞΟΔΑ: {total_expenses}")
            self.balance_var.set(f"ΥΠΟΛΟΙΠΟ ΛΟΓΑΡΙΑΣΜΟΥ: {balance}")
        except Exception as ep:
            messagebox.showerror('ΛΑΘΟΣ', ep)


if __name__ == "__main__":
    root = Tk()
    app = PersonalFinanceManager(root)
    root.mainloop()
