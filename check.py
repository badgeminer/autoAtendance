import sys
f = open("Ver",mode="r")
t= f.read().split(".")
f.close()
if int(t[2]) == 9:
  t[2] = 0
  if int(t[1]) == 9:
    t[1] = 0
    t[0] = int(t[0]) + 1
  else:
    t[1] = int(t[1]) + 1
else:
  t[2] = int(t[2]) + 1
f = open("Ver",mode="w")
f.write(f"{str(t[0])}.{str(t[1])}.{str(t[2])}")
f.close()
sys.exit(0)
