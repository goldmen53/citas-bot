"""
═══════════════════════════════════════════════════════════════════════════════
ANTI-BLOCKING MODULE
═══════════════════════════════════════════════════════════════════════════════
Ported from v1.0-legacy/main.py
Handles detection and recovery from Spanish site blocking
═══════════════════════════════════════════════════════════════════════════════
"""

import time
import logging
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException

logger = logging.getLogger(__name__)


class RestartLoopException(Exception):
    """Exception raised when blocking detected - signals to restart search loop"""
    pass


def guard_blocking_states(driver, start_url, timeout=5):
    """
    Detect blocking states from Spanish site and handle recovery.
    
    Blocking states detected:
    1. "[Go Back]" link at /html/body/a - Request Rejected (waits 610 sec)
    2. "Too Many Requests" h1 at /html/body/h1 - 429 error (waits 310 sec)
    3. HTML size < 1000 bytes - Indicates blocking response
    
    Args:
        driver: Selenium WebDriver instance
        start_url: URL to reconnect to (https://icp.administracionelectronica.gob.es/icpco/index)
        timeout: timeout for element detection (default 5 sec)
    
    Returns:
        bool: True if blocking detected and recovered, False if no blocking
    
    Raises:
        RestartLoopException: Signal to caller to restart the search loop
    """
    
    # Check 1: "[Go Back]" - Request Rejected Page
    try:
        back_element = driver.find_element(By.XPATH, '/html/body/a')
        if back_element.text.strip() == '[Go Back]':
            logger.warning('[BLOCK] Request rejected (403) → waiting 610s before reconnect')
            time.sleep(610)
            
            logger.info('[BLOCK] Reopening start page after rejection block')
            driver.get(start_url)
            return True
    except NoSuchElementException:
        pass
    except Exception as e:
        logger.debug(f'[BLOCK] Error checking Go Back element: {e}')
    
    # Check 2: "Too Many Requests" - HTTP 429
    try:
        h1_element = driver.find_element(By.XPATH, '/html/body/h1')
        if h1_element.text.strip() == 'Too Many Requests':
            logger.warning('[BLOCK] Too Many Requests (429) → waiting 310s before reconnect')
            time.sleep(310)
            
            logger.info('[BLOCK] Reopening start page after 429 block')
            driver.get(start_url)
            return True
    except NoSuchElementException:
        pass
    except Exception as e:
        logger.debug(f'[BLOCK] Error checking Too Many Requests: {e}')
    
    # Check 3: HTML size < 1000 bytes - Likely blocking response
    try:
        page_source = driver.page_source
        if len(page_source) < 1000:
            logger.warning(f'[BLOCK] Minimal HTML response ({len(page_source)} bytes) → waiting 300s')
            time.sleep(300)
            
            logger.info('[BLOCK] Reopening start page after minimal response block')
            driver.get(start_url)
            return True
    except Exception as e:
        logger.debug(f'[BLOCK] Error checking HTML size: {e}')
    
    return False


def wait_clickable(driver, by, value, timeout=30):
    """
    Wait for element to be clickable.
    
    Args:
        driver: Selenium WebDriver instance
        by: Selenium By locator type (By.XPATH, By.ID, etc)
        value: Locator value (XPath string, ID, etc)
        timeout: Maximum wait time in seconds
    
    Returns:
        WebElement: The clickable element
    
    Raises:
        TimeoutException: If element not clickable within timeout
    """
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((by, value))
    )


def safe_wait_clickable(driver, start_url, by, value, timeout=30):
    """
    Safely wait for element to be clickable with blocking detection.
    
    If blocking is detected during wait, raises RestartLoopException
    to signal caller to restart the search loop.
    
    Args:
        driver: Selenium WebDriver instance
        start_url: URL for reconnection if needed
        by: Selenium By locator type
        value: Locator value
        timeout: Maximum wait time
    
    Returns:
        WebElement: The clickable element
    
    Raises:
        RestartLoopException: If blocking detected during wait
        TimeoutException: If element not clickable within timeout
    """
    
    # Check for blocking before attempting wait
    if guard_blocking_states(driver, start_url, timeout=3):
        logger.warning('[WAIT] Blocking detected, restarting search loop')
        raise RestartLoopException('Blocking detected during wait_clickable')
    
    try:
        return wait_clickable(driver, by, value, timeout)
    except TimeoutException:
        logger.error(f'[TIMEOUT] Element not clickable: {value}')
        # Check blocking as cause of timeout
        if guard_blocking_states(driver, start_url, timeout=3):
            raise RestartLoopException('Blocking detected after wait timeout')
        raise


def click_button(driver, actions, start_url, path, by_type=By.XPATH):
    """
    Click a button element safely with blocking detection.
    
    Args:
        driver: Selenium WebDriver instance
        actions: ActionChains instance
        start_url: URL for reconnection if needed
        path: XPath or other locator
        by_type: Locator type (default By.XPATH)
    
    Returns:
        bool: True if blocking detected and recovered, False if successful
    
    Raises:
        RestartLoopException: If blocking makes action impossible
    """
    
    if guard_blocking_states(driver, start_url):
        logger.warning('[CLICK] Blocking detected before click')
        return True
    
    try:
        f_element = wait_clickable(driver, by_type, path)
        actions.move_to_element(f_element).click().perform()
        time.sleep(0.1)  # Stabilization delay
        return False
    except RestartLoopException:
        raise


def click_dropdown(driver, actions, start_url, path, select_value, by_type=By.XPATH):
    """
    Click and select from dropdown with blocking detection.
    
    Args:
        driver: Selenium WebDriver instance
        actions: ActionChains instance
        start_url: URL for reconnection if needed
        path: XPath to dropdown
        select_value: Value to select (string for visible text, int for index)
        by_type: Locator type (default By.XPATH)
    
    Returns:
        bool: True if blocking detected, False if successful
    
    Raises:
        RestartLoopException: If blocking detected
    """
    from selenium.webdriver.support.ui import Select
    
    if guard_blocking_states(driver, start_url):
        logger.warning('[DROPDOWN] Blocking detected before dropdown')
        return True
    
    try:
        f_element = safe_wait_clickable(driver, start_url, by_type, path)
        actions.move_to_element(f_element).perform()
        dropdown = Select(f_element)
        
        if isinstance(select_value, str):
            dropdown.select_by_visible_text(select_value)
        else:
            dropdown.select_by_index(select_value)
        
        time.sleep(0.1)  # Stabilization delay
        return False
    except RestartLoopException:
        raise


def enter_text(driver, actions, start_url, path, text, by_type=By.XPATH):
    """
    Enter text into field with blocking detection.
    
    Args:
        driver: Selenium WebDriver instance
        actions: ActionChains instance
        start_url: URL for reconnection if needed
        path: XPath to input field
        text: Text to enter
        by_type: Locator type (default By.XPATH)
    
    Returns:
        bool: True if blocking detected, False if successful
    
    Raises:
        RestartLoopException: If blocking detected
    """
    
    if guard_blocking_states(driver, start_url):
        logger.warning('[TEXT] Blocking detected before text entry')
        return True
    
    try:
        f_element = wait_clickable(driver, by_type, path)
        actions.move_to_element(f_element).click().perform()
        f_element.clear()
        f_element.send_keys(str(text))
        return False
    except RestartLoopException:
        raise
