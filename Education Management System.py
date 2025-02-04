from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import mysql.connector

def newemployee():
    identry.delete(0,END)
    nameentry.delete(0,END)
    phoneentry.delete(0,END)
    salaryentry.delete(0,END)
    roleentry.set("Select A Role")
    genderentry.set("Select A Gender")



def addemployee():
    ids = identry.get()
    name = nameentry.get()
    phone = phoneentry.get()
    salary = salaryentry.get()
    role = roleentry.get()
    gender = genderentry.get()

    if ids == "" or name == "" or phone == "" or salary == "" or role == "Select A Role" or gender == "Select A Gender":
        messagebox.showerror("Error", "All fields are required")
    else:
        try:
            con = mysql.connector.connect(host="localhost", user="root", password="Mohith@1315")
            cur = con.cursor()

            cur.execute("CREATE DATABASE IF NOT EXISTS employee")
            cur.execute("USE employee")

            query = """CREATE TABLE IF NOT EXISTS Employee (
                        Id INT PRIMARY KEY,
                        Name VARCHAR(100) NOT NULL,
                        Phone VARCHAR(15) NOT NULL UNIQUE,
                        Gender VARCHAR(50) NOT NULL,
                        Role VARCHAR(50) NOT NULL,
                        Salary DECIMAL(10, 2) NOT NULL);"""
            cur.execute(query)

            insert_query = """INSERT INTO Employee (id, name, phone, gender, role, salary) VALUES (%s, %s, %s, %s, %s, %s)"""
            data = (identry.get(), nameentry.get(), phoneentry.get(), genderentry.get(), roleentry.get(), salaryentry.get())
            cur.execute(insert_query, data)
            con.commit()

            tree.insert("", END, values=data)
            messagebox.showinfo("Success", "Employee Data Inserted Successfully")

            identry.delete(0, END)
            nameentry.delete(0, END)
            phoneentry.delete(0, END)
            salaryentry.delete(0, END)
            roleentry.set("Select A Role")
            genderentry.set("Select A Gender")
        except Exception as e:
            messagebox.showerror("Error", f"Error inserting data: {e}")
           
def select(e):
    index=tree.focus()
    if not index:
        return
    content=tree.item(index)
    data=content['values']

    if not data or len(data) < 6:
        messagebox.showerror("Error", "Row data is incomplete or missing.")
        return
    identry.delete(0, END)
    nameentry.delete(0, END)
    phoneentry.delete(0, END)
    salaryentry.delete(0, END)
    roleentry.set("Select A Role")
    genderentry.set("Select A Gender")
    
    identry.insert(0, data[0])
    nameentry.insert(0, data[1])
    phoneentry.insert(0, data[2])
    genderentry.set(data[3])
    roleentry.set(data[4])
    salaryentry.insert(0, data[5])


    
def update():
    index = tree.focus()
    if not index:
        messagebox.showwarning('No Selection', 'Please select a record to update.')
        return

    content = tree.item(index)
    listdata = content['values']

    if not listdata or len(listdata) < 6:
        messagebox.showerror("Error", "Row data is incomplete or missing.")
        return

    try:
        id = listdata[0]  
        Name = nameentry.get()
        Phone = phoneentry.get()
        Gender = genderentry.get()
        Role = roleentry.get()
        Salary = salaryentry.get()

        newdata = (Name, Phone, Gender, Role, Salary)

        con = mysql.connector.connect(host='localhost', user='root', password='Mohith@1315', database='employee')
        cur = con.cursor()

        cur.execute('SELECT * FROM Employee WHERE id=%s', (id,))
        current_data = cur.fetchone()

        if not current_data:
            messagebox.showerror("Error", "Record not found.")
            return

        # Get the existing data (excluding ID)
        current_d = current_data[1:6]

        if current_d == newdata:
            messagebox.showinfo("No Changes", "No changes detected. Please modify the data before updating.")
            return

        update_query = """
        UPDATE Employee
        SET Name = %s, Phone = %s, Gender = %s, Role = %s, Salary = %s
        WHERE id = %s
        """
        cur.execute(update_query, (*newdata, id))
        con.commit()

        tree.item(index, values=(id, Name, Phone, Gender, Role, Salary))

        messagebox.showinfo("Success", f"Employee with ID {id} updated successfully.")

    except Exception as e:
        messagebox.showerror("Error", f"Error updating data: {e}")

    finally:
        con.close()


def delete_all():
    confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete ALL employee records?")
    
    if not confirm:
        return

    try:
        con = mysql.connector.connect(host="localhost", user="root", passwd="Mohith@1315", database="employee")
        cur = con.cursor()

        delete_query = "DELETE FROM Employee"
        cur.execute(delete_query)
        con.commit()

        # Clear all rows from the treeview
        for item in tree.get_children():
            tree.delete(item)

        messagebox.showinfo("Success", "All employee records have been deleted successfully.")

        # Clear form fields
        identry.delete(0, END)
        nameentry.delete(0, END)
        phoneentry.delete(0, END)
        salaryentry.delete(0, END)
        roleentry.set("Select A Role")
        genderentry.set("Select A Gender")

    except Exception as e:
        messagebox.showerror("Error", f"Error deleting all data: {e}")

   

def delete():
    index = tree.selection()
    
    if not index:
        messagebox.showwarning("Select Row", "Please select a row to delete.")
        return
    content=tree.item(index)
    data=content['values']
    id = data[0]  

    con = mysql.connector.connect(host="localhost", user="root", passwd="Mohith@1315", database="employee")
    cur = con.cursor()

    delete_query = "DELETE FROM Employee WHERE id = %s"

    try:
        cur.execute(delete_query, (id,))
        con.commit()

        tree.delete(index)

        messagebox.showinfo("Success", f"Employee with Id No. {id} deleted successfully.")
        identry.delete(0, END)
        nameentry.delete(0, END)
        phoneentry.delete(0, END)
        salaryentry.delete(0, END)
        roleentry.set("Select A Role")
        genderentry.set("Select A Gender")

    except Exception as e:
        messagebox.showerror("Error", f"Error deleting data: {e}")
        
def search():
    selected_column = searchby.get()
    search_value = searchentry.get()      

    
    for item in tree.get_children():
        tree.delete(item)

    
    try:
        con = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Mohith@1315',  
            database='employee'
        )
        cur = con.cursor()

        
        cur.execute("DESCRIBE Employee")
        result = cur.fetchall()

        columns = []

        for col in result:
            columns.append(col[0])
        
        if selected_column not in columns:
            messagebox.showerror("Invalid Column", f"'{selected_column}' is not a valid column.")
            return

        # Execute the search query
        query = f"SELECT * FROM Employee WHERE {selected_column} = %s"
        cur.execute(query, (search_value,))
        results = cur.fetchall()

        if not results:
            messagebox.showinfo("No Match Found", f"No records found for {selected_column} = '{search_value}'.")
            return

        # Display results in the treeview
        for row in results:
            tree.insert("", END, values=row)

    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")
    
            

def showall():
    try:
        global cur,con
        con = mysql.connector.connect(host="localhost", user="root", passwd="Mohith@1315", database="employee")
        cur = con.cursor()

        select_query = "SELECT * FROM Employee"

        cur.execute(select_query)
        rows = cur.fetchall()
        tree.delete(*tree.get_children())

        if rows:
            for row in rows:
                tree.insert("", "end", values=row)

        messagebox.showinfo("Success", "Data loaded successfully.")

    except Exception as e:
        messagebox.showerror("Error", f"Error fetching data: {e}")
    finally:
        if con.is_connected():
            cur.close()
            con.close()        

def exitb():
    result=messagebox.askyesno("Confirm","Do you Want to exit")
    if result:
        root.destroy()
    else:
        pass
    

root=Tk()
root.title("HMS")
root.geometry("1200x420+0+0")
root.resizable(0,0)
root.config(bg='silver')

headlabel=Label(root,text="Employee Management System",font=("Arial", 20, "bold"),bg="silver",bd=10,relief=RIDGE)
headlabel.pack(fill=X,pady=(5,0))

exitb=Button(root,text="Exit",width=15,font=("Arial", 8, "bold"),bg="red",command=exitb)
exitb.place(x=1050,y=20)

employeeframe=Frame(root,bg="silver",bd=10,relief=RIDGE)
employeeframe.place(x=0,y=60,width=455,height=310)

idlabel=Label(employeeframe,text="Id:",font=("Arial", 20, "bold"),bg="silver")
idlabel.grid(row=0,column=0,padx=5,pady=5,sticky="W")

identry=Entry(employeeframe,width=50)
identry.grid(row=0,column=1,padx=5,pady=5)

namelabel=Label(employeeframe,text="Name:",font=("Arial", 20, "bold"),bg="silver")
namelabel.grid(row=1,column=0,padx=5,pady=5,sticky="W")

nameentry=Entry(employeeframe,width=50)
nameentry.grid(row=1,column=1,padx=5,pady=5)

phonelabel=Label(employeeframe,text="Phone:",font=("Arial", 20, "bold"),bg="silver")
phonelabel.grid(row=2,column=0,padx=5,pady=5,sticky="W")

phoneentry=Entry(employeeframe,width=50)
phoneentry.grid(row=2,column=1,padx=5,pady=5)

salarylabel=Label(employeeframe,text="Salary:",font=("Arial", 20, "bold"),bg="silver")
salarylabel.grid(row=5,column=0,padx=5,pady=5,sticky="W")

salaryentry=Entry(employeeframe,width=50)
salaryentry.grid(row=5,column=1,padx=5,pady=5)

rolelabel=Label(employeeframe,text="Role:",font=("Arial", 20, "bold"),bg="silver")
rolelabel.grid(row=4,column=0,padx=5,pady=5,sticky="W")

roleentry=ttk.Combobox(employeeframe,values=("Frontend Developer","Backend Developer","Fullstack Developer","Data Analyst","DevOps Engineer","QA Tester","UI/UX Designer"),width=47)
roleentry.grid(row=4,column=1,padx=5,pady=5)
roleentry.set("Select A Role")

genderlabel=Label(employeeframe,text="Gender:",font=("Arial", 20, "bold"),bg="silver")
genderlabel.grid(row=3,column=0,padx=5,pady=5,sticky="W")

genderentry=ttk.Combobox(employeeframe,values=("Male","Female","Others"),width=47)
genderentry.grid(row=3,column=1,padx=5,pady=5)
genderentry.set("Select A Gender")

searchframe=Frame(root,bg="silver",bd=10,relief=RIDGE)
searchframe.place(x=460,y=60,width=730)

searchby=ttk.Combobox(searchframe,values=("Id","Name","Phone","Salary","Gender","Role"),width=25)
searchby.grid(row=0,column=0)
searchby.set("Select A Option")

searchentry=Entry(searchframe,width=27)
searchentry.grid(row=0,column=1)

search=Button(searchframe,text="search",width=25,font=("Arial", 8, "bold"),bg="red",command=search)
search.grid(row=0,column=2)

showall=Button(searchframe,text="Show All",width=25,font=("Arial", 8, "bold"),bg="red",command=showall)
showall.grid(row=0,column=3)

treeframe=Frame(root,bg="silver",bd=10,relief=RIDGE)
treeframe.place(x=460,y=110,width=730,height=260)
columns=["Id","Name","Phone","Gender","Role","Salary"]
tree=ttk.Treeview(treeframe,columns=columns,show="headings")

tree.heading("Id",text="Id")
tree.heading("Name",text="Name")
tree.heading("Phone",text="Phone")
tree.heading("Gender",text="Gender")
tree.heading("Role",text="Role")
tree.heading("Salary",text="Salary")

tree.column("Id",width=50,anchor=W)
tree.column("Name",width=200,anchor=W)
tree.column("Phone",width=150,anchor=W)
tree.column("Gender",width=50,anchor=W)
tree.column("Role",width=150,anchor=W)
tree.column("Salary",width=100,anchor=W)


scrollbar_y = ttk.Scrollbar(treeframe, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar_y.set)
scrollbar_y.pack(side=RIGHT, fill=Y)

scrollbar_x = ttk.Scrollbar(treeframe, orient="horizontal", command=tree.xview)
tree.configure(xscroll=scrollbar_x.set)
scrollbar_x.pack(side=BOTTOM, fill=X)
tree.bind("<<TreeviewSelect>>", select)


tree.pack(fill=BOTH, expand=True)

butoonframe=Frame(root,width=1000,height=50,bg="silver",bd=10,relief=RIDGE)
butoonframe.place(x=0,y=375)

new=Button(butoonframe,text="New Employee",width=33,font=("Arial", 8, "bold"),bg="red",command=newemployee)
new.grid(row=0,column=0)

add=Button(butoonframe,text="Add Employee",width=33,font=("Arial", 8, "bold"),bg="red",command=addemployee)
add.grid(row=0,column=1)

update=Button(butoonframe,text="Update Employee",width=33,font=("Arial", 8, "bold"),bg="red",command=update)
update.grid(row=0,column=2)

delete=Button(butoonframe,text="Delete Employee",width=33,font=("Arial", 8, "bold"),bg="red",command=delete)
delete.grid(row=0,column=3)

deleteall=Button(butoonframe,text="Delete All",width=28,font=("Arial", 8, "bold"),bg="red",command=delete_all)
deleteall.grid(row=0,column=4)




root.mainloop()
