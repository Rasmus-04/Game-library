import cx_Freeze

executables = [cx_Freeze.Executable("D:\Programing\Python\Flappy_birds_test_exe\Flappybird.py")]

cx_Freeze.setup(
    name = "Flappy bird",
    options = {"build_exe": {"packages":["pygame", "random"], "include_files":["D:\Programing\Python\Flappy_birds_test_exe\Bg.png", "D:\Programing\Python\Flappy_birds_test_exe\Bird.png", "D:\Programing\Python\Flappy_birds_test_exe\Bird_down.png", "D:\Programing\Python\Flappy_birds_test_exe\Bird_up.png", "D:\Programing\Python\Flappy_birds_test_exe\cloud.png"]}},
    executables = executables
)