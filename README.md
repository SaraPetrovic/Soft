# Soft
Detekcija objekta na snimku, Soft kompjuting 2018/2019

Za pokretanje skripti potrebano je na racunaru imati instaliran Python 2.7 i instalirati potrebne biblioteke (OpenCV, pyautogui, imutils, numpy, argparse), u komandnoj liniji, pip install komandom.
U tresholding.py skripti implementirana je detekcija bilo kog objekta plave boje na snimku pomocu tresholding-a, kojim se komanduje kretanje pacman-a, dok je u neural_network.py skripti koriscena obucena neuronska mreza iz OpenCV biblioteke da bi se detektovala boca kojom se komanduje kretanje pacman-a.
Pokretanje neural_network.py se vrsi na sledeci nacin: python real_time_object_detection.py --prototxt MobileNetSSD_deploy.prototxt.txt --model MobileNetSSD_deploy.caffemodel
Program se moze testirati na bilo kojoj igrici koja koristi tastere na tastaturi za gore, dole, levo i desno. Ja sam testirala nad google-ovom Pacman igricom, kao i nad instaliranom desktop Pacman igricom.
