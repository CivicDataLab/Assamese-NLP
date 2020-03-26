import re
class as2en:
    
    # dictionary of vowels
    __vowels = {
        u'অ': 'a', u'আ': 'a', u'ই': 'i', u'ঈ': 'i', u'উ': 'u',
        u'ঊ': 'u', u'এ': 'e', u'ঐ': 'ai', u'ও': 'o', u'ঔ': 'au', u'ঋ': 'ri', u'ৠ': 'ri', u'ঌ': 'li', 
        u'ৡ': 'li', 'শ': 'x', 'ষ': 'x', u'স': 'x', u'ಂ': 'm', u'ಃ': 'ah'
        }
    
    # dictionary of consonants
    __consonants= {
        u'ক': 'k', u'খ': 'kh', u'গ': 'g', u'ঘ': 'gh', u'ঙ': 'ng',
        u'চ': 'ch', u'ছ': 'chh', u'জ': 'j', u'ঝ': 'jhh', u'ঞ': 'nj',
        u'ট': 't', u'ঠ': 'th', u'ড': 'd', u'ঢ': 'dh', u'ণ': 'n',
        u'ত': 't', u'থ': 'thh', u'দ': 'd', u'ধ': 'dh', u'ন': 'n',
        u'প': 'p', u'ফ': 'ph', u'ব': 'b', u'ভ': 'bh', u'ম': 'm',
        u'য': 'y', u'ৰ': 'r', u'ল': 'l', u'ৱ': 'v', u'শ': 'sh',
        u'ষ': 'shh', u'হ': 'h', u'খ়': 'kh', u'গ়': 'g',
        u'জ়': 'z', u'ড়': 'r', 'ঢ়': 'rh', u'ফ়': 'f', u'য়': 'y',
        u'ত়': 't', u'স়': 's', u'হ়': 'h', u'র': 'w'
    }

    # dictionary of conjunct consonants
    __compounds = {
        u'ক্ক': 'kk', u'ঙ্ক': 'ngk', u'ল্ক': 'lk', u'স্ক': 'sk', u'স্ফ': 'sph',
        u'ঙ্খ': 'ngkh', u'স্খ': 'skh', u'ঙ্গ': 'ngg', u'ঙ্ঘ': 'nggh', u'দ্ঘ': 'dgh',
        u'শ্চ': 'ss', u'চ্ছ': 'ssh', u'ঞ্ছ': 'nsh', u'ঞ্জ': 'nz', u'জ্ঞ': 'zn',
        u'ল্ট': 'lt', u'ণ্ঠ': 'nth', u'ষ্ঠ': 'sth', u'ণ্ড': 'nd', u'ষ্ণ': 'sn',
        u'ক্ষ': 'ks', u'প্ত': u'pt', u'স্ত': 'st', u'ক্ত': 'kt', u'গ্ন': 'gn',
        u'ম্ন': 'mn', u'শ্ন': 'sn', u'স্ন': 'sn', u'হ্ন': 'hn', u'ত্থ': 'tth', u'ন্থ': 'nth',
        u'ষ্থ': 'sth', u'ন্দ': 'nd', u'ব্দ': 'bd', u'ম্প': 'mp', u'ল্প': 'lp', 'ষ্প': 'sp',
        u'স্প': 'sp', u'ম্ফ': 'mph', u'স্ফ': 'sph', u'দ্ব': 'db', u'ম্ব': 'mb', u'হ্ব': 'hb',
        u'দ্ভ': 'dbh', u'ম্ভ': 'mbh', u'ক্ম': 'km', u'দ্ম': 'dm', u'হ্ম': 'hm', u'ম্ম': 'mm', 'স্ব': 's',
        u"দ্ধ": 'ddh'
    
    }

    # dictionary of modifiers
    __modifiers = {u'ৌ': 'au', u'ৈ': 'ai', u'া': 'a', u'ী': 'i', u'ি': 'i',
        u'ূ': 'uu', u'ো': 'o', u'ে': 'e', u'ু': 'u', 
        u'ঁ': 'n', u'।': '.', u'ঃ': 'h'}

    
    def _modifiedGlyphs(self, glyphs, _input):
        """
        Takes in glyphs and the input. 
        Returns the roman equivalent 
        """
        # see if a given set of glyphs have modifiers trailing them
        exp = re.compile( '((' + '|'.join(glyphs.keys()) + ')(' + '|'.join(self.__modifiers.keys()) + '))' )
        # print(exp)
        matches = exp.findall(_input)
        # if yes, replace the glpyh with its roman equivalent, and the modifier with it
        if matches != None:
            for match in matches:
                _input = _input.replace( match[0], glyphs[match[1]] + self.__modifiers[match[2]])
        return _input
    
    def transliterate(self, _input):
        """
        Takes in the input 
        Returns the roman equivalent according to defined custom rules
        """
        _input = re.sub(r'\xE2\x80\x8C', '', _input)
        consonants = self.__consonants
        vowels = self.__vowels
        input_list = []

        for i in _input.split():
            if i[-1] in consonants.keys() and len(i) > 1 and i[-1] != 'ব':
                input_list.append(i.replace(i[-1], consonants[i[-1]]))
            else:
                input_list.append(i)

        _input = ' '.join(input_list)
        _input = self._modifiedGlyphs(self.__compounds, _input)
        _input = self._modifiedGlyphs(self.__vowels, _input)
        _input = self._modifiedGlyphs(self.__consonants, _input)

        for k, v in self.__compounds.items():
            _input = _input.replace( k, v)

        for k, v in self.__consonants.items():
            # append 'o' to all the roman equivalent compounds
            _input = _input.replace(k, consonants[k] + 'o')

        for k, v in self.__vowels.items():
            _input = _input.replace(k, v + 'o')

        for k, v in self.__modifiers.items():
            _input = _input.replace(k, v)
        return _input

        
if __name__ == '__main__':
    x = as2en()
    _input = u"পৰিত্যক্ত সম্পত্তি"
    print(x.transliterate(_input))