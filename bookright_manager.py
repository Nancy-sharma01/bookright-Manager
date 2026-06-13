import os
import json

# ── Colors ────────────────────────────────────────────────
RESET  = "\033[0m"
BOLD   = "\033[1m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
GREEN  = "\033[92m"
RED    = "\033[91m"
MAGENTA = "\033[95m"
DIM    = "\033[2m"

DATA_FILE = "books.json"

# ── Load / Save ───────────────────────────────────────────
def load_books():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_books(books):
    with open(DATA_FILE, "w") as f:
        json.dump(books, f, indent=2)

# ── Helpers ───────────────────────────────────────────────
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def header():
    print(f"\n  {YELLOW}{BOLD}{'═' * 40}{RESET}")
    print(f"  {YELLOW}{BOLD}       📚  THE BOOKRIGHT MANAGER  📚{RESET}")
    print(f"  {YELLOW}{BOLD}{'═' * 40}{RESET}\n")

def pause():
    input(f"\n  {DIM}Press Enter to continue...{RESET}")

def show_book(i, book):
    status = f"{GREEN}✔ Read{RESET}" if book["read"] else f"{RED}✘ Unread{RESET}"
    stars  = f"{YELLOW}{'★' * book['rating']}{'☆' * (5 - book['rating'])}{RESET}"
    print(f"  {CYAN}{BOLD}[{i}]{RESET} {BOLD}{book['title']}{RESET}")
    print(f"      Author : {book['author']}")
    print(f"      Genre  : {book['genre']}")
    print(f"      Rating : {stars}")
    print(f"      Status : {status}")
    if book["review"]:
        print(f"      Review : {DIM}{book['review']}{RESET}")
    print()

# ── Features ──────────────────────────────────────────────
def view_all(books):
    clear()
    header()
    if not books:
        print(f"  {DIM}No books yet. Add some!{RESET}\n")
    else:
        print(f"  {MAGENTA}{BOLD}Your Book Collection ({len(books)} books){RESET}\n")
        for i, book in enumerate(books, 1):
            show_book(i, book)
    pause()

def add_book(books):
    clear()
    header()
    print(f"  {CYAN}{BOLD}➕ Add a New Book{RESET}\n")

    title  = input(f"  {CYAN}Book Title  :{RESET} ").strip()
    if not title:
        print(f"  {RED}Title cannot be empty!{RESET}")
        pause()
        return

    author = input(f"  {CYAN}Author Name :{RESET} ").strip() or "Unknown"
    genre  = input(f"  {CYAN}Genre       :{RESET} ").strip() or "General"

    while True:
        try:
            rating = int(input(f"  {CYAN}Rating (1-5):{RESET} ").strip())
            if 1 <= rating <= 5:
                break
            print(f"  {RED}Enter a number between 1 and 5.{RESET}")
        except ValueError:
            print(f"  {RED}Please enter a valid number.{RESET}")

    read_input = input(f"  {CYAN}Have you read it? (y/n):{RESET} ").strip().lower()
    read = read_input == "y"

    review = input(f"  {CYAN}Short review (optional):{RESET} ").strip()

    books.append({
        "title":  title,
        "author": author,
        "genre":  genre,
        "rating": rating,
        "read":   read,
        "review": review
    })
    save_books(books)
    print(f"\n  {GREEN}✔ '{title}' added successfully!{RESET}")
    pause()

def remove_book(books):
    clear()
    header()
    if not books:
        print(f"  {DIM}No books to remove.{RESET}")
        pause()
        return

    print(f"  {RED}{BOLD}🗑  Remove a Book{RESET}\n")
    for i, book in enumerate(books, 1):
        print(f"  {CYAN}[{i}]{RESET} {book['title']} — {DIM}{book['author']}{RESET}")

    try:
        choice = int(input(f"\n  {CYAN}Enter book number to remove (0 to cancel):{RESET} "))
        if choice == 0:
            return
        if 1 <= choice <= len(books):
            removed = books.pop(choice - 1)
            save_books(books)
            print(f"\n  {GREEN}✔ '{removed['title']}' removed.{RESET}")
        else:
            print(f"  {RED}Invalid number.{RESET}")
    except ValueError:
        print(f"  {RED}Please enter a valid number.{RESET}")
    pause()

def toggle_read(books):
    clear()
    header()
    if not books:
        print(f"  {DIM}No books available.{RESET}")
        pause()
        return

    print(f"  {CYAN}{BOLD}🔄 Mark as Read / Unread{RESET}\n")
    for i, book in enumerate(books, 1):
        status = f"{GREEN}Read{RESET}" if book["read"] else f"{RED}Unread{RESET}"
        print(f"  {CYAN}[{i}]{RESET} {book['title']} — {status}")

    try:
        choice = int(input(f"\n  {CYAN}Enter book number to toggle (0 to cancel):{RESET} "))
        if choice == 0:
            return
        if 1 <= choice <= len(books):
            books[choice - 1]["read"] = not books[choice - 1]["read"]
            save_books(books)
            new_status = "Read" if books[choice - 1]["read"] else "Unread"
            print(f"\n  {GREEN}✔ Marked as '{new_status}'.{RESET}")
        else:
            print(f"  {RED}Invalid number.{RESET}")
    except ValueError:
        print(f"  {RED}Please enter a valid number.{RESET}")
    pause()

def search_book(books):
    clear()
    header()
    print(f"  {CYAN}{BOLD}🔍 Search Books{RESET}\n")
    query = input(f"  {CYAN}Enter title or author to search:{RESET} ").strip().lower()

    results = [b for b in books if query in b["title"].lower() or query in b["author"].lower()]

    print()
    if results:
        print(f"  {GREEN}Found {len(results)} result(s):{RESET}\n")
        for i, book in enumerate(results, 1):
            show_book(i, book)
    else:
        print(f"  {RED}No books found for '{query}'.{RESET}\n")
    pause()

def show_stats(books):
    clear()
    header()
    print(f"  {MAGENTA}{BOLD}📊 Your Reading Stats{RESET}\n")

    total  = len(books)
    read   = sum(1 for b in books if b["read"])
    unread = total - read
    avg_rating = round(sum(b["rating"] for b in books) / total, 1) if total else 0

    print(f"  📚 Total Books   : {BOLD}{total}{RESET}")
    print(f"  {GREEN}✔ Read          : {read}{RESET}")
    print(f"  {RED}✘ Unread        : {unread}{RESET}")
    print(f"  {YELLOW}★ Avg Rating    : {avg_rating} / 5{RESET}")

    if books:
        top = max(books, key=lambda b: b["rating"])
        print(f"\n  {YELLOW}{BOLD}🏆 Top Rated Book:{RESET} {top['title']} by {top['author']} ({top['rating']}★)")

    print()
    pause()

# ── Main Menu ─────────────────────────────────────────────
def main():
    books = load_books()

    while True:
        clear()
        header()
        print(f"  {BOLD}  What would you like to do?{RESET}\n")
        print(f"  {CYAN}[1]{RESET}  View All Books")
        print(f"  {CYAN}[2]{RESET}  Add a Book")
        print(f"  {CYAN}[3]{RESET}  Remove a Book")
        print(f"  {CYAN}[4]{RESET}  Mark as Read / Unread")
        print(f"  {CYAN}[5]{RESET}  Search Books")
        print(f"  {CYAN}[6]{RESET}  Reading Stats")
        print(f"  {RED}[7]{RESET}  Exit\n")

        choice = input(f"  {CYAN}➤ Enter choice:{RESET} ").strip()

        if choice == "1":
            view_all(books)
        elif choice == "2":
            add_book(books)
        elif choice == "3":
            remove_book(books)
        elif choice == "4":
            toggle_read(books)
        elif choice == "5":
            search_book(books)
        elif choice == "6":
            show_stats(books)
        elif choice == "7":
            clear()
            print(f"\n  {YELLOW}{BOLD}Thanks for using Bookright Manager! Happy Reading! 📖{RESET}\n")
            break
        else:
            print(f"  {RED}Invalid choice. Try again.{RESET}")
            pause()

if __name__ == "__main__":
    main()
