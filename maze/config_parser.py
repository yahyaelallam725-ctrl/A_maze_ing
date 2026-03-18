from maze.errors import ParseError, ValidationError

class MazeConfig:
    def __init__(self, file_name: str) -> None:
        self.file_name: str = file_name
        self.width: int = 0
        self.height: int = 0
        self.entry: tuple[int, int] = (0, 0)
        self.exit: tuple[int, int] = (0, 0)
        self.output_file: str = ""
        self.perfect: bool = True
        self.seed: int | None = None

    def read_file(self) -> list[str]:
        """Reads file content using context manager for safe handling."""
        try:
            with open(self.file_name, "r") as file:
                data = file.read()
                return data.split("\n")
        except FileNotFoundError:
            raise ParseError(f"Configuration file '{self.file_name}' not found.")

    def parse(self, list_data: list[str]) -> dict:
        dic_data = {}
        mandatory_keys = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]
        
        for line_no, elm in enumerate(list_data, 1):
            elm = elm.strip()
            if elm == "" or elm.startswith("#"):
                continue
            
            if "=" not in elm:
                raise ParseError(f"Line {line_no}: '=' NOT FOUND")
            
            element = elm.split("=", 1)
            key = element[0].strip().upper()
            value = element[1].strip()

            if key in dic_data:
                raise ParseError(f"Line {line_no}: key '{key}' is duplicate")

            # تخزين البيانات
            if key in ["WIDTH", "HEIGHT", "SEED"]:
                try:
                    dic_data[key] = int(value)
                except ValueError:
                    raise ParseError(f"Line {line_no}: {key} must be an integer")
            
            elif key in ["ENTRY", "EXIT"]:
                if ',' not in value:
                    raise ParseError(f"Line {line_no}: Invalid coordinates format for {key}")
                coord = value.split(",")
                if len(coord) != 2:
                    raise ParseError(f"Line {line_no}: {key} must be x,y")
                try:
                    dic_data[key] = (int(coord[0].strip()), int(coord[1].strip()))
                except ValueError:
                    raise ParseError(f"Line {line_no}: Coordinates must be integers")
            
            elif key == "PERFECT":
                if value.lower() == "true":
                    dic_data[key] = True
                elif value.lower() == "false":
                    dic_data[key] = False
                else:
                    raise ParseError(f"Line {line_no}: PERFECT must be True or False")
            else:
                dic_data[key] = value
                   
        return dic_data

    def validate(self, data_dic: dict) -> bool:
        mandatory = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]
        for key in mandatory:
            if key not in data_dic:
                raise ValidationError(f"Mandatory key '{key}' not found in configuration")

        width = data_dic["WIDTH"]
        height = data_dic["HEIGHT"]
        entry = data_dic["ENTRY"]
        exit_pt = data_dic["EXIT"]

        if width <= 0 or height <= 0:
            raise ValidationError("WIDTH and HEIGHT must be positive integers")

        # فحص الحدود
        if not (0 <= entry[0] < width and 0 <= entry[1] < height):
            raise ValidationError(f"ENTRY {entry} is outside maze bounds")

        if not (0 <= exit_pt[0] < width and 0 <= exit_pt[1] < height):
            raise ValidationError(f"EXIT {exit_pt} is outside maze bounds")

        if entry == exit_pt:
            raise ValidationError("ENTRY and EXIT must be different")
            
        return True

    def load(self) -> None:
        try:
            firstdata_list = self.read_file()
            data_parse = self.parse(firstdata_list)
            self.validate(data_parse)

            self.width = data_parse["WIDTH"]
            self.height = data_parse["HEIGHT"]
            self.entry = data_parse["ENTRY"]
            self.exit = data_parse["EXIT"]
            self.output_file = data_parse["OUTPUT_FILE"]
            self.perfect = data_parse["PERFECT"]
            self.seed = data_parse.get("SEED")

        except (ParseError, ValueError, ValidationError) as e: 
            print(f"Configuration Error: {e}")
            exit()

