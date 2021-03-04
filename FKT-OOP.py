import re
import sympy as sy
from sympy import diff, integrate


koeffizienten = []


def hilfe():
    print("!b: beendet das Programm")
    print("!fkt: definiert Funktionen oder bearbeitet sie")
    print("Die Funktion 2x³+x+4 müsste als 2xh3+1x+4 eingetippt werden.")
    print("!wt: Wertetabellen")
    print("!nt: Nullstellen")
    print("!sp: Schnittpunkte")
    print("!ab: Ableitungen")
    print("!ig: Integrale")


class Funktionen:
    def __init__(self, parameter, koeffizienten_lokal):
        self.pattern1 = r"(\d){1}x"  #alle koeffizienten (außer der vor x^0, falls nicht in eingabe per \dxh0)
        self.pattern2 = r"h(\d){1}"  #alle exponenten
        self.pattern3 = r"(\d){1}"  #alle zahlen (koeffizienten + exponenten + "restzahl" (koeffizient von x^0)
        self.parameter = parameter
        self.koeffizienten_lokal = koeffizienten_lokal

    def matches(self, StringFunktion):
        match1 = re.findall(self.pattern1, StringFunktion)
        match2 = re.findall(self.pattern2, StringFunktion)
        match3 = re.findall(self.pattern3, StringFunktion)
        for i in range(len(match2)):  #alle strings aus den Listen werden zu ints
            match2[i] = int(match2[i])
        for i in range(len(match1)):
            match1[i] = int(match1[i])
        for i in range(len(match3)):
            match3[i] = int(match3[i])
        self.parameter.append(match1)
        self.parameter.append(match2)
        self.parameter.append(match3)

    def fallX(self):
        if len(self.parameter[0]) > 0 and len(self.parameter[1]) > 0:
            Fall1().fall1X()
        if len(self.parameter[0]) > 0 and not self.parameter[1]:
            Fall2().fall2X()

    def reset(self):
        self.parameter = []
        self.koeffizienten_lokal = []


class Fall1(Funktionen):
    def __init__(self):
        Funktionen.__init__(self, F.parameter, F.koeffizienten_lokal)

    def fall1X(self):
        for i in range(max(self.parameter[1]) + 1):
            self.koeffizienten_lokal.append(0)  # auffüllen der koeffizienten_lokal mit nullen, falls lücken existieren
        for i in range(len(self.parameter[1])):  # extrahiert alle zahlen aus match3, die in match2 sind
            if self.parameter[1][i] in self.parameter[2]:
                self.parameter[2].remove(self.parameter[1][i])
        for i in range(len(self.parameter[0])):  # extrahiert alle zahlen aus match3, die in match1 sind
            if self.parameter[0][i] in self.parameter[2]:
                self.parameter[2].remove(self.parameter[0][i])
        if len(self.parameter[0]) - len(self.parameter[1]) == 1 and not self.parameter[2]:  #nur +\dx
            Fall11().funktion()
        elif len(self.parameter[0]) - len(self.parameter[1]) == 1 and len(self.parameter[2]) > 0:  #+\dx und +\d
            Fall12().funktion()
        elif len(self.parameter[0]) - len(self.parameter[1]) == 0 and not self.parameter[2]:
            Fall13().funktion()
        elif len(self.parameter[0]) - len(self.parameter[1]) == 0 and len(self.parameter[2]) > 0:
            Fall14().funktion()


class Fall11(Fall1):
    def __init__(self):
        Funktionen.__init__(self, Fall1().parameter, Fall1().koeffizienten_lokal)

    def funktion(self):
        self.koeffizienten_lokal[max(self.parameter[1]) - 1] = self.parameter[0][-1]
        for i in range(len(self.parameter[1])):
            self.koeffizienten_lokal[max(self.parameter[1]) - self.parameter[1][i]] = self.parameter[0][i]
        koeffizienten.append(self.koeffizienten_lokal)


class Fall12(Fall1):
    def __init__(self):
        Funktionen.__init__(self, Fall1().parameter, Fall1().koeffizienten_lokal)

    def funktion(self):
        self.koeffizienten_lokal[len(self.parameter[0])] = self.parameter[2][0]
        self.koeffizienten_lokal[max(self.parameter[1]) - 1] = self.parameter[0][-1]
        for i in range(len(self.parameter[1])):
            self.koeffizienten_lokal[max(self.parameter[1]) - self.parameter[1][i]] = self.parameter[0][i]
        koeffizienten.append(self.koeffizienten_lokal)


class Fall13(Fall1):
    def __init__(self):
        Funktionen.__init__(self, Fall1().parameter, Fall1().koeffizienten_lokal)

    def funktion(self):
        for i in range(len(self.parameter[1])):
            self.koeffizienten_lokal[max(self.parameter[1]) - self.parameter[1][i]] = self.parameter[0][i]
        koeffizienten.append(self.koeffizienten_lokal)


class Fall14(Fall1):
    def __init__(self):
        Funktionen.__init__(self, Fall1().parameter, Fall1().koeffizienten_lokal)

    def funktion(self):
        self.koeffizienten_lokal[max(self.parameter[1])] = self.parameter[2][0]
        for i in range(len(self.parameter[1])):
            self.koeffizienten_lokal[max(self.parameter[1]) - self.parameter[1][i]] = self.parameter[0][i]
        koeffizienten.append(self.koeffizienten_lokal)


class Fall2(Funktionen):
    def __init__(self):
        Funktionen.__init__(self, F.parameter, F.koeffizienten_lokal)

    def fall2X(self):
        for i in range(len(self.parameter[0])):
            if self.parameter[0][i] in self.parameter[2]:
                self.parameter[2].remove(self.parameter[0][i])
        self.koeffizienten_lokal.append(0)
        self.koeffizienten_lokal.append(0)
        if len(self.parameter[2]) > 0:
            Fall21().funktion()
        elif len(self.parameter[2]) == 0:
            Fall22().funktion()


class Fall21(Fall2):
    def __init__(self):
        Funktionen.__init__(self, Fall2().parameter, Fall2().koeffizienten_lokal)

    def funktion(self):
        self.koeffizienten_lokal[1] = self.parameter[2][0]
        self.koeffizienten_lokal[0] = self.parameter[0][0]
        koeffizienten.append(self.koeffizienten_lokal)


class Fall22(Fall2):
    def __init__(self):
        Funktionen.__init__(self, Fall2().parameter, Fall2().koeffizienten_lokal)

    def funktion(self):
        self.koeffizienten_lokal[0] = self.parameter[0][0]
        koeffizienten.append(self.koeffizienten_lokal)


F = Funktionen([], [])


def funktionen():
    while True:
        print("Ohne Eingabe fortfahren, um zu beenden.")
        funktion = str(input("Gebe die Funktionen ein (ENTER nach jeder Eingabe): "))
        if funktion == "":
            break
        else:
            F.matches(funktion)
            F.fallX()
            F.reset()


def wertetabellen():
    SI = int(input("Gebe den Startindex der Wertetabelle ein: "))
    SE = int(input("Gebe den Endindex der Wertetabelle ein: "))
    assert SI < SE, ("Der Startindex muss kleiner als der Endindex sein.")
    argumente = list(range(SI, SE+1))
    v = 0
    wertetabellen = open("Wertetabellen.txt", "w")
    for n in range(len(koeffizienten)):
        werte = [0 for i in range(SI, SE+1)]
        for m in range(SI, SE+1):
            for k in range(0, len(koeffizienten[n])):
                werte[v] += koeffizienten[n][k]*m**(len(koeffizienten[n])-k-1)
            v = v + 1
            if v > len(werte):
                break
        wertetabellen.write("Funktion " + str(n+1) + ": " + str(list(zip(argumente, werte))) + "\n")
        v = 0
    wertetabellen.close()


def nullstellen():
    nullstellen = open("Nullstellen.txt", "w")
    x = sy.S('x')
    for i in koeffizienten:
        gleichung = 0
        for v in range(len(i)):
            gleichung += i[v]*x**(len(i)-v-1)
        nullstellen.write("Die Funktion " + str(koeffizienten.index(i)+1) + " hat die Nullstellen: " + str(sy.solve(sy.Eq(gleichung, 0))) + "\n")
    nullstellen.close()


def vergleich():
    schnittpunkte = open("Schnittpunkte.txt", "w")
    x = sy.S('x')
    gleichungen = []
    for i in koeffizienten:
        gleichung = 0
        for v in range(len(i)):
            gleichung += i[v]*x**(len(i)-v-1)
        gleichungen.append(gleichung)
    for i in range(len(gleichungen[0:-1])):
        for v in gleichungen[i+1:]:
            schnittpunkte.write("Die Funktionen " + str(gleichungen[i]) + " und " + str(v) + " haben die Schnittpunkte: " + str(sy.solve(sy.Eq(gleichungen[i], v))) + "\n")
    schnittpunkte.close()


def ableitungen():
    ableitungen = open("Ableitungen.txt", "w")
    x = sy.S("x")
    for i in koeffizienten:
        gleichung = 0
        for v in range(len(i)):
            gleichung += i[v]*x**(len(i)-v-1)
        ableitungen.write("Die Funktion " + str(koeffizienten.index(i)+1) + " hat die Ableitung: " + str(diff(gleichung, x)) + "\n")
    ableitungen.close()


def integrale():
    integrale = open("Integrale.txt", "w")
    x = sy.S("x")
    for i in koeffizienten:
        gleichung = 0
        for v in range(len(i)):
            gleichung += i[v]*x**(len(i)-v-1)
        integrale.write("Die Funktion " + str(koeffizienten.index(i)+1) + " hat die Stammfunktion: " + str(integrate(gleichung, x)) + "\n")
    integrale.close()


def stop():
        exit()


def userinput():
    if not koeffizienten:
        print("""                                             --- Funktionen-Rechner ---
                             Um alle Möglichkeiten zu nutzen, definiere die Funktionen (!fkt).
                                Gebe !h für die Auflistung der Eingabemöglichkeiten ein.""")
        ui = input(": ")
    else:
        ui = input(": ")
    if ui == "!h":
        hilfe()
    elif ui == "!b":
        stop()
    elif ui == "!fkt":
        funktionen()
    elif ui == "!wt":
        wertetabellen()
    elif ui == "!nt":
        nullstellen()
    elif ui == "!sp":
        vergleich()
    elif ui == "!ab":
        ableitungen()
    elif ui == "!ig":
        integrale()
    else:
        print("Eingabe ist nicht bekannt.")
        return userinput()

while True:
    userinput()
