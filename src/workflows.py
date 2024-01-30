import json
from selenium.webdriver.common.by import By


def execute_workflow(driver, config, store_name, workflow_name):
    '''function to execute pre-determined workflows from config
    '''
    workflow = config['stores'][store_name]['workflows'][workflow_name]
    result = None

    for step in workflow:
        if step['action'] == 'find_element':
            element = driver.find_element(getattr(By, step['by']), step['selector'])
            if 'operation' in step:
                if step['operation'] == 'get_attribute':
                    result = element.get_attribute(step['attribute'])
                elif step['operation'] == 'get_text':
                    result = element.text
                elif not step['operation']:
                    result = element
        elif step['action'] == 'strip' and result is not None:
            result = result.strip()

    return result
