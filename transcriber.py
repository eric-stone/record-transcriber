import re

# read input file lines into inputFileLines
inputFileLines = []
FILE = "/home/user/HOME/Dropbox/cprCourses.txt"

with open(FILE, "r") as inputFile:
    for line in inputFile:
        line = line.strip()
        # ignore blank lines and comments
        if len(line) > 0 and line[0] is not "#":
            inputFileLines.append(line)


class CprClass:
    def __init__(self):
        mv = "missingValue"
        self.date = mv
        self.startTime = mv
        self.endTime = mv
        self.totalHours = mv
        self.courseType = mv
        self.studentsEnrolled = mv
        self.studentsPassed = mv
        self.instructors = []
        self.classFor = mv
        self.courseOptions = mv

    def time(self, x):
        # make more robust
        if self.startTime == "missingValue" and self.endTime == "missingValue":
            self.startTime = x
        else:
            if int(x) > int(self.startTime):
                self.endTime = x
            else:
                self.endTime = self.startTime
                self.startTime = x

    def addInstructor(self, x):
        self.instructors.append(x)

cprClasses = []

tokenValues = \
    [
        ("date", "^20[0,1][0-9][0,1][0-9][0-3][0-9]$", (lambda x:x)),

        ("time", "^[0,1,2][0-9][0-9][0-9]$", (lambda x:x)),

        ("totalHours", "^[0-9]$", (lambda x:x)),
        ("totalHours", "^[0-9][.][0-9][0-9]*$", (lambda x:x)),

        ("courseType", "^HCP$", (lambda _:"Healthcare Provider")),
        ("courseType", "^H[Ss]F[Aa]$", (lambda _:"Heartsaver First Aid")),
        ("courseType", "^H[Ss]C[Pp][Rr]$", (lambda _:"Heartsaver CPR AED")),
        ("courseType", "^H[Ss]F[Aa]C[Pp][Rr]$", (lambda _:"Heartsaver First Aid CPR AED")),
        ("courseType", "^FF$", (lambda _:"Family and Friends")),

        ("numberOfStudents", "^[0-9]+[/][0-9]+$", (lambda x:(x.split("/")))),

        ("classFor", "^for-.+$", (lambda x:(x.split("for-")[1]))),

        ("courseOptions", "^opt-aci$", (lambda x:"Adult Child Infant")),
        ("courseOptions", "^opt-ac$", (lambda x:"Adult Child")),
        ("courseOptions", "^opt-ai$", (lambda x:"Adult Infant")),
        ("courseOptions", "^opt-a$", (lambda x:"Adult")),

        ("courseOptions", "^opt-r$", (lambda x:"Renewal")),
        ("courseOptions", "^opt-n$", (lambda x:"New")),

        ("instructor", "^inst-.+$", (lambda x:(x.split("inst-")[1]))),
        ]

instructorsAbbr = []
INSTFILE = "/home/user/HOME/Dropbox/cprInstructors.txt"
with open(INSTFILE, "r") as inputFile:
    for line in inputFile:
        line = line.strip()
        # ignore blank lines and comments
        if len(line) > 0 and line[0] is not "#":
            a, b = line.split(",")
            instructorsAbbr.append((a, b))

tokenValues.extend([("instructor", "^"+abr+"$", lambda _, n=name:n) for abr, name in instructorsAbbr])

for line in inputFileLines:
    c = CprClass()
    tokens = [t for t in line.split()]
    tokens = [(num, "unknownType", "unknownValue", item) for num, item in enumerate(tokens)]

    tokens2 = []

    for t in tokens:
        updatedToken = t
        for v in tokenValues:
            if re.match(v[1], t[3]):
                updatedToken = (t[0], v[0], v[2](t[3]), t[3])
        tokens2.append(updatedToken)

    tokens = tokens2

    for t in tokens:
        if t[1] in c.__dict__.keys():
            setattr(c, t[1], t[2])
        if t[2] == "Healthcare Provider":
            c.courseOptions = ""
        if t[1] == "time":
            c.time(t[2])
        if t[1] == "numberOfStudents":
            c.studentsEnrolled = t[2][1]
            c.studentsPassed = t[2][0]
        if t[1] == "instructor":
            c.addInstructor(t[2])
        if t[1] == "unknownType":
            print t
            import sys
            sys.exit("Unknown Token")

    cprClasses.append(c)

dates = [201504, 201503, 201502, 201501]
for year in range(2014, 2011, -1):
    for month in range(12, 00, -1):
        dates.append(int(str(year)+str("%02d" % month)))
print(dates)


classesTaught = []
classDates = []

totalCounts = {}
for d in dates:
    totalCounts[d] = [0, 0]

for c in cprClasses:
    classDates.append(c.date)
    for i in c.instructors:
        classesTaught.append((c.date, i))
    cdate = int(c.date[0:6])
    totalCounts[cdate][0] += 1
    totalCounts[cdate][1] += int(c.studentsPassed)


for _, i in instructorsAbbr:
    print i

    for d in dates:
        days = [k[6:8] for k, l in classesTaught if l == i and k[0:6] == str(d)[0:6]]
        print "     "+str(d)+" | ",
        for m in days:
            print str(m),
        print ""

csvFileFullPath = "/home/user/HOME/Dropbox/cprCourses.csv.text"
with open(csvFileFullPath, "w") as outFile:
    outFile.write("date, startTime, endTime, instructor, classType, classOptions, enrolled, passed, hours, classFor\n")

    outFileLine = ""
    for c in cprClasses:
        for i in c.instructors:
            outFileLine += c.date[0:4]+"-"+c.date[4:6]+"-"+c.date[6:8]+", "
            outFileLine += c.startTime+", "
            outFileLine += c.endTime+", "
            outFileLine += i+", "
            outFileLine += c.courseType+", "
            outFileLine += c.courseOptions+", "
            outFileLine += c.studentsEnrolled+", "
            outFileLine += c.studentsPassed+", "
            outFileLine += c.totalHours+", "
            outFileLine += c.classFor if c.classFor != "missingValue" else "" + ""

            outFileLine += "\n"

    outFileLine = outFileLine.replace("missingValue", "")
    outFile.write(outFileLine)

# classes per month
print ""
print "Classes per Month"
for d in dates:
    print "     "+str(d)+" | ",
    print " "+str(totalCounts[d][0]),
    print ""

print ""
print "Classes per Month"
for d in dates:
    print "     "+str(d)+" | ",
    for _ in range(0, totalCounts[d][0]/1):
        print "#",
    print ""


# students per month
print ""
print "Students per Month"
for d in dates:
    print "     "+str(d)+" | ",
    print ""+str(totalCounts[d][1]),
    print ""

print ""
print "Students per Month"
for d in dates:
    print "     "+str(d)+" | ",
    for _ in range(0, totalCounts[d][1]/10):
        print "#",
    print ""
