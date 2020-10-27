import IP2Location
import os
database = IP2Location.IP2Location(os.path.join("ip2loc.BIN"))

rec = database._dbcolumn
print(rec)