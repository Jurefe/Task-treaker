import sys
import json
import os
from datetime import datetime

JSON_FILE = 'tasks.json'

# --- FUNGSI BANTUAN (HELP) ---
def show_help():
    print("""
==================================================
        TASK TRACKER CLI - MENU BANTUAN
==================================================
Cara Penggunaan: python task_cli.py [perintah] [argumen]

PERINTAH UTAMA:
  add "deskripsi"          : Menambah tugas baru
  list                     : Menampilkan semua tugas
  list [status]            : Filter (todo, in-progress, done)
  update [id] "deskripsi"  : Mengubah deskripsi tugas
  delete [id]              : Menghapus tugas

STATUS:
  mark-in-progress [id]    : Ubah status ke 'sedang dikerjakan'
  mark-done [id]           : Ubah status ke 'selesai'

CONTOH:
  python task_cli.py add "Belajar Python"
  python task_cli.py list done
  python task_cli.py update 1 "Belajar Python Lanjut"
  python task_cli.py delete 2
==================================================
    """)

# ... (Fungsi load_tasks, save_tasks, add_task, dll tetap sama seperti sebelumnya) ...

def load_tasks():
    if not os.path.exists(JSON_FILE): return []
    with open(JSON_FILE, 'r') as file:
        try: return json.load(file)
        except: return []

def save_tasks(tasks):
    with open(JSON_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)

def add_task(description):
    tasks = load_tasks()
    new_id = max([t['id'] for t in tasks], default=0) + 1
    now = datetime.now().isoformat()
    tasks.append({"id": new_id, "description": description, "status": "todo", "createdAt": now, "updatedAt": now})
    save_tasks(tasks)
    print(f"Berhasil! Task ditambah dengan ID: {new_id}")

def list_tasks(filter_status=None):
    tasks = load_tasks()
    if not tasks:
        print("Daftar tugas kosong.")
        return
    for t in tasks:
        if filter_status and t['status'] != filter_status: continue
        print(f"[{t['id']}] {t['description']} ({t['status']})")

def update_task(task_id, new_desc):
    tasks = load_tasks()
    for t in tasks:
        if t['id'] == int(task_id):
            t['description'] = new_desc
            t['updatedAt'] = datetime.now().isoformat()
            save_tasks(tasks)
            print("Berhasil diupdate!")
            return
    print("ID tidak ditemukan.")

def delete_task(task_id):
    tasks = load_tasks()
    new_tasks = [t for t in tasks if t['id'] != int(task_id)]
    if len(tasks) == len(new_tasks):
        print("ID tidak ditemukan.")
    else:
        save_tasks(new_tasks)
        print("Berhasil dihapus!")

def mark_status(task_id, status):
    tasks = load_tasks()
    for t in tasks:
        if t['id'] == int(task_id):
            t['status'] = status
            t['updatedAt'] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Status diubah ke {status}")
            return
    print("ID tidak ditemukan.")

# --- SISTEM NAVIGASI (DENGAN HELP) ---

def main():
    # Jika user tidak ngetik apa-apa, langsung kasih lihat Help
    if len(sys.argv) < 2:
        show_help()
        return

    cmd = sys.argv[1]

    try:
        if cmd == "help":
            show_help()
        elif cmd == "add":
            add_task(sys.argv[2])
        elif cmd == "list":
            status = sys.argv[2] if len(sys.argv) > 2 else None
            list_tasks(status)
        elif cmd == "update":
            update_task(sys.argv[2], sys.argv[3])
        elif cmd == "delete":
            delete_task(sys.argv[2])
        elif cmd == "mark-in-progress":
            mark_status(sys.argv[2], "in-progress")
        elif cmd == "mark-done":
            mark_status(sys.argv[2], "done")
        else:
            print(f"Perintah '{cmd}' tidak ada. Ketik 'python task_cli.py help' untuk bantuan.")
    except (IndexError, ValueError):
        print("Error: Argumen salah atau kurang. Lihat 'help' untuk panduan.")

if __name__ == "__main__":
    main()