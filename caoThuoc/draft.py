set = ['Mỗi 1g chứa: ', ' 25 mg; Prilocain 25 mg ']

set2 = ['Trong một viên Bioeunice Eunice có chứa các thành phần:\r\n\r\n',
 '..…………10^6 CFU;\r\nBacillus subtilis…………………….10^6 CFU;\r\nStreptococus faecalis……………….10^6 CFU;\r\nEnzym Amylase………………………… 50 UI;\r\nEnzym Protease………………………….50 UI;\r\n',
 '………………………………………………..50 mg;\r\n',
 '………………………………………….50 mg\r\n',
 ' gluconate……………………….…….1mg;\r\nCao men bia………………………………………100 mg; ']

set3 = [' hydrocloride 10mg/g ']
set4 = [' 20mg; ']

# def extract_components(set):
#         components = []
#         component = None

#         if not set:
#                 return []

#         for i in set:
#                 # if len(set) > 1: 
#                 #         set.remove(set[0])

#                 lines = i.split(';')
#                 for line in lines:
#                         if not line.strip('.') or ':' in line:
#                                 continue
#                         cleaned_line = line.replace('…', '').replace('.', '')

#                         if cleaned_line[0].isdigit(): 
#                                 continue

#                         num_start = None
#                         for j, char in enumerate(cleaned_line):
#                                 if char.isdigit():
#                                         num_start = j
#                                         # if cleaned_line[j - 1] != ' ':
#                                         #         cleaned_line = cleaned_line[:(j-1)] + cleaned_line[j-1] + ' ' + cleaned_line[j:]
#                                         break

#                         print(cleaned_line)
#                         if num_start is not None:
#                                 component = cleaned_line.strip()
#                                 components.append(component)
#                         if component == '':
#                                 components.remove(component)
#         return components

set4 = [' 20mg; ']
def extract_components(set):
        components = []
        component = None

        if not set:
                return []

        for i in set:
                # if len(set) > 1: 
                #         set.remove(set[0])

                lines = i.split(';')
                for line in lines:
                        if not line.strip('.') or ':' in line:
                                continue
                        cleaned_line = line.replace('…', '').replace('.', '')
                        if cleaned_line[0].isdigit(): 
                                continue
                        num_start = None
                        for j, char in enumerate(cleaned_line):
                                if char.isdigit():
                                        num_start = j
                                        break

                        if num_start is not None:
                                component = cleaned_line[:num_start].strip()
                                if component :
                                      components.append(component)
        return components


def extract_components_2(lines):
    components = []

    for item in lines:
        # Split by semicolon (in case multiple components)
        parts = item.split(';')
        print(parts)
        for part in parts:
            part = part.strip().replace('…', '').replace('.', '')
            print(part)
            if not part:
                continue

            # Find where the first number appears
            for i, char in enumerate(part):
                if char.isdigit():
                    name = part[:i].strip()
                    if name:
                        components.append(name)
                    break  # Done with this part
    return components

def extract_components_official(set):
        components = []
        component = None

        if not set:
                return []

        for i in set:
                # if len(set) > 1: 
                #         set.remove(set[0])

                lines = i.split(';')
                for line in lines:
                        if not line.strip('.') or ':' in line:
                                continue
                        cleaned_line = line.replace('…', '').replace('.', '')
                        if cleaned_line[0].isdigit(): 
                                continue
                        num_start = None
                        for j, char in enumerate(cleaned_line):
                                if char.isdigit():
                                        num_start = j
                                        break

                        if num_start is not None:
                            component = cleaned_line[:num_start].strip()
                            if component:
                                components.append(component)
        return components



print(extract_components_2(set2))