
'''
    Contains recursive methods that unfold json objects
'''


def unfold_list(base_key, l):
    new_dict = dict()
    for i, val in enumerate(l):
        if isinstance(val, dict):
            new_k = base_key + '_' + str(i)
            new_dict.update(unfold(new_k, val))
        else:
            new_dict[base_key] = l
    return new_dict


def unfold(base_key, d):
    new_dict = dict()

    for k in d:
        new_k = base_key + '_' + k
        if isinstance(d[k], dict):
            new_dict.update(unfold(new_k, d[k]))
        elif isinstance(d[k], list):
            new_dict.update(unfold_list(new_k, d[k]))
        else:
            new_dict[new_k] = d[k]
    return new_dict


# =======================TEST==================================


def test():
    values = {'id': '/2048221/KA_24174_4', 'completeness': 5, 'country': ['netherlands'], 'europeanaCollectionName': ['2048221_Ag_EU_EuropeanaFashion_1040'], 'edmConceptPrefLabelLangAware': {'de': ['Seide', 'Stoffprobe', 'Tücher'], 'sv': ['provbit', 'siden', 'scarf'], 'pt': ['lenço (acessórios de traje)', 'seda'], 'el': ['swatch', 'μετάξι', 'φουλάρι'], 'en': ['silk', 'swatch', 'scarf (costume accessory)'], 'it': ['campione', 'seta', 'sciarpa'], 'fr': ['écharpe', 'échantillon', 'soie'], 'he': ['דוגמת אריג', 'צעיף', 'משי'], 'es': ['bufanda', 'seda', 'muestra de tejido'], 'nl': ['sjaal', 'zijde', 'staaltje'], 'sr': ['svila', 'uzorak', 'šal']}, 'edmConcept': ['http://thesaurus.europeanafashion.eu/thesaurus/10352', 'http://thesaurus.europeanafashion.eu/thesaurus/10618', 'http://thesaurus.europeanafashion.eu/thesaurus/10177'], 'edmConceptLabel': [{'def': 'Seide'}, {'def': 'Stoffprobe'}, {'def': 'Tücher'}, {'def': 'siden'}, {'def': 'provbit'}, {'def': 'scarf'}, {'def': 'seda'}, {'def': 'lenço (acessórios de traje)'}, {'def': 'μετάξι'}, {'def': 'swatch'}, {'def': 'φουλάρι'}, {'def': 'silk'}, {'def': 'swatch'}, {'def': 'scarf (costume accessory)'}, {'def': 'seta'}, {'def': 'campione'}, {'def': 'sciarpa'}, {'def': 'soie'}, {'def': 'échantillon'}, {'def': 'écharpe'}, {'def': 'משי'}, {'def': 'דוגמת אריג'}, {'def': 'צעיף'}, {'def': 'seda'}, {'def': 'muestra de tejido'}, {'def': 'bufanda'}, {'def': 'zijde'}, {'def': 'staaltje'}, {'def': 'sjaal'}, {'def': 'svila'}, {'def': 'uzorak'}, {'def': 'šal'}], 'edmDatasetName': [
        '2048221_Ag_EU_EuropeanaFashion_1040'], 'title': ["Stalenset 'Twill Silk, Hendred'"], 'dcDescription': ['Stalen hebben een grijs kartonnen omslag en zijn gelijmd'], 'europeanaCompleteness': 5, 'dataProvider': ['Amsterdam Museum'], 'rights': ['http://rightsstatements.org/vocab/InC/1.0/'], 'edmIsShownAt': ['http://www.europeana.eu/api/vHHKYVjNU/redirect?shownAt=http%3A%2F%2Fhdl.handle.net%2F11259%2Fcollection.80673&provider=Europeana+Fashion&id=http%3A%2F%2Fwww.europeana.eu%2Fresolve%2Frecord%2F2048221%2FKA_24174_4&profile=standard'], 'dcCreator': ['Metz & Co', 'Liberty & Co'], 'edmPreview': ['https://www.europeana.eu/api/v2/thumbnail-by-url.json?uri=http%3A%2F%2Frepos.europeanafashion.eu%2Fext2%2FAmsterdam%2520Museum%2Fa0%2Fa018ecd459555feac6fb01d930fc07c8.jpg%3Fthumb%3Dvertical&size=LARGE&type=IMAGE'], 'previewNoDistribute': False, 'dcTitleLangAware': {'def': ["Stalenset 'Twill Silk, Hendred'"]}, 'dcCreatorLangAware': {'def': ['Metz & Co', 'Liberty & Co']}, 'provider': ['Europeana Fashion'], 'timestamp': 1502191803171, 'score': 1.3905964, 'language': ['nl'], 'type': 'IMAGE', 'guid': 'http://www.europeana.eu/portal/record/2048221/KA_24174_4.html?utm_source=api&utm_medium=api&utm_campaign=vHHKYVjNU', 'link': 'http://www.europeana.eu/api/v2/record/2048221/KA_24174_4.json?wskey=vHHKYVjNU', 'timestamp_created_epoch': 1427807058894, 'timestamp_update_epoch': 1502191154613, 'timestamp_created': '2015-03-31T13:04:18.894Z', 'timestamp_update': '2017-08-08T11:19:14.613Z'}

    res = unfold('item', values)

    for k in res:
        print(k, '\t\t\t\t', res[k])


# test()
