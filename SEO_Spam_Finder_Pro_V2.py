"""
Created  by: ANISH R
Date: 2024-06-01
Version: 2.0
For any queries or suggestions, contact: anishry88@gmail.com ph: +91-9895 086 743
Developer: Anish R
Email:anishry88@gmail.com
Developer's Phone: +91-9895 086 743
Tool For CERT-K
-----------
Disclaimer:
-----------
This tool is intended for educational and ethical use only. The author is not responsible for any misuse
or damage caused by this software. Always obtain proper authorization before testing any website.
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ddgs import DDGS
import requests, csv, threading, webbrowser, ssl, socket
import whois


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("SEO Spam Finder Pro V2")
        self.root.geometry("1200x700")

        top = ttk.Frame(root)
        top.pack(fill="x", padx=5, pady=5)

        ttk.Label(top, text="Domain").grid(row=0, column=0)
        self.domain = ttk.Entry(top, width=40)
        self.domain.grid(row=0, column=1)

        ttk.Label(top, text="Keywords").grid(row=1, column=0)
        self.keywords = ttk.Entry(top, width=80)
        self.keywords.grid(row=1, column=1, columnspan=4, sticky="ew")

        ttk.Button(top, text="Search", command=self.start).grid(row=0, column=2)
        ttk.Button(top, text="Copy Selected", command=self.copy_selected).grid(row=0, column=3)
        ttk.Button(top, text="Copy All", command=self.copy_all).grid(row=0, column=4)
        ttk.Button(top, text="Export CSV", command=self.export_csv).grid(row=0, column=5)

        self.progress = ttk.Progressbar(root, mode="indeterminate")
        self.progress.pack(fill="x", padx=5)

        cols = ("Keyword","Status","URL","Redirect","SSL","Headers")
        self.tree = ttk.Treeview(root, columns=cols, show="headings")

        for c in cols:
            self.tree.heading(c, text=c, command=lambda col=c:self.sort(col))
            self.tree.column(c, width=150)

        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<Double-1>", self.open_url)

        self.status = tk.StringVar(value="Ready")
        ttk.Label(root, textvariable=self.status).pack(anchor="w")

    def sort(self, col):
        data = [(self.tree.set(i, col), i) for i in self.tree.get_children("")]
        data.sort()
        for idx, (_, item) in enumerate(data):
            self.tree.move(item, "", idx)

    def start(self):
        threading.Thread(target=self.search, daemon=True).start()

    def is_active(self, url):
        try:
            r = requests.get(url, timeout=10, allow_redirects=True,
                             headers={"User-Agent":"Mozilla/5.0"})
            return r.status_code == 200, r
        except Exception:
            return False, None

    def ssl_check(self, domain):
        try:
            ctx = ssl.create_default_context()
            with socket.create_connection((domain,443), timeout=5) as sock:
                with ctx.wrap_socket(sock, server_hostname=domain):
                    return "OK"
        except Exception:
            return "FAIL"

    def header_check(self, response):
        wanted = [
            "Strict-Transport-Security",
            "Content-Security-Policy",
            "X-Frame-Options"
        ]
        score = sum(1 for h in wanted if h in response.headers)
        return f"{score}/3"

    def search(self):
        self.progress.start()
        self.tree.delete(*self.tree.get_children())

        domain = self.domain.get().strip()
        keywords = [x.strip() for x in self.keywords.get().split(",") if x.strip()]

        try:
            w = whois.whois(domain)
            self.status.set(f"WHOIS OK | Registrar: {getattr(w,'registrar', 'Unknown')}")
        except Exception:
            pass

        ssl_status = self.ssl_check(domain)

        with DDGS() as ddgs:
            for kw in keywords:
                query = f"site:{domain} {kw}"

                try:
                    results = ddgs.text(query, max_results=50)

                    for r in results:
                        url = r.get("href", "")
                        if not url:
                            continue

                        active, resp = self.is_active(url)

                        if not active:
                            continue

                        redirect = "YES" if resp.url != url else "NO"

                        headers = self.header_check(resp)

                        self.tree.insert(
                            "",
                            "end",
                            values=(
                                kw,
                                resp.status_code,
                                resp.url,
                                redirect,
                                ssl_status,
                                headers
                            )
                        )
                except Exception:
                    pass

        self.progress.stop()
        self.status.set("Completed")

    def copy_selected(self):
        sel = self.tree.selection()
        if not sel:
            return
        url = self.tree.item(sel[0])["values"][2]
        self.root.clipboard_clear()
        self.root.clipboard_append(url)

    def copy_all(self):
        urls = []
        for i in self.tree.get_children():
            urls.append(str(self.tree.item(i)["values"][2]))
        self.root.clipboard_clear()
        self.root.clipboard_append("\n".join(urls))

    def export_csv(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv")
        if not path:
            return

        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["Keyword","Status","URL","Redirect","SSL","Headers"])

            for item in self.tree.get_children():
                w.writerow(self.tree.item(item)["values"])

        messagebox.showinfo("Export", "CSV file exported successfully")

    def open_url(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        url = self.tree.item(sel[0])["values"][2]
        webbrowser.open(url)


root = tk.Tk()
App(root)
root.mainloop()
