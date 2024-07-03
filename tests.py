import autoit

def open_notepad():
    autoit.run("notepad.exe")
    autoit.win_wait_active("[CLASS:Notepad]", 5)
    return autoit.win_get_title("[CLASS:Notepad]")

def write_in_notepad(title, text):
    autoit.win_activate("[CLASS:Notepad]")
    autoit.send(text)

def close_notepad():
    if not autoit.win_exists("[CLASS:Notepad]"):
        print("La fenêtre Notepad n'existe pas")
        return
    else:
        print("La fenêtre Notepad existe")
    
    autoit.win_close("[CLASS:Notepad]")
    autoit.win_wait_active("[CLASS:#32770]", 10)  # waits for the dialogue box
    autoit.control_click("[CLASS:#32770]", "Button2")  # doesn't save

def open_write_close():
    current_title = open_notepad()
    if "Sans titre" not in current_title:
        autoit.send("^n")  # Open a new Notepad window if the current one is not new
        autoit.win_wait_active("[CLASS:Notepad]", 5)
    
    write_in_notepad("[CLASS:Notepad]", "test")
    close_notepad()

open_write_close()
