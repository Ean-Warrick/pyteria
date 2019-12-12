def initiate(window, maximize, vsync):
    if maximize:
        window.maximize()

    if vsync:
        window.set_vsync(True)


