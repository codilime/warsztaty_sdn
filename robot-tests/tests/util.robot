*** Settings ***
Library       Collections
Resource      ../global_vars.robot


Library       libs.Cleaner    WITH NAME    Cleaner


*** Variables ***


${CONTROLLER_ENDPOINT}    ${CONTROLLER_IP}:${CONTROLLER_PORT}


*** Test Cases ***


Clean Networks
    [Tags]    clean_networks
    [Documentation]    Clean docker networks

    Cleaner.Clean Networks
