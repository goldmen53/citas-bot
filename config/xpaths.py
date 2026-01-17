"""
XPath'ы и селекторы для всех типов виз.
Централизованное хранилище адресов элементов на сайте.
"""

# Базовый URL испанского сервиса для всех типов виз
START_URL = "https://icp.administracionelectronica.gob.es/icpco/index"

XPATHS = {
    # Общие элементы (для всех типов виз)
    'common': {
        'cookie_close': '//*[@id="cookie_action_close_header"]',
        'exit_button': '//*[@id="btnSalir"]',
        'error_message': '//*[@id="mainWindow"]/div/div[2]/section/div[2]/form/div[1]/p',
    },
    
    # НИЕ с указанным регионом (специализированная виза)
    'nie_specified': {
        'form': '//*[@id="form"]',
        'province_dropdown': '//*[@id="form"]',  # Выбор провинции через форму
        'accept_button': '//*[@id="btnAceptar"]',
        'office_dropdown': '//*[@id="sede"]',
        'service_dropdown': '//*[@id="tramiteGrupo[1]"]',
        'enter_button': '//*[@id="btnEntrar"]',
        'person_type_radio': '//*[@id="comp04_id_citado"]/div[1]/fieldset/ul/li[2]/label',
        'passport_input': '//*[@id="txtIdCitado"]',
        'name_surname_input': '//*[@id="txtDesCitado"]',
        'birth_year_input': '//*[@id="txtAnnoCitado"]',
        'submit_button': '//*[@id="btnEnviar"]',
        'available_citations': '//*[@id="cita_"]',  # Базовый ID для поиска цитат
    },
    
    # НИЕ национальный (без привязки к региону)
    'nie_national': {
        'form': '//*[@id="form"]',
        'accept_button': '//*[@id="btnAceptar"]',
        'service_dropdown': '//*[@id="tramiteGrupo[1]"]',
        'enter_button': '//*[@id="btnEntrar"]',
        'person_type_radio': '//*[@id="comp04_id_citado"]/div[1]/fieldset/ul/li[2]/label',
        'passport_input': '//*[@id="txtIdCitado"]',
        'name_surname_input': '//*[@id="txtDesCitado"]',
        'birth_year_input': '//*[@id="txtAnnoCitado"]',
        'submit_button': '//*[@id="btnEnviar"]',
    },
    
    # ТИЕ (другой тип визы)
    'tie': {
        'form': '//*[@id="form"]',
        'accept_button': '//*[@id="btnAceptar"]',
        'service_dropdown': '//*[@id="tramiteGrupo[1]"]',
        'enter_button': '//*[@id="btnEntrar"]',
    },
}


def get_xpaths(visa_type: str) -> dict:
    """
    Получить XPath'ы для типа визы.
    
    Args:
        visa_type: Тип визы ('nie_specified', 'nie_national', 'tie')
    
    Returns:
        Словарь XPath'ов (специфичные + общие элементы)
    """
    xpaths = XPATHS.get(visa_type, {}).copy()
    xpaths.update(XPATHS['common'])  # Добавить общие элементы
    return xpaths
