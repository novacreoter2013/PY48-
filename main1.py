import random
import tkinter as tk
import winsound

WIDTH, HEIGHT = 400, 600
SPEED = 18
SCORE = 0

root = tk.Tk()
root.title("Car Dodger")
root.resizable(False, False)

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#333333")
canvas.pack()

for y in range(0, HEIGHT, 60):
    canvas.create_line(
        WIDTH // 2, y, WIDTH // 2, y + 35, fill="white", width=4, tags="road"
    )

player_x = 180
player = canvas.create_rectangle(
    player_x, 500, player_x + 40, 560, fill="#00d2ff", outline="white"
)

traffic = []


def spawn_vehicle():
    v_type = random.choice(["car", "truck"])
    lane_x = random.choice([50, 130, 210, 290])

    if v_type == "car":
        v_id = canvas.create_rectangle(
            lane_x, -70, lane_x + 40, -10, fill="#ff4757", outline="white"
        )
    else:
        v_id = canvas.create_rectangle(
            lane_x, -110, lane_x + 48, -10, fill="#ffa502", outline="black"
        )

    traffic.append((v_id, v_type))
    root.after(random.randint(900, 1500), spawn_vehicle)


def move_left(event):
    if canvas.coords(player)[0] > 20:
        canvas.move(player, -35, 0)


def move_right(event):
    if canvas.coords(player)[2] < WIDTH - 20:
        canvas.move(player, 35, 0)


root.bind("<Left>", move_left)
root.bind("<Right>", move_right)
root.bind("a", move_left)
root.bind("d", move_right)


def check_collision(box1, box2):
    return not (
        box1[2] < box2[0]
        or box1[0] > box2[2]
        or box1[3] < box2[1]
        or box1[1] > box2[3]
    )


def play_bg():
    winsound.PlaySound(
        "BG.mp3",
        winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP,
    )


def game_loop():
    global SCORE
    p_box = canvas.coords(player)

    canvas.move("road", 0, 10)
    for line in canvas.find_withtag("road"):
        if canvas.coords(line)[1] >= HEIGHT:
            canvas.move(line, 0, -HEIGHT)

    to_remove = []
    for item in traffic:
        v_id, v_type = item
        speed = 8 if v_type == "truck" else 11
        canvas.move(v_id, 0, speed)

        v_box = canvas.coords(v_id)

        if check_collision(p_box, v_box):
            winsound.PlaySound("YOU LOSE.mp3", winsound.SND_FILENAME)
            print("Game Ends! Final Score:", SCORE)
            root.destroy()
            return

        if v_box[1] > HEIGHT:
            canvas.delete(v_id)
            to_remove.append(item)
            SCORE += 1

    for item in to_remove:
        traffic.remove(item)

    root.after(SPEED, game_loop)


play_bg()
spawn_vehicle()
game_loop()
root.mainloop()