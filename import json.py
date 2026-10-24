import json
import os
import time
import tkinter as tk
from tkinter import ttk, messagebox

DATA_FILE = "data.json"

# 初始化数据
def init_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=4)

# 读取数据
def load_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

# 保存数据
def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

class AccountBookGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("个人收支记账系统")
        self.root.geometry("750x550")
        self.root.resizable(False, False)

        init_data()
        self.data = load_data()

        self.create_widgets()
        self.refresh_list()

    def create_widgets(self):
        # 标题
        title = tk.Label(self.root, text="个人收支记账系统", font=("微软雅黑", 22, "bold"), fg="#2c3e50")
        title.pack(pady=15)

        # 输入区域
        frame_input = tk.Frame(self.root)
        frame_input.pack(pady=5)

        tk.Label(frame_input, text="类型：", font=("微软雅黑", 12)).grid(row=0, column=0)
        self.type_var = tk.StringVar(value="收入")
        ttk.Combobox(frame_input, textvariable=self.type_var, values=["收入","支出"], width=8, state="readonly").grid(row=0,column=1,padx=5)

        tk.Label(frame_input, text="金额：", font=("微软雅黑", 12)).grid(row=0, column=2)
        self.money_entry = ttk.Entry(frame_input, width=10)
        self.money_entry.grid(row=0,column=3,padx=5)

        tk.Label(frame_input, text="备注：", font=("微软雅黑", 12)).grid(row=0, column=4)
        self.remark_entry = ttk.Entry(frame_input, width=18)
        self.remark_entry.grid(row=0,column=5,padx=5)

        # 按钮
        frame_btn = tk.Frame(self.root)
        frame_btn.pack(pady=8)

        ttk.Button(frame_btn, text="添加记录", command=self.add_record, width=12).grid(row=0,column=0,padx=5)
        ttk.Button(frame_btn, text="修改记录", command=self.edit_record, width=12).grid(row=0,column=1,padx=5)
        ttk.Button(frame_btn, text="删除记录", command=self.del_record, width=12).grid(row=0,column=2,padx=5)
        ttk.Button(frame_btn, text="收支统计", command=self.show_stat, width=12).grid(row=0,column=3,padx=5)

        # 列表
        frame_list = tk.Frame(self.root)
        frame_list.pack(pady=10, fill=tk.BOTH, expand=True, padx=20)

        scroll = ttk.Scrollbar(frame_list)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.list_box = tk.Listbox(frame_list, font=("微软雅黑", 11), yscrollcommand=scroll.set, height=14)
        self.list_box.pack(fill=tk.BOTH, expand=True)
        scroll.config(command=self.list_box.yview)

        # 统计栏
        self.stat_bar = tk.Label(self.root, text="总收入：0.00   总支出：0.00   结余：0.00", font=("微软雅黑", 12, "bold"), fg="#e74c3c")
        self.stat_bar.pack(pady=10)

    # 刷新列表
    def refresh_list(self):
        self.list_box.delete(0, tk.END)
        for i, item in enumerate(self.data, 1):
            self.list_box.insert(tk.END, f"{i:2} │ {item['type']:4} │ {item['money']:6.1f} │ {item['remark']} │ {item['time']}")
        self.update_bottom()

    # 底部统计
    def update_bottom(self):
        in_sum = sum(x['money'] for x in self.data if x['type'] == "收入")
        out_sum = sum(x['money'] for x in self.data if x['type'] == "支出")
        balance = in_sum - out_sum
        self.stat_bar.config(text=f"总收入：{in_sum:.2f}   总支出：{out_sum:.2f}   结余：{balance:.2f}")

    # 添加
    def add_record(self):
        t = self.type_var.get()
        money = self.money_entry.get().strip()
        remark = self.remark_entry.get().strip()

        if not money or not remark:
            messagebox.showwarning("提示","请填写完整")
            return
        try:
            money = float(money)
            if money <= 0:
                messagebox.showerror("错误","金额必须大于0")
                return
        except:
            messagebox.showerror("错误","请输入数字")
            return

        self.data.append({
            "type":t, "money":money, "remark":remark,
            "time":time.strftime("%m-%d %H:%M")
        })
        save_data(self.data)
        self.money_entry.delete(0,tk.END)
        self.remark_entry.delete(0,tk.END)
        self.refresh_list()
        messagebox.showinfo("成功","添加记录完成！")

    # 删除
    def del_record(self):
        try:
            idx = self.list_box.curselection()[0]
            del self.data[idx]
            save_data(self.data)
            self.refresh_list()
            messagebox.showinfo("成功","删除成功")
        except:
            messagebox.showwarning("提示","请选择一条记录")

    # 修改
    def edit_record(self):
        try:
            idx = self.list_box.curselection()[0]
            item = self.data[idx]
        except:
            messagebox.showwarning("提示","请选择记录")
            return

        top = tk.Toplevel(self.root)
        top.title("修改记录")
        top.geometry("350x200")
        top.grab_set()

        tk.Label(top,text="类型：").place(x=30,y=30)
        t_var = tk.StringVar(value=item['type'])
        ttk.Combobox(top,textvariable=t_var,values=["收入","支出"],state="readonly").place(x=80,y=30)

        tk.Label(top,text="金额：").place(x=30,y=70)
        m_entry = ttk.Entry(top)
        m_entry.insert(0,str(item['money']))
        m_entry.place(x=80,y=70)

        tk.Label(top,text="备注：").place(x=30,y=110)
        r_entry = ttk.Entry(top)
        r_entry.insert(0,item['remark'])
        r_entry.place(x=80,y=110)

        def save_edit():
            try:
                mon = float(m_entry.get())
                if mon <=0:
                    messagebox.showerror("错误","金额>0")
                    return
            except:
                messagebox.showerror("错误","输入数字")
                return

            self.data[idx]['type'] = t_var.get()
            self.data[idx]['money'] = mon
            self.data[idx]['remark'] = r_entry.get()
            save_data(self.data)
            self.refresh_list()
            top.destroy()
            messagebox.showinfo("成功","修改完成")

        ttk.Button(top,text="保存",command=save_edit).place(x=140,y=150)

    # 统计
    def show_stat(self):
        in_sum = sum(x['money'] for x in self.data if x['type']=="收入")
        out_sum = sum(x['money'] for x in self.data if x['type']=="支出")
        bal = in_sum - out_sum
        messagebox.showinfo("收支统计",f"总收入：{in_sum:.2f}\n总支出：{out_sum:.2f}\n结余：{bal:.2f}")

if __name__ == "__main__":
    root = tk.Tk()
    AccountBookGUI(root)
    root.mainloop()