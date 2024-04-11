try:
    import cv2
    import numpy as np
    from sys import argv
    from os import path


    if len(argv) < 1:
        print('Plz drag and drop a video into the .exe!')
        input('')
        exit()

    #  Made by Tarngaina, to get the best amount of rows and columns
    def do_the_thing(frames, width, height):
        best_size = None
        min_gap = float('inf')
        for x in range(frames//2):
            for y in range(frames//2):
                if x*y == frames:
                    fullw = x*width
                    fullh = y*height
                    gap = abs(fullw-fullh)
                    if gap < min_gap:
                        min_gap = gap
                        best_size = (x, y, fullw, fullh)
        if best_size:
            if best_size[-1] < 16384 and best_size[-2] < 16384:
                return best_size
        return None
    
    def get_numbers(frames, width, height):
        best_size = do_the_thing(frames, width, height)
        if best_size: return best_size

        print('Could not find any number to write the spritesheet')
        print('Try to lower the resolution')
        print('Or use one of the following amount of frames:')
        l = []
        for frame in range(frames):
            best_size = do_the_thing(frame, width, height)
            if best_size: l.append(frame)
        print(', '.join(str(s) for s in l[::-1]))
        return None
        
    video_file = argv[1]
    cap = cv2.VideoCapture(video_file)

    sprite_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    sprite_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if (unpack := get_numbers(num_frames, sprite_width, sprite_height)):
        num_cols, num_rows, img_width, img_heigth = unpack
    else:
        raise SyntaxError()  # lmao syntax error
    spritesheet = np.zeros((int(sprite_height*num_rows), int(sprite_width*num_cols), 3), int)

    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        # not more frames, breaking da loop
        if not ret:
            break

        row = frame_count // num_cols
        col = frame_count % num_cols

        # Dont ask me what this is :D
        spritesheet[row*sprite_height:(row+1)*sprite_height, col*sprite_width:(col+1)*sprite_width, :] = frame
        frame_count += 1


    cv2.imwrite(path.dirname(video_file) + '/spritesheet.png', spritesheet)
    print('Frame Count: ', frame_count)
    print('Num of columns (NumberOfFramesPerRowInAtlas): ',num_cols)
    print('Num of rows: ', num_rows)
    print('Width: ', img_width)
    print('Height: ', img_heigth)
    print(f'Resolution (Remember to subtract 1): {sprite_width}x{sprite_height}')

    cap.release()
    input('\nType anything to leave or just close the window <3')

except SyntaxError:
    input('Press enter to leave or close window')

except Exception as e:
    print(e)
    print()
    print('Something bad happen lol')
    input('Press enter to leave or close window')