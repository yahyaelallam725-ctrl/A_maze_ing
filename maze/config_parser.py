# from errors import ParseError, ValidationError
from maze.errors import ParseError, ValidationError


class MazeConfig:
    def __init__(self, file_name: str) -> None:
        self.file_name = file_name
        self.width = None
        self.height = None
        self.entry = None
        self.exit = None
        self.output_file = None
        self.perfect = None

    def read_file(self) -> list:
        try:
            with open(f"{self.file_name}","r") as file :
                data = file.read()
                list_data = data.split("\n")
                return list_data
        except FileNotFoundError as e :
            print(f"Error : {e}")
            exit()


    def parse(self,list_data : list) -> dict:
        dic_data ={}
        for elm in list_data:
            if elm == "" or  elm.strip().startswith("#"):
                continue
            if "=" in elm:
                elemnt = elm.split("=")
                if len(elemnt) != 2:
                    raise ParseError("data not valide")
                key = elemnt[0].strip()
                value = elemnt[1].strip()
            else :
                raise ParseError("'=' NOT FOND")
            if key in dic_data.keys():
                raise ParseError("key is deplicate")
            if key == "WIDTH" or key == "HEIGHT" :
                dic_data[key] = int(value)
            
            elif key == "EXIT" or key == "ENTRY":
                if ',' not in value  :
                    raise ParseError("you must enter valid coordinates")
                coordonee = value.strip().split(",")
                if len(coordonee) != 2:
                    raise ParseError("tuple not valide")
                x,y = coordonee[0] ,coordonee[1]
                corr_point =(int(x),int(y))
                dic_data[key] = corr_point
            elif key == "PERFECT":
                if value == "True":
                    dic_data[key] = True
                elif value == "False":
                    dic_data[key] = False
                else:
                    raise ParseError("enter True or False")
            else:
                dic_data[key] = value
        return dic_data


    def validate(self, data_dic: dict) -> bool:
        keys = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]
        keys_dic = data_dic.keys()
        for elm in keys:
            if elm not in keys_dic:
                raise ValidationError("key not fond")
        width = data_dic["WIDTH"]
        height = data_dic["HEIGHT"]
        entry = data_dic["ENTRY"]
        exit_ = data_dic["EXIT"]
        if width <= 0 or height <= 0:
            raise ValidationError("width or height is not valid")
        entry_x, entry_y = entry
        exit_x, exit_y = exit_
        if not (0 <= entry_x < width and 0 <= entry_y < height):
            raise ValidationError("ENTRY is outside maze bounds")
        if not (0 <= exit_x < width and 0 <= exit_y < height):
            raise ValidationError("EXIT is outside maze bounds")
        if entry == exit_:
            raise ValidationError("ENTRY and EXIT must be different")
        return True


    def load(self) -> None:
        try :
            firstdata_list = self.read_file()
            data_parse = self.parse(firstdata_list)
            self.validate(data_parse)
            self.width = data_parse["WIDTH"]
            self.height = data_parse["HEIGHT"]
            self.entry = data_parse["ENTRY"]
            self.exit = data_parse["EXIT"]
            self.output_file = data_parse["OUTPUT_FILE"]
            self.perfect = data_parse["PERFECT"]
        except (ParseError , ValueError, ValidationError) as e: 
            print(e)
            exit()