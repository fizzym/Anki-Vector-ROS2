def read_ini_file(path):
    f = open(path,"r")
    lines = f.readlines()
    serial = lines[0].strip().split("[")[-1].split("]")[0]
    cert = lines[1].strip().split("cert = ")[-1]
    ip = lines[2].strip().split("ip = ")[-1]+":443"
    name = lines[3].strip().split("name = ")[-1]
    guid = lines[4].strip().split("guid = ")[-1]
    return serial, cert, ip, name, guid