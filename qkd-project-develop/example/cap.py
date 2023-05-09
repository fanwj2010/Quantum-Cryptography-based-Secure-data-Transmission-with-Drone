import numpy as np

import cv2


def viedo_demo():
    cap = cv2.VideoCapture(0)

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            # frame = cv2.flip(frame, 0)

            # write the flipped frame
            out.write(frame)

            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    # Release everything if job is finished
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    #
    # capture = cv2.VideoCapture(0)
    # w = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
    # h = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
    # fps = capture.get(cv2.CAP_PROP_FPS)
    # filePath = "D:/test.mp4"
    # out = cv2.VideoWriter(filePath, cv2.CAP_ANY, np.int(capture.get(cv2.CAP_PROP_FOURCC)), fps,
    #                       (np.int(w), np.int(h)), True)
    # print(w,h,fps)
    # while True:
    #     ref, frame = capture.read()
    #     if ref is not True:
    #         break
    #     cv2.imshow("frame", frame)
    #     out.write(frame)
    #     # ESC - QUIT
    #     c = cv2.waitKey(30) & 0xff
    #     if c == 27:
    #         capture.release()
    #         break
    #
    # cv2.waitKey()
    # cv2.destroyAllWindows()



if __name__ == '__main__':
    viedo_demo()
