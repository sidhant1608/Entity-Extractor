
# coding: utf-8

# In[95]:
import pandas as pd
grid = pd.read_csv("grid.csv")

def process_string(string):
    uni = ['universiteit', 'جامعة', 'universitet', 'універсітэт', 'университет', 'বিশ্ববিদ্যালয়', 'univerzitet', 'universitat', 'unibersidad', 'univerzita', 'prifysgol', 'universitet', 'Universität', 'πανεπιστήμιο', 'university', 'university', 'Universidad', 'ülikool', 'unibertsitate', 'دانشگاه', 'yliopisto', 'Université', 'ollscoil', 'universidade', 'યુનિવર્સિટી', 'jami&#39;a', 'विश्वविद्यालय', 'university', 'sveučilište', 'inivèsite', 'egyetemi', 'համալսարան', 'Universitas', 'mahadum', 'háskóli', 'Università', 'אוּנִיבֶרְסִיטָה', '大学', 'universitas', 'უნივერსიტეტი', 'университет', 'សាកលវិទ្យាល័យ', 'ವಿಶ್ವವಿದ್ಯಾಲಯ', '대학', 'university', 'ວິທະຍາໄລ', 'universitetas', 'universitāte', 'anjerimanontolo', 'whare wānanga', 'универзитет', 'സർവ്വകലാശാല', 'их сургууль', 'विद्यापीठ', 'universiti', 'università', 'တက္ကသိုလ်', 'विश्वविद्यालय', 'Universiteit', 'universitet', 'yunivesite', 'ਯੂਨੀਵਰਸਿਟੀ', 'Uniwersytet', 'universidade', 'universitate', 'Университет', 'විශ්ව විද්යාලය', 'univerzitnú', 'univerza', 'jaamacad', 'universitet', 'универзитет', 'univesithi', 'unipersitas', 'universitet', 'chuo kikuu', 'பல்கலைக்கழக', 'విశ్వవిద్యాలయ', 'донишгоҳ', 'มหาวิทยาลัย', 'unibersidad', 'Üniversite', 'університет', 'جامع درس گاہ', 'universitet', 'trường đại học', 'אוניווערסיטעט', 'ile-ẹkọ giga', '大学', '大学', '大學', 'yunivesithi']
    return_dict = {}
    work = string.replace('\r', ' ').replace('\n', ' ')
    place = work.split(',')
    places = []
    for place in place:
        if ';' not in place:
            places.append(place)
        else:
            for item in place.split(';'):
                places.append(item)
    #print(places.address_strings)
    dept = ''
    school = ''
    univ = ''
    external = ''
    orgs = []
    for i in places:
        if ('Ministry' in i) or ('Inc' in i) or ('Agency' in i) or ('Limited' in i) or ('Unit' in i) or ('Ltd' in i) or ('Headquarters' in i) or ('Hospital' in i) or ('Institute' in i) or ('Department' in i) or ('University' in i) or ('School' in i) or ('College' in i) or ('Laboratory' in i) or ('Center' in i) or ('Team' in i) or ('Lab' in i) or ('Division' in i) or ('Group' in i) or ('Academy' in i) or ('Faculty' in i) or ('Instituto' in i) or ('Universidad' in i):
            orgs.append(i)
        for uni in uni:
            if uni in i:
                orgs.append(i)
    orgs = list(set(orgs))
    if len(orgs) != 0:
        location_str = ''
        for item in orgs:
            location_str += item
            location_str += ', '
        location_str = location_str[:-2]
        return_dict['organization'] = location_str
    else: return_dict['organization'] = None
    unit = 0
    for item in orgs:
        if ('Unit' in item) or ('Department' in item)  or ('Faculty' in item) or ('Dept' in item) or ('Team' in item) or ('Laboratory' in item) or ('Lab' in item) or ('Division' in item) or ('Group' in item):
            if dept == '':
                dept = item
            else:
                dept += dept+', '+item
        if ('College' in item) or ('School' in item) or ('Center' in item):
            if school == '':
                school = item
            else: school = school+', '+item
        if ('University' in item) or ('Institute' in item) or ('Hospital' in item) or ('Academy' in item) or ('Instituto' in item) or ('Universidad' in item):
            if univ == '':
                univ = item
            else: univ = univ+', '+item
        if ('Ltd' in item) or ('Headquarters' in item) or ('Limited' in item) or ('Agency' in item) or ('Corporation' in item) or ('Ministry' in item):
            if external == '' and unit >= 1:
                if item.strip() == 'Ltd.' or item.strip == 'Ltd' or item.strip == 'Limited':
                    external = orgs[unit - 1] +' '+item.strip()
                else: external = item
            else: external = external+', '+item
        unit += 1
    if dept == '': dept = "Not found"
    if univ == '':
        found = False
        for uni in uni:
           for i in places:
               if uni in i:
                univ += i
                univ += ', '
                univ = univ[:-2]
                found = True
        if found == False: univ = 'Not found'

        # if ',' in univ:
        #     abc = univ.split(',')
        #     school = abc[0]
        #     univ = ''
        #     for a in abc[1:]:
        #         univ += a
        #         univ += ', '
        #         univ = univ[:-2]
        # else: school = 'Not found'
    wok = univ.strip().rstrip()
    places = wok.split(',')
    result = False
    for place in places:
        a = grid[grid["Name"] == place]
        if len(a.Name) > 0:
            result = True
            return_dict['country'] = list(a.Country)[0]
            return_dict['city'] = list(a.City)[0]
        if result == True:
            break
    if result == False:
        for uni in grid['Name']:
            if uni in wok:
                a = grid[grid['Name'] == uni]
                return_dict['country'] = list(a.Country)[0]
                return_dict['city'] = list(a.City)[0]
                result = True
                break
    if result == False:
        return_dict['country'] = None
        return_dict['city'] = None
    if school == '':
        # school = 'Not found'
        if ',' in univ:
            abc = univ.split(',')
            school = abc[0]
            univ = ''
            for a in abc[1:]:
                univ += a
                univ += ', '
                univ = univ[:-2]
        else: school = 'Not found'
    if external == '': external = 'Not found'
    external = external.strip('').strip(' ')
    if external == 'Not found':
        external = None
    return_dict['external'] = external
    department = dept.strip('').strip(' ')
    if(department == 'Not found'):
        department = None
    return_dict['department'] = department
    school = school.strip('').strip(' ')
    if school == 'Not found':
        school = None
    return_dict['school'] = school
    university = univ.strip('').strip(' ')
    if university == 'Not found':
        university = None
    return_dict['university'] = university
    return_dict (return_dict)

