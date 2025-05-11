import random, os, time

BALANCE_FILE = "balance.txt"
f = 0
win = 0
lose = 0

def clearScreen(): 
    os.system("cls" if os.name == "nt" else "clear")

def load():
    try:
        with open(BALANCE_FILE, "r") as file:
            return round(float(file.read().strip()))
    except FileNotFoundError:
        return 1000

def save(balance):
    with open(BALANCE_FILE, "w") as file:
        file.write(str(balance))

# ───── SLOTS ─────

def slot_spin():
    global f
    symbols = ["🍒", "🔔", "💎", "🍋", "⭐", "7️⃣", "🍇", "🍉", "🍊"]
    if f == 0:
        slot1, slot2 = "💎", random.choice(symbols)
        slot3 = random.choice(symbols)
        f += 1
    else:
        slot1 = random.choice(symbols)
        slot2 = random.choice(symbols)
        slot3 = random.choice(symbols)
    return slot1, slot2, slot3

def slot_check(slot1, slot2, slot3, bet, auto):
    if slot1 == slot2 == slot3:
        if auto: return "JACKPOT!", bet * 9, True
        else: return "JACKPOT!", bet * 10, True
    if slot1 == slot2 == slot3 and slot1 == "💎":
        return "JACKPOT with 💎!", bet * 50, True
    elif slot1 == slot2 or slot1 == slot3 or slot2 == slot3:
        return "Matched two!", bet * 3, True
    else:
        return "No match.", -bet, False

def play_slots(balance):
    global win, lose
    auto = False
    print("🎰 Welcome to Slots!")
    print(f"Balance: 🪙 {balance}")
    while balance > 0:
        try:
            if not auto:
                bet = input("Enter bet (or type 'auto', '.' or 'back'): ").lower()
                if bet == "auto":
                    autoset = int(input("Auto bet amount (casino takes 20%): "))
                    bet = autoset
                    auto = True
                elif bet == "back":
                    break
                elif bet == ".":
                    cheat = balance + random.randint(1000, 9999)
                    save(cheat)
                    balance = cheat
                    print("👀 Cheat used. New balance:", balance)
                    continue
                else:
                    bet = int(bet)
                    if bet > balance or bet <= 0:
                        print("Invalid bet.")
                        continue
            else:
                bet = autoset
                if bet > balance:
                    print("Auto-bet too high. Exiting auto.")
                    auto = False
                    continue
                print(f"Auto-betting {bet}. Wins: {win} Losses: {lose}")
                time.sleep(0.3)

            slot1, slot2, slot3 = slot_spin()
            clearScreen()
            print(f"[ {slot1} | {slot2} | {slot3} ]")
            result, winnings, ifwon = slot_check(slot1, slot2, slot3, bet, auto)
            print(result)
            if auto and ifwon:
                balance += winnings // 1.25
            else:
                balance += winnings

            if winnings > 0:
                win += 1
                print(f"Won 🪙 {winnings}! New balance: 🪙 {balance}")
            else:
                lose += 1
                print(f"Lost 🪙 {-winnings}. New balance: 🪙 {balance}")
            save(balance)

        except KeyboardInterrupt:
            print("\nExiting Slots.")
            break
        except Exception as e:
            print("Error:", e)
            break
    return balance

# ───── BLACKJACK ─────

def bj_card(): return random.choice(['2','3','4','5','6','7','8','9','10','J','Q','K','A'])

def bj_total(hand):
    total, aces = 0, 0
    for c in hand:
        if c in ['J','Q','K']: total += 10
        elif c == 'A': total += 11; aces += 1
        else: total += int(c)
    while total > 21 and aces: total -= 10; aces -= 1
    return total

def play_blackjack(balance):
    print("🃏 Welcome to Blackjack!")
    bet = int(input("Enter your bet: "))
    if bet > balance or bet <= 0:
        print("Invalid bet.")
        return balance
    player = [bj_card(), bj_card()]
    dealer = [bj_card(), bj_card()]

    while True:
        print(f"Your hand: {' '.join(player)} (Total: {bj_total(player)})")
        print(f"Dealer shows: {dealer[0]}")
        move = input("Hit or stand? ").lower()
        if move == "hit":
            player.append(bj_card())
            if bj_total(player) > 21:
                print("Bust! You lose.")
                return balance - bet
        elif move == "stand":
            break
        else:
            continue

    while bj_total(dealer) < 17:
        dealer.append(bj_card())

    p, d = bj_total(player), bj_total(dealer)
    print(f"Dealer hand: {' '.join(dealer)} (Total: {d})")
    if d > 21 or p > d: print("You win!"); return balance + bet
    elif p == d: print("Push."); return balance
    else: print("You lose."); return balance - bet

# ───── ROULETTE ─────

def play_roulette(balance):
    print("🎡 Welcome to Roulette!")
    print("You can bet on 'red', 'black', or 'green'")
    bet_type = input("Enter your bet: ").lower()
    if bet_type not in ['red', 'black', 'green']:
        print("Invalid bet type.")
        return balance
    bet_amount = int(input("Enter your bet amount: "))
    if bet_amount > balance or bet_amount <= 0:
        print("Invalid bet.")
        return balance

    outcome = random.choices(['red', 'black', 'green'], [18, 18, 1])[0]
    print("Wheel spinning...")
    time.sleep(1)
    print(f"The ball landed on {outcome}!")

    if bet_type == outcome:
        if outcome == "green":
            print("Jackpot! 14x payout!")
            return balance + bet_amount * 14
        else:
            print("You win!")
            return balance + bet_amount
    else:
        print("You lose.")
        return balance - bet_amount

# ───── MAIN MENU ─────

def main():
    balance = load()
    while True:
        print("\n🎰 Python Casino 🎰")
        print("1. Play Slots")
        print("2. Play Blackjack")
        print("3. Play Roulette")
        print("4. Exit")
        print(f"🪙 Balance: {balance}")
        choice = input("Choose an option: ")
        if choice == "1":
            balance = play_slots(balance)
        elif choice == "2":
            balance = play_blackjack(balance)
            save(balance)
        elif choice == "3":
            balance = play_roulette(balance)
            save(balance)
        elif choice == "4":
            print("Thanks for playing!")
            save(balance)
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
