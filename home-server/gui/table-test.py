import tkinter as tk
import functions as f
import mariadb
import pandas as pd
import pandastable as pt
import devicepanel as dp

conn = f.connectMDB()
cur = conn.cursor()

df = pd.read_sql_query("SELECT * FROM energy WHERE id=2;", conn)

print(df)

#--main--#

root = tk.Tk()

f = tk.Frame(root)

f.pack(fill="both", expand=True)

pt = pt.Table(f, dataframe=df, showtoolbar=True, showstatusbar=True)
pt.show()

root.mainloop()

conn.commit()
conn.close()
